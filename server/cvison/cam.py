
from dbase.dataset import Dataset

from picamera import PiCamera
from time import sleep
from time import time
from subprocess import call

from PIL import Image

import thread, json, os

R_WARM = 3
R_REC = 5

BIG_CAM = True

class My_Cam:

    def __init__(self, pserve, clothes, playvid, appdirs, config, logger):
        self._pv = playvid
        self._cfg = config
        self._log = logger
        self._appdir = appdirs

        self.clothes = clothes
        self.pserve = pserve

    def start(self):

        self.cam = PiCamera()

        # self.cam.led = False
        self.cam.framerate = 24

        self.cam.hflip = True

        # Camera Controls
        self.cam.rotation = self._cfg.getint("PI CAMERA", "rotation") #90
        #cam.resolution = (640, 1024)

        self.cam.contrast = self._cfg.getint("PI CAMERA", "contrast") #100 # Range -100 100
        #cam.saturation = 100 # Range -100 100
        self.cam.brightness = self._cfg.getint("PI CAMERA", "brightness") # 80 # 0 100
        #cam.awb_mode = "shade"

        self.cam.iso = self._cfg.getint("PI CAMERA", "iso") # 1600

        self.cam.sensor_mode = self._cfg.getint("PI CAMERA", "sensor_mode") # 1

        self.cam.shutter_speed = 1 / self._cfg.getint("PI CAMERA", "shutter_speed")

        # Preview window
        self.x = self._cfg.getint("PI CAMERA", "x")
        self.y = self._cfg.getint("PI CAMERA", "y")
        self.w = self._cfg.getint("PI CAMERA", "width")
        self.h = self._cfg.getint("PI CAMERA", "height")


    def turn_on(self):
        self.start()
        self.pserve.send("m_camera", "cam_on")

        self._log.info("warming camera up")
        self.cam.start_preview(fullscreen=False, window = (self.x, self.y, self.w, self.h))
        self.pserve.send("m_camera", "preview_on")

    def turn_off(self):
        # Stop Preview Video
        self.quit()

        # Stop Camera Preview
        self.cam.stop_preview()
        self.pserve.send("m_camera", "preview_off")

        # Close off camera class
        self.cam.close()
        self.pserve.send("m_camera", "cam_off")


    def quit(self):
        self._pv.stop_auto()

    def rec_start(self):
        self.t = str(int(time()))

        # Campure thumbnail
        self._log.info("Capturing thumbnail")
        self.cam.capture('%s/cls/%s.jpg' % (self._appdir,self.t,))

        # Compress image
        cmp_im = Image.open('%s/cls/%s.jpg' % (self._appdir,self.t,))
        cmp_im.save('%s/cls/%s.jpg' % (self._appdir,self.t,), optimize=True, quality=20)

        self.pserve.send("m_camera", "thumb_captured")

        self._log.info("Recording video")
        self.pserve.send("m_camera", "video_start")
        self.cam.start_recording("%s/cls/%s.h264" % (self._appdir,self.t,))

    def rec_stop(self):

        self.cam.stop_recording()
        self._log.info("Recording stopped")
        self.pserve.send("m_camera", "video_end")

        # Compress video
        self.pserve.send("m_camera", "compression_begin")
        call("MP4Box -add %s/cls/%s.h264 %s/cls/%s.mp4"%(self._appdir,self.t, self._appdir,self.t,), shell=True)
        self.pserve.send("m_camera", "compression_off")

        os.remove("%s/cls/%s.h264"%(self._appdir,self.t,))

        self.pserve.send("m_camera", "getting_dresscode")
        cl = self.clothes.add("casual", self.t+".jpg")
        self.pserve.send("m_camera_dat", json.dumps(cl))

        self._log.info("Camera stop")
        self.cam.stop_preview()

        try:
            self._pv.add_size()
            thread.start_new_thread( self._pv.play_auto, (cl[0]["id"],) )
        except:
            self._log.error("Playing video failed")

        return cl
