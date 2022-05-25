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
#from .scroller import scroller
#from .dimension2d import polar_xy, clock_hand
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
        self.title="LDS 4In1 Sensor(Motion)"
        
 
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
            xHalf=410
            yHalf=205
            distance = 30
            ldsuid = int(lds['DID'])
            lds_object_file = self.LDSBus_Sensor.json_path + "/" + lds['OBJ'] + ".json"
            """
            Load and Parse the JSON File
            """
            with open(lds_object_file) as lds_json_file:
                lds_json = json.load(lds_json_file)
           
                ss=""
                for said, sensor in enumerate(lds_json['SNS']):
                    sns_value=self.LDSBus_Sensor.LDSBus_SDK_ReadValue(ldsuid,sensor)
                    #sns_value = self.LDSBus_Sensor.lds_bus.LDSBus_SDK_ReadValue(ldsuid, int(sensor['SAID']), int(sensor['CLS']))
                    if sns_value is not None:
                        if len(ss) == 0:
                            ss="%s:%-5.2f %s "% (sensor['NAME'][0:1],  float(sns_value['VALUE']), sensor['UNIT'][0:1])
                        else: ss=ss+","+"%s:%5.2f %s "%(sensor['NAME'][0:1], float( sns_value['VALUE']), sensor['UNIT'][0:1])

                        if  sensor['NAME'][0:1]=='M' and ui_4in1_sensor.data_gui==1:
                            self.Progress_box(x =x, y=y ,w = 290*2, h = 180*2, border=1, title="Motion",unit=" ", vmin=0, vmax=1, warning=1, value=float( sns_value['VALUE']),scale=2)
                            #self.circle_box(x =x, y=y, w = 290*2, h = 180*2, border=1, title="Motion",unit="m", vmin=0, vmax=1, lwarning=1, hwarning=1, value=float( sns_value['VALUE']))
 
                         
                if len(self._histroy ) >= self._maxLen:
                    self._histroy = self._histroy [1:self._maxLen]
                self._histroy .append(ss)

                if ui_4in1_sensor.data_gui!=1:
                    for item in self._histroy :
                        self.eve.cmd_text(x+50, y, 28, 0, item)
                        y+=distance
                        #print("%s\n"%(item ) )
                    #print("%d, %s \n"%(len(self._histroy ), self._histroy) )
                 
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


 
           