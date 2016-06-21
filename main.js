'use strict'

const electron = require("electron");
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;

var mainWindow = null;

app.on('window-all-closed', function () {
    app.quit();
});

app.on('ready', function () {
    mainWindow = new BrowserWindow({width: 582, height: 1035, frame: false, resizable: true});
    mainWindow.loadURL('file://'+__dirname+'/index.html');

    mainWindow.on('closed', function (){
        mainWindow = null;
    });
});
