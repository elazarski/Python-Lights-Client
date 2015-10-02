'''
Created on Sep 28, 2015

@author: eric
'''
from alsamidi import *
from multiprocessing import process
from queue import Queue

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
        
        """ Create I/O Processes """
        processes = []
        for i in inputData:
            p = process(target=self.inPFunc, args=(i, mpData))
            processes += [p]
            p.start()
        
        for o in outputData:
            p = process(target=self.outPFunc, args=(o, mpData))
            processes += [p]
            p.start()
        
        
        for p in processes:
            p.join()
            
            
    """ Input Process function """
    def inPFunc(self, track, mpData):
        print("input process started")
        for i in range(0, 10000):
            i*i
            
        print("input process done")
        
        
    """ Output Process function """
    def outPFunc(self, track, mpData):
        print("output thread")
        for i in range(0, 10000):
            i*i
            
        print("output process done")