from parametric import Parameter

class Instrument:
    base_parameter = Parameter
    def __init__(self):
        self.parameters = {}

    def add_parameter(self, name, value=None, get_cmd=None, set_cmd=None, get_parser=None):
        param = self.base_parameter(name, value=value, get_cmd=get_cmd, set_cmd=set_cmd, get_parser=get_parser)
        setattr(self, name, param)
        self.parameters[name] = param

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
