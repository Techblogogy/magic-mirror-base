import slib as sr
from flask_socketio import emit

from server import PServer
pserve = PServer()

from ntext.ntext import get_command

import snowboydecoder
from minfo import app_dir

import thread, platform

import logging
logger = logging.getLogger("TB")

# from server import IO_SPACE, socketio
# Custom voice listening function based on sound and vision

S_SNOWBOY = False

class Speech:

    def __init__(self):
        logger.info("Initializing libraries")

        self._r = sr.Recognizer()
        self._r.dynamic_energy_threshold = False

        # Check if running
        self.running = True
        self.detected = False

        # Create microphone instance and ajust for noise
        logger.info("Ajusting for ambient noise")

        machine_plt = platform.machine()[:3]
        ml_pt = (machine_plt == "arm")

        if ml_pt:
            self._m = sr.Microphone(device_index=2, sample_rate=48000)
        else:
            self._m = sr.Microphone(sample_rate=16000)

    	# print self._m.list_microphone_names()
        self.noise_adjust()

    # Starts audio library
    def start(self):
        if S_SNOWBOY:
            logger.info("Starting snowboy")

            # Ajust for ambient noise
            self.running = True

            # Start snowboy thread
            self.dec = snowboydecoder.HotwordDetector(app_dir+"/voice/snowboy.umdl", sensitivity=1, audio_gain=5)
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

            text = recon.recognize_bing(audio, key="c91e3cabd56a4dbbacd4af392a857661")
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

                snowboydecoder.play_audio_file(app_dir+"/voice/ding.wav")

            logger.debug("Bing Speech: %s", text)
        except sr.UnknownValueError:
            logger.info("Bing unrecognizable")
        except sr.RequestError as e:
            logger.error("Bing error; {0}".format(e))
