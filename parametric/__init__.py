from .parameter import Parameter, parametrize
from .instrument import Instrument
try:
    from .visa import VisaInstrument, VisaParameter, VisaInstrumentChannel
except ImportError:
    pass
try:
    from .zmq import Local, Remote
except ImportError:
    pass
