import subprocess
import os
import signal

from time import sleep


class PlayVid:

	def __init__(self, clothes, appdirs, logger, config):

		# Video playback position
		self.clothes = clothes
		self._appdir = appdirs
		self._log = logger
		self._cfg = config

		self.size_wrd = [
			self._cfg.getint("VIDEO WARDROBE", "x"),
			self._cfg.getint("VIDEO WARDROBE", "y"),
			self._cfg.getint("VIDEO WARDROBE", "width"),
			self._cfg.getint("VIDEO WARDROBE", "height")
		]

		self.size_add = [
			self._cfg.getint("VIDEO ADD PAGE", "x"),
			self._cfg.getint("VIDEO ADD PAGE", "y"),
			self._cfg.getint("VIDEO ADD PAGE", "width"),
			self._cfg.getint("VIDEO ADD PAGE", "height")
		]

		# Video File
		self.file = ""

		# OMXPlayer Process
		self.proc = None

		# is playing
		self.playing = False

	# Sets video for wardrobe
	def wrd_size(self):
		self.x = self.size_wrd[0]
		self.y = self.size_wrd[1]
		self.w = self.size_wrd[2]
		self.h = self.size_wrd[3]

	# Sets video for add page
	def add_size(self):
		self.x = self.size_add[0]
		self.y = self.size_add[1]
		self.w = self.size_add[2]
		self.h = self.size_add[3]

	# Sets Video File Path
	def set_p(self, p):
		self.file = p

	# Plays Video File
	def play(self):

		self._log.debug('omxplayer %s --win "%d, %d, %d, %d"' % (self.file, self.x, self.y, self.x+self.w, self.y+self.h))

		self.proc = subprocess.Popen('omxplayer %s --win "%d %d %d %d"' % (self.file, self.x, self.y, self.x+self.w, self.y+self.h), shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

	# Stops Video File
	def stop(self):
		# self.proc.terminate()
		os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
		os.system('killall omxplayer.bin')

	# Play Cycle
	def play_auto(self, dat):
		self.playing = True

		vid_id = self.clothes.get_video(dat)
		self.set_p( os.path.join(self._appdir, "cls", vid_id) )
		self.play()

		while self.playing:
			self._log.info("[PlayVid DEBUG] Playing video %s", (self.file))
			self._log.debug(self.proc.poll())

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
