# Copyright (C) 2018 Fassio Blatter
version="TooOld"
import stopeight.legacy
from stopeight.util.editor.data import ScribbleData

import stopeight.logging as log

def stroke_parallel(data:ScribbleData)->ScribbleData:
    return _convert(stopeight.legacy.stroke_parallel(list(map(tuple,data['coords'].tolist()))))

def stroke_sequential(data:ScribbleData)->ScribbleData:
    # type: (ScribbleData) -> ScribbleData
    return _convert(stopeight.legacy.stroke_sequential(list(map(tuple,data['coords'].tolist()))))

def _parse_file(filename):
    legacy_data= stopeight.legacy.parse_file(filename)
    return _convert(legacy_data)

def _convert(legacy_data):
    scribbledata = ScribbleData(size=len(legacy_data))
    for i,v in enumerate(legacy_data):
        scribbledata[i]['coords'] = [v[0],v[1]]
    return scribbledata

def open_SP()->ScribbleData:
    from stopeight.util.runnable import EditorApp
    from PyQt5.QtWidgets import QFileDialog
    filename = QFileDialog.getOpenFileName(EditorApp().window)
    assert type(filename[0]) == str
    assert len(filename[0]) != 0
    data = _parse_file(filename[0])
    return data

def TCT_to_bezier(data:ScribbleData)->ScribbleData:
    return stopeight.legacy.TCT_to_bezier(data)

##import stopeight.finders
##from stopeight.grapher import *
##
##def findTurns(data):
##    log.info("Invoking findTurns...")
##    ql = stopeight.getters.QListDpoint(data)
##    turns = stopeight.finders.Turns(ql)
##    print(turns)
##    assert type(turns) == list
##    return turns
##findTurns.__annotations__ = {'data': ScribbleData, 'return': list}
##
##def sequencial(data):
##    log.info("Invoking findCliffs...")
##    ql = stopeight.getters.QListDpoint(data)
##    turns = stopeight.finders.Cliffs(ql)
##    print(turns)
##    assert type(turns) == list
##    return turns
##sequencial.__annotations__ = {'data': ScribbleData, 'return': list}
##
##def parallel(data):
##    log.info("Invoking findSpiralCliffs...")
##    ql = stopeight.getters.QListDpoint(data)
##    turns = stopeight.finders.Spirals(ql)
##    print(turns)
##    assert type(turns) == list
##    return turns
##parallel.__annotations__ = {'data': ScribbleData, 'return': list}
##
##
import stopeight.getters
import numpy as np

def getFirstTurnByTriplets(data:ScribbleData)->ScribbleData:
    log.setLevel(log.DEBUG)
    log.info("Invoking getFirstTurnByTriplets with "+str(len(data))+" data points...")
    #from stopeight.matrix import Vectors
    #invec = Vectors(data)
    #log.debug("Creating a legacy QListDpoint from a matrix Vectors length "+str(len(invec)))
    ql = stopeight.getters.QListDpoint(data)
    log.debug("Initializing turn chopping algorithm length "+str(len(ql)))
    ta = stopeight.getters.Turn(ql)
    log.debug("Invoking turn chopping algorithm length "+str(len(ta)))
    out = ta.next()#.__array__()
    log.debug("Read length of a object of type "+str(type(out))+" and length "+str(len(out)))
    return out.view(ScribbleData)
