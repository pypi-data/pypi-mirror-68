#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.logging import logSwitch
log = logSwitch.logNone()

from stopeight.comparator.matrixTools import *
from stopeight.comparator import vectorTools
from numpy import zeros_like

class LineMatchClass:
    minTolerance = 2

    @staticmethod
    def align(point1,point2,reference,comparison):

        log.info('Moving reference to comparePoint')
        movement = idmatrix()
        movement = dot(translate(-reference[point1]),movement)
        compareRecord = zeros_like(reference)
        for pos,moveme in enumerate(reference):
            compareRecord[pos] = transform(moveme,movement)
        log.debug(compareRecord)
        log.info('We are aligning point %s ' %compareRecord[point2] + 'with %s' %comparison[1])
        referenceAngle = (compareRecord[point2]).getAngleToNegativeXAxis()
        comparisonAngle = (comparison[1]).getAngleToNegativeXAxis()

        angle = referenceAngle - comparisonAngle
        log.info('Rotating comparison: %s' %angle)
        movement = idmatrix()
        movement = dot(rotate(angle),movement)
        match = zeros_like(comparison)
        for pos,moveme in enumerate(comparison):
            match[pos]= transform(moveme,movement)

        log.info('Moving match to destination: %s' %reference[point1])
        movement = idmatrix()
        movement = dot(translate(reference[point1]),movement)
        for pos,moveme in enumerate(match):
            match[pos]= transform(moveme,movement)
        return match

    @staticmethod
    def __getSmallestDistance(line):
        smallestDistance = vectorTools.getVectorLength(line[1]-line[0])
        for i,point in enumerate(line[1:-1]):
            length = vectorTools.getVectorLength(line[i+1]-line[i])
            if length<smallestDistance:
                smallestDistance = length
        return smallestDistance

    @staticmethod
    def __withinToleranceRange(tolerance,point1,point2):
        if point2[0]<point1[0]+tolerance and point2[0]>point1[0]-tolerance and point2[1]<point1[1]+tolerance and point2[1]>point1[1]-tolerance:
            return True
        return False

    @staticmethod
    def compare(tolerance,first,second):
        for i,point in enumerate(first):
            if not LineMatchClass.__withinToleranceRange(tolerance,point,second[i]):
                return False
        return True

    @staticmethod
    def __scaleToAvg(tobescaled,target):
        log.debug('Comparing lengths of vectors in target...')
        dbAvg = target[0:len(tobescaled)].getAverageLength()
        log.debug(dbAvg)
        log.debug('...with lengths of vectors in tobescaled...')
        tobescaledAvg = tobescaled.getAverageLength()
        log.debug(tobescaledAvg)
        movement = idmatrix()
        # Uniform scale:
        scaleFactor = [dbAvg/tobescaledAvg,dbAvg/tobescaledAvg]
        log.debug(scaleFactor)
        log.info('Scale tobescaled to target: %s' %scaleFactor)
        movement = dot(scale(scaleFactor),movement)
        for pos,moveme in enumerate(tobescaled):
            tobescaled[pos]= transform(moveme,movement)
        return tobescaled

    @staticmethod
    def validate_data(invec,compvec):
        # prepare data, doing a check
        if len(invec)<=2 or len(compvec)<=2:
            #Should be replaced by try/except -> throw
            raise Exception('length of input or reference is below 3. Scale-Matching lines of size <3 is not possible.')
            return False
        if len(invec)!=len(compvec):
            raise Exception('length of input is not equal to length of reference')
            return False
        return True

    @staticmethod
    def __determine_tolerance(reference,toleranceDivider):
        tolerance = 15 # matching all shapes with points within pixel range; was 15
        if (len(reference)>=3):
            smallestDistance = LineMatchClass.__getSmallestDistance(reference)
        else:
            smallestDistance = tolerance
        tolerance = smallestDistance / toleranceDivider
        if (tolerance<LineMatchClass.minTolerance):
            tolerance=LineMatchClass.minTolerance
        log.info('Adjusting tolerance to: %s' %tolerance)
        return tolerance

    '''
    Will not return matches with uneven lengths!
    toleranceDivider = 2 is suitable for lineMatch, maybe use different value for symbolposition
    '''
    def __init__(self,compvec,toleranceDivider = 2):
        # Note: We are caching reference here, because tolerance depends on it
        self.reference = compvec.copy()
        
        # prepare data, adjusting tolerance (only needed Once for input and reverse)
        # GET TOLERANCE FROM ONE
        # TOLERANCE NEEDS TO BE TAKEN FROM THE ONE THAT IS NOT GOING TO BE SCALED, preferably reference, because it can be predetermined -> DB/Cache
        self.tolerance = LineMatchClass.__determine_tolerance(self.reference, toleranceDivider)

    def scale(self,invec):
        # modification of comparison (and reference?) actually starts here

        #Scale comparison, not reference, because tolerance is already adjusted to reference
        # AND SCALE THE OTHER
        # EVERY __compare NEEDS A different SCALE (except forward/backward)
        invec = LineMatchClass.__scaleToAvg(invec,self.reference)
        return invec

    # this has only been separated from __init__ to allow overwriting
    def match(self,invec):
        comparison = invec.copy()

        # this is being done if not instance of SubDivision
        if not LineMatchClass.validate_data(comparison,self.reference):
            raise Exception('data validation failed')

        comparison = self.scale(comparison)

        log.debug('Comparing:')
        log.debug(comparison)
        log.debug('To:')
        log.debug(self.reference)

        # all we need from here is comparison
        log.info('Moving comparison to point 0,0')
        inAtZero = comparison.moveToZero()
        log.debug(inAtZero)

        forward = LineMatchClass.align(0,1,self.reference,inAtZero)

        if LineMatchClass.compare(self.tolerance,self.reference,forward):
            log.info('We have a match!')
            return True
        else:
            log.info('No match.')
            return False

if __name__ == "__main__":
    from stopeight.util import runnable
    log = logSwitch.logPrint()
    log.info('Starting lineMatch...')
    input = array([[20,20],[55,130],[80,60],[120,85],[200,10]]).view(vectorTools.NumpyLine)
    log.info('rendering input.svg')
    #input.printVectors('input')
    dbrecord = array([[13,40],[50,125],[80,61],[123,79],[191,11]]).view(vectorTools.NumpyLine)
    log.info('rendering dbrecord.svg')
    #dbrecord.printVectors('dbrecord')
    matcher = LineMatchClass(dbrecord)
    print(type(matcher))
    print(dir(matcher))
    if matcher.match(input):
        print('Hooray!')
