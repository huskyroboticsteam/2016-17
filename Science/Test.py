from threading import Thread
import time


cont = True

def run():
    global cont
    counter = 0
    while cont:
        counter += 1
    print str(counter)
    return counter

def flipC():
    global cont
    cont = not cont

runningThread = Thread(target=run)
runningThread.start()
print "Thread running!"

startTime = time.time()
while time.time() - startTime < 5:
    pass

flipC()
