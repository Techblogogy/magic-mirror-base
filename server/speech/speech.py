import slib as sr
from flask_socketio import emit

from server import PServer
pserve = PServer()

from ntext.ntext import get_command

# from server import IO_SPACE, socketio
# Custom voice listening function based on sound and vision

S_DEBUG = True

class Speech:

    def __init__(self):
        print "test"
        self._r = sr.Recognizer()
        self._r.dynamic_energy_threshold = False

        self._m = sr.Microphone(sample_rate=8000)

    def start(self):
        print ("Starting")
        self.noise_adjust()
        self.stop = self._r.listen_in_background(self._m,self.detect_bing)

    # Ajust for ambient noise
    def noise_adjust(self):
        with self._m as source:
            self._r.adjust_for_ambient_noise(source, duration=2)

    # Bing Speech Key: 95f823d726974380840ac396bb5ebbcf
    # Pluses: quite accurate
    # Minuses: slow, 5000 month quota
    # Verdict: most likely (4 out of 5)
    def detect_bing(self,recon,audio):
        try:
            text = recon.recognize_bing(audio, key="c91e3cabd56a4dbbacd4af392a857661")
            cmd = get_command(text)

            pserve.send(cmd, "")
            print("Bing Speech: "+text)
        except sr.UnknownValueError:
            print("Bing unrecognizable")
        except sr.RequestError as e:
            print("Bing error; {0}".format(e))


voice = Speech()
voice.start()
