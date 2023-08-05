def fileAdapter(filename):
    import wave
    from stopeight.util.editor.modules import file_wave
    spf = wave.open(filename,'r')
    if spf.getcomptype()!='NONE':
        raise Exception("Compressed WAV files are not supported.")
    total_channels = spf.getnchannels()
    allChannels=[]
    for i in range(total_channels):
        allChannels.append(file_wave._getChannel(spf,i,total_channels))
    return allChannels

def allGraphs(allChannels):
    from stopeight.util.editor.modules import grapher
    import time
    graphs=[]
    a = time.time()
    for channel in allChannels:
        graphs.append(grapher._append(grapher.create_vector_graph(channel)))
    b = time.time()
    print("Elapsed: "+str(b-a))
    return graphs


def test_NonAveraged():
    from stopeight.util.parser import process_directory
    graphs = process_directory('./','.wav',fileAdapter,allGraphs)