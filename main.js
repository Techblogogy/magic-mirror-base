'use strict'

const electron = require("electron");
const con = require("connect");
const stat = require("serve-static");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

// Initiate Server
// con().use(stat(__dirname)).listen(8000, function () {});

var mainWindow = null;

app.on('window-all-closed', function () {
    app.quit();
});

app.on('ready', function () {

    mainWindow = new BrowserWindow({width: 582, height: 1035, frame: false, fullscreen:true, resizable: true});
    mainWindow.loadURL('file://'+__dirname+'/index.html');
    // mainWindow.loadURL('http://localhost:8000/index.html');

    mainWindow.on('closed', function (){
        mainWindow = null;
    });
});
