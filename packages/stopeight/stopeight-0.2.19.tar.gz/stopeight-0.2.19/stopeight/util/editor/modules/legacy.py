# Copyright (C) 2018 Fassio Blatter

import stopeight.legacy
from stopeight.util.editor.data import ScribbleData

def stroke_parallel(data):
    return stopeight.legacy.stroke_parallel(data)
stroke_parallel.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}

def stroke_sequential(data):
    # type: (ScribbleData) -> ScribbleData
    return stopeight.legacy.stroke_sequential(data)
stroke_sequential.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}

def parse_file(data):
    return stopeight.legacy.parse_file(data)
parse_file.__annotations__ = {'data': str, 'return': ScribbleData}


def TCT_to_bezier(data):
    return stopeight.legacy.TCT_to_bezier(data)
TCT_to_bezier.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}

##import stopeight.finders
##from stopeight.logging import logSwitch
##log = logSwitch.logPrint()
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
##import stopeight.getters
##import numpy as np
##
##def getFirstTurnByTriplets(data):
##    log.info("Invoking getFirstTurnByTriplets...")
##    ql = stopeight.getters.QListDpoint(data)
##    ta = stopeight.getters.Turn(ql)
##    turn = array(ta.next())
##    assert type(turn) == np.ndarray
##    return turn.view(ScribbleData)
##getFirstTurnByTriplets.__annotations__ = {'data': ScribbleData, 'return': ScribbleData}
##
