from brteve.brt_eve_bt817_8 import BrtEve
from brteve.brt_eve_rp2040 import BrtEveRP2040

from  .gesture import gesture
import supervisor
import microcontroller
import math
import time
import array
# import uctypes
import ulab.numpy as np
import board
from .dmx512 import dmx512


tag_count=1
tag_reset=tag_count;tag_count+=1
tag_Back=tag_count;tag_count+=1
tag_colorpicker=tag_count;tag_count+=1
tag_lightness=tag_count;tag_count+=1
tag_white=tag_count;tag_count+=1

 

tag_all_red=tag_count;tag_count+=1
tag_all_green=tag_count;tag_count+=1
tag_all_blue=tag_count;tag_count+=1
tag_all_dark=tag_count;tag_count+=1

class dmx_ui(object):
    def __init__(self , eve: BrtEve):
        self.eve=eve      
        self._COLOR_GREEN=[0x90, 0xC8, 0x3A]
        self._COLOR_GRAY=[0x33, 0x33, 0x33]
        self._COLOR_WARNING=[0xD4, 0x21, 0x33]
        self._COLOR_YELLOW=[0xFF, 0xFF, 0x00]
        self.dmx = dmx512(512,board.GP8)
        self.addrDMX=4

        w = self.eve.lcd_width
        h = self.eve.lcd_height
        left = w/2 - 252/2
        self.images = {
                              #addr0           size1  w2  h3  tag4 scale5 x6                y7
            'unified.blob'  : [0      - 4096 , 4096 , 0,  0,   0,  0,     0, 0],
            'circle_72x72'  : [4096   - 4096 , 5184 , 72, 72,  0,  1,     0, 0],
            'circle_140x140': [17792  - 4096 , 19648, 140,140, 0,  1,     0, 0],
            'circle_92x92'  : [9280   - 4096 , 8512 , 92, 92,  0,  1,     0, 0],
            'circle_92x92_1': [9280   - 4096 , 8512 , 92, 92,  0,  1,     left - 97         , h - 92      ],
            'circle_92x92_2': [9280   - 4096 , 8512 , 92, 92,  0,  1,     left - 97 * 2     , h - 92      ],
            'circle_92x92_3': [9280   - 4096 , 8512 , 92, 92,  0,  1,     left + 252 + 5    , h - 92      ],
            'circle_92x92_4': [9280   - 4096 , 8512 , 92, 92,  0,  1,     left + 252 + 102  , h - 92      ],
            'knob_252x252'  : [37440  - 4096 , 63552, 252,252, 0,  1,     left              , h - 252     ],
            'loop1_72x72'   : [100992 - 4096 , 5184 , 72, 72,  0,  1,     left - 100        , h - 252 + 30],
            'loopall_72x72' : [106176 - 4096 , 5184 , 72, 72,  0,  1,     left - 100        , h - 252 + 30],
            'loopoff_72x72' : [111360 - 4096 , 5184 , 72, 72,  0,  1,     left - 100        , h - 252 + 30],
            'mixoff_48x48'  : [116544 - 4096 , 2304 , 48, 48,  0,  1,     left + 252 + 52   , h - 252 + 30],
            'mixon_48x48'   : [118848 - 4096 , 2304 , 48, 48,  0,  1,     left + 252 + 52   , h - 252 + 30],
            'mute_48x48'    : [121152 - 4096 , 2304 , 48, 48,  0,  1,     left + 100        , h - 150     ],
            'next_36x28'    : [123456 - 4096 , 1024 , 36, 28,  0,  1,     left - 97 + 25    , h - 60      ],
            'prev_36x28'    : [126528 - 4096 , 1024 , 36, 28,  0,  1,     left - 97 * 2 + 23, h - 60      ],
            'pause_36x28'   : [124480 - 4096 , 1024 , 36, 28,  0,  1,     left + 252 + 31   , h - 60      ],
            'play_36x28'    : [125504 - 4096 , 1024 , 36, 28,  0,  1,     left + 252 + 31   , h - 60      ],
            'stop_36x28'    : [127552 - 4096 , 1024 , 36, 28,  0,  1,     left + 252 + 128  , h - 60      ],
            'circular_colorwheel'    : [128576 - 4096 , 63552 , 252, 252,  0,  1,     100  , 50      ],
            #'gs-16b-2c-44100hz.raw'    : [144960 - 4096 , 699328 , 250, 250,  0,  1,     100  , 50      ],
        } 


        count = 1
        for img in self.images:
            self.images[img][4] = count
            count+=1
            iamge=self.images[img]
#             addr=int(iamge[0])
#             if addr>=0:
#                 print(img,iamge)
#                 eve.cmd_flashread(iamge[0], iamge[0], iamge[1])
            
        img = self.images['circular_colorwheel']
        print(img)
        eve.cmd_flashread(img[0], img[0]+4096, img[1])  

#        eve.cmd_flashread(0, 4096, eve.RAM_G_SIZE/4)  # 1024*1024/4 ==256k  
        eve.finish()

        self.tWhitePercent=50

        self.radius=125
        self.sat=0.5
        self.hue=90
        self.lightness=128
        self.rgb=(255,255,255)
        self.x0=100
        self.y0=50
        self.hColorwheel=0
        self.message='please pick color'
        self.workMode='text'
 

        self.c_w=0
        self.counter=0
        values = [
            # rgb, hsv
            ((0.0, 0.0, 0.0), (  0  , 0.0, 0.0)), # black
            ((0.0, 0.0, 1.0), (4./6., 1.0, 1.0)), # blue
            ((0.0, 1.0, 0.0), (2./6., 1.0, 1.0)), # green
            ((0.0, 1.0, 1.0), (3./6., 1.0, 1.0)), # cyan
            ((1.0, 0.0, 0.0), (  0  , 1.0, 1.0)), # red
            ((1.0, 0.0, 1.0), (5./6., 1.0, 1.0)), # purple
            ((1.0, 1.0, 0.0), (1./6., 1.0, 1.0)), # yellow
            ((1.0, 1.0, 1.0), (  0  , 0.0, 1.0)), # white
            ((0.5, 0.5, 0.5), (  0  , 0.0, 0.5)), # grey
        ]
#         for (rgb, hsv) in values:
#             rgb1=self.hsv_to_rgb(hsv[0],hsv[1],hsv[2])
#             print(rgb,rgb1)
#             rgb2=self.hsvToRgb(hsv[0],hsv[1],hsv[2])
#             print("rgb2",rgb,rgb2)       

    def hsvToRgb(self , h,  s,  v):
        r, g, b=0,0,0
        R, G, B=0,0,0
        h = h / 360.0;
        v = v / 255.0;
        i = (int)(h * 6);
        f = h * 6 - i;
        p = v * (1 - s);
        q = v * (1 - f * s);
        t = v * (1 - (1 - f) * s);
        ss=(i % 6)
        print("ss",ss)
        if ss==0:
           r = v; g = t;b = p
        elif ss==1:
           r = q; g = v; b = p
        elif ss==2:
           r = p; g = v; b = t
        elif ss==3:
           r = p; g = q; b = v
        elif ss==4:
           r = t; g = p; b = v
        elif ss==5:
           r = v; g = p; b = q
        R = (int)(r * 255.0);
        G = (int)(g * 255.0);
        B = (int)(b * 255.0);
        return  ( (R << 16) , (G << 8), B)
 

        
    def hsv_to_rgb(self,h, s, v):
        i = math.floor(h*6)
        f = h*6 - i
        p = v * (1-s)
        q = v * (1-f*s)
        t = v * (1-(1-f)*s)

        r, g, b = [
            (v, t, p),
            (q, v, p),
            (p, v, t),
            (p, q, v),
            (t, p, v),
            (v, p, q),
        ][int(i%6)]

        return round(r), round(g), round(b)


    def getSat(self,x0,   y0,   x1,   y1,   r):
        sizeX = math.pow((x1 - x0), 2) 
        sizeY = math.pow((y1 - y0), 2)
        sat=math.sqrt(sizeX + sizeY) / r
        return sat
                         
    def getHue(self,x0,  y0,  x1,  y1):
        angleInRadian, angleInDegree=0,0

        if x0 == x1:
             if y1 < y0:
                 return 90
             elif y1 > y0:
                 return 270
             else:
                 return 0
        elif x1 > x0:
            if y1 > y0:
                angleInRadian = math.atan2((y1 - y0), (x1 - x0));
                angleInDegree = 360 - (angleInRadian * 180 / math.pi);
            else:    
                angleInRadian = math.atan2((y0 - y1), (x1 - x0));
                angleInDegree = angleInRadian * 180 / math.pi;
        else:
            if y1 > y0:
                angleInRadian = math.atan2((y1 - y0), (x0 - x1));
                angleInDegree = 180 + (angleInRadian * 180 / math.pi);
            else:
                angleInRadian = math.atan2((y0 - y1), (x0 - x1));
                angleInDegree = 180 - (angleInRadian * 180 / math.pi);

        return angleInDegree

    def updateRGB(self):
            print("rgb:",self.sat,self.hue,self.rgb)
            if self.sat>1:
                 print("invalid :",self.sat,self.hue,self.rgb)
                 return 
            self.message="sat:%5.3f,hue:%d,rgb:%x %x %x"%(self.sat,self.hue,self.rgb[0],self.rgb[1],self.rgb[2])
            print(self.message)
            self.writeOneFrame(self.rgb,self.tWhitePercent)
    def writeOneFrame(self,rgb,tWhitePercent):
          self.dmx.setStart4ch(self.addrDMX,rgb[1], rgb[0], rgb[2] ,int(tWhitePercent*2.55))
          self.dmx.write_frame() # re-write  
    def processEvent(self,tag,touch):
          if tag == tag_Back:
              print("back")
              return -1
          elif tag == tag_lightness:
             vv=touch.tagTrackTouched>>16
             self.lightness=255*(vv/65535)
             print("lightness",self.lightness)
             self.rgb=self.hsv_to_rgb(self.hue/360.0,self.sat,self.lightness)
             self.updateRGB()
 
          elif tag == tag_colorpicker:
            print("touch",touch.touchX,touch.touchY)
            x0=self.x0+self.radius
            y0=self.y0+self.radius
#             x1=touch.touchX-x0
#             y1=touch.touchY-y0
            x1=touch.touchX
            y1=touch.touchY
            if x1==32768 or y1==32768:
                print("invalid touch",x1,y1)
                return 0
            print("x0",x0,y0,x1,y1)
            self.sat=self.getSat(x0,y0,x1,y1,self.radius)
            self.hue=self.getHue(x0,y0,x1,y1)
#             sat=self.getSat(x1,y1,x0,y0,self.radius)
#             hue=self.getHue(x1,y1,x0,y0)
            #rgb=self.hsv_to_rgb(hue,sat,self.lightness)
            self.rgb=self.hsv_to_rgb(self.hue/360.0,self.sat,self.lightness)
            #rgb=self.hsvToRgb(hue,sat,self.lightness)
            self.updateRGB()
 

          elif tag == tag_white:
               vv=touch.tagTrackTouched>>16
               self.tWhitePercent=100*(vv/65535)
                 #print("tValue" ,tValue,tValue/65535,tPercent)
               self.writeOneFrame(self.rgb,self.tWhitePercent)

          elif tag == tag_all_red:
               self.rgb=(255,0,0)
               self.writeOneFrame(self.rgb,self.tWhitePercent)

          elif tag == tag_all_green:
               self.rgb=(0,255,0)
               self.writeOneFrame(self.rgb,self.tWhitePercent)

          elif tag == tag_all_blue:
               self.rgb=(0,0,255)
               self.writeOneFrame(self.rgb,self.tWhitePercent)
  
          elif tag == tag_all_dark:
               print("tag_all_dark")
               self.rgb=(0,0,0)
               self.tWhitePercent=0
               self.writeOneFrame(self.rgb,self.tWhitePercent)
  

          return 0

 
    def loop(self):
        eve=self.eve
        assetdir = "dmx512/"
        t=1
        self.dmx.off(self.addrDMX)
        self.dmx.off(self.addrDMX)
        
        self.dmx.setStart4ch(self.addrDMX,self.rgb[1], self.rgb[0], self.rgb[2] ,int(self.tWhitePercent*2.55))
        self.dmx.setStart4ch(self.addrDMX,self.rgb[1], self.rgb[0], self.rgb[2] ,int(self.tWhitePercent*2.55))
        touch_ges = gesture(self.eve)
        while True:
            eve.cmd_dlstart() #  cause problem
            eve.VertexFormat(2)
 
            #eve.cmd_dlstart()
            eve.ClearColorRGB(0, 0, 0)   # 255-> 1   ,new black color
            eve.Clear(1, 1, 1) 
            eve.ColorRGB(0xff, 0xff, 0xff)
            
            eve.cmd_fgcolor(0x003870)  # default
            eve.cmd_bgcolor(0x002040)  # 

            eve.cmd_text(10, 5, 30, 0, "DMX512 Testing" )  
            eve.Tag(tag_Back)
            eve.cmd_button(700, 5, 85,35,30, 0, "Back")
            
            x=self.x0; y=self.y0
            w=300
            h=250
            
            eve.Tag(tag_all_red)
            eve.cmd_button(50, 400, 130,35,31, 0, "RED")
            eve.Tag(tag_all_green)
            eve.cmd_button(200, 400, 130,35,31, 0, "GREEN")
            eve.Tag(tag_all_blue)
            eve.cmd_button(350, 400, 130,35,31, 0, "BLUE")         
            eve.Tag(tag_all_dark)
            eve.cmd_button(500, 400, 130,35,31, 0, "DARK")
            
            eve.Tag(tag_colorpicker)                        
            img = self.images['circular_colorwheel']
            eve.cmd_setbitmap(img[0], eve.ASTC_4x4, 2*self.radius, 2*self.radius)
            eve.Tag(tag_colorpicker)
            eve.Begin(eve.BITMAPS)
            eve.Vertex2f(self.x0, self.y0)

            eve.TagMask(0)
            #eve.ColorRGB((int)(tRedPercent*2.55), (int)(tGreenPercent*2.55), (int)(tBluePercent*2.55))
            eve.ColorRGB(self.rgb[0], self.rgb[1], self.rgb[2])
            eve.Begin(eve.RECTS)
            eve.LineWidth(5)
            eve.Vertex2f(x+350, y+80)
            eve.Vertex2f(x +350+w, y+h)
            
            eve.cmd_text(x +350, y+h+30, 28, 0, self.message)
            
            h=15
            eve.cmd_fgcolor(0xffffff)
            eve.cmd_bgcolor(0xffffff)  #white
            eve.ColorRGB(0xff,0xff,0xff)
            eve.cmd_text(x+350, y, 28, 0, "White LED lightness" )
            eve.TagMask(1)
            eve.Tag(tag_white)
            eve.cmd_track(x+350, y+35, w, h, tag_white)
            eve.cmd_slider(x+350, y+35, w, h, 0, self.tWhitePercent, 100)

            
            y= y+280
            eve.cmd_fgcolor(0xffffff)
            eve.cmd_bgcolor(0xffffff)  #white
            eve.ColorRGB(0xff,0xff,0xff)
            eve.Tag(tag_lightness)
            eve.cmd_track(x, y, w, h, tag_lightness)
            eve.cmd_slider(x, y, w, h, 0, self.lightness, 255)    
        
            touch=touch_ges.renew()

            eve.Display()
            eve.cmd_swap()   
            eve.flush() 
            if self.processEvent(touch.tagPressed,touch)<0: break      
            time.sleep(0.01)
            #if (t==1): break 
            t+=1
            #print(t)
        print("clear")
        eve.cmd_dlstart() #  cause problem
        eve.VertexFormat(2)
        eve.ClearColorRGB(0, 0, 0)   # 255-> 1   ,new black color
        eve.Clear(1, 1, 1) 
        eve.ColorRGB(0xff, 0xff, 0xff)
        eve.cmd_fgcolor(0x003870)  # default
        eve.cmd_bgcolor(0x002040)  # 
        eve.Display()
        eve.cmd_swap()   
        eve.flush() 
        self.dmx.deinit()
        del self.dmx 
        print("exit")


if __name__ == '__main__':
    # File "/lib/brteve/brt_eve_rp2040.py", line 23, in pin
    # self.pin_dcx_eve_ili9488 = pin(board.GP8) #D/CX pin of ILI9488
     
    host = BrtEveRP2040()
    eve = BrtEve(host)
    #self.eve = BrtEveExt(self.host)
    #eve.init(resolution="1280x800", touch="goodix")
    eve.init(resolution="800x480", touch="capacity")
    #eve=self.eve
    #eve.calibrate()
    # eve.wr32(eve.REG_TOUCH_TRANSFORM_A, 0xfffefefc) # pre setting for 1280x800 lcd
    # eve.wr32(eve.REG_TOUCH_TRANSFORM_B, 0xfffffcbf)
    # eve.wr32(eve.REG_TOUCH_TRANSFORM_C, 0x506adb4)
    # eve.wr32(eve.REG_TOUCH_TRANSFORM_D, 0xfffffed1)
    # eve.wr32(eve.REG_TOUCH_TRANSFORM_E, 0xfffefc79)
    # eve.wr32(eve.REG_TOUCH_TRANSFORM_F, 0x32c3211)

    dmx_ui(eve).loop()