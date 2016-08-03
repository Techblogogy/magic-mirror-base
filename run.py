import sys, os, thread, subprocess
from time import sleep

path = os.path.dirname(os.path.realpath(__file__))

def start_electron():
    # sleep(2)
    os.system("electron %s" % (path, ))
	# self.proc = subprocess.Popen(, shell=True, stdout=subprocess.PIPE)

def start_server():
    os.system("python server/run.py")

# thread.start_new_thread(start_server, ())
# thread.start_new_thread(start_electron, ())

# while True:
#     sleep(1)
#     pass

srv = subprocess.Popen("python server/run.py", shell=True, stdout=subprocess.PIPE)
sleep(2.5)
srv = subprocess.Popen("electron %s" % (path,), shell=True, stdout=subprocess.PIPE)
