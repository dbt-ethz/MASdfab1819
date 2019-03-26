add_library('peasycam')
from mola.core import *

def setup():
    global p,phaseMove
    p=0
    phaseMove=False
    size(640,480,P3D)

def constructCircle(radius,nSegs=16,z=0):
    vertices=[]
    deltaAngle=PI*2.0/nSegs
    for i in range(nSegs):
        cAngle=i*deltaAngle
        x=radius*cos(cAngle)
        y=radius*sin(cAngle)
        vertices.append(Vertex(x,y,z))
    return vertices

def mousePressed():
    global phaseMove
    phaseMove=not phaseMove

def draw():
    global p,phaseMove
    if phaseMove:
        p+=0.1
    camera(300,0,0,0,0,0,0,1,0)
    background(0)
    noFill()
    rotateX(HALF_PI)
    translate(0,0,-150)
    colorMode(HSB)
    for z in range(100):
        stroke(z,255,255)
        f=float(mouseY)/float(height)
        a=30*float(mouseX)/float(width)
        circleVertices=constructCircle(20+sin(z*f+p)*a,32,z*3)
        beginShape()
        for v in circleVertices:
            vertex(v.x,v.y,v.z)
        endShape(CLOSE)
