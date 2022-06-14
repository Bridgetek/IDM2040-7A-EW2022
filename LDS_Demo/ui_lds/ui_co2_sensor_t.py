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
from .ui_co2_sensor import ui_co2_sensor
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

class ui_co2_sensor_t(ui_co2_sensor):

    def __init__(self, eve: BrtEve, helper: helper, gesture: gesture, layout: layout,LDSBus_Sensor:LDSBus_Sensor):
        super().__init__(eve , helper, gesture, layout,LDSBus_Sensor)
        #self.ui_main = ui_main
        self.title="LDSBus CO2 Sensor(Temperature)"
        
        self.useBlend=1

    def interrupt(self):
        return 0

    

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
            ui_co2_sensor.data_gui=1
            print("tag_ui_lds_data_gui")
        elif tag == tag_ui_lds_data_text:     
            ui_co2_sensor.data_gui=0
            print("tag_ui_lds_data_text")


    def processOne(self,lds,x,y):
        boxW=self.boxW   
        boxH=self.boxH
        if (self.useBlend==1): self.eve.SaveContext() 
        self.barGraphHis(x = x, y=y, w = boxW, h = boxH, border=1,data=ui_co2_sensor.temperature_data,scale=2)
        if (self.useBlend==1):
            self.blendBk(x=x,y=y,w=boxW,h = boxH, border=1,scale=2,blend=1) 
            self.eve.RestoreContext()
        self.coordinateMarker(x,y,2*boxW,2*boxH,0,2,0,tvalue=self.value_t,MaxMin=2) 

    def draw(self):
        eve = self.eve
        layout = self.layout
        helper=self.helper
        eve.ColorRGB(0xff, 0xff, 0xff)
        eve.BlendFunc(eve.SRC_ALPHA, eve.ONE_MINUS_SRC_ALPHA) #reset to  default
        x = self.x0
        y = self.y0
        FONTSIZE = 29
        eve.cmd_text(x, y, 31, 0, self.title)
        if self.skipSensor: eve.cmd_text(x+70+len(self.title)*FONTSIZE, y, 28, 0, self.simulatorTitle)        
        self.drawBtn()
        self.event()
        ymargin = 50
        y +=  ymargin
        widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])      
        x+=100
        y+=20
        self.processOne(self.LDSBus_Sensor.lds,x,y) 
        self.preNext()