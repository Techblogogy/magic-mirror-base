import os
import urllib2
import subprocess
import zipfile

from server import t_running

user = "User"
file_path = "app.zip"
app_path = "C:\\Users\\"+user+"\\AppData\\Roaming\\ilt"

url = "https://github.com/Techblogogy/techblogogy.github.io/releases/download/6.0/app-win32-ia32.zip";

def download():

    if os.path.exists(app_path):
        subprocess.Popen(app_path+"\\app.exe")
    else:
        try:
            f = urllib2.urlopen(url);
            with open(os.path.basename(file_path), "wb") as local_file:
                local_file.write(f.read())
        except HTTPError, e:
            print "HTTP Error:", e.code, url
        except URLError, e:
            print "URL Error", e.reason, url

        with zipfile.ZipFile(file_path, "r") as z:
            z.extractall(app_path)

        subprocess.Popen(app_path+"\\shortcut.bat", shell=True)
        os.remove(file_path)

    t_running = False;

if os.path.exists('C:\\Users\\'+user):
    download()
