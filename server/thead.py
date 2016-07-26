from server import PServer
pserve = PServer()

import time

def send_left(t):
    while True:
        print "test"
        pserve.send()
        # pserve.socketio.emit("c2", "", namespace="/io")
        time.sleep(4)
