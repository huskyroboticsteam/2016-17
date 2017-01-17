import threading
import os
import subprocess


class MyThread(threading.Thread):
    def __init__(self, result, path):
        threading.Thread.__init__(self)
        self.result = result
        self.path = path

    def run(self):
        # Get lock to synchronize threads
        # self.lock.acquire()
        self.result.append((self.path, self.ping(self.path)))
        # Free lock to release next thread
        # self.lock.release()

    def ping(self, hostname):
        """ Use the ping utility to attempt to reach the host. We send 5 packets
        ('-c 5') and wait 3 milliseconds ('-W 3') for a response. The function
        returns the return code from the ping utility.
        """
        ret_code = subprocess.call(['ping', '-c', '5', '-W', '3', hostname],
                                   stdout=open(os.devnull, 'w'),
                                   stderr=open(os.devnull, 'w'))
        return ret_code == 0
