#!/usr/bin/env python

import argparse
import sys
import struct
import logging
try:
    import signal
except ImportError:
    signal = None

import trollius as asyncio

"""
Basic server and client communication using Trollius

This example sends joystick info from the base station to the rover.

Pass in command-line argument --help for usage info
"""

_HEADER_STRUCT = struct.Struct("<B")

_BEGIN_HEADER = _HEADER_STRUCT.pack(0)
_PING_BACK = _HEADER_STRUCT.pack(1)

_JOYSTICK_AXIS_HEADER = _HEADER_STRUCT.pack(2)
_JOYSTICK_AXIS_DATA = struct.Struct("<Bb")

class ServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        print 'Started server'
        self.transport = transport
        self.clients = list()
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.send_joystick_data_routine())

    def send_joystick_axis_data(self, axis, value):
        for addr in self.clients:
            self.transport.sendto(_JOYSTICK_AXIS_HEADER + _JOYSTICK_AXIS_DATA.pack(axis, value), addr)

    @asyncio.coroutine
    def send_joystick_data_routine(self):
        # CAUTION: This only works with one instance of the server instance, otherwise you'll have multiple servers getting SDL2 events
        while True:
            for event in sdl2.ext.get_events():
                if event.type == sdl2.SDL_JOYAXISMOTION:
                    if event.jaxis.which == 0:
                        #print event.jaxis.axis, event.jaxis.value
                        scaled_axis_value = int(round(event.jaxis.value / 327.68)) # Axis values from SDL2 are signed shorts. Scaling into range -100 to 100
                        self.send_joystick_axis_data(event.jaxis.axis, scaled_axis_value)
            yield asyncio.From(asyncio.sleep(1.0/120)) # Need to sleep in order for the loop to do other things

    def datagram_received(self, data, addr):
        header = data[0]
        if header == _BEGIN_HEADER:
            print("Received begin connection packet from {}".format(str(addr)))
            print("Adding client to list")
            self.clients.append(addr) # TODO: Remove clients when they disconnect or they don't ping in a while
        elif header == _PING_BACK:
            print("Received ping back packet from {}".format(str(addr)))
        else:
            print('Unknown packet data from {0}: "{1}"'.format(str(addr), data))
            self.transport.close()
            loop = asyncio.get_event_loop()
            loop.close()

    def error_received(self, exc):
        print 'Error received:', exc

    def connection_lost(self, exc):
        print 'stop', exc

class ClientProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport
        print('Sending begin connection packet')
        self.transport.sendto(_BEGIN_HEADER)

    def datagram_received(self, data, addr):
        header = data[0]
        payload = data[1:]
        if header == _JOYSTICK_AXIS_HEADER:
            axis, value = _JOYSTICK_AXIS_DATA.unpack(payload)
            print("Received axis {0} data: {1}".format(axis, value))
            self.transport.sendto(_PING_BACK)
        else:
            print('Unknown packet data: "{0}"'.format(data))
            self.transport.close()
            loop = asyncio.get_event_loop()
            loop.close()

    def error_received(self, exc):
        print 'Error received:', exc

    def connection_lost(self, exc):
        print 'closing transport', exc
        loop = asyncio.get_event_loop()
        loop.stop()

def start_server(loop, addr):
    import_sdl2()
    t = asyncio.Task(loop.create_datagram_endpoint(
        ServerProtocol, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport

def start_client(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        ClientProtocol, remote_addr=addr))
    loop.run_until_complete(t)

def import_sdl2():
    global sdl2
    import sdl2
    import sdl2.ext
    # Initializing SDL2 stuff
    sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
    sdl2.SDL_JoystickOpen(0)

def setup_logging():
    logger = logging.getLogger("trollius")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

ARGS = argparse.ArgumentParser(description="UDP Echo example.")
ARGS.add_argument(
    '--server', action="store_true", dest='server',
    default=False, help='Run udp server')
ARGS.add_argument(
    '--client', action="store_true", dest='client',
    default=False, help='Run udp client')
ARGS.add_argument(
    '--host', action="store", dest='host',
    default='127.0.0.1', help='Host name')
ARGS.add_argument(
    '--port', action="store", dest='port',
    default=9999, type=int, help='Port number')

if __name__ == '__main__':
    args = ARGS.parse_args()
    setup_logging()
    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    if (not (args.server or args.client)) or (args.server and args.client):
        print('Please specify --server or --client\n')
        ARGS.print_help()
    else:
        loop = asyncio.get_event_loop()
        if sys.platform != 'win32' and signal is not None:
            loop.add_signal_handler(signal.SIGINT, loop.stop)

        if '--server' in sys.argv:
            server = start_server(loop, (args.host, args.port))
        else:
            start_client(loop, (args.host, args.port))

        try:
            loop.run_forever()
        finally:
            if '--server' in sys.argv:
                server.close()
            loop.close()
