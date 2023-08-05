# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.server import symbolTools
from stopeight.server.zodbTools import DBLine
from stopeight.server.zsiTools import ABCSymbol
import time
import sys
from stopeight.multiprocessing import pooling

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def log_set(name, myset):
    log.debug(name)
    log.debug('={')
    for element in myset:
        log.debug(str(element))
        log.debug(',')
    log.debug('}\n')

def populate_lines(echo, lines):
    varray = ABCSymbol()
    for count, record_id in enumerate(lines):
        # bug workaround: macos ppc
        #if count < 60:
        line = DBLine.get(record_id)
        #strangely this is necessary to populate (with elixir-db)
        for point in line.points:
            pass
        varray.add_line(line)
        #else:
        #    raise Exception
    varray.id = -1
    return varray

def match_line(line):
    db0 = time.clock()
    dbLines = DBLine.getAll()
    allLines = []
    for dbrecord in dbLines:
        allLines.append(dbrecord.to_numpy_array())
    log.debug('m_l db: '+str(time.clock()-db0)+'s')
    py0 = time.clock()

    result = pooling.run(allLines,line.to_numpy_array()) 
##    symbol = pooling.MPLine(allLines)
##    lines = symbol.matchLine(line.to_numpy_array())
    log.debug('m_l py: '+str(time.clock()-py0)+'s')
    pop0 = time.clock()
    #build set (might be buggy!)
    log.info('found %d matches out of %d records!'%(len(result),len(dbLines)))
    resultSet = set()
    for recordNumber in result:
        resultSet.add(dbLines[recordNumber].id)
    
    response = populate_lines(line, resultSet)
    log.debug('m_l pop: '+str(time.clock()-pop0)+'s')
    log.debug('m_l total: '+str(time.clock()-db0)+'s')
    return response

def save_line(ABCLine):
    log.debug('saving line')
    id = symbolTools.STLine.save(ABCLine)
    return id

def delete_line(ABCLine):
    log.debug('deleting line')
    line = symbolTools.STLine.delete(ABCLine)
    return line

def get_line(ABCLine):
    log.debug('retrieving line')
    line = symbolTools.STLine.get(ABCLine)
    return line
