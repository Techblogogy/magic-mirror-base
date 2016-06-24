from os import system
import pyttsx

# system('say hello Batsenko')

engine = pyttsx.init()
engine.say("hi Fedor!")
engine.runAndWait()
