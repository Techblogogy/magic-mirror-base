from picamera import PiCamera
from time import sleep
from time import time
from subprocess import call

from minfo import app_dir

import thread, json

from server import PServer
pserve = PServer()

from cvison.store import clothes


R_WARM = 3
R_REC = 5

# Important Constants
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class My_Cam():
    __metaclass__ = Singleton

    # @classmethod
    def start(self):
        self.cam = PiCamera()

        self.cam.led = False
        self.cam.framerate = 24

        # Camera Controls
        self.cam.rotation = 90
        #cam.resolution = (640, 1024)

        self.cam.contrast = 100 # Range -100 100
        #cam.saturation = 100 # Range -100 100
        self.cam.brightness = 80 # 0 100
        #cam.awb_mode = "shade"

        self.cam.iso = 1600

        self.cam.sensor_mode = 1
        #cam.exposure_mode = "nightpreview"

        self.cam.shutter_speed = 1/500

    # @classmethod
    # def start_loop():
    #     thread.start_new_thread( self.rec(), (0,) )

    # @classmethod
    def turn_on(self):
        self.start()
        pserve.send("m_camera", "cam_on", namespace=IO_SPACE)

        print "warming camera up"
        self.cam.start_preview(fullscreen=False, window = (100, 20, 640, 480))
        pserve.send("m_camera", "preview_on", namespace=IO_SPACE)

    def turn_off(self):
        print "Recording stopped"
        self.cam.stop_preview()
        pserve.send("m_camera", "preview_off")

        self.cam.close()
        pserve.send("m_camera", "cam_off")

    # @classmethod
    def rec(self):
        t = str(int(time()))

        sleep(R_WARM)

        #TODO: Add socket sending
        print "Capturing thumbnail"
        self.cam.capture('%s/cls/%s.jpg' % (app_dir,t,))
        pserve.send("m_camera", "thumb_captured")

        #TODO: Add socket sending
        print "Recording video"
        pserve.send("m_camera", "video_start")
        self.cam.start_recording("%s/cls/%s.h264" % (app_dir,t,))

        # Wait record time
        sleep(R_REC)

        self.cam.stop_recording()
        pserve.send("m_camera", "video_end")

        print "[DEBUG] Camera stop"

        #TODO: Add socket sending
        pserve.send("m_camera", "compression_begin")
        call("MP4Box -add %s/cls/%s.h264 %s/cls/%s.mp4"%(app_dir,t, app_dir,t,), shell=True)
        pserve.send("m_camera", "compression_off")

        #TODO: Add socket sending
        cl = clothes.add("casual", t+".jpg")
        pserve.send("m_camera_dat", json.dumps(t))
        # print t

        return t

# cam = My_Cam()
# My_Cam.rec()
