import subprocess
import os
import signal

from time import sleep
from store import clothes
from minfo import app_dir

import logging
logger = logging.getLogger("TB")

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

		vid_id = clothes.get_video(dat)
		self.set_p(app_dir+"/cls/"+vid_id)
		self.play()

		while self.playing:
			logger.info("[PlayVid DEBUG] Playing video %s", (self.file))
			logger.debug(self.proc.poll())

			if self.proc.poll() == 0:
				self.play()
			elif self.proc.poll() == 1:
				self.playing = False
				break

			sleep(0.5)

		self.stop()

	# Stop Cycle
	def stop_auto(self):
		self.playing = False
		pass
