
from brteve.brt_eve_bt817_8 import BrtEve

# Configuration
USE_COCMD_SETBITMAP = 1
ENABLE_ROTATEAROUND = 1
# Graphics definitions
MAX_ANGLE           = 360
CIRCLE_MAX          = 65536

# Graphics unity
def ANGLE(x):
    return (x * 100 * CIRCLE_MAX / (MAX_ANGLE * 100))

FLASH_ADDRESS = (0x800000)
def ATFLASH(x):
    return (FLASH_ADDRESS | x / 32)

class _image:
    def __init__(self,
        index = 0,
        addressFlash = 0,
        addressRamg = 0,
        file_location = '',
        size = 0,
        x = 0,
        y = 0,
        w = 0,
        h = 0,
        bitmap_layout = 0,
        ext_format = 0,
        tag = 0,
        opt = 0,
        isFlash = 0):

        self.index         = index
        self.addressFlash  = addressFlash
        self.addressRamg   = addressRamg
        self.file_location = file_location
        self.size          = size
        self.x             = x
        self.y             = y
        self.w             = w
        self.h             = h
        self.bitmap_layout = bitmap_layout # see Table 13 – BITMAP_LAYOUT Format List
        self.ext_format    = ext_format # See Table 12 – Bitmap formats and bits per pixel
        self.tag           = tag
        self.opt           = opt
        self.isFlash       = isFlash

class helper_image():
    def __init__(self, eve: BrtEve) -> None:
        self.eve = eve

        # Status stores
        self.mangle = 0
        self.mrootx = 0
        self.mrooty = 0
        self.misRotate = 0
        self.misScale = 0


    def setup_bitmap(self, img: _image) :
        address = img.addressRamg

        if (img.isFlash) :
            address = ATFLASH(img.addressFlash)

        self.eve.cmd_setbitmap(address, img.bitmap_layout, img.w, img.h)

    def scale_bitmap(self, img: _image) :
        self.eve.cmd_loadidentity()
        self.eve.cmd_scale(self.scale_ratio * 65536, self.scale_ratio * 65536)
        self.eve.cmd_setmatrix()
        self.eve.BitmapSize(self.eve.BILINEAR, self.eve.BORDER, self.eve.BORDER, img.w * 2, img.h * 2)

    def rotate_bitmap(self, img: _image) :
        translateX = 1
        translateY = img.h - img.w

        if (img.w < img.h) :
            translateX = img.h - img.w
            translateY = 1

        mrootx = img.w/2
        mrooty = img.h/2

        if self.mrootx !=0 or self.mrooty !=0:
            mrootx = self.mrootx
            mrooty = self.mrooty

        if ENABLE_ROTATEAROUND:
            self.eve.cmd_loadidentity()
            self.eve.cmd_rotatearound(mrootx, mrooty, ANGLE(self.mangle), CIRCLE_MAX)
            self.eve.cmd_setmatrix()
        else:
            #  Use rotate and translate
            self.eve.cmd_loadidentity()
            self.eve.cmd_translate((translateX + mrootx) * CIRCLE_MAX,
                    (translateY + mrooty) * CIRCLE_MAX)
            self.eve.cmd_rotate(ANGLE(self.mangle))
            self.eve.cmd_translate(-(0 + mrootx) * CIRCLE_MAX,
                    -(0 + mrooty) * CIRCLE_MAX)
            self.eve.cmd_setmatrix()

    def draw_bitmap(self, img: _image) :
        if (img.tag != 0) : #  set TAG if the _image need to process gesture events
            self.eve.Tag(img.tag)
        else:
            self.eve.Tag(0)

        self.eve.Begin(self.eve.BITMAPS)
        self.eve.Vertex2f(img.x, img.y)

    def image_setup_scale(self, ratio) :
        self.misScale = 1
        self.scale_ratio = ratio

    def image_setup_rotate(self, angle, rootx = 0, rooty = 0) :
        self.misRotate = 1
        self.mangle = angle
        self.mrootx = rootx
        self.mrooty = rooty
        return 1

    def image_clear_scale(self) :
        self.misScale = 0
        self.scale_ratio = 1

    def image_clear_rotate(self) :
        self.misRotate = 0

    def image_copy_to_ramg(self, img: _image, isRestart) :
        ramgAddr = self.eve.RAM_G

        if (isRestart == 1) :
            ramgAddr = 0

        img.isFlash = 0
        img.addressRamg = ramgAddr
        self.eve.cmd_flashread(ramgAddr, img.addressFlash, img.size)
        ramgAddr += img.size
        return 1

    def image_copy_to_ramg_and_draw_image(self, img: _image, isRestart) :
        ramgAddr = self.eve.RAM_G

        if (isRestart == 1) :
            ramgAddr = 0

        img.isFlash = 0
        img.addressRamg = ramgAddr

        self.eve.cmd_flashread(ramgAddr, img.addressFlash, img.size)
        self.image_draw(img)

        ramgAddr += img.size
        return 1

    def image_draw(self, img: _image) :
        self.eve.SaveContext()

        if not img.file_location == '':

            self.eve.cmd_loadimage(0, img.opt)
            file_handler = open(img.file_location, "rb")
            self.eve.load(file_handler)
            file_handler.close()
        else:
            self.setup_bitmap(img)

        if (self.misRotate) :
            self.rotate_bitmap(img)
            self.misRotate = 0

        if (self.misScale) :
            self.scale_bitmap(img)
            self.misScale = 0

        self.draw_bitmap(img)
        self.eve.RestoreContext()
        return 1

    def image_load(self, img: _image) :
        eve=self.eve

        eve.cmd_loadimage(img.addressRamg , img.opt)
        file_handler = open(img.file_location, "rb")
        eve.load(file_handler)
        file_handler.close()

        # validate _image
        eve.flush()
        rp=eve.eve_write_pointer()
        eve.cmd_getprops()
        eve.flush()
        w=eve.rd32(eve.RAM_CMD + rp+4*2)
        h=eve.rd32(eve.RAM_CMD + rp+4*3)

        return w, h

    def image_load_from_jpeg(self, file_name, address, tag, opt) :
        img = _image()
        img.addressRamg = address
        img.file_location = file_name
        img.index = 0
        img.tag = tag
        img.opt = opt
        return self.image_load(img)

    def image_draw_from_file(self, file_name, x, y, w, h, bitmap_layout, ext_format, tag, opt) :
        img = _image()
        img.isFlash = 0
        img.file_location = file_name
        img.bitmap_layout = bitmap_layout
        img.ext_format = ext_format
        img.x = x
        img.y = y
        img.h = h
        img.w = w
        img.index = 0
        img.tag = tag
        img.opt = opt
        return self.image_draw(img)

    def image_draw_from_ram_g(self, address, x, y, w, h, bitmap_layout, ext_format, tag, opt) :
        img = _image()
        img.isFlash = 0
        img.addressRamg = address
        img.bitmap_layout = bitmap_layout
        img.ext_format = ext_format
        img.x = x
        img.y = y
        img.h = h
        img.w = w
        img.index = 0
        img.tag = tag
        img.opt = opt
        return self.image_draw(img)

    def image_draw_from_flash(self, address, x, y, w, h, bitmap_layout, ext_format, tag, opt) :
        img = _image()
        img.isFlash = 1
        img.addressFlash = address
        img.bitmap_layout = bitmap_layout
        img.ext_format = ext_format
        img.x = x
        img.y = y
        img.w = w
        img.h = h
        img.index = 0
        img.tag = tag
        img.opt = opt
        return self.image_draw(img)

    def zfill(self, s, num):
        strlen = len(s)
        for i in range(num - strlen):
            s = '0' + s
        return s

