'''
Created on Sep 30, 2015

@author: eric
'''

from optparse import OptionParser

class ArgsParser(object):
    '''
    Parse arguments for Python Lights Client
    '''

    def __init__(self):
        '''
        Initialize argument parser
        Initialize arguments
        '''
        global parser
        parser = OptionParser()
        parser.add_option("-S", "--setlist", action="store", dest="setlist",
                          help="Play a setlist", metavar="FILE")
        parser.add_option("-s", "--song", dest="song",
                          help="Play a song", metavar="FILE")
        
    def parse(self):
        options, args = parser.parse_args()
        
        """ Parse arguments """
        if options.song:
            return 0, options.song
        elif options.setlist:
            return 1, options.setlist
        else:
            return None