import slib as sr
from flask_socketio import emit

from server import PServer
pserve = PServer()

from ntext.ntext import get_command

import snowboydecoder
from minfo import app_dir

import thread

# from server import IO_SPACE, socketio
# Custom voice listening function based on sound and vision

S_DEBUG = True

class Speech:

    def __init__(self):
        print "[DEBUG SPEECH] Initializing libraries"

        # self._r = sr.Recognizer()
        # self._r.dynamic_energy_threshold = False

        # Check if running
        self.running = True

        # Snowboy detector
        self.dec = snowboydecoder.HotwordDetector(app_dir+"/voice/snowboy.umdl", sensitivity=0.5)

        # Create microphone instance
        # self._m = sr.Microphone(sample_rate=16000)

    # Starts audio library
    def start(self):
        print ("[DEBUG SPEECH] Started listening for trigger")

        # Ajust for ambient noise
        # self.noise_adjust()

        self.running = True

        # self.dec.start(detected_callback=self.detect_bing,
        #     interrupt_check=self.check_interrupt,
        #     sleep_time=0.03)

        # Start new thread
        thread.start_new_thread( self.start_snowboy, () )

        # self.stop = self._r.listen_in_background(self._m,self.detect_bing)

    # Stops audio libarary
    def stop(self):
        self.running = False

    # Starts snowboy voice thread
    def start_snowboy(self):
        # pass
        print self
        self.dec.start(detected_callback=self.detect_bing,
                       interrupt_check=self.check_interrupt,
                       sleep_time=0.03)

        self.dec.terminate()

    # Check for interrupt
    def check_interrupt(self):
        return not self.running

    # Ajust for ambient noise
    def noise_adjust(self):
        with self._m as source:
            self._r.adjust_for_ambient_noise(source, duration=2)

        if self._r.energy_threshold <= 300:
            self._r.energy_threshold = 300

        # print "[TB Speech] Threshold: %s" % (self._r.energy_threshold)

    # Bing Speech Key: 95f823d726974380840ac396bb5ebbcf
    # Pluses: quite accurate
    # Minuses: slow, 5000 month quota
    # Verdict: most likely (4 out of 5)
    # def detect_bing(self,recon,audio):
    def detect_bing(self):
        print "DETECTED"

        # # Listen for phrase
        # audio = self._r.listen()
        #
        # try:
        #     text = self._r.recognize_bing(audio, key="c91e3cabd56a4dbbacd4af392a857661")
        #     # pserve.send("mic_active", "smth")
        #     cmd = get_command(text)
        #     # cmd[0] - name || cmd[1] - item number to show || cmd[2] - tag array of words
        #     if cmd:
        #         print cmd[1]
        #         # print cmd[2]
        #         if cmd[0] == "add_tags":
        #             pserve.send(cmd[0], cmd[2])
        #             pserve.send("audio_detected","ok")
        #         else:
        #             pserve.send(cmd[0], cmd[1])
        #             pserve.send("audio_detected","ok")
        #         # pserve.send(cmd[0], cmd[2])
        #     print("Bing Speech: "+text)
        # except sr.UnknownValueError:
        #     print("Bing unrecognizable")
        # except sr.RequestError as e:
        #     print("Bing error; {0}".format(e))


# voice = Speech()
# voice.start()
