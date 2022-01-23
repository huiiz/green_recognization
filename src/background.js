'use strict'

import { app, protocol, BrowserWindow, Menu } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'
// const axios = require('axios');
var http = require("http");

var pyProc;
const path = require('path');

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])


async function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 1200,
    height: 620,
    webPreferences: {
      webSecurity: false,
      // Use pluginOptions.nodeIntegration, leave this alone
      // See nklayman.github.io/vue-cli-plugin-electron-builder/guide/security.html#node-integration for more info
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION
    },

  })
  createMenu();
  if (process.env.WEBPACK_DEV_SERVER_URL) {
    // Load the url of the dev server if in development mode
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    // Load the index.html when not in development
    win.loadURL('app://./index.html')
  }
}

// function startServer_PY() {
//   var {PythonShell} = require('python-shell');

//   let options = {
//       mode: 'text',
//       pythonPath: './flask_pack/venv/Scripts/python'
//   };

//   PythonShell.run('./flask_pack/app.py', options, function (err, results) {
//       if (err) throw err;
//       // results is an array consisting of messages collected during execution
//       console.log('response: ', results);
//   });
// }


// 启动flask server，通过子进程执行已经将python项目打包好的exe文件（打包阶段）
function startServer_EXE() {
  let script = path.join(__dirname, '/../pydist', 'app', 'app.exe')
  console.log(script)
  pyProc = require('child_process').execFile(script)
  if (pyProc != null) {
    console.log('flask server start success')
    setTimeout(() => {
      if (isDevelopment) {
        http.get("http://localhost:5001/set_path?is_d=1",function(data){})
        // axios.get('http://localhost:5001/set_path?is_d=1').then(function (response) {
        //   console.log(response);
        // })
        //   .catch(function (error) {
        //     console.log(error);
        //   });
      } else {
        http.get("http://localhost:5001/set_path?is_d=0",function(data){})
        // axios.get('http://localhost:5001/set_path?is_d=0').then(function (response) {
        //   console.log(response);
        // })
        //   .catch(function (error) {
        //     console.log(error);
        //   });
      }
    }, 1000);

  }
}

// 停止flask server 函数
function stopServer() {
  pyProc.kill()
  console.log('kill flask server  success')
  pyProc = null
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
  stopServer();
})

app.on('activate', () => {
  // On macOS it's common to re-create a window in the app when the
  // dock icon is clicked and there are no other windows open.
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', async () => {
  if (isDevelopment && !process.env.IS_TEST) {
    // Install Vue Devtools
    try {
      await installExtension(VUEJS3_DEVTOOLS)
    } catch (e) {
      console.error('Vue Devtools failed to install:', e.toString())
    }
  }
  startServer_EXE();
  createWindow()

})

// Exit cleanly on request from parent process in development mode.
if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}



// 设置菜单栏
function createMenu() {
  Menu.setApplicationMenu(null)
}