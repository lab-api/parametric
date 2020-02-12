from .parameter import Parameter
from .switch import Switch
from .attribute import Attribute, parametrize, Toggle
from .instrument import Instrument
try:
    from .visa import VisaInstrument, VisaParameter, VisaInstrumentChannel
except ImportError:
    pass
try:
    from .zmq import Local, Remote
except ImportError:
    pass
