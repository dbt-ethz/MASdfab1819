from __future__ import division
from mola.core import *
from mola.mathUtils import SinusFunction
import mola.polyUtils as polyUtils
import mola.vec as vec
import math
import gui

def initialize():
    global sinusGuiVertical,sinusGuiProfile,bUpdate
    global doUpdate
    doUpdate=False
    xPos=width-350
    sinusGuiVertical=gui.GuiSinus(gui.cp5, "Vertical", xPos+20, 120)
    sinusGuiVertical.sliderFrequency.setMax(10)
    sinusGuiVertical.sliderFrequency.setValue(1)
    sinusGuiVertical.sliderAmplitude.setValue(5)
    sinusGuiVertical.sliderPhase.setValue(0.25)
    sinusGuiProfile= gui.GuiSinus(gui.cp5, "Profile", xPos+20, 220)
    sinusGuiProfile.sliderFrequency.setValue(3)
    sinusGuiProfile.sliderAmplitude.setValue(5)
    sinusGuiProfile.sliderPhase.setValue(0.5)
    bUpdate = gui.createButton("Update", xPos+20, 20, 45, 45)
    guiEvents()
    createMesh()

def guiEvents():
    global doUpdate
    global freq_Z,amp_Z,phase_Z,freq_P,amp_P,phase_P
    freq_Z=sinusGuiVertical.getFrequency()
    amp_Z=sinusGuiVertical.getAmplitude()
    phase_Z=sinusGuiVertical.getPhase()
    freq_P=sinusGuiProfile.getFrequency()
    amp_P=sinusGuiProfile.getAmplitude()
    phase_P=sinusGuiProfile.getPhase()
    if bUpdate.getValue():
        doUpdate=True 
        createMesh()
        bUpdate.setValue(False)   
    
def createProfile(z):
    global freq_Z,amp_Z,phase_Z,freq_P,amp_P,phase_P
    vertices=polyUtils.constructCircle(15,128,z)
    iterations=4
    factor_Z=amp_Z*math.sin(freq_Z*(z/300)+phase_Z)
    for i in range(1,iterations,1):
        f=freq_P*i*i
        a=(factor_Z+amp_P)/(i*i)
        p=phase_P*z/300
        newVertices=[]
        v0=vertices[-2]
        v1=vertices[-1]
        for j,v2 in enumerate(vertices):
            nvec=polyUtils.normalVertex2D(v0,v1,v2)
            magnitude=a*math.sin(f*j/len(vertices)+p)
            nvec=vec.scale(nvec,magnitude)
            newVertices.append(vec.add(v2,nvec))
            v0=v1
            v1=v2
        vertices=newVertices
    return vertices

def createMesh():
    global column
    nZ=300
    vs0=None
    column=Mesh()
    for z in range(nZ):
        vs1=createProfile(z)
        if vs0!=None:
            for i0 in range(len(vs0)):
                i1=(i0+1)%len(vs0)
                column.faces.append(Face((vs0[i0],vs0[i1],vs1[i1],vs1[i0])))
        vs0=vs1
