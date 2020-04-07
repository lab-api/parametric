import attr

class parametrize:
    ''' A convenience constructor for classes with Parameters which forwards
        keyword arguments to update corresponding parameter values. This is
        functionally similar to @attr.s, which should be used *except when*
        serializability is required, e.g. for parallelized simulations.
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
