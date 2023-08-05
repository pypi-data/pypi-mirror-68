# Copyright (C) 2017 Fassio Blatter

import os
exec_dir = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
if (exec_dir==file_dir):
    raise Exception("This script should not be run from inside the module's directories.")

import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import Qt

class EditorWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        s = super().__init__(*args, **kwargs)
        self.setWindowTitle("Editor")

# Singleton
class EditorApp(QApplication):
    _instance=None
    window=None
    ## object.__call__ is object()(), not object() unlike type()
    def __new__(cls, *args, **kwargs):
        if cls._instance==None:
            cls._instance = super().__new__(cls,sys.argv)
            cls._instance.setAttribute(Qt.AA_CompressHighFrequencyEvents, False)
            cls._instance.setAttribute(Qt.AA_CompressTabletEvents, False)
            cls._instance.setAttribute(Qt.AA_SynthesizeTouchForUnhandledMouseEvents, False)
            cls._instance.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTouchEvents, False)
            cls._instance.setAttribute(Qt.AA_SynthesizeMouseForUnhandledTabletEvents, False)
        return cls._instance
    def __init__(self, *args, **kwargs):
        if self.window==None:
            super().__init__(sys.argv)
            self.window = EditorWindow()

class Singleton(type):
    """
    inherit: (StatefulClass,metaclass=Singleton)
    not suitable for StatefulClasses with custom new or init
    not suitable for StatefulClasses with their own type information
    """
    _instances = {}
    ## type.__call__ is type(), not type()() unlike object()()
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    ## Prohibited!
    # def __new__(cls, *args, **kwargs):
    #     print(str(cls)+"__new__")
    #     super(Singleton,cls).__new__(cls,*args, **kwargs)
    def __init__(cls, *args, **kwargs):
        super(Singleton,cls).__init__(*args, **kwargs)

class SingletonList(list,metaclass=Singleton):
    pass
import numpy
from numpy import ndarray
class SingletonNumpy(ndarray,metaclass=Singleton):
    def __call__(cls, *args, **kwargs):
        print("__call__ sub")

if __name__ == '__main__':
    print("__main__")
    test1 = SingletonList()
    test1.append("5")
    print(test1)
    if (len(test1)!=1):
        raise Exception("test1 assignment failed!")
    test2 = SingletonList()
    test2.append("7")
    print(test2)
    if (len(test2)!=2):
        raise Exception("test2 assignment failed!")
    if (len(test1)!=len(test2)):
        raise Exception("SingletonList instantiation test failed!")
    test3 = SingletonNumpy(shape=(1,),dtype=numpy.int16)
    test3[0]=77
    print(test3)
    if (len(test3)!=1):
        raise Exception("test3 assignment failed!")
    test4 = SingletonNumpy(shape=(1,),dtype=numpy.int16)
    test4 = numpy.append(test4,[88])
    print(test4)
    if (len(test4)!=2):
        raise Exception("test4 assignment failed!")
    if (len(test3)!=len(test4)-1):
        print(str(len(test3))+","+str(len(test4)))
        raise Exception("SingletonList instantiation test failed!")

