# Copyright (C) 2017 Fassio Blatter

from PyQt5.QtWidgets import QFileDialog,QInputDialog
from stopeight.util.editor.data import WaveData
from stopeight.util.runnable import EditorApp

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

def _convert(spf):
    if spf.getcomptype()!='NONE':
        raise Exception("Compressed WAV files are not supported.")
    
    import numpy as np

    #Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    datatype=None
    fconverter=lambda a:a
    if spf.getsampwidth()==1:
        #8bit unsigned
        datatype=np.uint8
        fconverter=lambda a: ((a/255.0) - 0.5) *2
    elif spf.getsampwidth()==2:
        #16bit signed
        datatype=np.int16
        fconverter=lambda a: a / 32767.0
    samples = np.fromstring(signal, datatype)

    n = spf.getnchannels()
    channels = ['{}'.format(i) for i in range(n)]
    channel_num, ok = QInputDialog().getItem(EditorApp().window,"Select Channel","Channel:",channels,0,False)
    if ok:
        #left samples[0::2]
        #right samples[1::2]
        return fconverter(np.asarray(samples[int(channel_num)::n], dtype=np.float64))

def open_WAV():
    import matplotlib.pyplot as ax
    import wave
    import sys

    filename = QFileDialog.getOpenFileName(EditorApp().window)
    log.info("Opening "+str(filename[0]))    
    spf = wave.open(filename[0],'r')
    result = _convert(spf)
    spf.close()
    log.debug("wave ndarray is "+str(type(result)))
    log.debug("Length of samples in mono file "+str(len(result)))
    return result.view(WaveData)
open_WAV.__annotations__ = {'return': WaveData}
