#!/usr/bin/env python

# Copyright (C) 2009-2016 Specific Purpose Software GmbH
from stopeight.logging import logSwitch
log = logSwitch.logNone()

from stopeight.util.runnable import EditorApp

from stopeight.util.editor.data import ScribbleData,ScribblePoint
from stopeight.util.editor.scribble import ScribbleArea
from PyQt5.QtWidgets import QFileDialog

def save_ScribbleData(data):
    # this is not a real error but saves us from writing more code
    data=data.data
    raise ValueError
save_ScribbleData.__annotations__ = {'data': ScribbleArea, 'return': type(None)}

def save_as_ScribbleData(data):
    filename = QFileDialog.getSaveFileName(EditorApp().window,"QFileDialog.getSaveFileName()","","NumPy Files (*.npy)")
    log.debug("Saving to File "+str(filename[0]))
    _to_file(filename[0],data.data)
    return filename
save_as_ScribbleData.__annotations__ = {'data': ScribbleArea, 'return': type(None)}

def open_ScribbleData():
    filename = QFileDialog.getOpenFileName(EditorApp().window)
    log.debug("Reading from File "+str(filename[0]))
    return _read(filename[0])
open_ScribbleData.__annotations__ = {'return': ScribbleData}

def _read(path):
    if path.endswith('.npy'):
        import numpy
        arr = numpy.load(path)
        if arr.dtype==ScribbleData().dtype:
            arr=arr.view(ScribbleData)
        return arr
    elif path.endswith('.json'):
        import json
        f = open(path,'r')
        return json.load(f)

def _write(data,timestamp,outdir=None):
    if outdir==None:
        from os.path import expanduser,join
        outdir=join(expanduser("~"))
    import datetime
    time = (datetime.datetime.utcfromtimestamp(timestamp))
    time = time.strftime('%Y%m%dT%H%M%S')
    name = time+"."+type(data).__name__
    import os
    from os import path
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    path = path.join(outdir,name)
    log.info("Writing method input data to: "+path)
    _to_file(path,data)

def _to_file(path,data):
    #import pickle
    #picl = pickle.Pickler(open(path+'.pickle','wb'),pickle.HIGHEST_PROTOCOL)
    #picl.dump(_DATA['MyScribble'].INPUT)

    import numpy
    if type(data).__bases__[0] == numpy.ndarray:
        numpy.save(path,data,allow_pickle=True,fix_imports=True)#python3: fix_imports=False
    else:
        import json
        f = open(path+'.json','w')
        json.dump(data,f)
