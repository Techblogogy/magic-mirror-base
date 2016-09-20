import serial, os, time, math, subprocess

def m_connect(c_port, logger):
    # connection = False

    while True:
        try:
            return serial.Serial(
                port=c_port,
                baudrate=9600,
                timeout=None,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
        except:
            logger.exception("Failed to connect trying again in 5 sec")

        time.sleep(5)

def m_remote(cfg, pserve, logger):

    logger.info("Connecting to remote")

    # Bind remote control connection
    con_proc = subprocess.Popen("sudo rfcomm bind %s %s" % (cfg.get("REMOTE","con_port"), cfg.get("REMOTE","mac_address")), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)


    ser = m_connect( cfg.get("REMOTE","com_port"), logger)

    t = 1
    t = int(t)

    k=0
    k=int(k)
    p=1
    p=int(p)

    while True:
        try:
            x = ser.readline()
        except:
            logger.exception("Unable to serial read probably dropped connection")


        try:
            x = int(x)
        except ValueError:
            x = 500;

        if 2000 > x > 800:
            if time.time() > t + 0.3 :
                print 'Up'

                pserve.socketio.emit("r_ctr", "up", namespace="/io")
                t = time.time()
        if x < 100 :
            if time.time() > t + 0.3 :
                t = time.time()
                print 'Down'

                pserve.socketio.emit("r_ctr", "down", namespace="/io")
        if 10900< x < 15000:
            if time.time() > t + 0.3 :
                print 'Left'

                pserve.socketio.emit("r_ctr", "right", namespace="/io")
                t = time.time()
        if 5000 < x < 10100 :
            if time.time() > t + 0.3 :
                t = time.time()
                print 'Right'

                pserve.socketio.emit("r_ctr", "left", namespace="/io")
        if 20001 == x :
            if time.time() > t + 0.2 :
                t = time.time()
                print 'Click'

                pserve.socketio.emit("r_ctr", "click", namespace="/io")
