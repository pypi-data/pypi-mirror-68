# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.logging import logSwitch
# Note: This is done depending on logging context
log = logSwitch.logPrint()

import numpy
from stopeight.server.zodbTools import DBLine
from stopeight.server.zsiTools import ABCSymbol,ABCLine
import time
from types import NoneType

class STLine():
    @staticmethod
    def save(line):
        if len(line.points)<=2:
            raise Exception('length of input or reference is below 3. Scale-Matching lines of size <3 is not possible.')
        # only use dbline if to be committed by session/stored or retrieved from db
        tobesaved = DBLine.from_numpy_array(line.to_numpy_array())
        tobesaved.store()
        log.info('created line id %d'%(tobesaved.id))
        return tobesaved.id

    @staticmethod
    def delete(line):
        dbline = DBLine.get(line.id)
        if (type(dbline)!=NoneType):
            # or dbline.view(matchline.ABCLine) ?
            echo = ABCLine.from_numpy_array(dbline.to_numpy_array())
            echo.id = dbline.id
            dbline.remove()
            log.info('deleted line id %d'%(line.id))
            return echo
        else:
            log.error('line id %d does not exist!'%(line.id))
            echo = ABCLine()
            echo.id = 0
            return echo

    @staticmethod
    def get(line):
        dbline = DBLine.get(line.id)
        if (type(dbline)!=NoneType):
            found = ABCLine.from_numpy_array(dbline.to_numpy_array())
            found.id = dbline.id
            log.info('retrieved line id %d'%(found.id))
            return found
        else:
            log.error('line id %d does not exist!'%(line.id))
            echo = ABCLine()
            echo.id = 0
            return echo
