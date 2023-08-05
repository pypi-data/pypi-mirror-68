from numpy import ndarray
import numpy
#todo make static call
#no module dependency here, so copy of print(array_instance.dtype)
Vectors_dtype = numpy.dtype({'names':['coords','type','tct_type','cov_type'], 'formats':[('<f8', (2,)),'<i4','<i4','<i4'], 'offsets':[0,16,20,24], 'itemsize':32})

class ScribbleData(ndarray):
    def __new__(cls,*args,**kwargs):
        try:
            if kwargs['size']>1:
                kwargs['shape']=(kwargs['size'])
            else:
                kwargs['shape']=(1)
            del kwargs['size'] 
        except KeyError:
            kwargs['shape']=(1)
#todo enums
        kwargs['dtype']= numpy.dtype(Vectors_dtype)
        return super(ScribbleData,cls).__new__(cls,*args,**kwargs)

class WaveData(ndarray):
    pass
