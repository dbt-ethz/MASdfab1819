add_library('peasycam')
# from mola import *
import math as m

class Vertex(object):
    def __init__(self, x = 0, y = 0, z = 0):
        """ basic vertex class
        """
        self.x = x
        self.y = y
        self.z = z

class PolarVertex(object):
    def __init__(self, center = Vertex(), radius = 10, alfa = 0, h = 1):
        """ polar vertex class
        """
        self.c = Vertex(center.x, center.y, center.z)# hacky deepcopy
        self.a = alfa
        self.r = radius
        self.h = h
        self.x = center.x + m.cos(alfa) * radius
        self.y = center.y + m.sin(alfa) * radius
        self.z = center.z + h
        
    def update(self, center = None, radius = None, alfa = None, h = None):
        """re-initializes the polar vertex with some edited parameters
        """
        if not(center == None):
            self.c = center
        if not(alfa == None):
            self.a = alfa
        if not(radius == None):
            self.r = radius
        if not(h == None):
            self.h = h
        print self.a
        self.x = self.c.x + m.cos(self.a) * self.r
        self.y = self.c.y + m.sin(self.a) * self.r
        self.z = self.c.z + self.h
        
    def peasy_shuffle(self):
        """ hacky method to deal with the peasycam lookat
        """
        temp_x, temp_y, temp_z = self.x, self.y, self.z
        self.x = temp_z
        self.y = temp_y
        self.z = temp_x
        
class Helix(object):
    def __init__(self, center = Vertex(), radius = 50.0, resolution = 20, layers = 5.5, layer_height = 5.0):
        """ simple continious helix
        """
        self.c = center
        self.r = radius
        self.res = int(resolution)
        self.l_count = layers
        self.l_height = layer_height
        self.v_count = int(self.l_count * resolution) + 1
        self.h_change = float(layer_height) / float(resolution)
        self.a_change = 2 * 3.1415 / float(resolution)
    
    def vertex_gen(self):
        """ generating all the polar vertexes of the helix
        """
        self.vertexes = []
        for i in range(self.v_count):
            loc_r = self.r
            loc_h = i * self.h_change
            loc_a = i * self.a_change
            self.vertexes.append(PolarVertex(self.c, loc_r, loc_a, loc_h))
    
    def warp(self, amplitude_z = 0.0, amplitude_r = 0.0, period_z = 0, period_r = 1):
        """ applying some warps to the "surface" of the helix
        """
        period_r = float(self.res) + period_r
        period_z = float(self.res) * period_z
        
        print period_z, period_r
        
        for v in self.vertexes:
            angle = v.a
            radius = v.r
            h = v.h
            center = v.c
            new_r = radius + m.sin(angle / period_r) * amplitude_r
            new_h = h + m.sin(angle / period_z) * amplitude_z
            
            v.update(radius = new_r, h = new_h)
            
    def decenter(self, period = 20.0, amplitude = 30.0):
        """ baroque decenter of the helix
        """
        period_z = 2 * 3.1415 / (float(self.res) * period)
        for index, v in enumerate(self.vertexes):
            center = PolarVertex(alfa = index * period_z, radius = amplitude)
            v.update(center = center)
            
    def peasy_shuffle(self):
        [v.peasy_shuffle() for v in self.vertexes]
    
def setup():
    global loc_helix
    loc_helix = Helix(layers = 100.0)
    loc_helix.vertex_gen()
    loc_helix.warp(amplitude_z = 20.0, amplitude_r = 30.0, period_r = -5, period_z = 7.3456)
    loc_helix.decenter(period = 100, amplitude = 30)
    loc_helix.peasy_shuffle()      # for Yuta, with love, Jonas <3
    
    helix_height = loc_helix.vertexes[-1].h
    print helix_height
    
    size (1500, 480, P3D)
    cam = PeasyCam(this, helix_height * .5, 0, 0, helix_height * .5)

def draw():
    
    min_radius = 100
    max_radius = 50
    
    colorMode(HSB)
    noFill()
    background(255)
    ondulation = 4
    ond_rad = 40    
    loc_vertexes = loc_helix.vertexes
    count = len(loc_vertexes)
    beginShape()
    for index, v in enumerate(loc_vertexes):
        # color definition based on the radius of the helix
        stroke((v.r - 30) * 4.0, 255, 255)
        vertex(v.x, v.y, v.z)
    endShape()
    
