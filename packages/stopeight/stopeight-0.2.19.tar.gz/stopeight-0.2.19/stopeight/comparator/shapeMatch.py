#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.logging import logSwitch
log = logSwitch.logNone()

from stopeight.comparator.lineMatch import LineMatchClass

class ShapeMatchClass(LineMatchClass):
    def __init__(self, compvec, toleranceDivider=2):
        LineMatchClass.__init__(self,compvec,toleranceDivider)

    def match(self,invec):
        '''
        This gives a boolean result for every line that entirely matches another line of the same length.
        '''
        #overwrite method in lineMatch for now
        #if we don't have SubSection matching,
        #and we don't have Directional matching,
        #it's only weighted (to be implemented: align from center not start)
        #this should be weighted, noreverse
        #is unweighted, reverse at the moment
        comparison = invec.copy()

        log.debug(dir(LineMatchClass))
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

        log.info('Moving comparison reversed to point 0,0')
        reverse = comparison.reverse()
        reverseAtZero = reverse.moveToZero()
        log.debug(reverseAtZero)

        forward = LineMatchClass.align(0,1,self.reference,inAtZero)
        backward = LineMatchClass.align(0,1,self.reference,reverseAtZero)

        if LineMatchClass.compare(self.tolerance,self.reference,forward) or LineMatchClass.compare(self.tolerance,self.reference,backward):
            log.info('We have a match!')
            return True
        else:
            log.info('No match.')
            return False

if __name__ == "__main__":
    from stopeight.util import runnable
    from stopeight.comparator import vectorTools
    from numpy import array
    log = logSwitch.logPrint()
    log.info('Starting shapeMatch...')
    input = array([[20,20],[55,130],[80,60],[120,85],[200,10]]).view(vectorTools.NumpyLine)
    log.info('rendering input.svg')
    input.printVectors('input')
    dbrecord = array([[13,40],[50,125],[80,61],[123,79],[191,11]]).view(vectorTools.NumpyLine)
    log.info('rendering dbrecord.svg')
    dbrecord.printVectors('dbrecord')
    matcher = ShapeMatchClass(dbrecord)
    if matcher.match(input):
        print('Hooray!')
