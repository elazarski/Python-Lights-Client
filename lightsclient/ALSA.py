'''
Created on Sep 28, 2015

@author: eric
'''
from alsamidi import *  # @UnusedWildImport
from multiprocessing import Process, current_process, Pipe  # @UnresolvedImport
from music21 import note, chord
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
        numInputTracks = len(inputData)
        numOutputTracks = len(outputData)
        
        processes = []
        inputConnections = []
        outputConnections = []
        
        for i in inputData:
            pConnection, cConnection = Pipe()
            p = Process(name="I{}".format(len(processes)), target=self.inPFunc, args=(i.notes, mpData.notes, cConnection))
            processes.append(p)
            p.start()
            inputConnections.append(pConnection)
           
        
        for o in outputData:
            pConnection, cConnection = Pipe()
            p = Process(name="O{}".format(len(processes)-numInputTracks), target=self.outPFunc, args=(o.notes, mpData.notes, cConnection))
            processes += [p]
            p.start()
            outputConnections.append(pConnection)
        
        
        """ Main loop """
        while True:
            ev = alsaseq.input()
            
            """ This checks if noteon """
            if ev[0] == 6:
                
                """ Checks if key in or control in """
                if ev[6][1] == 0:
                    
                    """ Make sure channel is expected, otherwise ignore """
                    if ev[7][0] <= numInputTracks:
                        inputConnections[ev[7][0]].send(ev[7][1])
                        
                else:
                    """ control in """ 
                    print("Control recieved event:", ev)
        
        
        for p in processes:
            p.join()
            
            
    """ Input Process function """
    def inPFunc(self, track, mpData, conn):
        print(current_process().name, "started")
        
        """ Declare necessary variables """
        currentNote = 0
        currentPart = 0
        currentMeasure = 0
        songDone = False
        
        """ Main loop """
        while not songDone:
            
            """ get data from main process """
            ev = conn.recv()
            
        
        print(current_process().name, "done")
        
        
    """ Output Process function """
    def outPFunc(self, track, mpData, conn):
        print(current_process().name, "started")
        
        print(current_process().name, "done")