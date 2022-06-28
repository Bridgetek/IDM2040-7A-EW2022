# Introduction
This folder contains the source code of LDS demo project for EW2022. It relies on CircuitPython 7.X 
with LDS SDK support. It can scan LDS Bus and read the sensor and present the data. 

1. The circuitPython with LDS SDK: IDM2040_LDS_SDK_Firmware/IDM2040_LDSBus_SDK_FIRMWARE.uf2. 
It shall be downloaded to IDM2040-7A board. 

2. Copy the following folder to the CircuitPython drive:
     * lib\brtEve  (it is located at: https://github.com/BRTSG-FOSS/pico-brteve/tree/main/circuitPython/lib/brteve)  
   It is the Eve library used by this demo. 
3. Copy the following folders and file to the CircuitPython drive: 
     * json: The json files used for parsing sensor data
     * ui_lds: The UI specific code
     * code.py: The standard start file of circuitPython application
4. Demo should start after power on IDM2040
