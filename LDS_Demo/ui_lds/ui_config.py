class ui_config():
    skipSensor=False
    def __init__(self):
        self.aa=240/96
        self.bb=256 *(1/self.aa)
        self.tagReleased=0
        self.firstTime=True
        self.simulatorTitle="."
        self.debug=False
        #self.debug=True #  have debug button
        
        self.btn_w = 110
        self.btn_h = 35
        self.x0 = 10
        self.y0 = 10

        self.xmargin =10
        self.xStart = 380
        self.timeout=100
