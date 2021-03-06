''' The Parameter class here is defined as a drop-in replacement for integers
    or floats in simulations, offering some enhanced functionalities. Suppose we
    have a parameter x with value 3:
        x = Parameter('x', 3)
    Mathematical operations on this parameter will behave exactly as with floats:
        x + 1: returns 4
        x * 2: returns 6
        x > 4: returns False
        x <= 4: returns True

    However, calling x directly will show that it is a Parameter:
        x: Parameter('x', 3)

    This allows the object itself to be passed to an optimizer. Additionally,
    custom functionalities can be added by passing functions to the get_cmd
    and set_cmd arguments.
'''
import numpy as np

class Parameter:
    def __init__(self, name, value=None, get_cmd=None, set_cmd=None, bounds=(-np.inf, np.inf), get_parser=None, set_parser=None):
        self.name = name
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd
        self.get_parser = get_parser
        self.set_parser = set_parser
        self.bounds = list(bounds)
        self.callbacks = {}
        self.enable_callbacks = True

        if value is not None:
            self.set(value)

    def __repr__(self):
        return "Parameter('{}', {})".format(self.name, self())

    def get(self):
        if self.get_cmd is not None:
            self.value = self.get_cmd()
        if self.value is None:
            raise ValueError('Value of parameter {} not yet set.'.format(self.name))
        if self.get_parser is not None:
            self.value = self.get_parser(self.value)
        return self.value

    def set(self, value):
        if not self.bounds[0] <= value <= self.bounds[1]:
            raise ValueError('Setpoint outside of defined bounds')
        if self.set_parser is not None:
            value = self.set_parser(value)
        self.value = value
        if self.set_cmd is not None:
            self.set_cmd(value)
        if self.enable_callbacks:
            for callback in self.callbacks.values():
                callback(value)

    def __call__(self, *args):
        ''' If called with no arguments, calls and returns the getter function.
            This defaults to simply the "value" attr, but the user can implement
            custom get functionality (e.g. querying a device) by passing a method
            into the get_cmd argument of __init__.

            If called with one argument, self.value is updated to that argument.
            If a custom setter has been implemented through the set_cmd argument
            of __init__, this value is also passed to that method.
        '''
        if len(args) == 0:
            return self.get()
        else:
            if args[0] is not None:
                self.set(args[0])

    @property
    def __name__(self):
        return self.name

    def __neg__(self):
        return -self()

    def __mul__(self, n):
        return n*self()

    __rmul__ = __mul__

    def __pow__(self, n):
        return self()**n

    def __rpow__(self, n):
        return n**self()

    def __add__(self, a):
        return self() + a

    __radd__ = __add__

    def __sub__(self, a):
        return self() - a

    def __rsub__(self, a):
        return -self.__sub__(a)

    def __truediv__(self, a):
        return self() / a

    def __rtruediv__(self, a):
        return a / self()

    def __lt__(self, a):
        return self() < a

    def __le__(self, a):
        return self() <= a

    def __gt__(self, a):
        return self() > a

    def __ge__(self, a):
        return self() >= a

    def __eq__(self, a):
        return self() == a

    def __iadd__(self, a):
        self(self.value+a)
        return self

    def __isub__(self, a):
        self(self.value-a)
        return self

    def __imult__(self, a):
        self(self.value*a)
        return self

    def __idiv__(self, a):
        self(self.value/a)
        return self
