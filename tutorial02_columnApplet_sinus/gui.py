from engineSinus import SinusFunction
import math

def initialize():
    global cam,cp5
    global listDisplay,bExport, bReset, bBase, bDance, sliderSlice,bRot
    global bDisplaySlice,displayMode
    global dancer
    dancer= loadShape("Female_Base_Mesh.obj")
    println(dancer.getVertexCount())
    dancer.scale(100,-100,100)
    dancer.translate(50,150,-50)
    dancer.disableStyle()
    createVignette()
    
    cY=100
    bDisplaySlice = createToggle("Slice", 20, cY, 45, 45)
    bBase = createToggle("Base", 70, cY, 45, 45)
    bDance = createToggle("Dancer", 120, cY, 45, 45)
    bRot = createToggle("Rotate", 170, cY, 45, 45)
    bExport = createButton("Export", 340, cY, 45, 45)

    sliderSlice = createSlider("Slice Z", 20, height-100, 0, 300).setSize(340,15)

    listDisplay = cp5.addScrollableList("display")
    listDisplay.setPosition(20, 50)
    listDisplay.setWidth(190)
    listDisplay.setHeight(500)
    listDisplay.setItems(["White","Group","Curvature","Area","Perimeter","Compactness","Vertical Angle","Horizontal Angle"])
    listDisplay.setOpen(True)
    listDisplay.setValue(0)
    listDisplay.bringToFront()
    displayMode="Group"

class GuiSinus(object):
    def __init__(self,cp5,i,x,y):
        self.sliderAmplitudeH = createSlider("H   Amplitude "+str(i), x, y, 0, 100)
        self.sliderFrequencyH = createSlider("H   Frequency "+str(i), x, y+20, 0, 50)
        self.sliderPhaseH = createSlider("H   Phase "+str(i), x, y+40, 0, 1)

        self.sliderAmplitudeV = createSlider("V   Amplitude "+str(i), x, y+60, 0, 100)
        self.sliderFrequencyV = createSlider("V   Frequency "+str(i), x, y+80, 0, 50)
        self.sliderPhaseV = createSlider("V   Phase "+str(i), x, y+100, 0, 1)
        
    def getSinusFunctionH(self):
        return SinusFunction(self.sliderFrequencyH.getValue()*math.pi*2,self.sliderAmplitudeH.getValue(),math.pi*2*self.sliderPhaseH.getValue(),0)
    def getSinusFunctionV(self):
        return SinusFunction(self.sliderFrequencyV.getValue()*math.pi*2,self.sliderAmplitudeV.getValue(),math.pi*2*self.sliderPhaseV.getValue(),0)

def createSlider(name, posX, posY, rangeX, rangeY):
    s = cp5.addSlider(name).setRange(rangeX, rangeY).setPosition(posX, posY)
    s.setSize(195, 15)
    s.setColorActive(color(255, 0, 155))
    s.setColorForeground(color(0))
    s.setColorBackground(color(70, 200))
    return s

def createButton(name, posX, posY, sX, sY):
    b = cp5.addToggle(name).setPosition(posX, posY).setSize(sX, sY)
    b.setColorForeground(color(255, 0, 155)).setColorBackground(color(70, 200))
    return b

def createToggle(name, posX, posY, sX, sY):
    b = cp5.addToggle(name).setPosition(posX, posY).setSize(sX, sY)
    b.setColorValue(10).setColorActive(color(255)).setColorForeground(color(255, 0, 155)).setColorBackground(color(70, 200))
    return b

def createVignette():
    global backgroundImage, msk
    msk = createGraphics(width, height)
    msk.beginDraw()
    msk.noStroke()
    msk.ellipseMode(RADIUS)
    rad = int(((width/2)**2 + (height/2)**2)**0.5)
    c = 255
    for r in range(rad, 0, -1):
        c -= 255.0/rad
        msk.fill(int(c))
        msk.ellipse(width/2, height/2, r, r)
    msk.endDraw()
    backgroundImage = createGraphics(width, height)
    backgroundImage.beginDraw()
    backgroundImage.background(80)
    backgroundImage.endDraw()
    backgroundImage.mask(msk)
    return backgroundImage

def loadLogo():
    global logo
    logo = loadImage("dbt_logo.png")
