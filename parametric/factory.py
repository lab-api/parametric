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

class Selector(Parameter):
    def __init__(self, name, value, options, *args, **kwargs):
        self.options = options
        self.type = type(value)
        super().__init__(name=name, value=value, *args, **kwargs)

    def set(self, value):
        value = self.type(value)
        if not value in self.options:
            raise ValueError(f'Value should be one of {self.options}.')

        self.value = value
        if self.set_cmd is not None:
            self.set_cmd(value)
        for callback in self.callbacks.values():
            callback(value)
