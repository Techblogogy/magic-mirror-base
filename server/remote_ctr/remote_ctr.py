import math
import time
# import turtle
import serial
# import bluetooth

#from server import socketio
#from server import IO_SPACE
#from flask_socketio import emit

from server import PServer
pserve = PServer()

B_COM = "/dev/rfcomm0"

def m_remote(t):
    ser = serial.Serial(
        port=B_COM,
        baudrate=9600,
        timeout=None,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    t = 1
    t = int(t)

    k=0
    k=int(k)
    p=1
    p=int(p)

    while True:
            x = ser.readline()
            try:
                x = int(x)
            except ValueError:
                x = 500;

            if 2000 > x > 800:
                if time.time() > t + 0.3 :
                    print 'Down'
                    pserve.socketio.emit("r_ctr", "down", namespace="/io")
                    #pserve.send("r_ctr", "down")
                    t = time.time()
            if x < 100 :
                if time.time() > t + 0.3 :
                    t = time.time()
                    print 'Up'
                    pserve.socketio.emit("r_ctr", "up", namespace="/io")
                    #pserve.send("r_ctr", "up")
            if 10900< x < 15000:
                if time.time() > t + 0.3 :
                    print 'Left'
                    pserve.socketio.emit("r_ctr", "left", namespace="/io")
                    #pserve.send("r_ctr", "left")
                    t = time.time()
            if 5000 < x < 10100 :
                if time.time() > t + 0.3 :
                    t = time.time()
                    print 'Right'
                    pserve.socketio.emit("r_ctr", "right", namespace="/io")
                    #pserve.send("r_ctr", "right")
            if 21022 < x :
                if time.time() > t + 0.2 :
                    t = time.time()
                    print 'Click'
                    pserve.socketio.emit("r_ctr", "click", namespace="/io")
                    #pserve.send("r_ctr", "click")
# dozimetr()
