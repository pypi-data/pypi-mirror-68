#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter
import stopeight.logging as log
log.basicConfig(level=log.DEBUG)

try:
    # new location for sip
    # https://www.riverbankcomputing.com/static/Docs/PyQt5/incompatibilities.html#pyqt-v5-11
   from PyQt5 import sip
except ImportError:
    from PyQt5 import QtCore
    import sip
from PyQt5.QtWidgets import QApplication,QMainWindow

from stopeight.util.runnable import EditorApp

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QToolBar,QGroupBox,QHBoxLayout

# False: Is part of a compiled library
_DATA = {'Modules': [
#                            ('stopeight.util.editor.modules.legacy', False),
                            ('stopeight.util.editor.modules.file', True),
                            ('stopeight.util.editor.modules.file_wave',True),
                            ('stopeight.util.editor.modules.grapher', False),
#                            ('stopeight.util.editor.modules.analyzer', False),
                    ]
         }

import importlib
active=[]
for module in _DATA['Modules']:
    try:
        importlib.import_module(module[0])
        active.append(module)
        log.warning("Successfully imported module "+module[0])
    except ImportError as ie:
        log.warning(ie)
        log.warning("Install stopeight-clibs or external library and reinstall stopeight afterwards to use module "+module[0])
    except:
        log.warning("Module "+module[0]+" not loaded!")
_DATA['Modules']=active
                
def main():
    log.setLevel(log.NOTSET)

    import sys
    app = EditorApp()

    connections = []

    outputs = []
    
    from stopeight.util.editor.wave import WaveArea
    wave = WaveArea()
    outputs.append(wave)
    
    wbar = QToolBar("WAV Viewer Toolbar")
    wgroup = QGroupBox()
    wbox = QtWidgets.QVBoxLayout()
    # Just some button connected to `plot` method
    plotbutton = QtWidgets.QPushButton('Plot')
    #from stopeight.util.editor.modules import file_wave
    #wave.data = file_wave._open()
    #plotbutton.clicked.connect(wave.plot)
    # set the layout
    wbox.addWidget(wave.plotbar)
    wbox.addWidget(plotbutton)
    wgroup.setLayout(wbox)
    wbar.addWidget(wgroup)
    EditorApp().window.addToolBar(wbar)

    EditorApp().window.setCentralWidget(wave.canvas)
    #EditorApp().window.addDockWidget(Qt.TopDockWidgetArea,wave)    

    # Create results area
    from stopeight.util.editor.scribble import ScribbleArea
    scribble = ScribbleArea()
    outputs.append(scribble)
    from PyQt5.QtCore import Qt
    scribble.setAllowedAreas(Qt.AllDockWidgetAreas)
    EditorApp().window.addDockWidget(Qt.RightDockWidgetArea,scribble)

    # Find modules
    callables = []
    for module in _DATA['Modules']:
        callables.append(module)

    from stopeight.util.editor.callwindow import outwindow
    logwindow = outwindow()
    logwindow.setAllowedAreas(Qt.BottomDockWidgetArea)
    EditorApp().window.addDockWidget(Qt.BottomDockWidgetArea,logwindow)

    # Hook up modules
    toolbox = QToolBar("Algorithm Selector")
    #toolbox = QtWidgets.QDockWidget()
    from stopeight.util.editor.command import Connector
    for module in callables:
        connections.append(Connector(module,outputs,logwindow))
    for connection in connections:
        group = QGroupBox()
        box = QHBoxLayout()
        box.addWidget(connection.select)
        box.addWidget(connection.button)
        group.setLayout(box)
        toolbox.addWidget(group)
    EditorApp().window.addToolBar(Qt.BottomToolBarArea,toolbox)
    #EditorApp().window.addDockWidget(Qt.BottomDockWidgetArea,toolbox)
    
    EditorApp().window.show()
    sys.exit(EditorApp().exec_())

if __name__ == '__main__':
    main()