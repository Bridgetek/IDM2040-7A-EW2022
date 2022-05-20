from IDM2040_demo.tags_all import *
import microcontroller
import watchdog
import time

import sys
import time
import gc

from brteve.brt_eve_rp2040 import BrtEveRP2040

if sys.implementation.name == "circuitpython":
    from brteve.brt_eve_bt817_8 import BrtEve
else:
    from ....lib.brteve.brt_eve_bt817_8 import BrtEve

# controler class
class main_app():

    def __init__(self):
        self.host = BrtEveRP2040()
        self.eve = BrtEve(self.host)
        #self.eve = BrtEveExt(self.host)
        #eve.init(resolution="1280x800", touch="goodix")
        #self.eve.init(resolution="1280x800", touch="capacity")  # old device
        self.eve.init(resolution="800x480", touch="capacity")
        #self.eve.calibrate()
        # eve.wr32(eve.REG_TOUCH_TRANSFORM_A, 0xfffefefc) # pre setting for 1280x800 lcd
        # eve.wr32(eve.REG_TOUCH_TRANSFORM_B, 0xfffffcbf)
        # eve.wr32(eve.REG_TOUCH_TRANSFORM_C, 0x506adb4)
        # eve.wr32(eve.REG_TOUCH_TRANSFORM_D, 0xfffffed1)
        # eve.wr32(eve.REG_TOUCH_TRANSFORM_E, 0xfffefc79)
        # eve.wr32(eve.REG_TOUCH_TRANSFORM_F, 0x32c3211)

        eve=self.eve  
 

    def drawBtn(self):
        eve = self.eve
        eve.ColorRGB(0xff, 0xff, 0xff)

        y =  90
        btn_w = 300
        btn_h = 60

        xmargin =100
        center = 200
        x1 = 50
        ymargin =40

        x2 = x1 + btn_w + xmargin
        x3 = x2 + btn_w + xmargin
        x4 = x3 + btn_w + xmargin
        x5 = x4 + btn_w + xmargin

        y2 = y + btn_h + ymargin
        y3 = y2 + btn_h + ymargin
        y4 = y3 + btn_h + ymargin

        eve.Tag(tag_cube_demo)
        eve.cmd_button(x1, y, btn_w, btn_h, 31, 0, "3D Cube Demo")
        eve.Tag(tag_blinka_dema)
        eve.cmd_button(x2, y, btn_w, btn_h, 31, 0, "Blinka Demo")
 

        eve.Tag(tag_image_View)
        eve.cmd_button(x1, y2, btn_w, btn_h, 31, 0, "Image Viewer")
        eve.Tag(tag_dmx512_demo)
        eve.cmd_button(x2, y2, btn_w, btn_h, 31, 0, "DMX512 Demo")
        
        eve.Tag(tag_audio_playback)
        eve.cmd_button(x1, y3, btn_w, btn_h, 31, 0, "Audio playback")
        eve.Tag(tag_video_playback)
        eve.cmd_button(x2, y3, btn_w, btn_h, 31, 0, "Video Playback")


#         eve.Tag(tag_alarm_clock)
#         eve.cmd_button(x1, y4, btn_w, btn_h, 31, 0, "Alarm clock")

#         eve.Tag(tag_lds_demo)
#         eve.cmd_button(x2, y4, btn_w, btn_h, 31, 0, "LDS Demo")

  
    def showException(self):
        self.eve.cmd_dlstart() #   
        self.eve.ColorRGB(255, 0, 0)  
        self.eve.cmd_text(520, 10, 30, 0, "Exception !")
        self.eve.Display()
        self.eve.cmd_swap()  #Co-processor faulty
        self.eve.flush()
        time.sleep(2)
    def showFreeMem(self):
        gc.collect()
        print("mem_free",gc.mem_free() )        
    def get_event(self):
        eve = self.eve     
        tag = eve.rd32(eve.REG_TOUCH_TAG) & 0xFF       
        return tag

    def processEvent(self,tag):
        eve = self.eve
        if tag == tag_cube_demo:
                print("tag_cube_demo")
                from IDM2040_demo.cube import cube 
                #del eve
                #eve.deinit()
                #eve.init(resolution="800x480", touch="capacity")
                cube(eve).loop()

        elif tag == tag_blinka_dema:
                print("tag_blinka_dema")
                #del eve
                #eve.init(resolution="800x480", touch="capacity")
                from IDM2040_demo.blinka_rotate import blinka_rotate  
                blinka_rotate(eve).run()

        elif tag == tag_dmx512_demo:
            #from IDM2040_demo.dmx512 import dmx512 as dmx512
            from  dmx512.dmx_ui import dmx_ui  
            dmx_ui(eve).loop()
            pass
        
#         elif tag == tag_alarm_clock:
#             print("tag_alarm_clock")
#             gc.collect()
#             print("mem_free",gc.mem_free() )
#             from alarm_clock.alarm_clock import alarm_clock 
#             alarm_clock(eve)
            
            
        elif tag == tag_image_View:
            print("tag_image_View")
            #from ir_sensors_and_gestures import ir_sensors_and_gestures
            from image_viewer.image_viewer import image_viewer  
            spi1 = eve.spi_sdcard()
            eve.finish()
            try:
                app=image_viewer(eve)
                app.deinit()
                self.showFreeMem()
            except  Exception as e:
                print("Exception:",e)
                #self.showException()
        elif tag == tag_audio_playback:
            print("tag_audio_playback")
            from audio_play.audio_play import audio_play             
            audio_play(eve)
        elif tag == tag_video_playback:
             print("tag_video_playback")
             import video2 as demo
             sdcard= "/sd/"
             demo.start(sdcard, eve)
             time.sleep(0.5)

    def loop(self):

        eve = self.eve
        #layout = self.layout
        #helper=self.helper
        eve.cmd_dlstart() #   
        eve.ClearColorRGB(0, 0, 0) #white

        eve.Clear(1, 1, 1)
        #self.eve.ClearColorA(0)

         
        x = 20; y = 10
        eve.cmd_text(x, y, 31, 0, "IDM2040 demo")


        self.drawBtn()
 

        ev = self.get_event()


        try:
            eve.Display()
            eve.cmd_swap() 
            eve.flush() 
            eve.cmd_loadidentity() 

        except  Exception as e:
            print("exceprion:",e)
        self.processEvent(ev)
        eve.Tag(0)
        time.sleep(0.05)



if __name__ == '__main__':
    mainMenu=main_app()
    mainMenu.showFreeMem()
 
    wdt = microcontroller.watchdog
    #wdt.timeout = 3
    #wdt.mode = watchdog.WatchDogMode.RAISE #Currently on RP2040, RAISE mode is not implemented
    #wdt.mode = watchdog.WatchDogMode.RESET
    try:
        while 1:
            mainMenu.loop()
            #wdt.feed()
    except watchdog.WatchDogTimeout as e:
        print("Watchdog expired")
    except Exception as e:
        print("Other exception:",e)
        microcontroller.reset()





