import time
import speech_recognition as sr

def callback(recon, audio):
    try:
        print("Google Speech: "+recon.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech unrecognizable")
    except sr.RequestError as e:
        print("Service unavalible")

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(m,callback)

# for _ in range(50): time.sleep(0.1)
# stop_listening()
while True: time.sleep(0.1)
