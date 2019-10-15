''' This module allows remote control of instruments interfaced with different
    computers using the ZMQ PAIR protocol. Suppose we have an instrument class
    called SharedInstrument. Computer A connects to this instrument as usual, then
    starts a Local link:
        inst = SharedInstrument.connect(addr)
        Local(inst, local_addr)

    Computer B starts a remote link to access the instrument:
        remote = Remote(SharedInstrument, local_addr)

    In both calls, local_addr is the address:port string of Computer A, for
    example '127.0.0.1:1105'.

    The Remote class mimics local control of the instrument, so Computer B can
    access getter and setter methods of its parameters in the usual way:
        remote.parameterA(5)     # sets parameterA to 5
        remote.parameterA()      # returns 5

    Remote procedure calls are also possible through the Remote.call() method,
    which accepts arbitrary arguments and/or keyword arguments. For example,
        remote.call('foo', 'bar', keyword='baz')
    is equivalent to calling Instrument.foo('bar', keyword='baz') locally.
    Arguments and keyword arguments should be JSON-compatible, and their types
    passed into Remote.call() will be preserved on the local end. The return value
    of the Instrument method will be returned by Remote.call().
'''

import zmq
from functools import partial
from threading import Thread
from parametric import Instrument

class Remote(Instrument):
    def __init__(self, instrument, address='127.0.0.1:1105'):
        super().__init__()
        self.socket = zmq.Context().socket(zmq.PAIR)
        self.socket.connect("tcp://{}".format(address))

        self.instrument = instrument()
        for parameter in self.instrument.parameters.values():
            self.add_parameter(parameter.name,
                               get_cmd=partial(self.get_cmd, parameter.name),
                               set_cmd=partial(self.set_cmd, parameter.name))

        for parameter in self.instrument.objectives.values():
            self.add_parameter(parameter.name,
                               get_cmd=partial(self.get_cmd, parameter.name))

    def get_cmd(self, name):
        self.socket.send_json({'op': 'get', 'parameter': name})
        return self.socket.recv_json()['response']

    def set_cmd(self, name, val):
        self.socket.send_json({'op': 'set', 'parameter': name, 'value': val})

    def call(self, func_name, *args, **kwargs):
        self.socket.send_json({'op': 'call', 'function': func_name, 'args': args, 'kwargs': kwargs})
        return self.socket.recv_json()['response']

class Local:
    ''' Subscribe to a zmq feed and update the attached Parameter when commands are received'''
    def __init__(self, instrument, address='127.0.0.1:1105'):
        self.instrument = instrument
        self.socket = zmq.Context().socket(zmq.PAIR)
        self.socket.bind("tcp://{}".format(address))

        Thread(target=self.receive).start()

    def receive(self):
        ''' Receives a JSON-formatted message containing an 'op' field
            ('get', 'set', or 'call') and other fields corresponding to the passed op.

            Examples of valid messages:
                {'op': 'get', 'parameter': 'x'}
                {'op': 'set', 'parameter': 'y', 'value': 3}
                {'op': 'call', 'function': 'foo', 'args': ['bar']}
        '''
        while True:
            msg = self.socket.recv_json()
            op = msg['op']

            ## setting Parameters
            if op == 'set':
                parameter = getattr(self.instrument, msg['parameter'])
                parameter(msg['value'])

            ## getting Parameter values
            elif op == 'get':
                parameter = getattr(self.instrument, msg['parameter'])
                self.socket.send_json({'response': parameter()})

            ## remote procedure calls
            elif op == 'call':
                func = getattr(self.instrument, msg['function'])
                args = msg['args']
                kwargs = msg['kwargs']
                response = func(*args, **kwargs)
                self.socket.send_json({'response': response})
