# Copyright (C) 2017 Fassio Blatter

from PyQt5.QtWidgets import QFileDialog,QInputDialog
from stopeight.util.editor.data import WaveData

import wave
import numpy as np
import sys

import stopeight.logging as log

def _getChannel(spf,channel_num=0,total_channels=1):
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
    assert type(channel_num) is int
    assert type(total_channels) is int
    #left samples[0::2]
    #right samples[1::2]
    return fconverter(np.asarray(np.fromstring(signal, datatype)[channel_num::total_channels], dtype=np.float64)).view(WaveData)

def _selectChannel(spf):
    from stopeight.util.runnable import EditorApp
    n = spf.getnchannels()
    channels = ['{}'.format(i) for i in range(n)]
    channel_num, ok = QInputDialog().getItem(EditorApp().window,"Select Channel","Channel:",channels,0,False)
    if ok:
        return int(channel_num),int(n)
    else:
        return 0,int(n)

def _open(filename):
    log.setLevel(log.INFO)
    spf = wave.open(filename,'r')
    if spf.getcomptype()!='NONE':
        raise Exception("Compressed WAV files are not supported.")
    channels = _selectChannel(spf)
    samples = _getChannel(spf,*channels)
    spf.close()
    log.debug("wave ndarray is "+str(type(samples)))
    log.info("Length of samples in track "+str(len(samples)))
    return samples

def open_WAV():
    log.setLevel(log.INFO)
    from stopeight.util.runnable import EditorApp
    filename = QFileDialog.getOpenFileName(EditorApp().window)
    assert type(filename[0]) == str
    assert len(filename[0]) != 0
    log.info("Opening "+str(filename[0]))
    samples = _open(filename[0])
    return samples
open_WAV.__annotations__ = {'return': WaveData}