from parametric import Parameter

class Knob(Parameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Switch(Parameter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Measurement(Parameter):
    def __init__(self, name, get_cmd, *args, **kwargs):
        super().__init__(name=name, get_cmd=get_cmd, *args, **kwargs)
