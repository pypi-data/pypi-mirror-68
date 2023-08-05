#!/usr/bin/env python

# This code is from an example found on the web.
# only used for debugging math stuff.

# <!-- The quadratic Bezier curve -->
#     <path id = "quadcurveABC" d = "M 100 350 q 150 -300 300 0" stroke = "blue" stroke-width = "5" fill = "none"/>

import sys
import os
display_prog = '/usr/lib/x86_64-linux-gnu/qt5/examples/svg/svgviewer/svgviewer' # Command to execute to display images.

class Scene:
    def __init__(self,name="SVG.out",height=400,width=400):
        #width="744.09448"
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 %d %d\" height=\"%d\" width=\"%d\">\n" % (self.width,self.height,self.height,self.width),
               " <g style=\"fill-opacity:1.0; stroke:black;\n",
               "  stroke-width:1;\">\n"]
        for item in self.items: var += item.strarray()
        var += [" </g>\n</svg>\n"]
        return var

    def set_height(self,height):
        self.height=height

    def write_svg(self,fileName=None):
        #if filename:
        #    self.svgname = filename
        #else:
        self.svgname = self.name + ".svg"
        file = open(self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return

    def display(self,prog=display_prog):
        if os.system("%s %s &" % (prog,self.svgname)):
            print('Displaying %s' %self.svgname)
        else:
#            import importlib
#            if importlib.find_loader('SVGViewer') is not None:
            try:
                from stopeight.util import SVGViewer
                SVGViewer.show(self.svgname)
            except BaseException as e:
                print(e)
                print('SVGViewer not found')
        return


class Line:
    def __init__(self,start,end):
        self.start = start #xy tuple
        self.end = end     #xy tuple
        return

    def strarray(self):
        return ["  <line x1=\"%d\" y1=\"%d\" x2=\"%d\" y2=\"%d\" />\n" %\
                (self.start[0],self.start[1],self.end[0],self.end[1])]


class Circle:
    def __init__(self,center,radius,color):
        self.center = center #xy tuple
        self.radius = radius #xy tuple
        self.color = color   #rgb tuple in range(0,256)
        return

    def strarray(self):
        return ["  <circle cx=\"%d\" cy=\"%d\" r=\"%d\"\n" %\
                (self.center[0],self.center[1],self.radius),
                "    style=\"fill:%s;\"  />\n" % colorstr(self.color)]

class Rectangle:
    def __init__(self,origin,height,width,color):
        self.origin = origin
        self.height = height
        self.width = width
        self.color = color
        return

    def strarray(self):
        return ["  <rect x=\"%d\" y=\"%d\" height=\"%d\"\n" %\
                (self.origin[0],self.origin[1],self.height),
                "    width=\"%d\" style=\"fill:%s;\" />\n" %\
                (self.width,colorstr(self.color))]

class Quad:
    def __init__(self,start,mid,end):
        self.start = start
        self.mid = mid
        self.end = end

    def strarray(self):
        # start-x start-y q rel-mid-x 2x:rel-mid-y rel-end-x rel-end-y %d
        #return ["  <path d = \"M 70 230 q 130 -320 260 0\"  fill = \"none\"/>"]
        return ["  <path d = \"M %d %d Q %d %d %d %d\"  fill = \"none\"/>" % \
            (self.start[0],self.start[1],\
            (self.mid[0]),\
            (self.mid[1]),\
            (self.end[0]),\
            (self.end[1]))]

class Text:
    def __init__(self,origin,text,size=8):
        self.origin = origin
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["  <text x=\"%d\" y=\"%d\" font-size=\"%d\">\n" %\
                (self.origin[0],self.origin[1],self.size),
                "   %s\n" % self.text,
                "  </text>\n"]


def colorstr(rgb): return ("#%x%x%x" % (int(rgb[0]/16),int(rgb[1]/16),int(rgb[2]/16)))

def test():
    scene = Scene('SVG')
    scene.add(Rectangle((100,100),200,200,(0,255,255)))
    scene.add(Line((200,200),(200,300)))
    scene.add(Line((200,200),(300,200)))
    scene.add(Line((200,200),(100,200)))
    scene.add(Line((200,200),(200,100)))
    scene.add(Circle((200,200),30,(0,0,255)))
    scene.add(Circle((200,300),30,(0,255,0)))
    scene.add(Circle((300,200),30,(255,0,0)))
    scene.add(Circle((100,200),30,(255,255,0)))
    scene.add(Circle((200,100),30,(255,0,255)))
    scene.add(Text((50,50),"Testing SVG"))
    scene.add(Quad((70,230),(130,-320),(260,0)))
    scene.write_svg()
    scene.display()
    return

if __name__ == '__main__': test()
