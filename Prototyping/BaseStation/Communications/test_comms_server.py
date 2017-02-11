#!/usr/bin/env python2

import comms
import signal
import threading

# Test server for comms.py
# Only works on Linux for now due to use of signal.pause()

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080

print("Setting up server...")
comms.setup_server(SERVER_IP, SERVER_PORT)

_stopping = False

def _shutdown_server(signum, frame):
    global _stopping
    _stopping = True
    print("Shutting down...")
    comms.shutdown()

signal.signal(signal.SIGINT, _shutdown_server)
signal.signal(signal.SIGTERM, _shutdown_server)

def _listen_loop():
    try:
        print("Entering listening loop...")
        while not _stopping:
            message, address = comms.receive_message(block=True)
            if message["type"] == comms.Protocol.emergency_stop:
                print(address, "Received emergency stop")
                break
            elif message["type"] == comms.Protocol.movement:
                print(address, "throttle {}, steering {}".format(message["throttle"], message["steering"]))
                comms.send_message({
                    "type": comms.Protocol.gps_coords,
                    "longitude": 42.0,
                    "latitude": 24.0
                }, address)
            elif message["type"] == None:
                # Comms is shutting down
                break
    finally:
        pass
        #_shutdown_server(None, None)

thread = threading.Thread(target=_listen_loop)
thread.daemon = True
thread.start()

signal.pause() # NOTE: This only works on Linux
