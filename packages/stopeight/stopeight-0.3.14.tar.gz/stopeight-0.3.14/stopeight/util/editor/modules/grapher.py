# Copyright (C) 2018 Fassio Blatter
from stopeight import grapher
version=grapher.version

from stopeight.util.editor.data import ScribbleData, WaveData
from stopeight.util.editor.scribble import ScribbleArea

import stopeight.logging as log

def _append(data):
    for id,vector in enumerate(data):
        if id!=0:
            data[id]['coords']+=data[id-1]['coords']
    return data

def _extrema(data):
    from operator import itemgetter
    left,right,bottom,top = min(data,key=lambda k: k[0][0])[0][0],max(data,key=lambda k: k[0][0])[0][0],min(data,key=lambda k: k[0][1])[0][1],max(data,key=lambda k: k[0][1])[0][1]
    #if scribble
    bottom,top = top,bottom
    return left,right,bottom,top

def _scalingfactors(left,right,bottom,top,width,height):
    d_x = abs(right - left)
    d_y = abs(top - bottom)
    o_x = width
    o_y = height
    return o_x/d_x,o_y/d_y

def _resize(scribbledata,width,height):
    log.setLevel(log.INFO)
    assert type(scribbledata) is ScribbleData, "Wrong input data.data type: %r" % type(scribbledata)
    log.debug("Width "+str(width)+" Height "+str(height))
    from stopeight.matrix import Vectors,Stack
    vectors = Vectors(scribbledata)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    stack=Stack()
    stack.identity()
    tx,ty=(-vectors.__array__()[0][0][0],-vectors.__array__()[0][0][1])
    log.debug("translating "+str(tx)+","+str(ty))
    stack.translate(tx,ty)
    vectors.apply(stack)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    stack = Stack()
    stack.identity()
    from numpy.core.umath import arctan2
    from numpy import rad2deg
    angle = -rad2deg(arctan2(vectors.__array__()[-1][0][1],vectors.__array__()[-1][0][0]))
    log.debug("Rotating "+str(angle))
    stack.rotate(angle)
    vectors.apply(stack)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    stack=Stack()
    stack.identity()
    left,right,bottom,top=_extrema(vectors.__array__())
    log.debug("Left "+str(left)+" Right "+str(right)+" Bottom "+str(bottom)+" Top "+str(top))
    log.debug("Width "+str(abs(right-left))+" Height "+str(abs(top-bottom)))
    sx,sy=_scalingfactors(left,right,bottom,top,width,height)
    log.info("Uniform scaling "+str(len(scribbledata))+" vectors with effective horiz: "+str(sx)+", and vert: "+str(sy)+" factors.")
    landscape= True if sx<sy else False
    log.debug("Mode landscape "+str(landscape))
    sx,sy= (sy,sy) if sx>sy else (sx,sx)
    log.debug("scaling "+str(sx)+","+str(sy))
    stack.scale(sx,sy)
    vectors.apply(stack)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    left,right,bottom,top=_extrema(vectors.__array__())
    log.debug("Left "+str(left)+" Right "+str(right)+" Bottom "+str(bottom)+" Top "+str(top))
    stack=Stack()
    stack.identity()
    tx,ty=(-left,-top)
    log.debug("translating "+str(tx)+","+str(ty))
    stack.translate(tx,ty)
    vectors.apply(stack)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    stack=Stack()
    stack.identity()
    tx,ty=((width-abs(right-left))/2,0) if not landscape else (0,(height-abs(top-bottom))/2)
    log.debug("translating "+str(tx)+","+str(ty))
    stack.translate(tx,ty)
    vectors.apply(stack)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    testvec = vectors.__array__()
    log.debug("Rendering...")
    log.debug("First "+str(testvec[0][0][0])+","+str(testvec[0][0][1])+" Last "+str(testvec[-1][0][0])+","+str(testvec[-1][0][1]))
    return testvec.view(ScribbleData) 

def create_vector_graph(data:WaveData)->ScribbleData:
    assert type(data) is WaveData, "Input Error, wrong datatype: %r" % type(data)
    log.debug("Loading with "+str(len(data)))
    #from stopeight.matrix import Vectors #Hard crash if symbol used but missing: create_vector_graph return value
    from stopeight.grapher import VectorDouble,create_vector_graph
    import numpy as np
    invec = VectorDouble(data)
    #result = invec.create_vector_graph(1,1.0,True).__array__()
    result = create_vector_graph(invec,1,1.0,True)
    assert type(result) is np.ndarray, "Cast Error: %r" % type(result)
    result = _append(result)
    log.debug("Return Length "+str(len(result)))
    return result.view(ScribbleData)

#grapher data y inverted, scribble data y normal
def resize(data):
    log.setLevel(log.DEBUG)
    #doesnt work: sip.wrappertype
    #log.warning("data "+str(type(data)))
    #log.warning("ScribbleArea "+str(ScribbleArea.__class__))
    #assert data.__class__ is type(ScribbleArea), "Wrong input data type: %r" % data
    data(_resize(data.data,data.width(),data.height()))
    return None
resize.__annotations__ = {'data':ScribbleArea,'return':type(None)}
