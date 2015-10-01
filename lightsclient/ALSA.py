'''
Created on Sep 28, 2015

@author: eric
'''
from alsamidi import *
from threading import Thread, Condition
from music21 import *
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
        
        threads = []
        inputConditions = []
        outputConditions = []
        
        """ Start input Threads """
        for i in inputData:
            t = Thread(target=self.inThreadFunc, args=(inputData, mpData))
            threads += [t]
            t.start()
            
        """ Start output threads """
        for o in outputData:
            t = Thread(target=self.outThreadFunc, args=(o, mpData))
            threads += [t]
            t.start()
            
        """ Join threads in the end """
        for t in threads:
            t.join()       
            
        
    """ Input Thread function """
    def inThreadFunc(self, track, mpData):
        print("input thread")
        
        
        
    """ Output Thread function """
    def outThreadFunc(self, track, mpData):
        print("output thread")