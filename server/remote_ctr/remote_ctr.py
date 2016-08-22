# import turtle
import serial, os, time, math
# import bluetooth

#from server import socketio
#from server import IO_SPACE
#from flask_socketio import emit

from server import PServer
pserve = PServer()

import logging
logger = logging.getLogger("TB")


from tb_config import conf_file as g_cfg

def m_remote(t):
    cfg = g_cfg().get_cfg()

    # os.system("rfcomm bind 0 20:16:01:11:92:31")
    logger.info("Connecting to remote")

    # os.popen('cat /etc/services').read()
    logger.info( os.popen("rfcomm bind %s %s" % (cfg.get("REMOTE","con_port"), cfg.get("REMOTE","mac_address"))).read() )

    ser = serial.Serial(
        port=cfg.get("REMOTE","com_port"),
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
		logger.debug(x)
            except ValueError:
                x = 500;

            if 2000 > x > 800:
                if time.time() > t + 0.3 :
                    print 'Up'
                    pserve.socketio.emit("r_ctr", "up", namespace="/io")
                    #pserve.send("r_ctr", "up")
                    t = time.time()
            if x < 10 :
                if time.time() > t + 0.3 :
                    t = time.time()
                    print 'Down'
                    pserve.socketio.emit("r_ctr", "down", namespace="/io")
                    #pserve.send("r_ctr", "down")
            if 10900< x < 15000:
                if time.time() > t + 0.3 :
                    print 'Left'
                    pserve.socketio.emit("r_ctr", "right", namespace="/io")
                    #pserve.send("r_ctr", "right")
                    t = time.time()
            if 5000 < x < 10100 :
                if time.time() > t + 0.3 :
                    t = time.time()
                    print 'Right'
                    pserve.socketio.emit("r_ctr", "left", namespace="/io")
                    #pserve.send("r_ctr", "left")
            if 20001 == x :
                if time.time() > t + 0.2 :
                    t = time.time()
                    print 'Click'

                    pserve.socketio.emit("r_ctr", "click", namespace="/io")
                    #pserve.send("r_ctr", "click")
# dozimetr()
