# Magic Mirror
Open Source Smart Mirror software for Rapsberry PI. Made by

# Required Tech
#### To run this software you will need:
* [NodeJS](https://nodejs.org/en/) to manage Javascript side dependencies
* [Electron](http://electron.atom.io) as a Font-End UI
* [Python 2](https://www.python.org/downloads/) as a server side scripting language
* [SQL Lite 3](https://www.sqlite.org/index.html) single file database for storing essential user data

#### Python side dependencies (TODO: create installer script)
* [Flask](http://flask.pocoo.org) for managing Electron UI requests `pip install flask`
* [Flask Socket IO](https://flask-socketio.readthedocs.io/en/latest/) for creating constant client/server connection `pip install flask-socketio`

### How to run?
To run:
- Clone git repository
- Navigate into it
- Run: npm install
- Execute: electron .
