import time
import json
from .helper import helper
from .gesture import gesture
from .datetime import hh_mm, hh_mm_ss_ms, milis, now, print_weekday, random
from .layout import layout
from .LDSBus_Sensor import LDSBus_Sensor
from .ui_common import ui_common
from .ui_config import ui_config
#from .ui_main import ui_main
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

class ui_relay(ui_config):
    def __init__(self, eve: BrtEve, helper: helper, gesture: gesture, layout: layout,LDSBus_Sensor:LDSBus_Sensor):
        super().__init__()
        self.eve = eve
        self.helper = helper
        self.gesture = gesture
        self.layout = layout
        self.LDSBus_Sensor = LDSBus_Sensor
        #self.ui_main = ui_main
        self.title="LDS 2Ch Relay"
        self.ldsuid=-1
        self.lds_json=None
        self.relay_state=[ True, False ]
        
        self._clearData=True
        self._histroy=[]
        self._maxLen=10

        self.hFanOn=5
        self.hFanOff=6
        assetdir = "ui_lds/"
#         bmAdd=1024*250        
#         print("hFanOn bmAdd %x"%(bmAdd) )
#         eve.cmd_dlstart() #  cause problem
#         eve.BitmapHandle(self.hFanOn)
#         eve.cmd_loadimage(bmAdd, 0)
#         eve.load(open(assetdir + "fanon.png", "rb"))
# 
#         
#         bmAdd=1024*280
#         print("hFanOff bmAdd %x"%(bmAdd) )
#         eve.BitmapHandle(self.hFanOff)
#         eve.cmd_loadimage(bmAdd, 0)
#         eve.load(open(assetdir + "fanoff.png", "rb"))
        eve.cmd_swap()

        self.milis_start = 0
        self.milis_stop = 0
        self.running = 0
        self.pause = 0
        self.split = []
 
    def interrupt(self):
        return 0

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
        eve.TagMask(0) #The value zero means the tag buffer is set as the default value, rather than the value given by TAG command in the display list

    def event(self):
        eve = self.eve
        layout = self.layout
        ges = self.gesture

        tag = ges.get().tagReleased
        if ( tag>0 ): print("Relay tag", tag, self.gesture.get().tagReleased, self.gesture.get().tagPressed)
        if tag == tag_ui_lds_reset_data:
           self._histroy=[]
        elif tag == tag_ui_lds_relay_ch1:
          if self.lds_json is not None:
            #print ("=============ALTERNATE RELAYS STATES================")
            for said, sensor in enumerate(self.lds_json['SNS']):
                #print ("%20s :type:%s %d" %  (sensor['NAME'],  sensor['TYPE'],int(sensor['SAID'])) )
                if sensor['TYPE'] == 'OUTPUT' and sensor['NAME']=='Relay - CH 1':
                    data = b'\x01' if self.relay_state[said] == True else b'\x00'
                    self.relay_state[said] = not self.relay_state[said]
                    self.LDSBus_Sensor.LDSBus_SDK_WriteValue(self.ldsuid, sensor,  data)
                    #self.LDSBus_Sensor.lds_bus.LDSBus_SDK_WriteValue(self.ldsuid, int(sensor['SAID']), int(sensor['CLS']), data, len(data))
                    time.sleep(0.1)
                    sns_value = self.LDSBus_Sensor.LDSBus_SDK_ReadValue(self.ldsuid,sensor)
                    #sns_value = self.LDSBus_Sensor.lds_bus.LDSBus_SDK_ReadValue(self.ldsuid, int(sensor['SAID']), int(sensor['CLS']))
                    if sns_value is not None:
                        print ("%20s : %-8s %s" %  (sensor['NAME'],  sns_value['VALUE'], sensor['UNIT']))
        elif tag == tag_ui_lds_relay_ch2:
          if self.lds_json is not None:
            #print ("=============ALTERNATE RELAYS STATES================")
            for said, sensor in enumerate(self.lds_json['SNS']):
                #print ("%20s :type:%s %d" %  (sensor['NAME'],  sensor['TYPE'],int(sensor['SAID'])) )
                if sensor['TYPE'] == 'OUTPUT' and sensor['NAME']=='Relay - CH 2':
                    data = b'\x01' if self.relay_state[said] == True else b'\x00'
                    self.relay_state[said] = not self.relay_state[said]
                    self.LDSBus_Sensor.LDSBus_SDK_WriteValue(self.ldsuid, sensor,  data)
                    time.sleep(0.1)
                    sns_value = self.LDSBus_Sensor.LDSBus_SDK_ReadValue(self.ldsuid,sensor)
                    #sns_value = self.LDSBus_Sensor.lds_bus.LDSBus_SDK_ReadValue(self.ldsuid, int(sensor['SAID']), int(sensor['CLS']))
                    if sns_value is not None:
                        print ("%20s : %-8s %s" %  (sensor['NAME'],  sns_value['VALUE'], sensor['UNIT']))


    def draw_img(self, img_id, tag , x ,y,formatW=None):
        eve = self.eve
        img = self.layout.images[img_id]
        if formatW is None:
            formatW=self.eve.ASTC_4x4

        #print('draw_img tag=', img,tag)

        self.helper.image_draw_from_ram_g(
            img[0], x, y, img[2], img[3], formatW, 0, tag, self.eve.OPT_DITHER)

    def processOne(self,lds,x,y):
            eve = self.eve
            distance = 30
            ldsuid = int(lds['DID'])
            if self.firstTime:  
                #self.firstTime=False;
                print("ldsuid:",ldsuid, "OBJ:",lds['OBJ'] ," lds:",lds)
            self.ldsuid=ldsuid
            lds_object_file = self.LDSBus_Sensor.json_path + "/" + lds['OBJ'] + ".json"
            """
            Load and Parse the JSON File
            """
            with open(lds_object_file) as lds_json_file:
                lds_json = json.load(lds_json_file)
                self.lds_json=lds_json
                ss=""
                for said, sensor in enumerate(lds_json['SNS']):
                    time.sleep(0.01)
                    if self.LDSBus_Sensor.LDSBus_SDK_Process_LDSUID(ldsuid) >= 0:

                        sns_value = self.LDSBus_Sensor.LDSBus_SDK_ReadValue(ldsuid,sensor)
                        #sns_value = self.LDSBus_Sensor.lds_bus.LDSBus_SDK_ReadValue(ldsuid, int(sensor['SAID']), int(sensor['CLS']))
                        if self.firstTime:print ("DID=%d %20s :type:%s %s "%  (ldsuid,sensor['NAME'],  sensor['TYPE'],sns_value) )
                        if sns_value is not None:
                            #print("%s\n"%(sns_value ) )
                            self.eve.TagMask(1)
                            if sensor['NAME']=='Relay - CH 1':
                                vv=sns_value['VALUE']
                                eve.Tag(tag_ui_lds_relay_ch1)
                                ss=0
                                if vv=='0':
                                    ss=0
                                    self.layout.draw_asset4(tag_ui_lds_relay_ch1,"fanOff",x+120,y+100) 
                                elif vv=='1':
                                    ss=65535
                                    self.layout.draw_asset4(tag_ui_lds_relay_ch1,"fanOn",x+120,y+100)   
                            if sensor['NAME']=='Relay - CH 2': 
                                vv=sns_value['VALUE']
                                eve.Tag(tag_ui_lds_relay_ch2)
                                ss=0
                                if vv=='0':
                                    ss=0
                                    self.layout.draw_asset4(tag_ui_lds_relay_ch2,"fanOff",x+520,y+100) 
                                elif vv=='1':
                                    ss=65535
                                    self.layout.draw_asset4(tag_ui_lds_relay_ch2,"fanOn",x+520,y+100) 
  
                         
            if self.firstTime:  
                self.firstTime=False;
                   
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

        eve.cmd_text(x, y, 28, 0, self.title)

        eve.Tag(tag_ui_lds_info)
        eve.cmd_button(x+len(self.title)*FONTSIZE, y, btn_w, btn_h, 30, 0, "Info")

        if self.skipSensor: eve.cmd_text(x+70+len(self.title)*FONTSIZE, y, 28, 0, self.simulatorTitle)

        
        self.drawBtn()
        self.event()

        ymargin = 50
        y +=  ymargin
        widgets_box(eve,x,y-1,800,1, 1, [0x00, 0xff, 0xff])
        

        eve.ColorRGB(255, 255, 255)

        y +=  ymargin

        eve.cmd_text(x+100, y, 31, 0, "Channel 1")

        eve.cmd_text(x+500, y, 31, 0, "Channel 2")
 
        self.processOne(self.LDSBus_Sensor.lds,x,y)
