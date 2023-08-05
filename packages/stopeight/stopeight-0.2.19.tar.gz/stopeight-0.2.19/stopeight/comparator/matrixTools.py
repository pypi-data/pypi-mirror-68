# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from numpy import array,pi,cos,sin
#from SVG import Scene
#from numpy.oldnumeric.ma import dot
from numpy import dot

# This matrix is a: Column first style

_deg_to_rad = lambda deg: 2 * pi / (360.0/deg)

def idmatrix():
    return array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

def translate(a):
    m = array([[1,0,0],[0,1,0],[a[0],a[1],1]])
    return m

def scale(a):
    m = array([[a[0],0,0],[0,a[1],0],[0,0,1]])
    return m

def rotate(deg):
    if (deg!=0):
        c = cos(_deg_to_rad(deg))
        s = sin(_deg_to_rad(deg))
        m = array([[c,s,0],[-s,c,0],[0,0,1]])
    else:
        m = idmatrix()
    return m

def transform(a, m):
    b = array([0,0])
    b[0]= a[0] * m[0][0] + a[1]* m[1][0] + m[2][0]
    b[1]= a[0] * m[0][1] + a[1]* m[1][1] + m[2][1]
    return b

def center(a):
    return transform(a,translate(array([0,0])))

if __name__ == '__main__':
    from stopeight.util import runnable
    a = array([30,30])
    m = idmatrix()
    print ('rotate vector with matrix:')
    m = dot(translate(array([10,15])),m)
    #m = dot(scale(array([0.5,0.5])),m)
    m = dot(rotate(-90),m)
    result = transform(a,m)
    print(a)
    print(result)
#    scene = Scene('matrixTools',255,255)
#    scene.add(Line(center(array([0,0])),center(a)))
#    scene.add(Line(center(array([0,0])),center(result)))
#    scene.write_svg()
#    scene.display()
#    return
