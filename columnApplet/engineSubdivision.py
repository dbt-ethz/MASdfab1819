from mola.core import *
import mola.subdivision as subdivision
import mola.vec as _vec
import mola.io as io
import mola.faceUtils as faceUtils
import mola.renderP5 as renderer
import math
import gui

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
        column = column_subdivide(column, 1.0)
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
        if faceUtils.center(f).z < 100:
            f.group = 'pedestal'
        elif faceUtils.center(f).z > 200:
            f.group = 'capital'
        else: f.group = 'shaft'

def column_subdivide(mesh_, c_var=1):
    newFaces = []
    for f in mesh_.faces:
        #pedestal_______
        if f.group=='pedestal':
            fsc=sd_sided_tapered(f,.2)
            for f_ in fsc:
                f_.group = 'p_level_2'
            fsc[0].group='p_level_3'
            fsc[-1].group='p_level_3'
            newFaces.extend(fsc)
        elif f.group=='p_level_3':
            fsc=sd_sided_tapered(f,.2)
            for f_ in fsc:
                f_.group = 'p_level_4'
            fsc[0].group='stop'
            fsc[-1].group='stop'
            newFaces.extend(fsc)
        elif f.group=='p_level_4':
            fsc=subdivision.extrude(f,5)
            for f_ in fsc:
                f_.group = 'p_level_5'
            newFaces.extend(fsc)
        elif f.group=='p_level_2':
            fsc=subdivision.extrude(f,-15)
            for f_ in fsc:
                f_.group = 'stop'
            fsc[-1].group='p_level_3'
            newFaces.extend(fsc)
        #shaft_______
        elif f.group=='shaft':
            fsc=sd_sided_tapered(f,.2)
            for f_ in fsc:
                f_.group = 's_level_2'
            fsc[0].group='s_level_3'
            fsc[-1].group='s_level_3'
            newFaces.extend(fsc)
        elif f.group=='s_level_3':
            fsc=sd_sided_tapered(f,.2)
            for f_ in fsc:
                f_.group = 's_level_4'
            fsc[0].group='stop'
            fsc[-1].group='stop'
            newFaces.extend(fsc)
        elif f.group=='s_level_4':
            fsc=subdivision.extrude(f,5)
            for f_ in fsc:
                f_.group = 's_level_6'
            newFaces.extend(fsc)
        elif f.group=='s_level_2':
            fsc=subdivision.extrude(f,-15)
            for f_ in fsc:
                f_.group = 's_level_5'
            #fsc[-1].group='s_level_3'
            newFaces.extend(fsc)
        elif f.group=='s_level_6':
            fsc=subdivision.extrudeTapered(f,4.5,.4)
            for f_ in fsc:
                f_.group = 's_level_5'
            fsc[-1].group='s_level_6'
            newFaces.extend(fsc)
        #capital______
        elif f.group=='capital':
            fsc=sd_sided_tapered(f,.2)
            for f_ in fsc:
                f_.group = 'c_level_2'
            fsc[0].group='c_level_3'
            fsc[-1].group='c_level_3'
            newFaces.extend(fsc)
        elif f.group=='c_level_3':
            fsc=sd_sided_tapered(f,.2)
            for f_ in fsc:
                f_.group = 'c_level_4'
            fsc[0].group='c_level_3'
            fsc[-1].group='c_level_3'
            newFaces.extend(fsc)
        elif f.group=='c_level_4':
            fsc=subdivision.extrude(f,10)
            for f_ in fsc:
                f_.group = 'c_level_5'
            newFaces.extend(fsc)
        else:
            newFaces.append(f)
    m=Mesh()
    m.faces=newFaces
    for f in m.faces:
        if faceUtils.area(f)<25:
            f.group = 'stop'
    return m

def column_pedestal_capital(_mesh):
        newFaces = []
        for f in _mesh.faces:
            fsc=f_ped_cap_expand(f,60,80)
            for f_ in fsc:
                f_.group = f.group
            newFaces.extend(fsc)
        m=Mesh()
        m.faces=newFaces
        for f in m.faces:
            if faceUtils.area(f)<25:
                f.group = 'stop'
        return m


def sd_sided_tapered(_face,d):

    bottom = _vec.subtract(_face.vertices[2],_face.vertices[1])
    top    = _vec.subtract(_face.vertices[3],_face.vertices[0])

    b_vertices = []
    b_vertices.append(_face.vertices[1])
    pv = _vec.add(_face.vertices[1],_vec.scale(bottom,d))
    b_vertices.append(pv)
    pv = _vec.add(_face.vertices[1],_vec.scale(bottom,1-d))
    b_vertices.append(pv)
    b_vertices.append(_face.vertices[2])

    t_vertices = []
    t_vertices.append(_face.vertices[0])
    pv = _vec.add(_face.vertices[0],_vec.scale(top,d))
    t_vertices.append(pv)
    pv = _vec.add(_face.vertices[0],_vec.scale(top,1-d))
    t_vertices.append(pv)
    t_vertices.append(_face.vertices[3])
    new_faces=[]

    for i in range(3):
        vts = []
        vts.append(b_vertices[i+1])
        vts.append(t_vertices[i+1])
        vts.append(t_vertices[i])
        vts.append(b_vertices[i])
        new_faces.append(Face(vts))
    return new_faces

def f_ped_cap_expand(_face, pedestal_h, capital_h):
    new_faces=[]
    vts = []
    var1=1.1
    var2=0.9
    for vt in _face.vertices:
        if vt.z<pedestal_h:
            vt = Vertex(vt.x*var1,vt.y*var1,vt.z)
        elif vt.z>280:
            vt = Vertex(vt.x,vt.y,vt.z)
        elif vt.z>capital_h:
            vt = Vertex(vt.x*var2,vt.y*var2,vt.z)
        vts.append(vt)
    new_faces.append(Face(vts))
    return new_faces