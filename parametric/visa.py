import visa
from parametric import Instrument, Parameter

class VisaParameter:
    def __init__(self, name, instrument, value=None, get_cmd=None, set_cmd=None, get_parser=None):
        self.name = name
        self.instrument = instrument
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd
        self.get_parser = get_parser

    def get(self):
        if isinstance(self.get_cmd, str):
            result = self.instrument.query(self.get_cmd)
        else:
            result = self.get_cmd()
        if self.get_parser is not None:
            return self.get_parser(result)
        else:
            return result

    def set(self, value):
        if isinstance(self.set_cmd, str):
            self.instrument.write(self.set_cmd.format(value))
        else:
            self.set_cmd(value)

    def __call__(self, *args):
        if len(args) == 0:
            return self.get()
        else:
            self.set(args[0])

class VisaInstrument(Instrument):
    base_parameter = VisaParameter
    def __init__(self, address, visa_handle=None, read_termination=None, write_termination = None):
        super().__init__()
        if visa_handle is None:
            visa_handle = visa.ResourceManager().open_resource(address)
        self.visa_handle = visa_handle
        self.visa_handle.write_termination = write_termination
        self.visa_handle.read_termination = read_termination

    def add_parameter(self, name, get_cmd=None, set_cmd=None, get_parser=None):
        param = VisaParameter(name, self, get_cmd=get_cmd, set_cmd=set_cmd, get_parser=get_parser)
        setattr(self, name, param)
        self.parameters[name] = param

    def query(self, cmd):
        return self.visa_handle.query(cmd)

    def write(self, cmd):
        return self.visa_handle.write(cmd)

class VisaInstrumentChannel:
    def __init__(self, instrument, channel):
        self.instrument = instrument
        self.channel = channel

    def add_parameter(self, name, get_cmd=None, set_cmd=None):
        param = VisaParameter(self.instrument, get_cmd=get_cmd, set_cmd=set_cmd)
        setattr(self, name, param)
