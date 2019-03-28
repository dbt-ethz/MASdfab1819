from mola.core import *
from mola.mathUtils import SinusFunction
import mola.subdivision as subdivision
import mola.polyUtils as polyUtils
import mola.faceUtils as faceUtils
import mola.io as io
import mola.vec as vec
import math, gui
"""
    initialise() is called once at the beginning
    guiEvents() is called in each frame
    global doUpdate indicates that the main applet should update the PSHAPE
    global column should store the mesh which represents the column geometry
"""
def initialize():
    global sinusGuiVertical, sinusGuiSubdiv, bUpdate, bReset, bSubdiv, bSmooth
    global column
    global doUpdate
    doUpdate=False
    xPos=width-350

    sinusGuiVertical = gui.GuiSinus(gui.cp5, "Sinus Profile", xPos+20, 200)
    sinusGuiVertical.sliderFrequency.setMax(0.5)
    sinusGuiVertical.sliderAmplitude.setMax(10)

    bUpdate = gui.createButton("Update", xPos+20, 100, 45, 45)
    bReset = gui.createButton("Reset", xPos+70, 100, 45, 45)
    bSubdiv = gui.createButton("Subdiv", xPos+20, 300, 45, 45)
    bSmooth = gui.createButton("Smooth", xPos+120, 300, 45, 45)

    sinusGuiSubdiv = gui.GuiSinus(gui.cp5, "Sinus Subdiv", xPos+20, 380)
    sinusGuiSubdiv.sliderFrequency.setMax(0.5)
    sinusGuiSubdiv.sliderAmplitude.setMax(10)

    column = io.importOBJ(sketchPath()+'/data/column_in.obj')
    assign_pedestal_capital(column)

def guiEvents():
    global column
    global zFreq, zAmp, zPhase, zOffset
    global sdFreq, sdAmp, sdPhase, sdOffset
    global doUpdate
    zFreq = sinusGuiVertical.getFrequency()
    zAmp = sinusGuiVertical.getAmplitude()
    zPhase = sinusGuiVertical.getPhase()
    zOffset = sinusGuiVertical.getOffset()
    sdFreq = sinusGuiSubdiv.getFrequency()
    sdAmp = sinusGuiSubdiv.getAmplitude()
    sdPhase = sinusGuiSubdiv.getPhase()
    sdOffset = sinusGuiSubdiv.getOffset()
    
    # sine events
    if bUpdate.getValue():
        column = shapeProfile(column)
        assign_pedestal_capital(column)
        doUpdate=True
        bUpdate.setValue(False)

    if bReset.getValue():
        sinusGuiVertical.sliderFrequency.setValue(0)
        sinusGuiVertical.sliderAmplitude.setValue(0)
        sinusGuiVertical.sliderPhase.setValue(0)
        sinusGuiVertical.sliderOffset.setValue(0)
        column = io.importOBJ(sketchPath()+'/data/column_in.obj')
        bReset.setValue(False)
        doUpdate=True

    # subdiv events
    if bSubdiv.getValue():
        column = column_subdivide(column)
        bSubdiv.setValue(False)
        doUpdate=True

    if bSmooth.getValue():
        column.updateAdjacencies()
        column = subdivision.subdivideCatmull(column)
        bSmooth.setValue(False)
        doUpdate=True

def shapeProfile(mesh):
    zFunction = SinusFunction(zFreq, zAmp, zPhase, zOffset)
    for v in mesh.vertices:
        pos_z = (v.z/300.0)*2*math.pi
        val_z = zFunction.getValue(pos_z)
        normal = vec.subtract(v, Vertex(0, 0, v.z))
        normal = vec.unitize(normal)
        nvec = vec.scale(normal, val_z)
        v.add(nvec)
    return mesh

def assign_pedestal_capital(mesh):
    for f in mesh.faces:
        if faceUtils.center(f).z < 80:
            f.group = "pedestal"
        elif faceUtils.center(f).z > 280:
            f.group = "capital"
        else: f.group = "shaft"

def column_subdivide(_mesh):
    sdFunction = SinusFunction(sdFreq, sdAmp, sdPhase, sdOffset)

    newFaces=[]
    for f in _mesh.faces:
        if f.group=='shaft':
            fcs = sd_sided_tapered (f,0.2)
            for _f in fcs:
                _f.group='s_level_2'
            fcs[1].group = 's_level_3'
            newFaces.extend(fcs)
        
        elif f.group=='s_level_2':
            fcs=sd_sided_tapered (f,0.1)
            for _f in fcs:
                _f.group='stop'
            fcs[1].group='s_level_4'
            newFaces.extend(fcs)
            
        elif f.group=='s_level_3':
            fcs=subdivision.extrude(f,-10)
            for _f in fcs:
                if abs ( faceUtils.vertical_angle(_f)) < PI/2-0.1:
                    _f.group = 'stop'
                    newFaces.append(_f)
            
        elif f.group=='s_level_4':
            # sine based extrusion
            z = faceUtils.center(f).z
            pos_z = (z/300.0)*2*math.pi
            value = sdFunction.getValue(pos_z)

            fcs=subdivision.extrude(f,value)
            for _f in fcs:
                if abs ( faceUtils.vertical_angle(_f)) < PI/2-0.1:
                    _f.group = 's_level_5'
                    newFaces.append(_f)
            
        # pedestal_________
        elif f.group == 'pedestal':
            fcs = sd_sided_tapered (f,0.2)
            for _f in fcs:
                _f.group='p_level_2'
            fcs[1].group = 'p_level_3'
            newFaces.extend(fcs)
        
        elif f.group=='p_level_2':
            fcs=sd_sided_tapered (f,0.1)
            for _f in fcs:
                _f.group='stop'
            fcs[1].group='p_level_4'
            newFaces.extend(fcs)
            
        elif f.group=='p_level_3':
            fcs=subdivision.extrude(f,-10)
            for _f in fcs:
                if abs (faceUtils.vertical_angle(_f)) < PI/2-0.1:
                    _f.group = 'stop'
                    newFaces.append(_f)
        
        elif f.group == 'p_level_4':
            fcs=subdivision.extrude(f,5)
            for _f in fcs:
                if abs(faceUtils.vertical_angle(_f))< PI/2-0.1:
                    if fcs.index(_f)==1: _f.group ='stop'
                    else: 
                        _f.group = 'p_level_5'
                        newFaces.append(_f)
                        
        elif f.group == 'p_level_5':
            # sine based extrusion
            z = faceUtils.center(f).z
            pos_z = (z/300.0)*2*math.pi
            value = sdFunction.getValue(pos_z)

            fcs = subdivision.extrudeTapered(f,value*3,0.5)
            for _f in fcs:
                _f.group='stop'
            newFaces.extend(fcs)
        # capital______
        elif f.group == 'capital':
                fcs = sd_sided_tapered (f,0.4)
                for _f in fcs:
                    _f.group='p_level_2'
                fcs[1].group = 'p_level_3'
                newFaces.extend(fcs)

        else:
            newFaces.append(f)
            
    m=Mesh()
    m.faces=newFaces
    return m

def sd_sided_tapered(face, d=0.1):
    # d should be between 0.01 and 0.49
    bottom = vec.subtract(face.vertices[2], face.vertices[1])
    top = vec.subtract(face.vertices[3], face.vertices[0])

    b_vertices = []
    b_vertices.append(face.vertices[1])
    pv = vec.add(face.vertices[1], vec.scale(bottom, d))
    b_vertices.append(pv)
    pv = vec.add(face.vertices[1], vec.scale(bottom, 1-d))
    b_vertices.append(pv)
    b_vertices.append(face.vertices[2])

    t_vertices = []
    t_vertices.append(face.vertices[0])
    pv = vec.add(face.vertices[0], vec.scale(top, d))
    t_vertices.append(pv)
    pv = vec.add(face.vertices[0], vec.scale(top, 1-d))
    t_vertices.append(pv)
    t_vertices.append(face.vertices[3])

    newFaces = []
    for i in range(3):
        vts = []
        vts.append(t_vertices[i])
        vts.append(b_vertices[i])
        vts.append(b_vertices[i+1])
        vts.append(t_vertices[i+1])
        newFaces.append(Face(vts))
    return newFaces