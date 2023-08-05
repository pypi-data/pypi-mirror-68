# matchline: Comparing sequences of points in 2 dimensions.
# Copyright (C) 2009-2012 Specific Purpose Software GmbH
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; NO OTHER VERSION than version 2.0 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

def run():
    from ZSI.client import Binding, NamedParamBinding
    from stopeight.server.zsiTools import ABCPoint,ABCLine,ABCSymbol
    from stopeight.server import zsiTools
    from numpy import ndarray
    import sys
    import traceback

    from stopeight.server import server_include
    url=server_include.server_url+str(server_include.server_port)

    fp = open(__file__+'.log', 'a')
    b = NamedParamBinding(typesmodule=zsiTools,url=url, tracefile=fp)

    try:
        input = ABCSymbol()

        #line = ABCLine.from_numpy_array([[0,50],[25,25],[50,0],[70,70]])
        line = ABCLine.from_numpy_array([[0,50],[25,25],[50,0]])

        # for identifying echo in result
        line.id=0
        input.add_line(line)

        #for identifying echo in result
        input.id=0
        for i in input.lines:
            print("Input line:")
            for p in i:
                print(str(p.x),str(p.y))
                pass
        print('sending SOAP method: matchLine...')
        result = b.matchLine(sdklffjkdsla=input)
        for i in result['ABCSymbol']:
            print("Matched line:")
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
