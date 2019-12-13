import attr
from functools import partial
from parametric import Parameter

class parametrize:
    ''' A convenience constructor for classes with Parameters which forwards
        keyword arguments to update corresponding parameter values.

        Example:
        >>> @parametrize
        ... class MyExperiment:
        ...    x = Attribute('x', 0)

        ...    exp1 = MyExperiment()
        ...    exp2 = MyExperiment(x=3)

        ...    print(exp1.x())
        ...    print(exp2.x())
        0
        3

        The parameters defined in the decorated class are conveniently stored in
        its __parameters__ dict:
        >>> print(exp1.__parameters__)
        {'x', Parameter('x', 0)}
    '''
    def __init__(self, cls, **parameters):
        self.cls = attr.s(cls, repr=False)
        cls.__parameters__ = property(lambda cls: self.list_parameters(cls))

    def __call__(self, **parameters):
        self.instance = self.cls.__call__(**parameters)
        return self.instance

    def list_parameters(self, cls):
        parameters = {}
        for name in dir(cls):
            if name not in dir(self) and name != '__parameters__':
                item = getattr(cls, name)
                if isinstance(item, Parameter):
                    parameters[item.name] = item
        return parameters

def convert_parameter(name, value, converter=None):
    if isinstance(value, Parameter):
        if callable(converter):
            value.set_parser = converter
        return value
    if callable(converter):
        return Parameter(name, converter(value), set_parser=converter)
    return Parameter(name, value)

def Attribute(name, value, converter=None):
    ''' A convenience factory for constructing classes with Parameters using the
        attrs syntactic sugar. The following two class instantiations are equivalent:

            ## standard definition:
            >>> class Foo:
            ...     def __init__(self):
            ...         x = Parameter('x', 1)
            ... foo = Foo()
            ... foo.x(2)
            ... print(foo.x())
            2

            ## attrs method:
            >>> @parametrize
            ... class Foo:
            ...     x = Attribute('x', 1)
            ... foo = Foo(x=2)
            ... print(foo.x())
            2

        As demonstrated in this example, using the attrs method with Attribute
        in place of Parameter lets us define classes more cleanly and pass in
        specific Parameter values at instantiation. This is useful, for example,
        for parallel simulations, where many instances of a class may be instantiated
        with different parameter sets.

        Note that Parameters defined in this method are instance variables, not
        class variables (this is one nice feature of attrs). For example:

            >>> foo = Foo(x=2)
            ... bar = Foo(x=3)
            ... bar.x(4)
            ... print(foo.x())
            ... print(bar.x())
            2
            4

        Updating one variable does not affect the other!

        Passing a callable to the converter keyword argument lets you define
        types for the Attribute's value:
            >>> @parametrize
            ... class Bar:
            ...     y = Attribute('y', 1, converter=int)
            ... bar = Bar(y=1.1)
            ... print(bar.y())
            1
    '''
    return attr.ib(converter=partial(convert_parameter, name, converter=converter),
           factory=partial(Parameter, name, value))
