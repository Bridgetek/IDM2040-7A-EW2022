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
        
        self.btn_w = 75
        self.btn_h = 30

        self.xmargin =10
        self.xStart = 380
