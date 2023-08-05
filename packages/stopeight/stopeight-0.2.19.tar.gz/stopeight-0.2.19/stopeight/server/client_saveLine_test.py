# Copyright (C) 2009-2012 Specific Purpose Software GmbH

def run():
    from ZSI.client import Binding, NamedParamBinding
    from stopeight.server.zsiTools import ABCPoint,ABCLine,ABCSymbol
    from stopeight.server import zsiTools
    from numpy import ndarray
    import sys
    import traceback
    from ZSI import TC

    from stopeight.server import server_include
    url=server_include.server_url+str(server_include.server_port)

    fp = open(__file__+'.log', 'a')
    b = NamedParamBinding(typesmodule=zsiTools,url=url, tracefile=fp)

    try:
        input = ABCSymbol()
        #line = ABCLine.from_numpy_array([[0,50],[25,25],[50,0],[70,70]])
        line = ABCLine.from_numpy_array([[0,55],[25,25],[55,0]])
        # for identifying echo in result
        line.id=0
        input.add_line(line)

        # for identifying echo in result
        input.id=0
        for i in input.lines:
            print("Input line:")
            for p in i:
                print(str(p.x),str(p.y))
                pass
        print("sending SOAP method: saveLine...")
        # parameter name doesn't seem to matter
        result = b.saveLine(sdklffjkdsla=input)
        for i in result['ABCSymbol']:
            print("Saved line id: "+(i.id))
            for p in i:
                print(str(p.x),str(p.y))
                pass

    except:
        exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
        print("*** print_tb:")
        traceback.print_tb(exceptionTraceback, limit=1, file=sys.stdout)
        print("*** print_exception:")
        traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, limit=10, file=sys.stdout)
    fp.close()

if __name__ == "__main__":
    from stopeight.util import runnable
    run()
