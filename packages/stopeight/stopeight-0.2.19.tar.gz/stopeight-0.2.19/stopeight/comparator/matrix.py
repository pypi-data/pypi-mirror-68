from numpy import array,sqrt,square,cos,sin
from math import pi

_deg_to_rad = lambda deg: 2 * pi / (360.0/deg)
_length = lambda xy : sqrt(square(xy[0])+square(xy[1]))


def vector(vector=array([0,0])):
    m = array([[vector[0],0],[0,vector[1]]])
    return m

def id():
    return array([[1,0],[0,1]])

def translation(vector=array([0,0])):
    m = array([[vector[0]/_length((vector[0],vector[1])),-(vector[1]/_length((vector[0],vector[1])))],
            [vector[1]/_length((vector[0],vector[1])),vector[0]/_length((vector[0],vector[1]))]])
    return m

def translation(vector=array([0,0])):
    # scale 50%
    # [0.5,0]
    # [0,0.5]
    # rotate 180
    # [-1,-0]
    # [0,-1]
    return mul(array([[0.5,0],[0,0.5]]),array([[-1,0],[0,-1]]))

def rotation(degree):
    m = array([[cos(_deg_to_rad(degree)),-sin(_deg_to_rad(degree))],[sin(_deg_to_rad(degree)),cos(_deg_to_rad(degree))]])
    return m

def scale(vector=array([1,1])):
    m = array([[vector[0],0],[0,vector[1]]])
    return m

def mul(m1,m2):
    m3 = array([[m1[0][0]*m2[0][0],m1[0][1]*m2[1][0]],[m1[1][0]*m2[0][1],m1[1][1]*m2[1][1]]])
    return m3

def apply(m1,m2):
    m3 = array([(m1[0][0]*m2[1][0]+m1[0][1]*m2[1][1]),(m1[1][0]*m2[1][0]+m1[1][1]*m2[1][1])])
    return m3

def apply2(m1,m2):
    m3 = array([(m1[0][0]*m2[0][0]+m1[0][1]*m2[1][0]),(m1[1][0]*m2[0][1]+m1[1][1]*m2[1][1])])
    return m3

def apply3(m1,m2):
    m3 = array([(m1[0][0]*m2[1][1]+m1[0][1]*m2[1][0]),(m1[1][0]*m2[0][1]+m1[1][1]*m2[0][1])])
    return m3

if __name__ == '__main__':
    a = vector(array([30,30]))
    print(apply( 
            translation(a), 
            a ,
            ))