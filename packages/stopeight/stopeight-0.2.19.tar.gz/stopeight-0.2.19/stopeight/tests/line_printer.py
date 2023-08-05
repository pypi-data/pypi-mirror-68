from stopeight.util import runnable

import os
from stopeight.util.TCT_printer import TCTPrinter

if __name__=='__main__':
    from stopeight.util import runnable
    from stopeight import legacy
    import sys
    nopath = False
    if len(sys.argv)>1:
        if sys.argv[1]==None:
            nopath = True
    else:
        nopath = True
    if nopath:
        raise Exception("Please specify a unpacked legacy pen-stroke file (i.e. stopeight-clibs/legacy/tests/stage3-build04-authWorking/almostStraightLeg.sp)")
    noout = False
    if len(sys.argv)>2:
        if sys.argv[2]==None:
            noout = True
    else:
        noout = True
    if noout:
        raise Exception("Please specify the svg output file name (i.e. line_printer.out)")
    myprinter = TCTPrinter(sys.argv[2])
    fileline = legacy.parse_file(sys.argv[1])
    myprinter.lines(fileline)
    fileline = legacy.stroke_sequential(fileline)
    fileline = legacy.TCT_to_bezier(fileline)
    myprinter.TCTs(fileline)
    myprinter.write()
    print("SVG ouput written to "+sys.argv[2]+".svg")
