# Copyright (C) 2019 Fassio Blatter
from stopeight import analyzer
version=analyzer.version

from stopeight.util.editor.data import ScribbleData

def legal_segments(data):
    from stopeight.matrix import Vectors
    from stopeight.analyzer import legal_segments
    return legal_segments(Vectors(data)).__array__().view(ScribbleData)
legal_segments.__annotations__ = {'data':ScribbleData,'return':ScribbleData}

