import subprocess
import os
import signal

from time import sleep

# cmds = [
# 	'omxplayer ~/test.mp4 --win "0,0,320,512"',
# 	'omxplayer ~/test.mp4 --win "330,0,650,512"',
# 	'omxplayer ~/test.mp4 --win "660,0,980,512"',
# 	'omxplayer ~/test.mp4 --win "990,0,1310,512"'
# 	'omxplayer ~/test.mp4 --win "660,0,980,512"'
# ]
#
#
# proc = subprocess.Popen(cmds[0], shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)
# sleep(5)
# os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

#proc = [Popen(cmd, shell=True) for cmd in cmds]

#for p in proc:
#	p.wait()

#call('omxplayer ~/test.mp4 --win "0,0,320,512"', shell=True)
#call('omxplayer ~/test.mp4 --win "100,0,420,512"', shell=True)
#call('omxplayer ~/test.mp4 --win "640,0,320,512"', shell=True)



class PlayVid:

	def __init__(self):
		# Video playback position
		self.x = 0
		self.y = 0

		self.w = 320
		self.h = 512

		# Video File
		self.file = ""

		# OMXPlayer Process
		self.proc = None

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

pv = PlayVid()

pv.set_p("~/test.mp4")
pv.play()
# pv.proc.wait()
sleep(5)
pv.stop()
