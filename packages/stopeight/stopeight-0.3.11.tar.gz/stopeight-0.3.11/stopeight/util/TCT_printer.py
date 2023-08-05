from stopeight.util import SVG
import os

import stopeight.logging as log
log.disable(log.CRITICAL)

class TCTPrinter:
    def __init__(self,filename):
        self.width=256
        self.height=256 #default, override before write
        self.scene = SVG.Scene(filename,self.height,self.width)
        self.offset = lambda xy: (xy[0],xy[1])
    
    def lines(self,nline):
        log.debug('Graphics adding to line queue '+str(nline))
        for i,l in enumerate(nline[0:-1]):
            log.debug('Graphics starting line from '+str(nline[i]))
            self.scene.add(SVG.Line((self.offset(nline[i])),(self.offset(nline[i+1]))))
            #self.scene.add(SVG.Line((200,200),(200,300)))

    def TCTs(self,TCTpath):
        log.debug('Segments adding to quad queue '+str(TCTpath))
        for quad in [TCTpath[x:x+3] for x in range(len(TCTpath)-2) if (x % 2 == 0)]:
            log.debug('Graphics starting quad '+str(quad))
            self.scene.add(SVG.Quad(quad[0],quad[1],quad[2]))

    def text(self,text):
        self.scene.add(SVG.Text(self.offset((0,128)),text))

    def write(self,display=False):
        self.scene.set_height(self.height)
        self.scene.write_svg()
        if display:
            self.scene.display()
