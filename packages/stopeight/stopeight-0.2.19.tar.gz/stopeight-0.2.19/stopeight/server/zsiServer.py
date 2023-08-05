# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.logging import logSwitch
# Note: This is done depending on logging context
log = logSwitch.logPrint()

from stopeight.server import zsiTools
from stopeight.server import requestProcessing

import sys

def matchLine(ABCSymbol):
    try:
        return requestProcessing.match_line(ABCSymbol.lines[0])
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

def saveLine(ABCSymbol):
    try:
        id = requestProcessing.save_line(ABCSymbol.lines[0])
        output = ABCSymbol
        # assigning new id from database
        output[0].id = id
        return output
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

def getLine(ABCSymbol):
    try:
        output = ABCSymbol
        line = requestProcessing.get_line(ABCSymbol.lines[0])
        output.lines=[]
        output.add_line(line)
        return output
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

def deleteLine(ABCSymbol):
    try:
        output = ABCSymbol
        line = requestProcessing.delete_line(ABCSymbol.lines[0])
        # assigning id of deleted line or 0 if error
        output.lines=[]
        output.add_line(line)
        return output
    except Exception:
        log.error(logSwitch.concatenate_traceback(sys))
        raise Exception

