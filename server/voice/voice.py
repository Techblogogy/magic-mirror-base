import speech_recognition as sr
from flask_socketio import emit

from server import IO_SPACE, socketio

class voice:

    def __init__(self):
        self._r = sr.Recognizer()
        self._m = sr.Microphone()

    def start(self):
        self.noise_adjust()
        self.stop = self._r.listen_in_background(self._m,self.detected)

    # Ajust for ambient noise
    def noise_adjust(self):
        with self._m as source:
            self._r.adjust_for_ambient_noise(source)

    # @staticmethod
    def detected(self,recon,audio):
        try:
            text = recon.recognize_google(audio);
            print("Google Speech: "+text)
            # socketio.emit("myresponse", text, namespace=IO_SPACE)
        except sr.UnknownValueError:
            print("Google Speech unrecognizable")
        except sr.RequestError as e:
            print("Service unavalible")
