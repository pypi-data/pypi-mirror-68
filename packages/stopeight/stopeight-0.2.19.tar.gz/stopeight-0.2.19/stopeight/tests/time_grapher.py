from stopeight.util.editor.modules.file_wave import _convert
import wave
from stopeight.util.editor.data import WaveData,ScribbleData,ScribblePoint
from stopeight.util.editor.modules.grapher import _append
from stopeight.grapher import create_vector_graph
import numpy as np

import time

if __name__ == '__main__':
    filename = "afterstanley3-bass.wav"
    spf = wave.open(filename,'r')
    result = _convert(spf)
    spf.close()
    data = result.view(WaveData)
    a = time.clock()
    for i in range(1,10):
        result = create_vector_graph(data,1,1.0,True).__array__()
    b = time.clock()
    print("Elapsed: "+str(b-a))
    assert type(result) is np.ndarray, "Cast Error: %r" % type(result)
    result = _append(result)
    print("Return Length "+str(len(result)))
    array = result.view(ScribbleData)
    print(type(array))
    print(len(array))