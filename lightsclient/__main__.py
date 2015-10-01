import sys
from ctypes import cdll, byref, create_string_buffer
from lightsclient.ALSA import ALSA
from lightsclient.args import ArgsParser
from lightsclient.interface import Interface

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
    args = argsParser.parse()
    
    print("Starting")
    sequencer = ALSA()
    
    if args:
        num, str = args
        playWithArgs(num, str, sequencer)
    else:
        playNoArgs(sequencer)
    
    """ Close ALSA Sequencer """
    sequencer.close()
    
    sys.exit(0)
    
    """ Continues based on arguments """
def playWithArgs(num, str, sequencer):
    
    """ Initialize interface """
    i = Interface()
    
    """ Check arguments """
    if num == 0:
        """ song """
        songPath = i.getInput(str)
        data = i.parseFiles(songPath)
        sequencer.playSong(data)
    elif num == 1:
        """ setlist """
        songs = i.parseSetlist(str)
        
        """ Load and play each song in songs """
        for song in songs:
            songPath = i.getInput(song) 
            data = i.parseFiles(songPath)
            sequencer.playSong(data)
        
    
    """ No arguments """
def playNoArgs(sequencer):
 
    """ Initialize interface """
    i = Interface()
    
    """ Get user input """
    songPath = i.getInput()
    
    """ parse data """
    data = i.parseFiles(songPath)
    
    """ play the song """
    sequencer.playSong(data)
    
    
if __name__ == "__main__":
    main()