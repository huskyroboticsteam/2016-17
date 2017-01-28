#!/usr/bin/env python
"""Basic server and client communication using Trollius"""
import argparse
import sys
import struct
try:
    import signal
except ImportError:
    signal = None

import trollius as asyncio

_HEADER_STRUCT = struct.Struct("<B")

_BEGIN_HEADER = _HEADER_STRUCT.pack(0)
_END_HEADER = _HEADER_STRUCT.pack(1)

_POSITION_HEADER = _HEADER_STRUCT.pack(2)[0]
_POSITION_STRUCT = struct.Struct("<dd")

class ServerProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        print 'Started server'
        self.transport = transport

    def datagram_received(self, data, addr):
        header = data[0]
        if header == _BEGIN_HEADER:
            print("Received begin connection packet from {}".format(str(addr)))
            print("Sending position")
            self.transport.sendto(_POSITION_HEADER + _POSITION_STRUCT.pack(-0.1, 1.2), addr)
        elif header == _END_HEADER:
            print("Received end connection packet from {}".format(str(addr)))
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
        if header == _POSITION_HEADER:
            longitude, latitude = _POSITION_STRUCT.unpack(payload)
            print("Received position: {0} {1}".format(longitude, latitude))
            print("Sending end connection packet")
            self.transport.sendto(_END_HEADER)
            self.transport.close()
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
    t = asyncio.Task(loop.create_datagram_endpoint(
        ServerProtocol, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport


def start_client(loop, addr):
    t = asyncio.Task(loop.create_datagram_endpoint(
        ClientProtocol, remote_addr=addr))
    loop.run_until_complete(t)


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