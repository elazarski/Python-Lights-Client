'''
Created on Sep 28, 2015

@author: eric
'''
from alsamidi import *
from multiprocessing import Process, current_process, Pipe  # @UnresolvedImport

class ALSA(object):
    '''
    Deals with ALSA sequencer
        Starts/Stops Sequencer
        Starts/Stops threads
    '''

    def __init__(self):
        '''
        opens ALSA Sequencer
        initializes queues for threads
        '''
        alsaseq.client("Test", 2, 2, False)
        alsaseq.start()
        print("ALSA Sequencer started")
        
        
    """ Close ALSA  Sequencer """
    def close(self):
        alsaseq.stop()
        print("ALSA Sequencer closed")
        
        
    """ Function to play a song.
    This method creates I/O threads
    and waits for them to finish """
    def playSong(self, data):
        inputData = data[0]
        outputData = data[1]
        mpData = data[2]
        
        numInputTracks = len(inputData)
        numOutputTracks = len(outputData)
        
        
        """ Create I/O Processes """
        processes = []
        parent_connections = []
        
        for i in inputData:
            pConnection, cConnection = Pipe()
            p = Process(name="I{}".format(len(processes)), target=self.inPFunc, args=(i, mpData, cConnection))
            processes.append(p)
            p.start()
            parent_connections.append(pConnection)
        
        
        
        for o in outputData:
            pConnection, cConnection = Pipe()
            p = Process(name="O{}".format(len(processes)-numInputTracks), target=self.outPFunc, args=(o, mpData, cConnection))
            processes += [p]
            p.start()
            parent_connections.append(pConnection)
        
        
        for p in processes:
            p.join()
            
            
    """ Input Process function """
    def inPFunc(self, track, mpData, conn):
        print(current_process().name)
        num = 0
        for i in range(0, 1000000):
            num += i*i
            
        print(num)
        print(current_process().name, "done")
        
        
    """ Output Process function """
    def outPFunc(self, track, mpData, conn):
        print(current_process().name)
        num = 0
        for i in range(0, 1000000):
            num += i*i
            
        print(num)
        print(current_process().name, "done")