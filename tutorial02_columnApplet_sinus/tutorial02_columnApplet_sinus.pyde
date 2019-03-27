add_library('peasycam')
add_library('controlP5')

import math, datetime
import engineSinus as engine
import gui as gui
import mola.io as io
import mola.slicer as slicer
import mola.renderP5 as renderer
import mola.color as coloriser

def setup():
    global sliceZ,pshapeSlice,guiDimX

    guiDimX=400
    pshapeSlice=None
    sliceZ=0
    size(1600, 900, P3D)
    #fullScreen(P3D)
    gui.cam = PeasyCam(this,350)
    gui.cp5 = ControlP5(this)
    gui.cp5.setAutoDraw(False)
    gui.initialize()
    engine.initialize()

    update()

def draw():

    if mouseX < guiDimX or mouseX>width-guiDimX:
        gui.cam.setActive(False)
    else:
        gui.cam.setActive(True)

    background(255)
    hint(DISABLE_DEPTH_TEST)
    gui.cam.beginHUD()
    image(gui.backgroundImage, 0, 0)
    gui.cam.endHUD()
    hint(ENABLE_DEPTH_TEST)

    display3D()
    display2D()


def update():
    global pshapeColumn
    fill(200)
    if gui.displayMode=="White":
        for f in engine.column.faces:
            f.color=(1,1,1,1)
    if gui.displayMode=="Curvature":
        coloriser.colorFacesByCurvature(engine.column.faces)
    if gui.displayMode=="Area":
        coloriser.colorFacesByArea(engine.column.faces)
    if gui.displayMode=="Perimeter":
        coloriser.colorFacesByPerimeter(engine.column.faces)
    if gui.displayMode=="Compactness":
        coloriser.colorFacesByCompactness(engine.column.faces)
    if gui.displayMode=="Vertical Angle":
        coloriser.colorFacesByVerticalAngle(engine.column.faces)
    if gui.displayMode=="Horizontal Angle":
        coloriser.colorFacesByHorizontalAngle(engine.column.faces)
    if gui.displayMode=="Group":
        faceGroups={}
        randomSeed(1)
        for f in engine.column.faces:
            faceGroups[f.group]=(random(0,1),random(0,1),random(0,1),1)
        for f in engine.column.faces:
            f.color= faceGroups[f.group]
    noStroke()
    pshapeColumn=renderer.createMeshShape(engine.column)

def display2D():
    global screen
    gui.cam.beginHUD()
    fill(40)
    gui.cp5.draw()
    pushMatrix()
    translate(guiDimX/2-5,height-guiDimX/2-100)
    scale(3)
    stroke(255)
    strokeWeight(0.25)
    noFill()
    rect(-60,-60,120,120)
    stroke(0,255,0)
    ellipse(0,0,25,25)
    if pshapeSlice!=None:
        strokeWeight(1)
        shape(pshapeSlice)
    popMatrix()
    gui.cam.endHUD()

def display3D():
    global sliceZ,pshapeSlice, rotZ
    if sliceZ!=gui.sliderSlice.getValue():
        sliceZ=gui.sliderSlice.getValue()
        stroke(255,0,0)
        pshapeSlice=renderer.createLinesShape(slicer.slice(engine.column,sliceZ))

    selectedIndex = gui.listDisplay.getValue()
    selectedDisplayMode = gui.listDisplay.getItem(int(selectedIndex)).get("text")
    if selectedDisplayMode!=gui.displayMode:
        gui.displayMode=selectedDisplayMode
        update()

    # mesh rendering
    directionalLight(255, 255, 255, 1, 1, 1)
    directionalLight(255, 255, 255, -1, -1, -1)
    noStroke()
    pushMatrix()
    if gui.bDance.getBooleanValue():
        fill(255,50)
        shape(gui.dancer)
    rotateX(math.pi*0.5)
    translate(0,0,-150)
    if gui.bRot.getBooleanValue():
        rotZ+=0.01
    else:
        rotZ=0
    rotateZ(rotZ)
    if gui.bBase.getBooleanValue():
        pushMatrix()
        translate(0, 0, -10)
        fill(150)
        box(120, 120, 20)
        popMatrix()
    if pshapeColumn!=None:
        shape(pshapeColumn)
    if gui.bDisplaySlice.getValue():
        pushMatrix()
        translate(0,0,sliceZ)
        fill(200,100)
        rect(-60,-60,120,120)
        popMatrix()
        if pshapeSlice!=None:
            shape(pshapeSlice)
    popMatrix()
    
def keyPressed():
    if key == 's':
        saveFrame("/screenshots/" + get_time_stamp() + ".jpg")
        
def get_time_stamp():
    ts = str(year())+str(month())+str(day())+str("_")+str(hour())+str(minute())+str(second())
    return ts
