#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.comparator.matrixTools import *
from stopeight.comparator import vectorTools
from stopeight.comparator.shapeMatch import ShapeMatchClass

import stopeight.logging as log
log.disable(log.CRITICAL)

class ShapeMatchSubSectionClass:
    def __init__(self,compvec,toleranceDivider = 2):
        self.reference = compvec.copy()
        self.toleranceDivider = toleranceDivider

    def match(self,invec):
        '''
        This gives a boolean result for every line that is contained within another line.
        unequal length
        '''
        #multiple (instantiations) after change
        #order of vectors doesn't matter, will be flipped
        if (len(self.reference)<len(invec)):
            return False
            # under certain circumstances it may make sense to match a long input to a short reference
            #long = invec.copy()
            #short = self.reference.copy()
        else:
            short = invec.copy()
            long=self.reference.copy()            
        difference = len(long)-len(short)
        for count in range(difference+1):
            reordered = long.reorderToNStart(count)
            reordered = reordered[0:len(short)]
            unweightedReverse = ShapeMatchClass(short,self.toleranceDivider)
            if unweightedReverse.match(reordered):
                return True

if __name__ == "__main__":
    from stopeight.util import runnable
    from stopeight.comparator import vectorTools
    log.info('Starting shapeMatch...')
    input = array([[20,20],[55,130],[80,60],[120,85],[200,10]]).view(vectorTools.NumpyLine)
    log.info('rendering input.svg')
    input.printVectors('input')
    dbrecord = array([[5,5],[13,40],[50,125],[80,61],[123,79],[191,11],[10,10]]).view(vectorTools.NumpyLine)
    log.info('rendering dbrecord.svg')
    dbrecord.printVectors('dbrecord')
    matcher = ShapeMatchSubSectionClass(dbrecord)
    if matcher.match(input):
        print('Hooray!')
