#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.logging import logSwitch
# Note: This is done depending on logging context
log = logSwitch.logNone()

import numpy
from stopeight.comparator import vectorTools
#from stopeight.comparator.shapeMatch import ShapeMatchClass
from stopeight.comparator.shapeMatchSubSection import ShapeMatchSubSectionClass
import multiprocessing
from stopeight.comparator.vectorTools import NumpyLine

class mp_data_line():
    def __init__(self,input,dbrecord,listpos):
        if (isinstance(input, numpy.ndarray) and isinstance(dbrecord, numpy.ndarray)):
            self.input_line=input
            self.record_line=dbrecord
            self.record_id=listpos
#            self.record_id=dbrecord.id
            log.debug('mp_data_line():'+'record'+str(dbrecord)+'added')
        else:
            log.error('mp_data_line(): Numpy array expected')

def _mp_match_func_name(nline):
    '''
    ShapeMatchSubSectionClass: unweightedReverseSubSection
    ShapeMatchClass: unweightedReverse
    '''
    return ShapeMatchSubSectionClass(nline)

def mp_match_line(next_record,results):
    counter = 0
    while 1:
        try:
            data=next_record.get(False)
        except:
            break
        counter += 1
        Geometry = _mp_match_func_name(data.record_line.view(NumpyLine))
        if Geometry.match(data.input_line.view(NumpyLine)):
            results.append((data.record_id))

class MPLine():
    allLines = []
    def __init__(cls, lines):
        if isinstance(lines, list) and all(isinstance(item,numpy.ndarray) for item in lines):
            cls.allLines = lines
            log.debug('MPLine.init():'+str(len(lines))+'records added')
        else:
            log.error('MPLine.init(): list of Numpy arrays please '+str(type(lines)))
    
    def matchLine(self,line):
        if (isinstance(line, numpy.ndarray)):
            manager = multiprocessing.Manager()
            log.debug('MPLine.matchLine(): Manager initialized')

            results = manager.list()

            comparison = line
    #        comparison = comparison.view(dtype=numpy.dtype(float))
            log.debug('comparing %s:'%(comparison))
            next_record = multiprocessing.Queue()
            log.debug('MPLine.matchLine(): Queue created')
            log.debug('MPLine.matchLine():'+'initializing'+str(len(self.allLines))+'records')
            for n,dbrecord in enumerate(self.allLines):
                if not isinstance(dbrecord, numpy.ndarray):
                    log.error('MPLine.matchLine(): allLines(): wrong format '+str(type(dbrecord)))
                    break
                log.debug('to %s'%(dbrecord))
    #            dbrecord = dbrecord.view(dtype=numpy.dtype(float),type=numpy.ndarray)
                next_record.put(mp_data_line(comparison,dbrecord,n))
            pool = []
            for i in range(0,multiprocessing.cpu_count()): #number of CPUs plus 1
                process = multiprocessing.Process(target=mp_match_line, args=(next_record,results))
                pool.append(process)
                process.start()
            for proc in pool:
                proc.join()
            for r in results:
                log.info('MPLine.matchLine(): found '+str(r))
            manager.shutdown
            log.debug('MPLine.matchLine(): Manager shutdown')
            return results
        else:
            log.warning('MPLine.matchLine(): is not Numpy array')
            log.error('MPLine.matchLine():'+str(type(line))+'unexpected')

def run(dbrecords,line):
    matcher = MPLine(dbrecords)
    log.info('sending job to pooling')
    return matcher.matchLine(line)

def runNPopulate(dbrecords,line):
    result = run(dbrecords,line)
    return populate(result)

def populate(result):
    results = []
    for pos in result:
        log.info('matched line position '+str(pos))
        results.append(dbrecords[pos])
    return results
    
    
if __name__ == "__main__":
    log = logSwitch.logPrint()
    log.info('Starting lineMatch...')
    s = numpy.array([[20,20],[55,130],[80,60],[120,85],[200,10]])
    #log.info('rendering input.svg')
    #input.printVectors('input')
    dbrecord = numpy.array([[13,40],[50,125],[80,61],[123,79],[191,11]])
    #log.info('rendering dbrecord.svg')
    #dbrecord.printVectors('dbrecord')
    dbrecords = []
    dbrecords.append(dbrecord)
    res = runNPopulate(dbrecords,s)    
    if len(res)>0:
        log.info('Hooray! '+str(len(res))+'results')
