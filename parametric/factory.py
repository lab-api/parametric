from parametric import Parameter

def Knob(name, value, *args, **kwargs):
    return Parameter(name, value, *args, kind='knob', **kwargs)


def Switch(name, value, *args, **kwargs):
    return Parameter(name, value, *args, kind='switch', **kwargs)

def Measurement(name, get_cmd, *args, **kwargs):
    return Parameter(name, *args, get_cmd=get_cmd, kind='measurement', set_cmd=None, **kwargs)
