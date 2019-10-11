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

    def get_cmd(self, name):
        self.socket.send_string('GET {}'.format(name))
        return float(self.socket.recv_string())

    def set_cmd(self, name, val):
        self.socket.send_string('SET {} {}'.format(name, val))

class Local:
    ''' Subscribe to a zmq feed and update the attached Parameter when commands are received'''
    def __init__(self, instrument, address='127.0.0.1:1105'):
        self.instrument = instrument
        self.socket = zmq.Context().socket(zmq.PAIR)
        self.socket.bind("tcp://{}".format(address))

        Thread(target=self.receive).start()

    def receive(self):
        ''' Receives a message consisting of a command ('SET' or 'GET'), a parameter name, and
            a value in the case of a set command and handles accordingly.

            Example formats: "GET x", "SET x 5"
        '''
        while True:
            msg = self.socket.recv_string()
            command = msg.split(' ')[0]
            parameter = getattr(self.instrument, msg.split(' ')[1])
            if command == 'SET':
                value = msg.split(' ')[2]
                parameter(float(value))

            elif command == 'GET':
                self.socket.send_string(str(parameter()))
