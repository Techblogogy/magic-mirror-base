import slib as sr
from flask_socketio import emit

from server import PServer
pserve = PServer()

from ntext.ntext import get_command

import logging
logger = logging.getLogger("TB")

try:
    import snowboydecoder
except:
    logger.error("Snowboy Not Found :(")

from minfo import app_dir

import thread, platform

from tb_config import conf_file as g_cfg



class Speech:

    def __init__(self):
        logger.info("Initializing Speech Libraries")

        # Get Configuation File
        cfg = g_cfg().get_cfg()

        self.snowboy_trigger = cfg.getboolean("SPEECH", "snowboy_trigger")
        self.api_key = cfg.get("API KEYS", "bing_speech")

        self.s_sensitivity = cfg.getint("SPEECH", "snowboy_sensitivity")
        self.s_gain = cfg.getint("SPEECH", "snowboy_gain")

        self._r = sr.Recognizer()
        self._r.dynamic_energy_threshold = cfg.getboolean("SPEECH", "dynamic_threshold") #False
        self._r.audio_gain = cfg.getint("SPEECH", "audio_gain")

        # Check if running
        self.running = True
        self.detected = False

        # Create microphone instance and ajust for noise
        logger.info("Ajusting for ambient noise")

        self._m = sr.Microphone(
            device_index=cfg.getint("SPEECH", "device_index"),
            sample_rate=cfg.getint("SPEECH", "sample_rate")
        )

    	# print self._m.list_microphone_names()
        self.noise_adjust()

    # Starts audio library
    def start(self):
        if self.snowboy_trigger:
            logger.info("Starting snowboy")

            # Ajust for ambient noise
            self.running = True

            # Start snowboy thread
            self.dec = snowboydecoder.HotwordDetector(
                app_dir+"/voice/snowboy.umdl",
                sensitivity=self.s_sensitivity,
                audio_gain=self.s_gain
            )
            thread.start_new_thread( self.start_snowboy, () )

        else:
            self.stop = self._r.listen_in_background(self._m,self.detect_bing)

    # Stops audio libarary
    def stop(self):
        self.running = False

    # Starts snowboy voice thread
    def start_snowboy(self):

        self.dec.start(detected_callback=self.detected_snowboy,
                       interrupt_check=self.check_interrupt,
                       sleep_time=0.03)
        self.dec.terminate()

        logger.info("Stopping snowboy")

        logger.info("Starting Bing")
        if self.detected:
            self.bing_snowboy()

        # self.detect_bing()

    # Check for interrupt
    def check_interrupt(self):
        return not self.running

    # Ajust for ambient noise
    def noise_adjust(self):
        with self._m as source:
            self._r.adjust_for_ambient_noise(source, duration=2)

        #if self._r.energy_threshold <= 300:
        # self._r.energy_threshold /= 2

    	# print self._r.energy_threshold

        # print "[TB Speech] Threshold: %s" % (self._r.energy_threshold)

    # Voice detection
    def detected_snowboy(self):
        logger.info("SNOWBOY DETECTED")
        self.detected = True

        snowboydecoder.play_audio_file(app_dir+"/voice/dong.wav")
        self.stop()

    # Bing Speech Key: 95f823d726974380840ac396bb5ebbcf
    # Pluses: quite accurate
    # Minuses: slow, 5000 month quota
    # Verdict: most likely (4 out of 5)
    def bing_snowboy(self):
        self.detected = False

        # Listen for phrase
        with self._m as source:
            audio = self._r.listen(source)

        # Send audio to bing
        self.detect_bing(self._r, audio)

        # Start snowboy in a thread
        self.start()

    def detect_bing(self,recon,audio):
        try:

            text = recon.recognize_bing(audio, key=self.api_key)
            cmd = get_command(text)

            if cmd:
                logger.debug("Item Number: %d", cmd[1])

                if cmd[0] == "add_tags" or cmd[0] == "edit_dresscode":
                    pserve.send(cmd[0], cmd[2])
                elif cmd[0] == "search":
                    pserve.send(cmd[0], cmd[2])
                else:
                    pserve.send(cmd[0], cmd[1])

                pserve.send("audio_detected",cmd[0])

                try:
                    snowboydecoder.play_audio_file(app_dir+"/voice/ding.wav")
                except:
                    logger.error("Snowboy error")

            logger.debug("Bing Speech: %s", text)
        except sr.UnknownValueError:
            logger.info("Bing unrecognizable")
        except sr.RequestError as e:
            logger.error("Bing error; {0}".format(e))
