#!/usr/bin/env python

import argparse
import sys
import struct
import logging
import threading
import Queue
try:
    import signal
except ImportError:
    signal = None

import trollius as asyncio

"""
Communications code written using Trollius

Why Trollius you ask? Well I like event loops, asynchronous code, and Python generators.

Yeah it's not the best idea to do this considering that this is a module that others can call at will, and the event loop isn't being used at all other than in here, but whatever.

It works other than the fact that loop.stop() doesn't stop the loop for some reason. Must be a trollius bug
"""

class ServerProtocol(asyncio.DatagramProtocol):
    '''The server protocol (base-station) implementation'''

    def connection_made(self, transport):
        '''Invoked only when the server has successfully started listening'''
        #print 'Started server'
        global global_transport
        global_transport = transport

    def datagram_received(self, data, addr):
        '''
        Handles a datagram packet of payload `data` from client `addr`

        `addr` is a tuple of the format (address, port)
        '''
        receive_queue.put((data, addr), True)

    def error_received(self, exc):
        '''Handles exceptions raised from within the event loop relating to the protocol'''
        #print 'Error received:', exc

    def connection_lost(self, exc):
        '''Invoked when the loop or transport is closed(?)'''
        #print 'stop', exc

class ClientProtocol(asyncio.DatagramProtocol):
    '''The client protocol (rover) implementation'''

    def connection_made(self, transport):
        '''Invoked when the client establishes a connection to the server'''
        global global_transport
        global_transport = transport

    def datagram_received(self, data, addr):
        '''
        Handles a datagram packet of payload `data` from server `addr`

        `addr` is a tuple of the format (address, port)
        '''
        receive_queue.put((data, addr), True)

    def error_received(self, exc):
        '''Handles exceptions raised from within the event loop relating to the protocol'''
        print 'Error received:', exc

    def connection_lost(self, exc):
        '''Invoked when the loop or transport is closed(?)'''
        print 'closing transport', exc
        loop = asyncio.get_event_loop()
        loop.stop()

def start_server(loop, addr):
    '''
    Starts the server event loop on the given asyncio loop `loop` that listens
    on the given address `addr`

    `addr` is a tuple representing the address to listen on, of the format
    (address, port)
    '''
    t = asyncio.Task(loop.create_datagram_endpoint(
        ServerProtocol, local_addr=addr))
    transport, server = loop.run_until_complete(t)
    return transport

def start_client(loop, addr):
    '''
    Starts the client event loop on the given asyncio loop `loop` that connects
    to the given address `addr`

    `addr` is a tuple representing the server to connect to, of the format
    (address, port) 
    '''
    t = asyncio.Task(loop.create_datagram_endpoint(
        ClientProtocol, remote_addr=addr))
    loop.run_until_complete(t)

def setup_logging():
    '''
    Sets up a logger for Trollius so errors will be logged to console

    Should be invoked only once.
    '''
    logger = logging.getLogger("trollius")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

def main(loop, mode, host, port):
    asyncio.set_event_loop(loop)
    if not (mode == "server" or mode == "client"):
        raise Exception("Mode must be 'server' or 'client': " + str(mode))
    setup_logging()

    if mode == "server":
        server = start_server(loop, (host, port))
    else:
        start_client(loop, (host, port))

    try:
        loop.run_forever()
    finally:
        if mode == "server":
            server.close()
        loop.close()

def receive_message():
    '''
    Returns a message received from elsewhere. If no message is available, returns None

    Format: (data, (host, port))
    '''
    if "ran_setup" not in globals():
        raise Exception("Communications hasn't been setup")
    try:
        return receive_queue.get(False)
    except Queue.Empty:
        return None

def send_message(data, addr=None):
    '''
    Sends a message to a given address

    `addr` is in the format (host, port)
    '''
    if "ran_setup" not in globals():
        raise Exception("Communications hasn't been setup")
    if "loop" not in globals():
        raise Exception("Event loop isn't available yet")
    if "global_transport" not in globals():
        raise Exception("Transport object not available yet")
    loop.call_soon_threadsafe(global_transport.sendto, data, addr)

def _stop_loop():
    loop.stop()

def _common_setup():
    global loop
    loop = asyncio.get_event_loop()
    if sys.platform != 'win32' and signal is not None:
        loop.add_signal_handler(signal.SIGINT, _stop_loop)
        loop.add_signal_handler(signal.SIGTERM, _stop_loop)

def setup_server(host, port):
    '''
    Initializes the server in a separate thread that listens on the given host and port

    If a setup has already been invoked, then Exception is thrown
    '''
    with global_lock:
        if "ran_setup" in globals():
            if ran_setup == "client":
                raise Exception("Cannot initialize server. Client has already been initialized")
            elif ran_setup == "server":
                raise Exception("Server has already been initialized")
            else:
                raise Exception("A setup function has been initialized already: " + str(ran_setup))
        globals()["ran_setup"] = "server"
        _common_setup()
        global event_loop_thread
        event_loop_thread = threading.Thread(target=main, args=(loop, ran_setup, host, port))
        event_loop_thread.start()

def setup_client(host, port):
    '''
    Initializes the client in a separate thread that connects to the given host and port

    If a setup has already been invoked, then Exception is thrown
    '''
    with global_lock:
        if "ran_setup" in globals():
            if ran_setup == "client":
                raise Exception("Client has already been initialized")
            elif ran_setup == "server":
                raise Exception("Cannot initialize client. Server has already been initialized")
            else:
                raise Exception("A setup function has been initialized already: " + str(ran_setup))
        globals()["ran_setup"] = "client"
        _common_setup()
        global event_loop_thread
        event_loop_thread = threading.Thread(target=main, args=(loop, ran_setup, host, port))
        event_loop_thread.start()

def stop():
    '''Stops the client or server'''
    if "loop" in globals():
        _stop_loop()
    else:
        raise Exception("Cannot stop loop which hasn't been started")

receive_queue = Queue.Queue()
global_lock = threading.Lock()
