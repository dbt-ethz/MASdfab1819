from mola.core import *
import mola.subdivision as subdivision
import mola.vec as _vec
import mola.io as io
import mola.faceUtils as faceUtils
import mola.renderP5 as renderer
import math
import gui

"""
    initialise() is called once at the beginning
    guiEvents() is called in each frame
    global doUpdate indicates that the main applet should update the PSHAPE
    global column should store the mesh which represents the column geometry
"""
def initialize():
    global bShape,bSubdiv,bReset,bSmooth
    global initialColumn, column
    xPos=width-350
    # adding gui buttons and toggles
    bShape = gui.createButton("Shape", xPos+20, 100, 45, 45)
    bSubdiv = gui.createButton("Subdiv", xPos+70, 100, 45, 45)
    bReset = gui.createButton("Reset", xPos+120, 100, 45, 45)
    bSmooth = gui.createButton("Smooth", xPos+170, 100, 45, 45)

    initialColumn = io.importOBJ(sketchPath()+'/data/column_in.obj')
    column = initialColumn
    assign_pedestal_capital(column)

def guiEvents():
    global doUpdate,column,initialColumn
    doUpdate=False
    if bSubdiv.getValue():
        column = column_subdivide(column)
        bSubdiv.setValue(False)
        doUpdate=True
    if bShape.getValue():
        column = column_pedestal_capital(column)
        bShape.setValue(False)
        doUpdate=True
    if bReset.getValue():
        column = initialColumn
        bReset.setValue(False)
        doUpdate=True
    if bSmooth.getValue():
        column.updateAdjacencies()
        column = subdivision.subdivideCatmull(column)
        bSmooth.setValue(False)
        doUpdate=True

def assign_pedestal_capital(_mesh):
    
def column_subdivide(mesh_):

def column_pedestal_capital(_mesh):

def sd_sided_tapered(_face,d):

def f_ped_cap_expand(_face, pedestal_h, capital_h):
