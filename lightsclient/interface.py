'''
Created on Sep 24, 2015

@author: eric
'''

from os.path import expanduser, isdir, exists
from xml.dom import minidom

class Interface(object):
    '''
    User input class
    use getInput to get user input, returns directory if required files exist
    '''


    def __init__(self):
        '''
        Empty Constructor
        '''

    """Get user input"""    
    def getInput(self, song=None):
        lightsPath = expanduser("~") + "/PA/Lights Files/"
        
        if not song == None:
            song = lightsPath + song
            """Check if correct input"""
            if isdir(song):
                    
                """Check for data.xml and gp.xml"""
                dataExists = exists(song + "data.xml")
                gpExists = exists(song + "gp.xml")
                if dataExists and gpExists:
                    return song
                
                
        """Get user input"""
        songPath = lightsPath + input('Enter title of song: ') + "/"
        
        """Check if song folder exists"""
        if not isdir(songPath):
            songExists = False
            
            """While loop, exits when user inputs song that exists"""
            while not songExists:
               
                """Get user input"""
                songPath = lightsPath + input('Enter title of song: ') + "/"
                
                """Check if correct input"""
                if isdir(songPath):
                    
                    """Check for data.xml and gp.xml"""
                    dataExists = exists(songPath + "data.xml")
                    gpExists = exists(songPath + "gp.xml")
                    
                    if dataExists and gpExists:
                        songExists = True
        
        
        """Return songPath after correct input recieved"""
        return songPath
    
    
    """Parse XML Files"""
    def parseFiles(self, songPath):
        data = songPath + "data.xml"
        gp = songPath + "gp.xml"
        
        datadoc = minidom.parse(data)
        MPtrack = datadoc.getElementsByTagName("mpTrack")
        