from __future__ import division
from mola.core import *
from mola.mathUtils import SinusFunction
import mola.polyUtils as polyUtils
import mola.vec as vec
import math
import gui

def initialize():
    createMesh()

def createMesh():
    global column, nLayers, nSegments, layerHeight
    layerHeight=0.5
    nLayers=600
    nSegments=200
    vs0=None
    column=Mesh()
    for z in range(nLayers):
        vs1=polyUtils.constructCircle(15,nSegments,z*layerHeight)
        if vs0!=None:
            for i0 in range(len(vs0)):
                i1=(i0+1)%len(vs0)
                column.faces.append(Face((vs0[i0],vs0[i1],vs1[i1],vs1[i0])))
        vs0=vs1
