 
 
from brteve.brt_eve_bt817_8 import BrtEve
from brteve.brt_eve_rp2040 import BrtEveRP2040

from IDM2040_demo.blinka_rotate import blinka_rotate  



print("start blinka")

#if __name__ == "__main__":
host = BrtEveRP2040()
eve = BrtEve(host)
#eve.init(resolution="1280x800", touch="goodix")
eve.init(resolution="800x480", touch="capacity")
 
blinka_rotate(eve).run()
