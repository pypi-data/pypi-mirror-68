#!/usr/bin/env python

from stopeight.logging import logSwitch
log = logSwitch.logNone

if __name__=='__main__':
    from stopeight.util.tableau_printer import tPrinter
    import numpy
    nopath = False
    import sys
    if len(sys.argv)>1:
        if sys.argv[1]==None:
            nopath = True
    else:
        nopath = True
    if nopath:
        raise Exception("Please specify a file name for the test output")
    printer = tPrinter(sys.argv[1],3)
    nline = numpy.array(( (0,0),(0,256),(0,256),(256,256),(256,256),(256,0),(256,0),(0,0) ))
    printer.draw(nline)
    log.debug('testing offset function '+str(printer.offset(nline[0])))
    printer.draw(nline)
    log.debug('testing offset function '+str(printer.offset(nline[0])))
    printer.draw(nline)
    printer.write()
