import sys
from ctypes import cdll, byref, create_string_buffer
from LightsClient.interface import Interface
from LightsClient.ALSA import ALSA
from LightsClient.args import ArgsParser

def main(args=None):
    
    """ Set process name """
    name = "Lights Client"
    length = len(name)
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(length+1)
    buff.value = bytes(name, 'utf8')
    libc.prctl(15, byref(buff), 0, 0, 0)
    
    """ Parse arguments """
    argsParser = ArgsParser()
    argsParser.parse()
        
    print("Starting")
    
    sequencer = ALSA()
    
    i = Interface()
    songPath = i.getInput()
    data = i.parseFiles(songPath)
    
    sequencer.playSong(data)
    
    """ Close ALSA Sequencer """
    sequencer.close()
    
    sys.exit(0)
    
if __name__ == "__main__":
    main()