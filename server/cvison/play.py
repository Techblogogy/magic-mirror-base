import subprocess
import os
import signal

from time import sleep

class PlayVid:

	def __init__(self):
		# Video playback position
		self.x = 92
		self.y = 80

		self.w = 843
		self.h = 1350

		# Video File
		self.file = ""

		# OMXPlayer Process
		self.proc = None

		# is playing
		self.playing = False

	# Sets Video File Path
	def set_p(self, p):
		self.file = p

	# Plays Video File
	def play(self):
		self.proc = subprocess.Popen('omxplayer '+self.file+' --win "'+str(self.x)+','+str(self.y)+','+str(self.x+self.w)+','+str(self.y+self.h)+'"', shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

	# Stops Video File
	def stop(self):
		# self.proc.terminate()
		os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
		os.system('killall omxplayer.bin')

	# Play Cycle
	def play_auto(self, dat):
		self.playing = True

		while self.playing:
			print "[PlayVid DEBUG] Playing video"
			sleep(0.5)
		# self.set_p("~/test.mp4")
		# self.play()
		# pv.proc.wait()
		# # sleep(5)
		# self.stop()

	# Stop Cycle
	def stop_auto(self):
		self.playing = False
		pass
