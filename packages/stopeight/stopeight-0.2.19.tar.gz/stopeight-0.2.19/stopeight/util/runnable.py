# Copyright (C) 2017 Fassio Blatter

import os,sys
exec_dir = os.path.abspath(os.path.join(os.getcwd(),os.pardir))
file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
if (exec_dir==file_dir):
    raise Exception("This script should not be run from inside the module's directories.")

from PyQt5.QtWidgets import QApplication,QMainWindow
class EditorApp(QApplication):
    _instance = None
    window = None
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(EditorApp,cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not self.window:
            import sys
            super(EditorApp,self).__init__(sys.argv)
            self.window = QMainWindow()
            self.window.setWindowTitle("Editor")

##class Singleton(type):
##    print("_instances")
##    _instances = " (same test data)"
##    def __call__(cls, *args, **kwargs):
##        print("__call__"+cls._instances)
##        return type.__call__(cls,*args, **kwargs)
##    def __new__(meta,name,bases,dict):
##        print("__new__"+meta._instances)
##        return type.__new__(meta,name,bases,dict)
##    def __init__(meta,name,bases,dict):
##        print("__init__"+meta._instances)
##        return type.__init__(meta,name,bases,dict)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            #cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
            cls._instances[cls] = type.__call__(cls,*args, **kwargs)
        return cls._instances[cls]

##class Singleton(type):
##    _instances = {}
##    def __new__(meta,name,bases,dict):
##        print(meta,name,bases,dict)
##        if meta not in meta._instances:
##            meta._instances[meta] = type.__new__(meta,name,bases,dict)
##        return meta._instances[meta]
##    def __init__(meta,name,bases,dict):
##        pass


##class Singleton(object):
##    _instances = {}
##    def __call__(cls, *args, **kwargs):
##        if cls not in cls._instances:
##            cls._instances[cls] = super(Singleton,cls).__call__(*args, **kwargs)
##        return cls._instances[cls]

from future.utils import with_metaclass
class SingletonList(with_metaclass(Singleton,list)):
    pass
import numpy
from numpy import ndarray
class SingletonNumpy(with_metaclass(Singleton,ndarray)):
    def __call__(cls, *args, **kwargs):
        print("__call__ sub")
##SingletonList = Singleton('SingletonList',(list,),{})
##SingletonNumpy = Singleton('SingletonNumpy',(numpy.ndarray,),{})

##class Singleton(object):
##    _instance = None
##    def __new__(cls,name,bases,dict):
##        if not cls._instance:
##            cls._instance = object.__new__(cls)
##        return cls._instance
##    def __init__(cls,name,bases,dict):
##        pass

##class SingletonList(Singleton(list)):
##    pass
##import numpy
##class SingletonNumpy(Singleton(numpy)):
##    pass

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
        raise Exception("Singleton instantiation test failed!")
    test3 = SingletonNumpy(shape=(1,),dtype=numpy.int16)
    #test3 = SingletonNumpy()
    print(test3[0])
