from parametric import Parameter

class Instrument:
    base_parameter = Parameter
    def __init__(self):
        self.parameters = {}

    def add_parameter(self, name, value=None, get_cmd=None, set_cmd=None, get_parser=None):
        param = self.base_parameter(name, value=value, get_cmd=get_cmd, set_cmd=set_cmd, get_parser=get_parser)
        setattr(self, name, param)
        self.parameters[name] = param
