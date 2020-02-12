import attr
from functools import partial
from parametric import Parameter

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
