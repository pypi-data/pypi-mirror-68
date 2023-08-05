#!/usr/bin/env python

if __name__=='__main__':
    from stopeight.util.TCT_printer import TCTPrinter
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
    printer = TCTPrinter(sys.argv[1])
    nline = numpy.array(((200,200),(200,300)))
    printer.lines(nline)
    printer.lines(nline)
    printer.lines(nline)
    #printer.scene.add(SVG.Line((200,200),(200,300)))
    printer.write()
