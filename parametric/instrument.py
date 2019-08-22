from parametric import Parameter

class Instrument:
    def __init__(self):
        pass

    def add_parameter(self, name, get_cmd=None, set_cmd=None, get_parser=None):
        param = Parameter(self, get_cmd=get_cmd, set_cmd=set_cmd, get_parser=get_parser)
        setattr(self, name, param)
