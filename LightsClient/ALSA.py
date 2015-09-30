'''
Created on Sep 28, 2015

@author: eric
'''
from alsamidi import *

class ALSA(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        opens ALSA Sequencer
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
        
        