# Impeach

[![GitHub license](https://img.shields.io/badge/license-BSD-green.svg)](https://raw.githubusercontent.com/1tz/Impeach/master/LICENSE)

Immersive peach is an immersive analytics tool based on Flask.

![preview](./128x128.png)



## Preview

![move](./move.gif)

## Instructions

#### Google Chrome

1. Download and install [Google Chrome](https://www.google.com/chrome)
2. Launch Google Chrome
3. In the URL bar, input `chrome://flags` 
4. Input `WebXR` in the serach box
5. Toggle `WebVR` `WebXR Device API` `WebXR orientation sensor device` to `Enabled`
6. Relaunch Google Chrome
7. (Optional) Install [WebVR-Extension](https://github.com/spite/WebVR-Extension) to debug in developer mode

#### HTC VIVE

1. Plug in the usb flash drive in your HTC VIVE box
2. Double click the `.exe` file and install HTC VIVE and SteamVR
3. Sign up your HTC VIVE account when HTC VIVE is installed
4. Setup your device according to SteamVR instruction
5. Launch SteamVR and make sure all devices shows green

#### Python 3

1. Download [Python 3](https://www.python.org/downloads)

2. Install Python according to the instruction, please toggle `pip`

3. Install Python packages by pip:

    `pip install flask numpy networkx`

4. Run this project:

   `python /your/path/to/impeach/webservice/main.py`

5. Launch Chrome Canary and input `localhost:8080` in the URL bar

## Structure

Impeach

├──generateGraph

│   └── Weibo  

│       ├── GraphInfo

│       ├── Layout

│       └── res 

└──webService

​    ├── static

​    │   ├── build

​    │   ├── fonts

​    │   ├── js

​    │   └── obj

​    └── templates