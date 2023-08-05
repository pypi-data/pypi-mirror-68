from stopeight.util import SVG,TCT_printer
from stopeight.util.editor.modules.grapher import _resize
from stopeight.util.editor.data import ScribbleData

import stopeight.logging as log
log.disable(log.CRITICAL)

class tPrinter(TCT_printer.TCTPrinter):
    def __init__(self,filename,columns=2):
        TCT_printer.TCTPrinter.__init__(self,filename)
        self.counter=0
        self.columns=columns
        self.scene = SVG.Scene(filename,self.height,self.columns*self.width)
        offset_x = lambda x: x+((self.counter % self.columns) * self.width)
        offset_y = lambda y: y+((self.counter//self.columns) * self.height)
        self.offset = lambda xy: (offset_x(xy[0]),offset_y(xy[1]))
        self.scroll = lambda c: ((c//self.columns)+1) * self.height
    
    def draw(self,nline,resize=True):
        #assert type(nline) is type(ScribbleData)
        if resize:
            TCT_printer.TCTPrinter.lines(self,_resize(nline,256,256)['coords'])
        else:
            TCT_printer.TCTPrinter.lines(self,nline['coords'])
        self.counter+=1

    def text(self,text):
        TCT_printer.TCTPrinter.text(self,text)
        self.counter+=1

    def write(self):
        self.scene.set_height(self.scroll(self.counter))
        self.scene.write_svg()