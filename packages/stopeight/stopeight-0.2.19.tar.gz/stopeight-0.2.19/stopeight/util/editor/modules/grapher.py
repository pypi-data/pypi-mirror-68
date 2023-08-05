# Copyright (C) 2018 Fassio Blatter
from stopeight import grapher
version=grapher.version

from stopeight.util.editor.data import ScribbleData, WaveData, ScribblePoint
from stopeight.util.editor.scribble import ScribbleArea

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

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

def _scalingfactors(left,right,bottom,top,obj):
    d_x = abs(right - left)
    d_y = abs(top - bottom)
    o_x = obj.width()
    o_y = obj.height()
    return o_x/d_x,o_y/d_y

def create_vector_graph(data):
    assert type(data) is WaveData, "Input Error, wrong datatype: %r" % type(data)
    log.debug("Loading with "+str(len(data)))
    from stopeight.grapher import VectorDouble,VectorTimeCodeDouble,create_vector_graph
    import numpy as np
    invec = VectorDouble(data)
    result = invec.create_vector_graph(1,1.0,True).__array__()
    assert type(result) is np.ndarray, "Cast Error: %r" % type(result)
    result = _append(result)
    log.debug("Return Length "+str(len(result)))
    return result.view(ScribbleData)
create_vector_graph.__annotations__ = {'data':WaveData,'return':ScribbleData}

#grapher data y inverted, scribble data y normal
def resize(data):
    #doesnt work: sip.wrappertype
    #log.warning("data "+str(type(data)))
    #log.warning("ScribbleArea "+str(ScribbleArea.__class__))
    #assert type(data) is type(ScribbleArea), "Wrong input data type: %r" % data
    assert type(data.data) is ScribbleData, "Wrong input data.data type: %r" % type(data.data)
    log.debug("Width "+str(data.width())+" Height "+str(data.height()))
    from stopeight.matrix import Vectors,Stack
    vectors = Vectors(data.data)
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
    sx,sy=_scalingfactors(left,right,bottom,top,data)
    log.warning("scaling data "+str(sx)+","+str(sy))
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
    tx,ty=((data.width()-abs(right-left))/2,0) if not landscape else (0,(data.height()-abs(top-bottom))/2)
    log.debug("translating "+str(tx)+","+str(ty))
    stack.translate(tx,ty)
    vectors.apply(stack)
    log.debug("First "+str(vectors.__array__()[0][0][0])+","+str(vectors.__array__()[0][0][1])+" Last "+str(vectors.__array__()[-1][0][0])+","+str(vectors.__array__()[-1][0][1]))
    testvec = vectors.__array__()
##    from stopeight.util.editor.data import ScribblePoint
##    testvec = []
##    test=ScribblePoint([0.0,data.height()/2])
##    testvec.append(test)
##    test=ScribblePoint([data.width()/2,data.height()/2])
##    testvec.append(test)
    log.debug("Rendering...")
    log.debug("First "+str(testvec[0][0][0])+","+str(testvec[0][0][1])+" Last "+str(testvec[-1][0][0])+","+str(testvec[-1][0][1]))
    #Hack copy
    result = ScribbleData(size=len(testvec))
    for i,v in enumerate(testvec):
        result[i]['coords'] = [v[0][0],v[0][1]]
    data(result)
    return None
resize.__annotations__ = {'data':ScribbleArea,'return':type(None)}
