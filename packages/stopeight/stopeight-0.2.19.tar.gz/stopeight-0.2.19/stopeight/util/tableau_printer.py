from stopeight.logging import logSwitch
log = logSwitch.logNone
from stopeight.util import SVG,TCT_printer

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
    
    def draw(self,nline):
        TCT_printer.TCTPrinter.lines(self,nline)
        self.counter+=1

    def text(self,text):
        TCT_printer.TCTPrinter.text(self,text)
        self.counter+=1

    def write(self):
        self.scene.set_height(self.scroll(self.counter))
        self.scene.write_svg()
        self.scene.display()

