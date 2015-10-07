'''
Created on Sep 28, 2015

@author: eric
'''
from alsamidi import *  # @UnusedWildImport
from multiprocessing import Process, current_process, Pipe  # @UnresolvedImport
from lightsclient.inputprocess import InputProcess
from lightsclient.outputprocess import OutputProcess
from lightsclient.forwardprocess import ForwardProcess

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
        alsaseq.client("Lights Client", 2, 2, False)
        alsaseq.start()
        print("ALSA Sequencer started")
        
        
    # Close ALSA  Sequencer
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
        
        # Create I/O Processes
        numInputTracks = len(inputData)
        numOutputTracks = len(outputData)
        
        processes = []
        inputConnections = []
        outputConnections = []
        
        # There will always only be one of these
        f = ForwardProcess()
        
        # Create input processes
        for i in inputData:
            
            # Create Pipes
            childConnection, parentConnection = Pipe(False)
            processInConnection, processOutConnection = Pipe(False)
            
            # Create and start Process
            p = Process(name="i{}".format(len(processes)),
                        target=InputProcess().process,
                        args=(i.notes, mpData.notes, childConnection, processOutConnection))
            p.start()
            
            # Add data to appropriate lists
            processes.append(p)
            inputConnections.append(parentConnection)
            f.addInPipe(processInConnection)
        
        
        # Create output processes
        for o in outputData:
            
            # Create Pipes
            childConnection, parentConnection = Pipe(False)
            processInConnection, processOutConnection = Pipe(False)
            
            # Create and start process
            p = Process(name="o{}".format(len(processes) - numInputTracks),
                        target=OutputProcess(numInputTracks).process,
                        args=(o.notes, mpData.notes, processInConnection, parentConnection))
            p.start()
            
            # add data to appropriate lists
            processes.append(p)
            outputConnections.append(childConnection)
            f.addOutPipe(processOutConnection)
            
            
        # Create and start forward thread
        processes.append(Process(name="f",
                                 target=f.process,
                                 args=()))
        
        processes[len(processes)-1].start()
    
        
        # Main loop
        while True:
            ev = alsaseq.input()
            
            # This checks if noteon
            if ev[0] == 6:
                
                # Checks if key in or control in
                if ev[6][1] == 0:
                    
                    # Make sure channel is expected, otherwise ignore
                    if ev[7][0] <= numInputTracks:
                        inputConnections[ev[7][0]].send(ev[7][1])
                        
                else:
                    # control in 
                    print("Control recieved event:", ev)
                    
            
            for o in outputConnections:
                if o.poll(timeout=0.01):
                    e = o.recv()
                    print("Main process recieved note", e)
                    
                       
        # Join processes at the end
        for p in processes:
            p.join()
            