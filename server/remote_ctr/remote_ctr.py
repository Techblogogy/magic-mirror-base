import math
import time
# import turtle
import serial
# import bluetooth

from server import socketio
from server import IO_SPACE
from flask_socketio import emit

B_COM = "/dev/rfcomm1"

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
                    socketio.emit("m_remote", "down", namespace=IO_SPACE)
                    t = time.time()
            if x < 100 :
                if time.time() > t + 0.3 :
                    t = time.time()
                    print 'Up'
                    socketio.emit("m_remote", "up", namespace=IO_SPACE)
            if 10900< x < 15000:
                if time.time() > t + 0.3 :
                    print 'Left'
                    socketio.emit("m_remote", "left", namespace=IO_SPACE)
                    t = time.time()
            if 5000 < x < 10100 :
                if time.time() > t + 0.3 :
                    t = time.time()
                    print 'Right'
                    socketio.emit("m_remote", "right", namespace=IO_SPACE)
            if 21022 < x :
                if time.time() > t + 0.2 :
                    t = time.time()
                    print 'Click'
                    socketio.emit("m_remote", "click", namespace=IO_SPACE)
# dozimetr()
