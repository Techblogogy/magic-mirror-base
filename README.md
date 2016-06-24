# Magic Mirror
Open Source Smart Mirror software for Rapsberry PI. Made by

# Required Tech
#### To run this software you will need:
* [NodeJS](https://nodejs.org/en/) to manage Javascript side dependencies
* [Python 2](https://www.python.org/downloads/) as a server side scripting language
* [SQL Lite 3](https://www.sqlite.org/index.html) single file database for storing essential user data
* [Electron](http://electron.atom.io) as a Font-End UI `npm install electron-prebuilt -g`

#### Python side dependencies (TODO: create installer script)
To install dependencies run listed commands in terminal
* [Flask](http://flask.pocoo.org) for managing Electron UI requests `pip install flask`
* [Flask Socket IO](https://flask-socketio.readthedocs.io/en/latest/) for creating constant client/server connection `pip install flask-socketio`
* [Speech Recognition](https://github.com/Uberi/speech_recognition) provides boiler plate for voice recognition API's `pip install SpeechRecognition`
* [PyAudio](http://people.csail.mit.edu/hubert/pyaudio/#downloads) for microphone listening `pip install pyaudio`

# Running software
    git clone https://github.com/Techblogogy/magic-mirror-base
