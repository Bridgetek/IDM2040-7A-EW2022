import time
from .helper import helper
from .gesture import gesture
from .datetime import hh_mm, hh_mm_ss_ms, milis, now, print_weekday, random
from .layout import layout
from .LDSBus_Sensor import LDSBus_Sensor
from .ui_config import ui_config
from .tags import *
from . import datetime
#from .scroller import scroller
#from .dimension2d import polar_xy, clock_hand
from .widgets import widgets_box, widgets_point

import sys
if sys.implementation.name == "circuitpython":
    from brteve.brt_eve_bt817_8 import BrtEve
else:
    from ....lib.brteve.brt_eve_bt817_8 import BrtEve

class ui_lds_scan(ui_config):
    def __init__(self, eve: BrtEve, helper: helper, gesture: gesture, layout: layout,LDSBus_Sensor: LDSBus_Sensor,exit=0):
        super().__init__()
        self.eve = eve
        self.helper = helper
        self.gesture = gesture
        self.layout = layout
        self.LDSBus_Sensor = LDSBus_Sensor
        self.title="Device List"
        self.exit=exit
        self._rescan=True
        #self._rescan=False
 

    def event(self):
        eve = self.eve
        layout = self.layout
        ges = self.gesture

        tag = ges.get().tagReleased
        self.tagReleased=self.gesture.get().tagReleased
        if ( tag>0 ): print("lds_scan tag", tag, self.gesture.get().tagReleased, self.gesture.get().tagPressed ,self.tagReleased)

 
    def interrupt(self):
        return 0

    def drawBtn(self):
        eve = self.eve
        eve.ColorRGB(0xff, 0xff, 0xff)

        y = self.layout.APP_Y 
        btn_w = self.btn_w
        btn_h = self.btn_h
        x1 = self.xStart
        x5 = x1 + 310
        x4 = x1 + 210
        if (self.exit==1):
            eve.Tag(tag_ui_back)
            eve.cmd_button(x4, y, btn_w, btn_h, 31, 0, "Back")
        eve.Tag(tag_ui_lds_scan)
        eve.cmd_button(x5, y, btn_w, btn_h, 31, 0, "Scan")


    def draw(self):
        eve = self.eve
        layout = self.layout
        helper=self.helper
        eve.ColorRGB(0xff, 0xff, 0xff)
        x = self.x0
        y = self.y0
        FONTSIZE = 16
        eve.cmd_text(x, y, 30, 0, self.title)
        if self.skipSensor: eve.cmd_text(x+70+len(self.title)*FONTSIZE, y, 28, 0, self.simulatorTitle)
        self.drawBtn()
        self.event()        
        eve.Tag(0)  
        ymargin = 70
        y +=  ymargin       
        distance = 50
        eve.ColorRGB(255, 255, 255)

        if self._rescan :
            self._rescan =False
            self.LDSBus_Sensor.scanLDS()

        eve.ColorRGB(85, 85, 127)
        eve.ColorRGB(170, 85, 0)
        eve.cmd_text(x, y, 29, 0, "LDS Name")
        eve.cmd_text(x+310, y, 29, 0, "DID")
        eve.cmd_text(x+365, y, 29, 0, "UID")
        eve.cmd_text(x+640, y, 29, 0, 'MFG')
        widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])
        y +=  distance
        widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])
        eve.ColorRGB(255, 255, 255)
        i=0
        y+=5
        for index, lds in self.LDSBus_Sensor.lds_list.items():
            if (i %2)==0: eve.ColorRGB(170, 85, 0)
            esle:eve.ColorRGB(85, 85, 0)
            eve.ColorRGB(255, 255, 255)
#         for index, lds_a in self.LDSBus_Sensor.lds_list_all.items():
#  
#             eve.ColorRGB(255, 255, 255)
#             did=lds_a['DID']
#             lds=self.LDSBus_Sensor.lds_list.get(int(did) )
#             #lds=self.LDSBus_Sensor.lds_list[int(did)]
            enableBut=True
            if (lds is  None):
                lds=lds_a
                enableBut=False
                eve.ColorRGB(100,100, 100)
                #print("offline",did)                                
            eve.cmd_text(x, y, 28, 0, lds['NAME'])
            eve.cmd_text(x+310, y, 28, 0, lds['DID'])
            #eve.cmd_text(x+370, y, 28, 0, lds['UID'])
            if (enableBut): eve.Tag(tag_ui_lds_data_0+i) # start from 1
            eve.cmd_button(x+370, y, 250,30,28, 0, lds['UID'])
            #eve.TagMask(0)
            eve.Tag(0) # start from 1
            eve.cmd_text(x+640, y, 28, 0, lds['MFG'])
            y+=distance
            i=i+1
            widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])
"""
   {3: {'TERM': 'off', 'PRV': '1.0', 'NAME': 'LDSBus Thermocouple Sensor', 'MFG': '23062021', 'DID': '3', 'NICK': 'LDSBus Thermocouple Sensor', 'UID': 'LS01010105232113104', 'SNO': '000003EB', 'OBJ': '32769'}, 
   1: {'TERM': 'off', 'PRV': '1.0', 'NAME': 'LDSBus 4in1 Sensor', 'MFG': '17092021', 'DID': '1', 'NICK': 'LDSBus 4in1 Sensor', 'UID': 'LS01010101272100039', 'SNO': '41363B88', 'OBJ': '32768'}}
"""
            