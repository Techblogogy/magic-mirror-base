# INFO:
# mac = /Users/{USER}/Library/Application Support/
# windows = C:\Users\{USER}\AppData\Local\
# linux = /home/{USER}/.local/share/

from appdirs import AppDirs
import os

APP_NAME = "mirror_server"
APP_AUTHOR = "tb"

app_drs = AppDirs(APP_NAME, APP_AUTHOR)
app_dir = app_drs.user_data_dir

if not os.path.exists(app_dir):
    os.makedirs(app_dir)

if not os.path.exists(app_dir+"/cls"):
    os.makedirs(app_dir+"/cls")

# print app_dir
