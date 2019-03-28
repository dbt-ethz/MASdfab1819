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
    
    for f in _mesh.faces:
        if faceUtils.center(f).z<80: 
            f.group='pedestal'
        elif faceUtils.center(f).z> 290:
            f.group='pedestal'
        else: f.group = 'shaft'
    
def column_subdivide(_mesh):
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
            fcs=subdivision.extrude(f,5)
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
                if abs ( faceUtils.vertical_angle(_f)) < PI/2-0.1:
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
            fcs = subdivision.extrudeTapered(f,10,0.5)
            for _f in fcs:
                _f.group='stop'
            newFaces.extend(fcs)
        # capital______
        
        else:
            newFaces.append(f)
            
    m=Mesh()
    m.faces=newFaces
    
    return m
                
        
                
        
        
    
    
    

def column_pedestal_capital(_mesh):
    pass

def sd_sided_tapered(_face,d=0.1):
    # d should be between 0.01 and 0.49
    bottom = _vec.subtract(_face.vertices[2], _face.vertices[1])
    top = _vec.subtract(_face.vertices[3], _face.vertices[0])
    
    b_vertices = []
    b_vertices.append(_face.vertices[1])
    pv = _vec.add(_face.vertices[1], _vec.scale(bottom,d))
    b_vertices.append(pv)
    pv = _vec.add(_face.vertices[1], _vec.scale(bottom,1-d))
    b_vertices.append(pv)
    b_vertices.append(_face.vertices[2])
    
    t_vertices = []
    t_vertices.append(_face.vertices[0])
    pv = _vec.add(_face.vertices[0], _vec.scale(top,d))
    t_vertices.append(pv)
    pv = _vec.add(_face.vertices[0], _vec.scale(top,1-d))
    t_vertices.append(pv)
    t_vertices.append(_face.vertices[3])
    
    new_faces=[]
    
    for i in range (3):
        vts=[]
        vts.append(t_vertices[i])
        vts.append(b_vertices[i])
        vts.append(b_vertices[i+1])
        vts.append(t_vertices[i+1])
        new_faces.append(Face(vts))
    return new_faces
    

def f_ped_cap_expand(_face, pedestal_h, capital_h):
    pass
