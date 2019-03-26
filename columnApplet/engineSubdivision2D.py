from __future__ import division
from mola.core import *
from mola.mathUtils import SinusFunction
import mola.polyUtils as polyUtils
import mola.vec as vec
import math
import gui

"""
    initialise() is called once at the beginning
    guiEvents() is called in each frame
    global doUpdate indicates that the main applet should update the PSHAPE
    global column should store the mesh which represents the column geometry
"""

def initialize():
    global sinusGuiVertical,bUpdate
    global doUpdate
    doUpdate=False
    xPos=width-350
    sinusGuiVertical=gui.GuiSinus(gui.cp5, "Vertical", xPos+20, 120)
    sinusGuiVertical.sliderFrequency.setMax(10)
    sinusGuiVertical.sliderFrequency.setValue(1)
    sinusGuiVertical.sliderAmplitude.setValue(5)
    sinusGuiVertical.sliderPhase.setValue(0.25)
    bUpdate = gui.createButton("Update", xPos+20, 20, 45, 45)
    guiEvents()
    createMesh()

def guiEvents():
    global freq_Z,doUpdate
    freq_Z=sinusGuiVertical.getFrequency()
    if bUpdate.getValue():
        doUpdate=True
        createMesh()
        bUpdate.setValue(False)

def createMesh():
    global column
    nZ=300
    vs0=None
    column=Mesh()
    for z in range(nZ):
        vs1=createProfileSubdivision(z)
        if vs0!=None:
            for i0 in range(len(vs0)):
                i1=(i0+1)%len(vs0)
                column.faces.append(Face((vs0[i0],vs0[i1],vs1[i1],vs1[i0])))
        vs0=vs1

def createProfileSubdivision(z):
    global freq_Z
    vertices=polyUtils.constructCircle(15,8,z)
    for i in range(3):
        newVertices=[]
        v0=vertices[-1]
        for i,v1 in enumerate(vertices):
            newVertices.append(v0)
            n=polyUtils.normalEdge2DNonUnified(v0,v1)

            n=vec.scale(n,math.sin(freq_Z*z/300))
            center=vec.betweenRel(v0,v1,0.5)
            newVertices.append(vec.add(center,n))
            v0=v1
        vertices=newVertices
    #vertices=polyUtils.subdivideCatmull2D(vertices)
    return vertices
