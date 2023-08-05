# Copyright (C) 2009-2016 Specific Purpose Software GmbH

from numpy import array,pi,cos,sin
from numpy import sqrt,exp
#from SVG import Scene
#from numpy.oldnumeric.ma import dot
from numpy import dot

# This matrix is a: Column first style

_deg_to_rad = lambda deg: 2 * pi / (360.0/deg)

def idmatrix():
    return array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

class Matrix:
    def __init__(self,translation=[0,0],rotation=0):
        self.x = translation[0]
        self.y = translation[1]
        self.rot = _deg_to_rad(rotation)

#def scale(a):
#    m = array([[a[0],0,0],[0,a[1],0],[0,0,1]])
#    return m

# row first
def transform(a, m):
    b = array([0,0])
    b[0] = cos(m.rot) * a[0] + -sin(m.rot) * a[1] + m.x
    b[1] = sin(m.rot) * a[0] + cos(m.rot) * a[1] + m.y
    return b

#def center(a):
#    return transform(a,translate(array([0,0])))

if __name__ == '__main__':
    from stopeight.util import runnable
    a = array([30,30])
    #m = idmatrix()
    print ('rotate vector with matrix:')
    #m = dot(translate(array([10,15])),m)
    #m = dot(scale(array([0.5,0.5])),m)
    #m = dot(rotate(-90),m)
    m = Matrix([10,15],-90)
    result = transform(a,m)
    print(a)
    print(result)
#    scene = Scene('matrixTools',255,255)
#    scene.add(Line(center(array([0,0])),center(a)))
#    scene.add(Line(center(array([0,0])),center(result)))
#    scene.write_svg()
#    scene.display()
#    return
