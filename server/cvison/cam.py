from picamera import PiCamera
from time import sleep
from time import time
from subprocess import call

R_WARM = 2
R_REC = 5

class My_Cam():

    @classmethod
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

    @classmethod
    def rec(self):
        self.start()

        t = str(int(time()))

        #TODO: Add socket sending
        print "warming camera up"

        self.cam.start_preview(fullscreen=False, window = (100, 20, 640, 480))
        sleep(R_WARM)

        #TODO: Add socket sending
        print "Capturing thumbnail"
        self.cam.capture('/home/pi/%s.jpg' % (t,))

        #TODO: Add socket sending
        print "Recording video"

        self.cam.start_recording("/home/pi/%s.h264" % (t,))
        sleep(R_REC)
        self.cam.stop_recording()

        #TODO: Add socket sending
        print "Recording stopped"
        self.cam.stop_preview()
        self.cam.close()

        #TODO: Add socket sending
        call("MP4Box -add /home/pi/%s.h264 /home/pi/%s.mp4"%(t,t,), shell=True)

        #TODO: Add socket sending
        print t

        return t

# cam = My_Cam()
# My_Cam.rec()
