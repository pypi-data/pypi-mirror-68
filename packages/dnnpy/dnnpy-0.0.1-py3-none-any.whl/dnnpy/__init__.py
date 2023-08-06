import operator

import numpy as np

__all__ = ['Parameter', 'Module']


class Parameter(np.ndarray):
    """ Numpy array with gradient information. """

    def __new__(cls, value=None, shape=None, dtype=None):
        if value is None:
            value = np.empty(shape, dtype)
        obj = np.asarray(value, dtype=dtype).view(cls)
        obj._grad = None
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

        # discard gradients
        self._grad = None

    @property
    def grad(self):
        """ Accumulated gradient for this parameter. """
        return self._grad

    @grad.setter
    def grad(self, value):
        """
        Accumulates the gradient for this parameter.

        Notes
        -----
        Since gradients are accumulated, the setter for the gradients does not
        simply overwrite the existing gradients, but accumulates them on
        assignment. This might lead to unexpected results when doing something
        like:
        >>> par.grad = par.grad + 2  # actual result will be `par.grad * 2 + 2`
        Use in-place operations for this kind of situations!
        """
        if value is None:
            del self.grad
        elif np.all(value == 0):
            self.zero_grad()
        elif self._grad is None:
            msg = "Gradients have not yet been initialised!"
            raise ValueError(msg)
        elif self._grad is not value:
            self._grad += value

    @grad.deleter
    def grad(self):
        """ Remove the gradients from the parameter. """
        self._grad = None

    def zero_grad(self):
        """ Set the gradients of this parameter to all zeros. """
        self._grad = np.zeros_like(self)


class Module:
    """Base class for all modules."""

    def __init__(self):
        self.predicting = False
        self._parameters = {}

        self._forward_cache = []
        self._shape_cache = []

    def __call__(self, *inputs):
        if self.predicting:
            # keep cache clean
            return self.compute_outputs(*inputs)[0]

        return self.forward(*inputs)

    # # # attribute stuff # # #

    def __dir__(self):
        yield from super().__dir__()
        yield from self._parameters.keys()

    def __getattr__(self, name):
        try:
            return self._parameters[name]
        except KeyError:
            msg = "'{}' object has no attribute '{}'"
            raise AttributeError(msg.format(type(self).__name__, name))

    def __setattr__(self, name, value):
        try:
            # necessary to allow initialisation of _parameters in __init__
            _parameters = self.__dict__.get('_parameters', {})
            par = _parameters[name]
        except KeyError:
            if isinstance(value, Parameter):
                return self.register_parameter(name, value)

            return super().__setattr__(name, value)

        if par is not value:
            par[...] = value
        del par.grad

    def __delattr__(self, name):
        try:
            return self.deregister_parameter(name)
        except KeyError:
            return super().__delattr__(name)

    # # # non-magic stuff # # #

    def register_parameter(self, name, value):
        """
        Register a parameter with gradients to this module.

        Parameters
        ----------
        name : str
            Name of the parameter.
        value : ndarray or Parameter
            Values of the parameters to be registered.
        """
        name = str(name)
        param = Parameter(value)
        self._parameters[name] = param
        return param

    def deregister_parameter(self, name):
        """
        Deregister a parameter with its gradients from this module.

        Parameters
        ----------
        name : str
            Name of the parameter.

        Returns
        -------
        arr : ndarray
            Values of the unregistered parameter.
        """
        par = self._parameters.pop(str(name))
        return np.asarray(par)

    def named_parameters(self):
        """
        Iterator over module parameter (name, value) pairs.

        Yields
        -------
        name : str
            Name of the parameter
        param : Parameter
            Module parameter values with gradients.
        """
        yield from self._parameters.items()

    def parameters(self):
        """
        Iterator over module parameter values.

        Yields
        ------
        param : Parameter
            Module parameter values with gradients.
        """
        for _, par in self.named_parameters():
            yield par

    def reset_parameters(self, **kwargs):
        """ Initialise parameters. """
        for name, _ in self.named_parameters():
            self.__setattr__(name, 0)

    def zero_grad(self):
        """ (Re)set parameter gradients to zero. """
        for param in self.parameters():
            param.zero_grad()

    def train(self):
        """ Put the module in training mode. """
        self.predicting = False
        return self

    def eval(self):
        """ Put the module in evaluation mode. """
        self.predicting = True
        return self

    def forward(self, *inputs):
        """
        Forward pass through this module.

        Parameters
        ----------
        input0, input1, ..., inputn : ndarray
            One or more inputs.

        Returns
        -------
        out : ndarray or tuple of ndarrays
            One or more module outputs.

        See Also
        --------
        Module.compute_outputs : forward implementation without magic.
        Module.backward : automagic backward pass.

        Notes
        -----
        This is a wrapper around `Module.compute_outputs` that caches
        the values that are necessary for gradient computation automagically.
        """
        self._shape_cache.append(tuple(np.shape(x) for x in inputs))
        out, cache = self.compute_outputs(*inputs)
        self._forward_cache.append(cache)
        return out

    def backward(self, *grads):
        """
        Backward pass through this module.

        Parameters
        ----------
        grad0, grad1, ..., gradn : ndarray
            Gradients from one or more subsequent modules.

        Returns
        -------
        dx : ndarray or tuple of ndarrays
            Gradients w.r.t. to the input(s).

        See Also
        --------
        Module.compute_gradients : backward implementation without magic.
        Module.forward : automagic forward pass.

        Notes
        -----
        This is a wrapper around `Module.compute_gradients` that uses
        the values cached when calling `Module.forward` automagically.
        It also allows adds the ability to accumulate gradients
        when the output of this module is used in multiple subsequent modules.
        Updates the parameter gradients.
        """
        if self.predicting:
            raise ValueError("module not in training mode")

        shapes = self._shape_cache.pop()
        dx_accs = tuple(np.zeros(shape) for shape in shapes)

        cache = self._forward_cache.pop()
        try:
            for grad in grads:
                dxs = self.compute_grads(grad, cache)
                if len(shapes) == 1:
                    dxs = [dxs]

                for dx_acc, dx in zip(dx_accs, dxs):
                    dx_acc += dx
        except TypeError as e:
            # restore caches if zero_grad was not called (annoying in ipython)
            self._shape_cache.append(shapes)
            self._forward_cache.append(cache)
            raise TypeError(e.args[0] + "\nDid you forget to call zero_grad()?")

        return dx_accs[0] if len(dx_accs) == 1 else dx_accs

    def compute_outputs(self, *inputs):
        """
        Compute outputs for this module.

        Parameters
        ----------
        input0, input1, ..., inputn : ndarray
            One or more inputs.

        Returns
        -------
        out : ndarray or tuple of ndarrays
            One or more module outputs.
        cache : ndarray or tuple of ndarrays
            One or more values that are necessary for the gradient computation.

        See Also
        --------
        Module.forward : wrapper around this method for auto-magic caching.
        Module.compute_gradients : needs the cache data.
        """
        raise NotImplementedError()

    def compute_grads(self, grads, cache):
        """
        Compute gradients for this module.

        Parameters
        ----------
        grads : ndarray
            Gradients from subsequent module.
        cache : ndarray or tuple of ndarrays
            Cached values from the forward pass.

        Returns
        -------
        grad0, grad1, ..., gradn : ndarray
            Gradients w.r.t. to the input(s).

        See Also
        --------
        Module.backward : wrapper around this method for auto-magic caching.
        Module.compute_outputs : provides the cache data.

        Notes
        -----
        Updates the parameter gradients.
        """
        raise NotImplementedError()


class Container(Module):

    def __init__(self):
        super().__init__()
        self._modules = []
        self._name_index = {}

    # # # attribute stuff # # #

    def __dir__(self):
        yield from super().__dir__()
        yield from self._name_index.keys()

    def __getattr__(self, name):
        try:
            idx = self._name_index[name]
            return self._modules[idx]
        except KeyError:
            return super().__getattr__(name)

    def __setattr__(self, name, value):
        if value is self:
            raise ValueError("Adding a module to itself is not allowed!")

        try:
            _name_index = self.__dict__.get('_name_index', {})
            idx = _name_index[name]
            self._modules[idx] = value
        except KeyError:
            if isinstance(value, Module):
                return self.add_module(value, name=name)

            super().__setattr__(name, value)

    def __delattr__(self, name):
        try:
            return self.pop_module(name)
        except KeyError:
            return super().__delattr__(name)

    # # # list-like stuff # # #

    def __getitem__(self, index):
        return self._modules[index]

    def __setitem__(self, index, module):
        if isinstance(index, slice):
            raise NotImplementedError("Sliced assignment not implemented!")
        self._modules[index] = module

    def __delitem__(self, index):
        if isinstance(index, slice):
            iterable = range(index.start or 0, index.stop or -1, index.step or 1)
            for idx in iterable:
                self.pop_module(idx)
        else:
            self.pop_module(index)

    def __len__(self):
        return self._modules.__len__()

    def __iter__(self):
        return self._modules.__iter__()

    def __reversed__(self):
        return self._modules.__reversed__()

    # # # non-magic stuff # # #

    def add_module(self, module, name=None):
        """
        Add a submodule with its parameters to this container.

        Parameters
        ----------
        module : Module
            Module object.
        name : str, optional
            Name of the submodule.
        """
        if module is self:
            raise ValueError("Adding a module to itself is not allowed!")
        if name is not None:
            self._name_index[name] = len(self._modules)
        self._modules.append(module)
        return module

    def pop_module(self, identifier=-1):
        """
        Remove submodule with its parameters from this container.

        Parameters
        ----------
        identifier : str or int, optional
            Name or index of the submodule.
            If identifier is None, the last submodule is removed.

        Returns
        -------
        module : Module
            The removed submodule.
        """
        try:
            idx = operator.index(identifier)
        except TypeError:
            name = str(identifier)
            idx = self._name_index.pop(name)

        module = self._modules.pop(idx)
        self._name_index = {k: v if v < idx else v - 1
                            for k, v in self._name_index}

        return module

    def named_parameters(self):
        index_name = {v: k for k, v in self._name_index.items()}
        for idx, mod in enumerate(self._modules):
            m_name = index_name.get(idx, "({:d})".format(idx))
            for p_name, par in mod.named_parameters():
                yield '.'.join([m_name, p_name]), par

    def reset_parameters(self, **kwargs):
        for mod in self._modules:
            mod.reset_parameters(**kwargs)

    def compute_outputs(self, *inputs):
        raise NotImplementedError()

    def compute_grads(self, grads, cache):
        raise NotImplementedError()


class LossFunction:
    """Base class for loss functions"""
    def __init__(self):
        self.y_hat = None
        self.y_true = None

    def forward(self, y_hat, y):
        """Don't forget to store y_hat and y by adding self.y_hat = ... and self.y = ..."""
        raise NotImplementedError()

    def backward(self):
        raise NotImplementedError()

    def compute_loss(self, y_hat: np.ndarray, y_true: np.ndarray):
        raise NotImplementedError()


class Optimiser:
    """ Base class for optimisers. """

    def __init__(self, parameters, lr: float):
        """
        Create an optimiser instance.

        Parameters
        ----------
        parameters : iterable
            Iterable over the parameters that need to be updated.
        lr : float
            Learning rate or step size for updating the parameters.
        """
        self.parameters = list(parameters)
        if len(self.parameters) == 0:
            raise ValueError("no parameters to optimise")

        self.lr = float(lr)
        if self.lr < 0.:
            raise ValueError("learning rate must be positive")

    def step(self):
        """
        Update all parameters under control of this optimiser
        by making one step in the direction computed by the algorithm
        for each of the parameters.
        """
        raise NotImplementedError("method must be implemented in subclass")
