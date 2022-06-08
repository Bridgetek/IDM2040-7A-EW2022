import time
import math
#import random
from random import randint
import json
from .helper import helper
from .gesture import gesture
from .datetime import hh_mm, hh_mm_ss_ms, milis, now, print_weekday, random
from .layout import layout
from .LDSBus_Sensor import LDSBus_Sensor
from .ui_common import ui_common
from .ui_4in1_sensor import ui_4in1_sensor
from .tags import *
from . import datetime
from .widgets import widgets_box, widgets_point

import sys
if sys.implementation.name == "circuitpython":
    from brteve.brt_eve_bt817_8 import BrtEve
else:
    from ....lib.brteve.brt_eve_bt817_8 import BrtEve

class ui_4in1_sensor_m(ui_4in1_sensor):
    data_gui=1
    def __init__(self, eve: BrtEve, helper: helper, gesture: gesture, layout: layout,LDSBus_Sensor:LDSBus_Sensor):
        super().__init__(eve , helper, gesture, layout,LDSBus_Sensor)
        #self.ui_main = ui_main
        self.title="LDSBus 4in1 Sensor(Motion)"
        
 
    def event(self):
        eve = self.eve
        layout = self.layout
        ges = self.gesture

        tag = ges.get().tagReleased
        if ( tag>0 ): print("4in1 tag", tag, self.gesture.get().tagReleased, self.gesture.get().tagPressed)
        if tag == tag_ui_lds_reset_data:
           self._histroy=[]
           self.humidity_data=[[0, 0]] * self.HUMIDITY_MAX_SAMPLE
           self.humidity_sample_num = 0
           self.temperature_data=[[0, 0]] * self.temperature_MAX_SAMPLE
           self.temperature_sample_num = 0
        elif tag == tag_ui_lds_data_gui:     
            ui_4in1_sensor.data_gui=1
            print("tag_ui_lds_data_gui")
        elif tag == tag_ui_lds_data_text:     
            ui_4in1_sensor.data_gui=0
            print("tag_ui_lds_data_text")       

    def processOne(self,lds,x,y):
#         self.Progress_box(x =x, y=y ,w = 290*2, h = 180*2, border=1, title="Motion",unit=" ", vmin=0, vmax=1, warning=1, value=self.value_m,scale=2)
        if self.value_m>=1:
            self.layout.draw_asset_MCU(tag_ui_lds_4in1_m,"m_active",x =x+120, y=y+10,fm=self.eve.ASTC_4x4,scale=2)
        else:
            self.layout.draw_asset_MCU(tag_ui_lds_4in1_m,"m_inactive",x =x+120, y=y+10,fm=self.eve.ASTC_4x4,scale=2)
  
    def draw(self):
        eve = self.eve
        layout = self.layout
        helper=self.helper
        eve.ColorRGB(0xff, 0xff, 0xff)     
        x = self.x0
        y = self.y0
        FONTSIZE = 29
        eve.cmd_text(x, y, 31, 0, self.title)
        if self.skipSensor: eve.cmd_text(x+len(self.title)*FONTSIZE, y, 28, 0, self.simulatorTitle)        
        self.drawBtn()
        self.event()
        ymargin = 50
        y +=  ymargin
        widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])           
        eve.ColorRGB(255, 255, 255)
        x+=100
        y+=20
        self.processOne(self.LDSBus_Sensor.lds,x,y) 
        if self.firstTime:  self.firstTime=False; print("lds:",self.LDSBus_Sensor.lds)
        ms = time.monotonic_ns() / 1000_000
        if ms - self.last_timeout < self.readingInterval: return
        self.last_timeout =  time.monotonic_ns() / 1000_000
        if self.readOne(self.LDSBus_Sensor.lds)>0:
            self.last_timeout =  time.monotonic_ns() / 1000_000