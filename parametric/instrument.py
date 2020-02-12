from parametric import Parameter

class Instrument:
    base_parameter = Parameter
    def __init__(self, name=''):
        self.name = name

    def connect(self, address):
        pass

    @classmethod
    def remote(cls, address):
        ''' Open and return a mimicked Instrument on a remote PC. '''
        from parametric import Remote
        return Remote(cls, address)

    def host(self, address):
        ''' Make the device accessible over ZMQ on the specified address. '''
        from parametric import Local
        self.local = Local(self, address)

    def children(self, kind=None, return_values=False):
        ''' Returns all instances of a passed type in the dictionary. '''
        instances = {}
        namespace = self.__dict__
        for x in namespace.keys():
            if isinstance(namespace[x], Parameter):
                if kind is not None and namespace[x].kind != kind:
                    continue
                parameter = namespace[x]
                if return_values:
                    instances[parameter.name] = parameter.get()
                else:
                    instances[parameter.name] = parameter

            elif isinstance(namespace[x], Instrument):
                instances[namespace[x].name] = namespace[x].children()

        return instances
