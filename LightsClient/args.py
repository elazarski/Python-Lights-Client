'''
Created on Sep 30, 2015

@author: eric
'''

from optparse import OptionParser

class ArgsParser(object):
    '''
    Parse arguments for Python Lights Client
    '''

    global parser

    def __init__(self):
        '''
        Initialize argument parser
        Initialize arguments
        '''
        parser = OptionParser()
        parser.add_option("-S", "--setlist", dest="setlist", help="Play a setlist", metavar="FILE")
        parser.add_option("-s", "--song", dest="song", help="Play a song", metavar="FILE")
        
    def parse(self):
        options, args = parser.parse_args()
        print(options, args)