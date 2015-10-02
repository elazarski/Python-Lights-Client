import sys
from lightsclient.ALSA import ALSA
from lightsclient.args import ArgsParser
from lightsclient.interface import Interface
import setproctitle

def main(args=None):
    
    """ Set process name """
    setproctitle("Lights Client")
    
    """ Parse arguments """
    argsParser = ArgsParser()
    args = argsParser.parse()
    
    print("Starting")
    sequencer = ALSA()
    
    if args:
        num, title = args
        playWithArgs(num, title, sequencer)
    else:
        playNoArgs(sequencer)
    
    """ Close ALSA Sequencer """
    sequencer.close()
    
    sys.exit(0)
    
    """ Continues based on arguments """
def playWithArgs(num, title, sequencer):
    
    """ Initialize interface """
    i = Interface()
    
    """ Check arguments """
    if num == 0:
        """ song """
        songPath = i.getInput(title)
        data = i.parseFiles(songPath)
        sequencer.playSong(data)
    elif num == 1:
        """ setlist """
        songs = i.parseSetlist(title)
        
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