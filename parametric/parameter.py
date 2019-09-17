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
    def __init__(self, name, value=None, get_cmd=None, set_cmd=None, bounds=(None, None)):
        self.name = name
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd
        self.bounds = bounds

        self(value)

    def __repr__(self):
        return f"Parameter('{self.name}', {self()})"

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
            if self.get_cmd is not None:
                self.value = self.get_cmd()
            if self.value is None:
                raise ValueError(f'Value of parameter {self.name} not yet set.')
            return self.value
        else:
            self.value = args[0]
            if args[0] == None:
                return
            if self.bounds[0] is not None:
                if args[0] < self.bounds[0]:
                    raise ValueError('Setpoint outside of defined bounds')
                    return
            if self.bounds[1] is not None:
                if args[0] > self.bounds[1]:
                    raise ValueError('Setpoint outside of defined bounds')
                    return
            if self.set_cmd is not None:
                self.set_cmd(args[0])


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

def parametrize(self, **kwargs):
    ''' Converts passed keyword arguments into Parameters. For example,
        calling parametrize(self, a=1) in a class constructor will attach
        a Parameter attribute called a with value 1 to the class.
    '''
    for name, value in kwargs.items():
        setattr(self, name, Parameter(name, value))
