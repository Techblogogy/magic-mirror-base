from picamera import PiCamera
from time import sleep
from time import time
from subprocess import call

from minfo import app_dir

from PIL import Image

import thread, json, os

from server import PServer
pserve = PServer()

from cvison.play import PlayVid
pv = PlayVid()

from store import clothes

import logging
logger = logging.getLogger("TB")

from tb_config import conf_file as g_cfg

R_WARM = 3
R_REC = 5

BIG_CAM = True

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
        cfg = g_cfg().get_cfg()

        self.cam = PiCamera()

        # self.cam.led = False
        self.cam.framerate = 24

        # Camera Controls
        self.cam.rotation = cfg.getint("PI CAMERA", "rotation") #90
        #cam.resolution = (640, 1024)

        self.cam.contrast = cfg.getint("PI CAMERA", "contrast") #100 # Range -100 100
        #cam.saturation = 100 # Range -100 100
        self.cam.brightness = cfg.getint("PI CAMERA", "brightness") # 80 # 0 100
        #cam.awb_mode = "shade"

        self.cam.iso = cfg.getint("PI CAMERA", "iso") # 1600

        self.cam.sensor_mode = cfg.getint("PI CAMERA", "sensor_mode") # 1
        #cam.exposure_mode = "nightpreview"

        # Calculate shutter speed
        # s_speed = cfg.get("PI CAMERA", "shutter_speed")

        # logger.debug(1/500)

        # self.cam.shutter_speed = int(s_speed[0])/int(s_speed[1]) if len(s_speed) < 2 else int(s_speed[0])


        self.cam.shutter_speed = 1 / cfg.getint("PI CAMERA", "shutter_speed")

        # Preview window
        self.x = cfg.getint("PI CAMERA", "x")
        self.y = cfg.getint("PI CAMERA", "y")
        self.w = cfg.getint("PI CAMERA", "width")
        self.h = cfg.getint("PI CAMERA", "height")


    def turn_on(self):
        self.start()
        pserve.send("m_camera", "cam_on")

        logger.info("warming camera up")
        self.cam.start_preview(fullscreen=False, window = (self.x, self.y, self.w, self.h))
        pserve.send("m_camera", "preview_on")

    def turn_off(self):
        # Stop Preview Video
        self.quit()

        # Stop Camera Preview
        self.cam.stop_preview()
        pserve.send("m_camera", "preview_off")

        # Close off camera class
        self.cam.close()
        pserve.send("m_camera", "cam_off")


    def quit(self):
        pv.stop_auto()

    # @classmethod
    def rec(self):
        t = str(int(time()))

        sleep(R_WARM)

        # Campure thumbnail
        logger.info("Capturing thumbnail")
        self.cam.capture('%s/cls/%s.jpg' % (app_dir,t,))

        # Compress image
        cmp_im = Image.open('%s/cls/%s.jpg' % (app_dir,t,))
        cmp_im.save('%s/cls/%s.jpg' % (app_dir,t,), optimize=True, quality=80)

        pserve.send("m_camera", "thumb_captured")

        logger.info("Recording video")
        pserve.send("m_camera", "video_start")
        self.cam.start_recording("%s/cls/%s.h264" % (app_dir,t,))

        # Wait record time
        sleep(R_REC)

        self.cam.stop_recording()
        logger.info("Recording stopped")
        pserve.send("m_camera", "video_end")

        pserve.send("m_camera", "compression_begin")
        call("MP4Box -add %s/cls/%s.h264 %s/cls/%s.mp4"%(app_dir,t, app_dir,t,), shell=True)
        pserve.send("m_camera", "compression_off")

        os.remove("%s/cls/%s.h264"%(app_dir,t,))

        pserve.send("m_camera", "getting_dresscode")
        cl = clothes.add("casual", t+".jpg")
        pserve.send("m_camera_dat", json.dumps(cl))

        logger.info("Camera stop")
        self.cam.stop_preview()

        try:
            pv.add_size()
            thread.start_new_thread( pv.play_auto, (cl[0]["id"],) )
        except:
            logger.error("Playing video failed")

        return cl
