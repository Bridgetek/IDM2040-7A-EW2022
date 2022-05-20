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

class ui_co2_sensor(ui_common):
    data_gui=1
    HUMIDITY_MAX_SAMPLE=128
    humidity_sample_num = 0
    humidity_data=[[0, 0]] * HUMIDITY_MAX_SAMPLE
    temperature_MAX_SAMPLE=128
    temperature_sample_num = 0
    temperature_data=[[0, 0]] *temperature_MAX_SAMPLE
    def __init__(self, eve: BrtEve, helper: helper, gesture: gesture, layout: layout,LDSBus_Sensor:LDSBus_Sensor):
        super().__init__(eve,helper,gesture,layout,LDSBus_Sensor)

        #self.ui_main = ui_main
        self.title="LDS CO2 Sensor"
        self.value_co2=0 
        self.value_t=0 
        self.value_h=0     
        self.value_a=0     

    last_push_humidity = 0
    def push_humidity(self, value):
        now = time.monotonic_ns()
        TIME_PATTERN= 1 #second
        if now - self.last_push_humidity < TIME_PATTERN *1e9:
            #pass
            return

        self.last_push_humidity = now

        timestamp = time.monotonic_ns() / 1e9
        data = [timestamp, value]

        try:
            # new data on top
            temp=ui_co2_sensor.humidity_data[0:ui_co2_sensor.HUMIDITY_MAX_SAMPLE] # get index from 0 to max-1
            ui_co2_sensor.humidity_data = [data] + temp                  # add value to top

            if ui_co2_sensor.humidity_sample_num < ui_co2_sensor.HUMIDITY_MAX_SAMPLE:
                ui_co2_sensor.humidity_sample_num += 1
            else:
                ui_co2_sensor.humidity_sample_num=1
                ui_co2_sensor.humidity_data=[data]
        except  Exception as e:
            print("exceprion:",e)
            print("len:%d humidity_sample_num %d"%(len(ui_co2_sensor.humidity_data),ui_co2_sensor.humidity_sample_num) )

    last_push_temperature  = 0
    def push_temperature (self, value):
        now = time.monotonic_ns()
        TIME_PATTERN= 1 #second
        if now - self.last_push_temperature < TIME_PATTERN *1e9:
            #pass
            return

        self.last_push_temperature = now

        timestamp = time.monotonic_ns() / 1e9
        data = [timestamp, value]

        try:
            # new data on top
            temp=ui_co2_sensor.temperature_data[0:ui_co2_sensor.temperature_MAX_SAMPLE] # get index from 0 to max-1
            ui_co2_sensor.temperature_data = [data] + temp                  # add value to top

            if ui_co2_sensor.temperature_sample_num < ui_co2_sensor.temperature_MAX_SAMPLE:
                ui_co2_sensor.temperature_sample_num += 1
            else:
                ui_co2_sensor.temperature_sample_num=1
                ui_co2_sensor.temperature_data=[data]
        except  Exception as e:
            print("exceprion:",e)
            print("len:%d humidity_sample_num %d"%(len(ui_co2_sensor.temperature_data),ui_co2_sensor.temperature_sample_num) )

  
    def drawBtn(self):
        eve = self.eve
        eve.ColorRGB(0xff, 0xff, 0xff)

        y = self.layout.APP_Y 
        btn_w = self.btn_w
        btn_h = self.btn_h

        xmargin =self.xmargin
        x1 = self.xStart

        x2 = x1 + btn_w + xmargin
        x3 = x2 + btn_w + xmargin
        x4 = x3 + btn_w + xmargin
        x5 = x4 + btn_w + xmargin

        x2 = x1 + btn_w + xmargin
        x3 = x2 + btn_w + xmargin
        x4 = x3 + btn_w + xmargin
        x5 = x4 + btn_w + xmargin
        if ( self.debug):
            eve.Tag(tag_ui_lds_home)
            eve.cmd_button(x1, y, btn_w, btn_h, 30, 0, "Home")
            eve.Tag(tag_ui_lds_reset_data)
            eve.cmd_button(x2, y, btn_w, btn_h, 30, 0, "Reset")
            eve.Tag(tag_ui_lds_data_text)
            eve.cmd_button(x3, y, btn_w, btn_h, 30, 0, "Text")
            eve.Tag(tag_ui_lds_data_gui)
            eve.cmd_button(x4, y, btn_w, btn_h, 30, 0, "GUI")

        eve.Tag(tag_ui_lds_back)
        eve.cmd_button(x5, y, btn_w, btn_h, 30, 0, "Back")

        #eve.Tag(0)
        eve.TagMask(0) #The value zero means the tag buffer is set as the default value, rather than the value given by TAG command in the display list

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
            xHalf=410
            yHalf=205
            width=290
            distance = 30
            ldsuid = int(lds['DID'])
            lds_object_file = self.LDSBus_Sensor.json_path + "/" + lds['OBJ'] + ".json"
            """
            Load and Parse the JSON File
            """
            with open(lds_object_file) as lds_json_file:
                lds_json = json.load(lds_json_file)
           
                if self.LDSBus_Sensor.LDSBus_SDK_Process_LDSUID(ldsuid) >= 0:
                    ss=""
                    for said, sensor in enumerate(lds_json['SNS']):
                        sns_value=self.LDSBus_Sensor.LDSBus_SDK_ReadValue(ldsuid,sensor)
                        #sns_value = self.LDSBus_Sensor.lds_bus.LDSBus_SDK_ReadValue(ldsuid, int(sensor['SAID']), int(sensor['CLS']))
                        if sns_value is not None:
                            if len(ss) == 0:
                                ss="%s:%-5.2f %s "% (sensor['NAME'][0:1],  float(sns_value['VALUE']), sensor['UNIT'][0:1])
                            else: ss=ss+","+"%s:%5.2f %s "%(sensor['NAME'][0:1], float( sns_value['VALUE']), sensor['UNIT'][0:1])
                            if  sensor['NAME'][0:1]=='T' and ui_co2_sensor.data_gui==1:
                                self.value_t=float( sns_value['VALUE'])
                                self.push_temperature(self.value_t)                                
                            if  sensor['NAME'][0:1]=='A' and ui_co2_sensor.data_gui==1:
                                self.value_a=float( sns_value['VALUE'])
                            if  sensor['NAME'][0:1]=='H' and ui_co2_sensor.data_gui==1:
                                #print("Humdity", sns_value['VALUE'])
                                self.value_h=float( sns_value['VALUE'])
                                self.push_humidity(self.value_h)                               
                            if  sensor['NAME']=='CO2' and ui_co2_sensor.data_gui==1: #Motion
                                co2=float( sns_value['VALUE'])
                                if (co2!=0 ) and (co2!=self.value_co2):
                                    self.value_co2=co2
                                #print("CO2", sns_value['VALUE'])
                               

    
                            #pass

                    if len(self._histroy ) >= self._maxLen:
                        self._histroy = self._histroy [1:self._maxLen]
                    self._histroy .append(ss)

                    if ui_co2_sensor.data_gui!=1:
                        for item in self._histroy :
                            self.eve.cmd_text(x+50, y, 28, 0, item)
                            y+=distance
                            #print("%s\n"%(item ) )
                    #print("%d, %s \n"%(len(self._histroy ), self._histroy) )
                else:
                    print ("%20s : %s ,ldsuid=%d" %  ("CO2 SENSOR PROCESS", "FAILED" ,ldsuid))
                
                if ui_co2_sensor.data_gui==1:

                    self.eve.TagMask(1)
                    self.eve.Tag(tag_ui_lds_co2_t)
 
                    if (self.useBlend==1): self.eve.SaveContext() 
                    self.barGraphHis(x = x, y=y, w = width, h = 180, border=1,  data=ui_co2_sensor.temperature_data,scale=1,blend=1)
                    if (self.useBlend==1):
                        self.blendBk(x=x,y=y,w=width,h = 180, border=1 ,blend=1) 
                        self.eve.RestoreContext()
                    self.coordinateMarker(x,y,width,180,1,1,0,tvalue=self.value_t)


                    self.eve.Tag(tag_ui_lds_co2_a)
                    if (self.useBlend==1): self.eve.SaveContext() 
                    self.circle_box(x =x+xHalf, y=y, w = width, h = 180, border=1, title="Ambient",unit="L", vmin=0, vmax=1000, lwarning=10, hwarning=800, value=self.value_a)
                    if (self.useBlend==1):self.eve.RestoreContext()


                    self.eve.Tag(tag_ui_lds_co2_h)
                    if (self.useBlend==1): self.eve.SaveContext() 
                    self.statitics_box(x = x+xHalf, y=y+yHalf, w = width, h = 180, border=1,data=ui_co2_sensor.humidity_data ,tvalue=self.value_h)
                    if (self.useBlend==1):self.eve.RestoreContext()


                    self.eve.Tag(tag_ui_lds_co2_co2)
                    self.circle_box(x =x, y=y+yHalf, w = width, h = 180, border=1, title="CO2",unit="ppm", vmin=0, vmax=2000, lwarning=20, hwarning=1600, value=self.value_co2)

    def draw(self):
        eve = self.eve
        layout = self.layout
        helper=self.helper
        eve.ColorRGB(0xff, 0xff, 0xff)
        
        x = 10
        y = 10
        FONTSIZE = 18
        btn_w = 60
        btn_h = 30

        #X=34 ,10 ,H=780,410,82
        #print("X=%d ,%s ,H=%d,%d,%d  \n"%( self.layout.APP_X ,self.layout.APP_Y,  self.layout.APP_H,self.layout.APP_W, self.layout.MENU_W ) )

        eve.cmd_text(x, y, 28, 0, self.title)

        eve.Tag(tag_ui_lds_info)
        eve.cmd_button(x+len(self.title)*FONTSIZE, y, btn_w, btn_h, 30, 0, "Info")

        if self.skipSensor: eve.cmd_text(x+70+len(self.title)*FONTSIZE, y, 30, 0, self.simulatorTitle)
        
        self.drawBtn()
        self.event()

        ymargin = 50
        y +=  ymargin
        widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])
       
        #eve.ColorRGB(0, 0, 0)       

        eve.ColorRGB(255, 255, 255)
        x+=50
        y+=20
        #self.eve.SaveContext() 

        self.processOne(self.LDSBus_Sensor.lds,x,y) 
        if self.firstTime:  self.firstTime=False; print("lds:",self.LDSBus_Sensor.lds)
        #self.eve.RestoreContext()

 
           