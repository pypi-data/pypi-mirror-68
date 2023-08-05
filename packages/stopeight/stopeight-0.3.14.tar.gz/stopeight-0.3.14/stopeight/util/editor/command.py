# Copyright (C) 2018 Fassio Blatter

from stopeight.util import runnable
from sys import modules as loader

from PyQt5.QtWidgets import QComboBox,QPushButton

import stopeight.logging as log
_LOGDIR = '.stopeight' # this is not for logging messages; it is for data files

from inspect import signature
class Algorithm_Select(dict):
    def __init__(self, module, **kwargs):
        super(Algorithm_Select,self).__init__(**kwargs)
        self._module = module
        module_name = self._module[0]
        import importlib
        importlib.import_module(module_name)
        import types
        for key in dir(loader[module_name]):
            if not key.startswith('_'):
                builtin = isinstance(loader[module_name].__dict__[key],types.BuiltinFunctionType)
                dynamic = isinstance(loader[module_name].__dict__[key],types.FunctionType)
                if builtin or dynamic:
                    name = loader[module_name].__dict__[key].__name__
                    if builtin:
                        log.debug("Function "+name+" is C")
                    if dynamic:
                        log.debug("Function "+name+" is Python")
                    try:
                        return_type=signature(loader[module_name].__dict__[key]).return_annotation
                        try:
                            data_type=signature(loader[module_name].__dict__[key]).parameters['data'].annotation
                        except:
                            data_type = type(None)
                    except ValueError as v:
                        return_type = None
                        data_type = None
                    self[name]=(return_type,data_type)

import sys,traceback

class Algorithm_Run:

    @staticmethod
    def _auto_out(module_name,package_type,function_name):
        top = module_name+'.'+function_name
        import os
        sub = 'HEAD'
        import pkg_resources
        if (package_type==True):
            #get head from current directory (os.getcwd()).endswith('stopeight')
            if pkg_resources.require('stopeight')[0].version.find('+g'):
                sub=pkg_resources.require('stopeight')[0].version.split('+g')[1].split('.')[0]
            else:
                sub=pkg_resources.require('stopeight')[0].version
        else:
            #get head from stopeight-clibs
            sub=loader[module_name].version
        top = os.path.join(top,sub)
        return top

    @staticmethod
    def run(module,currentText,customsubpath,inputdata=None):
        import time
        time = time.time()
        outputdata=None
        try:
            if type(inputdata)!=type(None):
                try:
                    backup = inputdata[:]
                    log.info("Invoking "+currentText+" with "+str(len(inputdata))+" inputdata sets...")
                except TypeError:
                    #hack, should be copy of whole object
                    backup = inputdata.data[:]
                    log.info("Invoking "+currentText+" with custom input data type"+str(type(inputdata))+".")
                log.debug(str(inputdata))
                outputdata = loader[module[0]].__dict__[currentText](inputdata)
            else:
                backup = None
                log.info("Invoking "+currentText+" without inputdata.")
                outputdata = loader[module[0]].__dict__[currentText]()
                log.info("Size after call: Output "+str(len(outputdata)))

        #except:
        except AssertionError as ass:
            log.error(str(traceback.extract_tb(sys.exc_info()[2],limit=2).format()[1]))
        except BaseException as be:
            log.critical(str(sys.exc_info()[1])+" during method invokation: "+module[0]+'.'+currentText)
            from stopeight.util.editor.modules import file
            from os.path import expanduser,join
            file._write(backup,time,outdir=join(expanduser("~"),_LOGDIR
                                                ,Algorithm_Run._auto_out(module[0],module[1],currentText)
                                                ,customsubpath
                                                ))
            if outputdata!=None:
                try:
                    del outputdata[:]
                    if (len(outputdata)>0):
                        raise Exception("outputdata clear failed!")
                except TypeError:
                    pass
        return outputdata
    
from PyQt5.QtCore import Qt
from contextlib import redirect_stdout,redirect_stderr
#def zoo(a: str)->int:
    #if (signature(zoo).return_annotation!=Signature.empty):
class Connector:
    def __init__(self,command,outputObjects,logwindow):
        self.logwindow = logwindow
        self._outputs = outputObjects
        self._module = command
        self.select = QComboBox()
        self.methods = Algorithm_Select(self._module)
        for method in iter(self.methods):
            self.select.addItem(method)
        self.button = QPushButton()
        self.button.setText("Run")
        self.button.clicked.connect(self.run)

    @staticmethod
    def _execute(executed,output,_module,functionName,customsubpath,logwindow,_data):
        if executed:
            raise Exception("There are multiple objects handling "+str(type(_data))+". The \
current version does not support handling multiple Input objects of the same type. Please remove "+str(type(_module))+" from module list.")
        with redirect_stderr(sys.stdout):
            with redirect_stdout(logwindow.f):
                try:
                    if type(_data) != type(None):
                        log.info("Executing "+functionName+" with "+str(type(_data)))
                        computed=Algorithm_Run.run(_module,functionName,customsubpath,inputdata=_data)
                    else:
                        log.info("Executing "+functionName+" with without data")
                        computed=Algorithm_Run.run(_module,functionName,"")
                    if output!=None:
                        if type(computed)!=type(output.data):
                            raise TypeError("functionreturn "+str(type(computed))+" of function "+str(functionName)+" not equal callannotation "+str(type(output.data)))
                        output(computed)
                        output.data=computed
                except AssertionError as ass:
                    log.info("AssertionError occurred during execution "+str(ass))
                except TypeError as tpe:
                    log.info("TypeError occurred during execution "+str(tpe))
                except BaseException as be:
                    raise be
        log.debug("update logwindow")
        logwindow.update()
        return True

    def run(self):
        log.setLevel(log.INFO)
        functionName = self.select.currentText()
        log.debug(str(self.methods))
        if functionName in self.methods:
            executed = False
            functionentry = (self.methods[functionName])[1]
            log.debug("Method "+str(functionName)+" has functionentry "+str(functionentry))
            functionreturn = (self.methods[functionName])[0]
            log.debug("Method "+str(functionName)+" has functionreturn "+str(functionreturn))
            #check return type of unique functionname
            if functionreturn==type(None):
                #custom types: check all outputs for matching type
                for _input in self._outputs:
                    inputtype = type(_input)
                    log.debug("Output has custom type "+str(inputtype))
                    if functionentry==inputtype:
                        log.debug("FunctionEntry "+str(functionentry)+" inputtype "+str(inputtype))
                        if not executed:
                            executed = Connector._execute(executed,None,self._module,functionName,str(inputtype.__name__),self.logwindow,_input)
            else:
                #generic types: check all outputs for receiving __call__
                for output in self._outputs:
                    callannotation = signature(output.__call__).parameters['data'].annotation
                    log.debug("Output has callannotation "+str(callannotation))
                    if functionreturn == callannotation:
                        # currently, only one input object is supported
                        # collecting data from all inputs
                        for _input in self._outputs:
                            log.debug("Type of input object data "+str(type(_input.data)))
                            if functionentry==type(_input.data):
                                executed = Connector._execute(executed,output,self._module,functionName,_input.identify(),self.logwindow,_input.data)
                        if not executed and functionentry==type(None):
                            executed = Connector._execute(executed,output,self._module,functionName,"",self.logwindow,None)
        else:
            raise NameError("Function not found")
        

#class WaveConnector(Connector):
#    def __init__(self,command,scribble):
#        super().__init__(command,[WaveData()],scribble)

#    def run(self):
#        super().run()
