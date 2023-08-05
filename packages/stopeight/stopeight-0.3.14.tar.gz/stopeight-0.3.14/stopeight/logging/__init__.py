import inspect
import os

def _path(stack):
    # bug: PERFORMANCE
    return os.path.relpath(stack,os.path.dirname(os.path.realpath(__file__)))

NOTSET=0
DEBUG=10
def debug(message):
    basicConfig().debug(_path(inspect.stack()[1][1]),message)

INFO=20
def info(message):
    basicConfig().info(_path(inspect.stack()[1][1]),message)

WARNING=30
def warning(message):
    basicConfig().warning(_path(inspect.stack()[1][1]),message)

ERROR=40
def error(message):
    basicConfig().error(_path(inspect.stack()[1][1]),message)

CRITICAL=50
def critical(message):
    basicConfig().critical(_path(inspect.stack()[1][1]),message)

class configClass():
    _level=NOTSET
    _defaultLevel=_level

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        if 'level' in kwargs:
            self._defaultLevel=kwargs['level']
            self._level=self._defaultLevel
        else:
            self._level=self._defaultLevel
        return self

# Singleton
class basicConfig(configClass):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if 'force' in kwargs:
            if kwargs['force']==True:
                del kwargs['force']
                cls._instance = super().__new__(cls, *args, **kwargs)
                return cls._instance
        if cls._instance == None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def debug(self,relpath,message):
        if self._level <= DEBUG:
            print(str(relpath)+": "+"debug: "+str(message))

    def info(self,relpath,message):
        if self._level <= INFO:
            print(str(relpath)+": "+"info: "+str(message))

    def warning(self,relpath,message):
        if self._level <= WARNING:
            print(str(relpath)+": "+"WARN: "+str(message))

    def error(self,relpath,message):
        if self._level <= ERROR:
            print(str(relpath)+": "+"ERROR: "+str(message))

    def critical(self,relpath,message):
        if self._level <= CRITICAL:
            print(str(relpath)+": "+"CRITICAL: "+str(message))

def setLevel(level):
    basicConfig()._level=level

def disable(level):
    basicConfig()._level=level+1