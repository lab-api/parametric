import visa

class VisaParameter:
    def __init__(self, instrument, get_cmd=None, set_cmd=None, get_parser=None):
        self.instrument = instrument
        self.get_cmd = get_cmd
        self.set_cmd = set_cmd
        self.get_parser = get_parser

    def __call__(self, *args):
        if len(args) == 0:
            if isinstance(self.get_cmd, str):
                result = self.instrument.query(self.get_cmd)
            else:
                result = self.get_cmd()
            if self.get_parser is not None:
                return self.get_parser(result)
            else:
                return result
        else:
            if isinstance(self.set_cmd, str):
                self.instrument.write(self.set_cmd.format(args[0]))
            else:
                self.set_cmd(args[0])

class VisaInstrument:
    def __init__(self, address, visa_handle=None, read_termination=None, write_termination = None):
        if visa_handle is None:
            visa_handle = visa.ResourceManager().open_resource(address)
        self.visa_handle = visa_handle
        self.visa_handle.write_termination = write_termination
        self.visa_handle.read_termination = read_termination

    def query(self, cmd):
        return self.visa_handle.query(cmd)

    def write(self, cmd):
        return self.visa_handle.write(cmd)

    def add_parameter(self, name, get_cmd=None, set_cmd=None, get_parser=None):
        param = VisaParameter(self, get_cmd=get_cmd, set_cmd=set_cmd, get_parser=get_parser)
        setattr(self, name, param)

class VisaInstrumentChannel:
    def __init__(self, instrument, channel):
        self.instrument = instrument
        self.channel = channel

    def add_parameter(self, name, get_cmd=None, set_cmd=None):
        param = VisaParameter(self.instrument, get_cmd=get_cmd, set_cmd=set_cmd)
        setattr(self, name, param)
