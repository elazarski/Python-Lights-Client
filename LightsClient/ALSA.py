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
    This method creates I/O threads """
    def playSong(self, data):
        data[0][0].show('text')
        