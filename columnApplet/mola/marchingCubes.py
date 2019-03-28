#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__     = ['Benjamin Dillenburger','Demetris Shammas','Mathias Bernhard']
__copyright__  = 'Copyright 2019 / Digital Building Technologies DBT / ETH Zurich'
__license__    = 'MIT License'
__email__      = ['<dbt@arch.ethz.ch>']

import math
from mola.core import Vertex
from mola.core import Mesh
from mola.core import Face

def _v( v1,  v2,  iso):
	if (abs(v2 - v1) < 0.0000001):
		return 0
	return (iso - v1) / (v2 - v1)

def marchingCubesFromGrid(grid,iso):
    return marchingCubes(grid.nX,grid.nY,grid.nZ,grid.values,iso)

def marchingCubes(nX,nY,nZ,values,iso):
	mesh =  Mesh()
	nYZ = nY * nZ
	index = 0
	n =[0]*8
	switcher = {
		0:lambda: Vertex(x + _v(n[0], n[1], iso), y + 1, z),
		1:lambda: Vertex(x + 1, y + _v(n[2], n[1], iso), z),
		2:lambda: Vertex(x + _v(n[3], n[2], iso), y, z),
		3:lambda: Vertex(x, y + _v(n[3], n[0], iso), z),
		4:lambda: Vertex(x + _v(n[4], n[5], iso), y + 1, z + 1),
		5:lambda: Vertex(x + 1, y + _v(n[6], n[5], iso), z + 1),
		6:lambda: Vertex(x + _v(n[7], n[6], iso), y, z + 1),
		7:lambda: Vertex(x, y + _v(n[7], n[4], iso), z + 1),
		8:lambda: Vertex(x, y + 1, z + _v(n[0], n[4], iso)),
		9:lambda: Vertex(x + 1, y + 1, z + _v(n[1], n[5], iso)),
		10:lambda: Vertex(x, y, z + _v(n[3], n[7], iso)),
		11:lambda: Vertex(x + 1, y, z + _v(n[2], n[6], iso))
	}
	for x in range(nX - 1):
		for y in range(nY - 1):
			for z in range(nZ - 1):
				caseNumber = 0
				index = z + y * nZ + x * nYZ
				# collecting the values
				n[0] = values[index + nZ]# 0,1,0
				n[1] = values[index + nYZ + nZ]#1,1,0
				n[2] = values[index + nYZ]# 1,0,0
				n[3] = values[index]# 0,0,0
				n[4] = values[index + nZ + 1]# 0,1,1
				n[5] = values[index + nYZ + nZ + 1]# 1,1,1
				n[6] = values[index + nYZ + 1]# 1,0,1
				n[7] = values[index + 1]# 0,0,1
				for i in range(7,-1,-1):
					if n[i] > iso:
						caseNumber+=1
					if i > 0:
						caseNumber = caseNumber << 1
				# collecting the faces
				offset = caseNumber * 15
				for i in range(offset,offset + 15,3):
					if _faces[i] > -1:
						vs=[]
						for j in range(i,i+3):
							v = switcher[_faces[j]]()
							mesh.vertices.append(v)
							vs.append(v)
							if len(vs) == 3:
								mesh.faces.append(Face(vs))
	return mesh

_faces = ( -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 8, 3, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 8, 3, 9, 8, 1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 2, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 8, 3, 1, 2,
		11, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 2, 11, 0, 2, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 8, 3, 2,
		11, 8, 11, 9, 8, -1, -1, -1, -1, -1, -1, 3, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 10, 2,
		8, 10, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 9, 0, 2, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 10,
		2, 1, 9, 10, 9, 8, 10, -1, -1, -1, -1, -1, -1, 3, 11, 1, 10, 11, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0,
		11, 1, 0, 8, 11, 8, 10, 11, -1, -1, -1, -1, -1, -1, 3, 9, 0, 3, 10, 9, 10, 11, 9, -1, -1, -1, -1, -1, -1, 9,
		8, 11, 11, 8, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, 4, 3, 0, 7, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 9, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, 4, 1, 9, 4, 7, 1, 7, 3, 1, -1, -1, -1, -1, -1, -1, 1, 2, 11, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, 3, 4, 7, 3, 0, 4, 1, 2, 11, -1, -1, -1, -1, -1, -1, 9, 2, 11, 9, 0, 2, 8, 4, 7, -1, -1, -1, -1, -1, -1,
		2, 11, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4, -1, -1, -1, 8, 4, 7, 3, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10,
		4, 7, 10, 2, 4, 2, 0, 4, -1, -1, -1, -1, -1, -1, 9, 0, 1, 8, 4, 7, 2, 3, 10, -1, -1, -1, -1, -1, -1, 4, 7,
		10, 9, 4, 10, 9, 10, 2, 9, 2, 1, -1, -1, -1, 3, 11, 1, 3, 10, 11, 7, 8, 4, -1, -1, -1, -1, -1, -1, 1, 10,
		11, 1, 4, 10, 1, 0, 4, 7, 10, 4, -1, -1, -1, 4, 7, 8, 9, 0, 10, 9, 10, 11, 10, 0, 3, -1, -1, -1, 4, 7, 10,
		4, 10, 9, 9, 10, 11, -1, -1, -1, -1, -1, -1, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 5,
		4, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 5, 4, 1, 5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, 5,
		4, 8, 3, 5, 3, 1, 5, -1, -1, -1, -1, -1, -1, 1, 2, 11, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 0, 8,
		1, 2, 11, 4, 9, 5, -1, -1, -1, -1, -1, -1, 5, 2, 11, 5, 4, 2, 4, 0, 2, -1, -1, -1, -1, -1, -1, 2, 11, 5, 3,
		2, 5, 3, 5, 4, 3, 4, 8, -1, -1, -1, 9, 5, 4, 2, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 10, 2, 0, 8,
		10, 4, 9, 5, -1, -1, -1, -1, -1, -1, 0, 5, 4, 0, 1, 5, 2, 3, 10, -1, -1, -1, -1, -1, -1, 2, 1, 5, 2, 5, 8,
		2, 8, 10, 4, 8, 5, -1, -1, -1, 11, 3, 10, 11, 1, 3, 9, 5, 4, -1, -1, -1, -1, -1, -1, 4, 9, 5, 0, 8, 1, 8,
		11, 1, 8, 10, 11, -1, -1, -1, 5, 4, 0, 5, 0, 10, 5, 10, 11, 10, 0, 3, -1, -1, -1, 5, 4, 8, 5, 8, 11, 11, 8,
		10, -1, -1, -1, -1, -1, -1, 9, 7, 8, 5, 7, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 3, 0, 9, 5, 3, 5, 7, 3,
		-1, -1, -1, -1, -1, -1, 0, 7, 8, 0, 1, 7, 1, 5, 7, -1, -1, -1, -1, -1, -1, 1, 5, 3, 3, 5, 7, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, 9, 7, 8, 9, 5, 7, 11, 1, 2, -1, -1, -1, -1, -1, -1, 11, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3,
		-1, -1, -1, 8, 0, 2, 8, 2, 5, 8, 5, 7, 11, 5, 2, -1, -1, -1, 2, 11, 5, 2, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1,
		-1, 7, 9, 5, 7, 8, 9, 3, 10, 2, -1, -1, -1, -1, -1, -1, 9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 10, -1, -1, -1, 2,
		3, 10, 0, 1, 8, 1, 7, 8, 1, 5, 7, -1, -1, -1, 10, 2, 1, 10, 1, 7, 7, 1, 5, -1, -1, -1, -1, -1, -1, 9, 5, 8,
		8, 5, 7, 11, 1, 3, 11, 3, 10, -1, -1, -1, 5, 7, 0, 5, 0, 9, 7, 10, 0, 1, 0, 11, 10, 11, 0, 10, 11, 0, 10, 0,
		3, 11, 5, 0, 8, 0, 7, 5, 7, 0, 10, 11, 5, 7, 10, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, 11, 6, 5, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 8, 3, 5, 11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 0, 1, 5,
		11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 8, 3, 1, 9, 8, 5, 11, 6, -1, -1, -1, -1, -1, -1, 1, 6, 5, 2,
		6, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 6, 5, 1, 2, 6, 3, 0, 8, -1, -1, -1, -1, -1, -1, 9, 6, 5, 9, 0,
		6, 0, 2, 6, -1, -1, -1, -1, -1, -1, 5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8, -1, -1, -1, 2, 3, 10, 11, 6, 5, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, 10, 0, 8, 10, 2, 0, 11, 6, 5, -1, -1, -1, -1, -1, -1, 0, 1, 9, 2, 3, 10, 5,
		11, 6, -1, -1, -1, -1, -1, -1, 5, 11, 6, 1, 9, 2, 9, 10, 2, 9, 8, 10, -1, -1, -1, 6, 3, 10, 6, 5, 3, 5, 1,
		3, -1, -1, -1, -1, -1, -1, 0, 8, 10, 0, 10, 5, 0, 5, 1, 5, 10, 6, -1, -1, -1, 3, 10, 6, 0, 3, 6, 0, 6, 5, 0,
		5, 9, -1, -1, -1, 6, 5, 9, 6, 9, 10, 10, 9, 8, -1, -1, -1, -1, -1, -1, 5, 11, 6, 4, 7, 8, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, 4, 3, 0, 4, 7, 3, 6, 5, 11, -1, -1, -1, -1, -1, -1, 1, 9, 0, 5, 11, 6, 8, 4, 7, -1, -1,
		-1, -1, -1, -1, 11, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4, -1, -1, -1, 6, 1, 2, 6, 5, 1, 4, 7, 8, -1, -1, -1, -1,
		-1, -1, 1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7, -1, -1, -1, 8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6, -1, -1, -1, 7,
		3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9, 3, 10, 2, 7, 8, 4, 11, 6, 5, -1, -1, -1, -1, -1, -1, 5, 11, 6, 4,
		7, 2, 4, 2, 0, 2, 7, 10, -1, -1, -1, 0, 1, 9, 4, 7, 8, 2, 3, 10, 5, 11, 6, -1, -1, -1, 9, 2, 1, 9, 10, 2, 9,
		4, 10, 7, 10, 4, 5, 11, 6, 8, 4, 7, 3, 10, 5, 3, 5, 1, 5, 10, 6, -1, -1, -1, 5, 1, 10, 5, 10, 6, 1, 0, 10,
		7, 10, 4, 0, 4, 10, 0, 5, 9, 0, 6, 5, 0, 3, 6, 10, 6, 3, 8, 4, 7, 6, 5, 9, 6, 9, 10, 4, 7, 9, 7, 10, 9, -1,
		-1, -1, 11, 4, 9, 6, 4, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 11, 6, 4, 9, 11, 0, 8, 3, -1, -1, -1, -1,
		-1, -1, 11, 0, 1, 11, 6, 0, 6, 4, 0, -1, -1, -1, -1, -1, -1, 8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 11, -1, -1,
		-1, 1, 4, 9, 1, 2, 4, 2, 6, 4, -1, -1, -1, -1, -1, -1, 3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4, -1, -1, -1, 0, 2,
		4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, 3, 2, 8, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, 11, 4, 9,
		11, 6, 4, 10, 2, 3, -1, -1, -1, -1, -1, -1, 0, 8, 2, 2, 8, 10, 4, 9, 11, 4, 11, 6, -1, -1, -1, 3, 10, 2, 0,
		1, 6, 0, 6, 4, 6, 1, 11, -1, -1, -1, 6, 4, 1, 6, 1, 11, 4, 8, 1, 2, 1, 10, 8, 10, 1, 9, 6, 4, 9, 3, 6, 9, 1,
		3, 10, 6, 3, -1, -1, -1, 8, 10, 1, 8, 1, 0, 10, 6, 1, 9, 1, 4, 6, 4, 1, 3, 10, 6, 3, 6, 0, 0, 6, 4, -1, -1,
		-1, -1, -1, -1, 6, 4, 8, 10, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, 11, 6, 7, 8, 11, 8, 9, 11, -1, -1,
		-1, -1, -1, -1, 0, 7, 3, 0, 11, 7, 0, 9, 11, 6, 7, 11, -1, -1, -1, 11, 6, 7, 1, 11, 7, 1, 7, 8, 1, 8, 0, -1,
		-1, -1, 11, 6, 7, 11, 7, 1, 1, 7, 3, -1, -1, -1, -1, -1, -1, 1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7, -1, -1, -1,
		2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9, 7, 8, 0, 7, 0, 6, 6, 0, 2, -1, -1, -1, -1, -1, -1, 7, 3, 2, 6,
		7, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 3, 10, 11, 6, 8, 11, 8, 9, 8, 6, 7, -1, -1, -1, 2, 0, 7, 2, 7,
		10, 0, 9, 7, 6, 7, 11, 9, 11, 7, 1, 8, 0, 1, 7, 8, 1, 11, 7, 6, 7, 11, 2, 3, 10, 10, 2, 1, 10, 1, 7, 11, 6,
		1, 6, 7, 1, -1, -1, -1, 8, 9, 6, 8, 6, 7, 9, 1, 6, 10, 6, 3, 1, 3, 6, 0, 9, 1, 10, 6, 7, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, 7, 8, 0, 7, 0, 6, 3, 10, 0, 10, 6, 0, -1, -1, -1, 7, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, 7, 6, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 0, 8, 10, 7, 6, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, 0, 1, 9, 10, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, 1, 9, 8, 3, 1, 10, 7, 6, -1,
		-1, -1, -1, -1, -1, 11, 1, 2, 6, 10, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 2, 11, 3, 0, 8, 6, 10, 7, -1,
		-1, -1, -1, -1, -1, 2, 9, 0, 2, 11, 9, 6, 10, 7, -1, -1, -1, -1, -1, -1, 6, 10, 7, 2, 11, 3, 11, 8, 3, 11,
		9, 8, -1, -1, -1, 7, 2, 3, 6, 2, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, 7, 0, 8, 7, 6, 0, 6, 2, 0, -1, -1,
		-1, -1, -1, -1, 2, 7, 6, 2, 3, 7, 0, 1, 9, -1, -1, -1, -1, -1, -1, 1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6, -1,
		-1, -1, 11, 7, 6, 11, 1, 7, 1, 3, 7, -1, -1, -1, -1, -1, -1, 11, 7, 6, 1, 7, 11, 1, 8, 7, 1, 0, 8, -1, -1,
		-1, 0, 3, 7, 0, 7, 11, 0, 11, 9, 6, 11, 7, -1, -1, -1, 7, 6, 11, 7, 11, 8, 8, 11, 9, -1, -1, -1, -1, -1, -1,
		6, 8, 4, 10, 8, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 6, 10, 3, 0, 6, 0, 4, 6, -1, -1, -1, -1, -1, -1,
		8, 6, 10, 8, 4, 6, 9, 0, 1, -1, -1, -1, -1, -1, -1, 9, 4, 6, 9, 6, 3, 9, 3, 1, 10, 3, 6, -1, -1, -1, 6, 8,
		4, 6, 10, 8, 2, 11, 1, -1, -1, -1, -1, -1, -1, 1, 2, 11, 3, 0, 10, 0, 6, 10, 0, 4, 6, -1, -1, -1, 4, 10, 8,
		4, 6, 10, 0, 2, 9, 2, 11, 9, -1, -1, -1, 11, 9, 3, 11, 3, 2, 9, 4, 3, 10, 3, 6, 4, 6, 3, 8, 2, 3, 8, 4, 2,
		4, 6, 2, -1, -1, -1, -1, -1, -1, 0, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 9, 0, 2, 3, 4, 2,
		4, 6, 4, 3, 8, -1, -1, -1, 1, 9, 4, 1, 4, 2, 2, 4, 6, -1, -1, -1, -1, -1, -1, 8, 1, 3, 8, 6, 1, 8, 4, 6, 6,
		11, 1, -1, -1, -1, 11, 1, 0, 11, 0, 6, 6, 0, 4, -1, -1, -1, -1, -1, -1, 4, 6, 3, 4, 3, 8, 6, 11, 3, 0, 3, 9,
		11, 9, 3, 11, 9, 4, 6, 11, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 9, 5, 7, 6, 10, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, 0, 8, 3, 4, 9, 5, 10, 7, 6, -1, -1, -1, -1, -1, -1, 5, 0, 1, 5, 4, 0, 7, 6, 10, -1, -1, -1, -1,
		-1, -1, 10, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5, -1, -1, -1, 9, 5, 4, 11, 1, 2, 7, 6, 10, -1, -1, -1, -1, -1,
		-1, 6, 10, 7, 1, 2, 11, 0, 8, 3, 4, 9, 5, -1, -1, -1, 7, 6, 10, 5, 4, 11, 4, 2, 11, 4, 0, 2, -1, -1, -1, 3,
		4, 8, 3, 5, 4, 3, 2, 5, 11, 5, 2, 10, 7, 6, 7, 2, 3, 7, 6, 2, 5, 4, 9, -1, -1, -1, -1, -1, -1, 9, 5, 4, 0,
		8, 6, 0, 6, 2, 6, 8, 7, -1, -1, -1, 3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0, -1, -1, -1, 6, 2, 8, 6, 8, 7, 2, 1,
		8, 4, 8, 5, 1, 5, 8, 9, 5, 4, 11, 1, 6, 1, 7, 6, 1, 3, 7, -1, -1, -1, 1, 6, 11, 1, 7, 6, 1, 0, 7, 8, 7, 0,
		9, 5, 4, 4, 0, 11, 4, 11, 5, 0, 3, 11, 6, 11, 7, 3, 7, 11, 7, 6, 11, 7, 11, 8, 5, 4, 11, 4, 8, 11, -1, -1,
		-1, 6, 9, 5, 6, 10, 9, 10, 8, 9, -1, -1, -1, -1, -1, -1, 3, 6, 10, 0, 6, 3, 0, 5, 6, 0, 9, 5, -1, -1, -1, 0,
		10, 8, 0, 5, 10, 0, 1, 5, 5, 6, 10, -1, -1, -1, 6, 10, 3, 6, 3, 5, 5, 3, 1, -1, -1, -1, -1, -1, -1, 1, 2,
		11, 9, 5, 10, 9, 10, 8, 10, 5, 6, -1, -1, -1, 0, 10, 3, 0, 6, 10, 0, 9, 6, 5, 6, 9, 1, 2, 11, 10, 8, 5, 10,
		5, 6, 8, 0, 5, 11, 5, 2, 0, 2, 5, 6, 10, 3, 6, 3, 5, 2, 11, 3, 11, 5, 3, -1, -1, -1, 5, 8, 9, 5, 2, 8, 5, 6,
		2, 3, 8, 2, -1, -1, -1, 9, 5, 6, 9, 6, 0, 0, 6, 2, -1, -1, -1, -1, -1, -1, 1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8,
		2, 6, 2, 8, 1, 5, 6, 2, 1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 3, 6, 1, 6, 11, 3, 8, 6, 5, 6, 9, 8, 9,
		6, 11, 1, 0, 11, 0, 6, 9, 5, 0, 5, 6, 0, -1, -1, -1, 0, 3, 8, 5, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		11, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 10, 5, 11, 7, 5, 10, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, 10, 5, 11, 10, 7, 5, 8, 3, 0, -1, -1, -1, -1, -1, -1, 5, 10, 7, 5, 11, 10, 1, 9, 0, -1, -1, -1, -1,
		-1, -1, 11, 7, 5, 11, 10, 7, 9, 8, 1, 8, 3, 1, -1, -1, -1, 10, 1, 2, 10, 7, 1, 7, 5, 1, -1, -1, -1, -1, -1,
		-1, 0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 10, -1, -1, -1, 9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 10, 7, -1, -1, -1, 7, 5,
		2, 7, 2, 10, 5, 9, 2, 3, 2, 8, 9, 8, 2, 2, 5, 11, 2, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, 8, 2, 0, 8, 5,
		2, 8, 7, 5, 11, 2, 5, -1, -1, -1, 9, 0, 1, 5, 11, 3, 5, 3, 7, 3, 11, 2, -1, -1, -1, 9, 8, 2, 9, 2, 1, 8, 7,
		2, 11, 2, 5, 7, 5, 2, 1, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 8, 7, 0, 7, 1, 1, 7, 5, -1,
		-1, -1, -1, -1, -1, 9, 0, 3, 9, 3, 5, 5, 3, 7, -1, -1, -1, -1, -1, -1, 9, 8, 7, 5, 9, 7, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, 5, 8, 4, 5, 11, 8, 11, 10, 8, -1, -1, -1, -1, -1, -1, 5, 0, 4, 5, 10, 0, 5, 11, 10, 10, 3,
		0, -1, -1, -1, 0, 1, 9, 8, 4, 11, 8, 11, 10, 11, 4, 5, -1, -1, -1, 11, 10, 4, 11, 4, 5, 10, 3, 4, 9, 4, 1,
		3, 1, 4, 2, 5, 1, 2, 8, 5, 2, 10, 8, 4, 5, 8, -1, -1, -1, 0, 4, 10, 0, 10, 3, 4, 5, 10, 2, 10, 1, 5, 1, 10,
		0, 2, 5, 0, 5, 9, 2, 10, 5, 4, 5, 8, 10, 8, 5, 9, 4, 5, 2, 10, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 5,
		11, 3, 5, 2, 3, 4, 5, 3, 8, 4, -1, -1, -1, 5, 11, 2, 5, 2, 4, 4, 2, 0, -1, -1, -1, -1, -1, -1, 3, 11, 2, 3,
		5, 11, 3, 8, 5, 4, 5, 8, 0, 1, 9, 5, 11, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2, -1, -1, -1, 8, 4, 5, 8, 5, 3, 3, 5,
		1, -1, -1, -1, -1, -1, -1, 0, 4, 5, 1, 0, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, 4, 5, 8, 5, 3, 9, 0, 5,
		0, 3, 5, -1, -1, -1, 9, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 10, 7, 4, 9, 10, 9, 11, 10,
		-1, -1, -1, -1, -1, -1, 0, 8, 3, 4, 9, 7, 9, 10, 7, 9, 11, 10, -1, -1, -1, 1, 11, 10, 1, 10, 4, 1, 4, 0, 7,
		4, 10, -1, -1, -1, 3, 1, 4, 3, 4, 8, 1, 11, 4, 7, 4, 10, 11, 10, 4, 4, 10, 7, 9, 10, 4, 9, 2, 10, 9, 1, 2,
		-1, -1, -1, 9, 7, 4, 9, 10, 7, 9, 1, 10, 2, 10, 1, 0, 8, 3, 10, 7, 4, 10, 4, 2, 2, 4, 0, -1, -1, -1, -1, -1,
		-1, 10, 7, 4, 10, 4, 2, 8, 3, 4, 3, 2, 4, -1, -1, -1, 2, 9, 11, 2, 7, 9, 2, 3, 7, 7, 4, 9, -1, -1, -1, 9,
		11, 7, 9, 7, 4, 11, 2, 7, 8, 7, 0, 2, 0, 7, 3, 7, 11, 3, 11, 2, 7, 4, 11, 1, 11, 0, 4, 0, 11, 1, 11, 2, 8,
		7, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 9, 1, 4, 1, 7, 7, 1, 3, -1, -1, -1, -1, -1, -1, 4, 9, 1, 4, 1,
		7, 0, 8, 1, 8, 7, 1, -1, -1, -1, 4, 0, 3, 7, 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, 4, 8, 7, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, 9, 11, 8, 11, 10, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 0, 9, 3, 9,
		10, 10, 9, 11, -1, -1, -1, -1, -1, -1, 0, 1, 11, 0, 11, 8, 8, 11, 10, -1, -1, -1, -1, -1, -1, 3, 1, 11, 10,
		3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 2, 10, 1, 10, 9, 9, 10, 8, -1, -1, -1, -1, -1, -1, 3, 0, 9, 3,
		9, 10, 1, 2, 9, 2, 10, 9, -1, -1, -1, 0, 2, 10, 8, 0, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 2, 10, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 3, 8, 2, 8, 11, 11, 8, 9, -1, -1, -1, -1, -1, -1, 9, 11, 2,
		0, 9, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 3, 8, 2, 8, 11, 0, 1, 8, 1, 11, 8, -1, -1, -1, 1, 11, 2, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 3, 8, 9, 1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 9, 1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 3, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
		-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 )
