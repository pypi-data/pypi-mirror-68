#!/usr/bin/env python

# Copyright (C) 2016 Specific Purpose Software GmbH

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


from PyQt5.QtCore import QDir, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QImage, QImageWriter, QPainter, QPen, qRgb
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QAction, QApplication, QColorDialog, QFileDialog,
        QInputDialog, QMainWindow, QMenu, QMessageBox, QWidget)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter

from PyQt5.QtGui import QTabletEvent
from PyQt5.QtCore import QEvent

from stopeight.util.runnable import EditorApp
from stopeight.util.editor.data import ScribbleData

import stopeight.logging as log

class ScribbleArea(QtWidgets.QDockWidget):
    def __init__(self, parent=EditorApp().window):
        super(ScribbleArea, self).__init__("ScribbleArea",parent)
        self.setMinimumSize(QSize(300, 256))

        self.setAttribute(Qt.WA_StaticContents)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setAttribute(Qt.WA_TouchPadAcceptSingleTouchEvents)
        self.scribbling = False
        self.scribblingData=[]
        self.scribblingTop=self.scribblingBottom=self.scribblingLeft=self.scribblingRight=None
        self.scribblingMove=0
        self.scribblingDrawIndex = 0
        self.scribblingFingerCount = 0
        self.scribblingCurrentFinger=None

        self.myPenWidth = 1
        self.myPenColor = Qt.blue
        self.image = QImage()

        self.data = ScribbleData()

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(qRgb(255, 255, 255))
        self.update()

    def _input(self, x, y):
        self.scribblingData.append((x,y))
        if y<self.scribblingTop:
            self.scribblingTop=y
        if y>self.scribblingBottom:
            self.scribblingBottom=y
        if x<self.scribblingLeft:
            self.scribblingLeft=x
        if x>self.scribblingRight:
            self.scribblingRight=x

    def _press(self,event):
        self.clearImage()
        self.scribbling = True
        if (event.type() == QEvent.TouchBegin):
            self.scribblingFingerCount=len(event.touchPoints())
            self.scribblingCurrentFinger=len(event.touchPoints())-1
            self.scribblingTop=self.scribblingBottom=0
            self.scribblingLeft=self.scribblingRight=0
        elif (event.type() == QEvent.MouseButtonPress):
            self.scribblingTop=self.scribblingBottom=event.localPos().y()
            self.scribblingLeft=self.scribblingRight=event.localPos().x()
        elif (event.type() == QEvent.TabletPress):
            self.scribblingTop=self.scribblingBottom=event.posF().y()
            self.scribblingLeft=self.scribblingRight=event.posF().x()
        self.scribblingDrawIndex=0

    def _move(self, event):
        if (event.type() == QEvent.TouchUpdate):
            if (len(event.touchPoints())!=self.scribblingFingerCount):
                self.scribblingFingerCount=len(event.touchPoints())
                self.scribblingCurrentFinger=len(event.touchPoints())-1
        self.scribblingMove+=1
        if self.scribblingMove > 20:
            self._drawLines()
            self.scribblingMove=0

    def _release(self, event):
        self.scribbling = False
        if (event.type() == QEvent.TouchEnd):
            self.scribblingFingerCount=0
            if (len(event.touchPoints())!=self.scribblingFingerCount):
                self.scribblingCurrentFinger=len(event.touchPoints())-1
        self._drawLines()
        if type(self.data) is not type(None):
            del self.data
        self.data = ScribbleData(size=len(self.scribblingData))
        for i,v in enumerate(self.scribblingData):
            self.data[i]['coords'] = [v[0],v[1]]
        #don't assign new self.data = [], maybe self.data[:] = []
        if type(self.scribblingData) is not type(None):
            del self.scribblingData
        self.scribblingData = []

    def _cancel(self, event):
        self.scribbling = False
        if (event.type() == QEvent.TouchCancel):
            self.scribblingFingerCount=0
            if (len(event.touchPoints())!=self.scribblingFingerCount):
                self.scribblingCurrentFinger=len(event.touchPoints())-1
        if type(self.scribblingData) is not type(None):
            del self.scribblingData
        self.scribblingData=[]
        self.scribblingTop=self.scribblingBottom=self.scribblingLeft=self.scribblingRight=None
        self.scribblingMove=0
        self.scribblingDrawIndex = 0


    def _drawLines(self):
        painter = QPainter(self.image)
        if len(self.scribblingData)>self.scribblingDrawIndex+1:
            try:
                painter.setPen(QPen(self.myPenColor, self.myPenWidth, Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
                for n in range(len(self.scribblingData)-1-self.scribblingDrawIndex):
                    painter.drawLine(QPoint(self.scribblingData[n+self.scribblingDrawIndex][0],self.scribblingData[n+self.scribblingDrawIndex][1]), QPoint(self.scribblingData[n+1+self.scribblingDrawIndex][0],self.scribblingData[n+1+self.scribblingDrawIndex][1]))
            finally:
                painter.end()
            rad = self.myPenWidth / 2 + 2
            self.update(QRect(QPoint(self.scribblingLeft,self.scribblingTop), QPoint(self.scribblingRight,self.scribblingBottom)).normalized().adjusted(-rad, -rad, +rad, +rad))
            self.scribblingDrawIndex=len(self.scribblingData)-1
            self.scribblingTop=self.scribblingBottom=self.scribblingData[-1][1]
            self.scribblingLeft=self.scribblingRight=self.scribblingData[-1][0]

    #todo: Remove try/catch in tableteventrealease
    #todo: Switch to hiResGlobalX; remainder: global - int(global); QWidget mapFromGlobal
    def event(self,event):
        if (event.type() == QEvent.MouseButtonPress):
            if event.button() == Qt.LeftButton:
                self._press(event)
                self._input(event.localPos().x(),event.localPos().y())
                return True           
        elif (event.type() == QEvent.MouseMove and self.scribbling):
            if (event.buttons() & Qt.LeftButton) and self.scribbling:
                self._input(event.localPos().x(),event.localPos().y())
                self._move(event)
                return True
        elif (event.type() == QEvent.MouseButtonRelease and self.scribbling):
            if (event.button() == Qt.LeftButton) and self.scribbling:
                self._input(event.localPos().x(),event.localPos().y())
                self._release(event)
                return True
        elif (event.type() == QEvent.TabletPress):
            self._press(event)
            self._input(event.posF().x(),event.posF().y())
            return True
        elif (event.type() == QEvent.TabletMove) and self.scribbling:
            self._input(event.posF().x(),event.posF().y())            
            self._move(event)
            return True
        elif (event.type() == QEvent.TabletRelease) and self.scribbling:
            self._input(event.posF().x(),event.posF().y())
            self._release(event)
            try:
                self.tablet_id=event.uniqueId()
            except:
                self.__dict__.__delattr__('tablet_id')
            return True
        elif (event.type() == QEvent.TouchBegin):
            self._press(event)
            self._input(event.touchPoints()[-1].pos().x(),event.touchPoints()[-1].pos().y())
            return True
        elif (event.type() == QEvent.TouchUpdate and self.scribbling):
            self._input(event.touchPoints()[-1].pos().x(),event.touchPoints()[-1].pos().y())
            self._move(event)
            return True
        elif (event.type() == QEvent.TouchEnd and self.scribbling):
            self._input(event.touchPoints()[-1].pos().x(),event.touchPoints()[-1].pos().y())
            self._release(event)
            return True
        elif (event.type() == QEvent.TouchCancel and self.scribbling):
            self._input(event.touchPoints()[-1].pos().x(),event.touchPoints()[-1].pos().y())
            self._cancel(event)
            return True
        return super().event(event)

    def identify(self)->str:
        import os
            
        #if (os.getcwd()).endswith('stopeight'):
        #    if (self.select.module_name=='stopeight.util.editor.modules.file'):
        if hasattr(self,'tablet_id'):
            sub = str(self.tablet_id)
        else:
            sub = 'MouseData'
        return sub

    def paintEvent(self, event):
        painter = QPainter(self)
        dirtyRect = event.rect()
        try:
            painter.drawImage(dirtyRect, self.image, dirtyRect)
        finally:
            painter.end()

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width() + 128, self.image.width())
            newHeight = max(self.height() + 128, self.image.height())
            self.resizeImage(self.image, QSize(newWidth, newHeight))
            self.update()
        super(ScribbleArea, self).resizeEvent(event)

    def __call__(self, data, color=Qt.blue, clear=True):
        assert type(self.data) is ScribbleData
        if clear:
            self.clearImage()
        #self.data=data
        #for d,c in self.data,self.colors:
        #self.scribble.plot(d,c)
        log.debug("Drawing "+str(len(data))+" lines")
        painter = QPainter(self.image)
        try:
            painter.setPen(QPen(color, self.myPenWidth, Qt.SolidLine,Qt.RoundCap, Qt.RoundJoin))
            for first,second in zip(data,data[1:]):
                painter.drawLine(first['coords'][0],first['coords'][1],second['coords'][0],second['coords'][1])
        finally:
            painter.end()
        self.update()
    __call__.__annotations__ = {'data': ScribbleData}

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QImage(newSize, QImage.Format_RGB32)
        newImage.fill(qRgb(255, 255, 255))
        painter = QPainter(newImage)
        try:
            painter.drawImage(QPoint(0, 0), image)
        finally:
            painter.end()
        self.image = newImage

    def print_(self):
        printer = QPrinter(QPrinter.HighResolution)

        printDialog = QPrintDialog(printer, self)
        if printDialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)
            rect = painter.viewport()
            size = self.image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.image.rect())
            try:
                painter.drawImage(0, 0, self.image)
            finally:
                painter.end()

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth

#    def penColor(self):
#        newColor = QColorDialog.getColor(self.penColor())
#        if newColor.isValid():
#            self.setPenColor(newColor)

#    def penWidth(self):
#        newWidth, ok = QInputDialog.getInt(self, "Scribble",
#                "Select pen width:", self.penWidth(), 1, 50, 1)
#        if ok:
#            self.setPenWidth(newWidth)

