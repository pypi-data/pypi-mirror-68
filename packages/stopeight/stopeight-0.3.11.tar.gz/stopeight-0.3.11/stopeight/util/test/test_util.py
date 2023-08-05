def test_linePrinter():
    from stopeight.util.TCT_printer import TCTPrinter
    from stopeight import legacy
    myprinter = TCTPrinter('linePrinter.out')
    fileline = legacy.parse_file('stopeight-clibs/legacy/tests/stage3-build04-authWorking/almostStraightLeg.sp')
    myprinter.lines(fileline)
    fileline = legacy.stroke_sequential(fileline)
    fileline = legacy.TCT_to_bezier(fileline)
    myprinter.TCTs(fileline)
    myprinter.write()

def test_tableauPrinter():
    from stopeight.util.editor.data import ScribbleData
    from stopeight.util.tableau_printer import tPrinter
    import numpy
    printer = tPrinter('tableauPrinter.out',3)
    data = ( (0,0),(0,256),(0,256),(256,256),(256,256),(256,0),(256,0),(0,0) )
    nline = ScribbleData(size=len(data))
    for i,v in enumerate(data):
        nline[i]['coords'] = [v[0],v[1]]
    printer.draw(nline)
    print('testing offset function '+str(printer.offset(nline[0])))
    printer.draw(nline)
    print('testing offset function '+str(printer.offset(nline[0])))
    printer.draw(nline)
    printer.write()

def test_TCTPrinter():
    from stopeight.util.TCT_printer import TCTPrinter
    import numpy
    printer = TCTPrinter('TCTPrinter.out')
    nline = numpy.array(((200,200),(200,300)))
    printer.lines(nline)
    printer.lines(nline)
    printer.lines(nline)
    #printer.scene.add(SVG.Line((200,200),(200,300)))
    printer.write()