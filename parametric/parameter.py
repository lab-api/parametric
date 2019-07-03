import numpy as np

class Parameter:
    def __init__(self, name, get_cmd = None, set_cmd = None, composite=False, bounds=(None, None)):
        self.name = name
        self.value = None
        self.getter = get_cmd
        self.setter = set_cmd
        self.composite = composite
        self.bounds = bounds

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
            if self.getter is not None:
                self.value = self.getter()
            return self.value
        else:
            if self.composite:
                raise Exception('Composite parameters are read-only.')
            if self.bounds[0] is not None:
                if args[0] < self.bounds[0]:
                    raise ValueError('Setpoint outside of defined bounds')
                    return
            if self.bounds[1] is not None:
                if args[0] > self.bounds[1]:
                    raise ValueError('Setpoint outside of defined bounds')
                    return
            if self.setter is not None:
                self.setter(args[0])
            self.value = args[0]

    def __neg__(self):
        ''' Returns this parameter with its value multiplied by -1. '''
        return Parameter(f'-{self.name}',
                         get_cmd = lambda: -1*self(),
                         set_cmd = lambda x: self(-x))

    def __mul__(self, n):
        ''' Returns a new parameter multiplied by a factor n. '''
        if type(n) in [int, float]:
            return Parameter(f'{n}*{self.name}',
                             get_cmd = lambda: n*self(),
                             set_cmd=lambda x: self(x/n))
        elif isinstance(n, Parameter):
            return Parameter(f'{self.name}*{n.name}',
                             get_cmd = lambda: n()*self(),
                             composite=True)
        raise TypeError(""" Parameter added to invalid type. Supported
                            types are int, float, or Parameter. """)

    __rmul__ = __mul__

    def __pow__(self, n):
        ''' Returns a new parameter raised to a power n. '''
        return Parameter(f'{self.name}^{n}',
                         get_cmd = lambda: self()**n,
                         set_cmd=lambda x: self(np.exp(np.log(x)/n)))

    def __add__(self, a):
        ''' Returns a new parameter offset by a constant a '''
        if type(a) in [int, float]:
            return Parameter(f'{self.name}+{a}',
                              get_cmd = lambda: self()+a,
                              set_cmd=lambda x: self(x-a))
        elif isinstance(a, Parameter):
            return Parameter(f'{self.name}+{a.name}',
                              get_cmd = lambda: self()+a(),
                              composite=True)
        raise TypeError(""" Parameter added to invalid type. Supported
                            types are int, float, or Parameter. """)

    __radd__ = __add__

    def __sub__(self, a):
        ''' Returns a new parameter offset by a constant -a '''
        if type(a) in [int, float]:
            return Parameter(f'{self.name}-{a}',
                             get_cmd = lambda: self()-a,
                             set_cmd=lambda x: self(x+a))
        elif isinstance(a, Parameter):
            return Parameter(f'{self.name}-{a.name}',
                             get_cmd = lambda: self()-a(),
                             composite=True)
        raise TypeError(""" Parameter added to invalid type. Supported
                            types are int, float, or Parameter. """)

    def __rsub__(self, a):
        return -self.__sub__(a)

    def __truediv__(self, a):
        ''' Returns a new parameter divided by a '''
        if type(a) in [int, float]:
            return Parameter(f'{self.name}/{a}',
                              get_cmd = lambda: self()/a,
                              set_cmd=lambda x: self(x*a))
        elif isinstance(a, Parameter):
            return Parameter(f'{self.name}/{a.name}',
                              get_cmd = lambda: self()/a(),
                              composite=True)
        raise TypeError(""" Parameter added to invalid type. Supported
                            types are int, float, or Parameter. """)

    def __rtruediv__(self, a):
        ''' Returns a divided by this parameter '''
        if type(a) in [int, float]:
            return Parameter(f'{self.name}/{a}',
                             get_cmd = lambda: a/self(),
                             set_cmd=lambda x: self(a/x))
        elif isinstance(a, Parameter):
            return Parameter(f'{self.name}/{a.name}',
                             get_cmd = lambda: a()/self(),
                             composite=True)
        raise TypeError(""" Parameter added to invalid type. Supported
                            types are int, float, or Parameter. """)