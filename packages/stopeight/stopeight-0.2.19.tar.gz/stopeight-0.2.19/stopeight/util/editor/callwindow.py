from PyQt5.QtWidgets import QDockWidget,QTextEdit,QVBoxLayout,QGroupBox
from PyQt5.QtCore import Qt, QSize
from stopeight.util.runnable import EditorApp

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

import sys
import os
import io


import funcsigs

class outwindow(QDockWidget):
    def __init__(self,parent=EditorApp().window):
        super(outwindow,self).__init__("LogWindow",parent)
        self.setMinimumSize(QSize(30, 0))

        self.text = QTextEdit()
        self.setWidget(self.text)
        self.text.setText("")
        self.data = None
        self.f = io.BytesIO()

    #def __call__(self,data=None):
    #    with stdout_redirector(self.f):
    #        print('foobar')
    #        print(12)
    #        #libc.puts(b'this comes from C')
    #        os.system('echo and this is from echo')
    #__call__.__annotations__ = {'data': funcsigs._empty}
    
    def update(self):
        print('From callwindow: "{0}"'.format(self.f.getvalue().decode('utf-8')))
        self.text.setText(self.f.getvalue().decode('utf-8'))
        self.show()
        self.f.close()
        self.f = io.BytesIO()
