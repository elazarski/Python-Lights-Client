'''
Created on Sep 24, 2015

@author: eric
'''

from os.path import expanduser, isdir, exists
from xml.etree import ElementTree
from music21 import converter, repeat

class Interface(object):
    '''
    User input class
    use getInput to get user input, returns directory if required files exist
    '''


    def __init__(self):
        '''
        initializes path
        '''
        global lightsPath
        lightsPath = expanduser("~") + "/PA/Lights Files/"

    """ Get user input """    
    def getInput(self, song=None):
        songPath = lightsPath + "Songs/"
        
        if song is not None:
            song = songPath + song + "/"
            """ Check if correct input """
            if isdir(song):
                    
                """ Check for data.xml and m.mid """
                dataExists = exists(song + "data.xml")
                mExists = exists(song + "m.mid")
                if dataExists and mExists:
                    return song
                
                
        """ Get user input """
        songPath = songPath + input('Enter title of song: ') + "/"
        
        """ Check if song folder exists """
        if not isdir(songPath):
            songExists = False
            
            """ While loop, exits when user inputs song that exists """
            while not songExists:
               
                """ Get user input """
                songPath = lightsPath + input('Enter title of song: ') + "/"
                
                """ Check if correct input """
                if isdir(songPath):
                    
                    """ Check for data.xml and m.mid """
                    dataExists = exists(songPath + "data.xml")
                    mExists = exists(songPath + "m.mid")
                    
                    if dataExists and mExists:
                        songExists = True
        
        
        """ Return songPath after correct input received """
        return songPath
    
    
    """ Parse XML Files and MIDI Files """
    def parseFiles(self, songPath):
        data = songPath + "data.xml"
        m = songPath + "m.mid"
        
        MPTrack = None
        inputTracks = []
        outputTracks = []
        
        tree = ElementTree.parse(data)
        
        """ populate MPTrack, inputTracks, and outputTracks """
        for elem in tree.iterfind("mpTrack"):
            MPTrack = int(elem.text) - 1           
        
        for elem in tree.iterfind("inputTrack"):
            inputTracks.append(int(elem.text) - 1)
            
        for elem in tree.iterfind("outputTrack"):
            outputTracks.append(int(elem.text) - 1)
        
        
        """ parse m.mid """
        song = converter.parse(m)

        inputData = []
        outputData = []
        MPData = None
        
        """ Populate return lists """
        for i in range(0, len(song.parts)):
            for track in inputTracks:
                if i == track:
                    inputData.append(song.parts[i])
            for track in outputTracks:
                if i == track:
                    outputData.append(song.parts[i])
            if i == MPTrack:
                MPData = song.parts[i]

        
        """ Return data """
        return [inputData, outputData, MPData]
    
    def parseSetlist(self, setlist):
        setlistPath = lightsPath + "Setlists/"
        
        songs = []
        
        """ check just to make sure """
        if isdir(setlistPath):
            filePath = setlistPath + setlist + ".xml"
            
            if exists(filePath):
                tree = ElementTree.parse(filePath)
                for song in tree.iterfind("song"):
                    songs.append(song.text)
                
            
        """ Return data """
        return songs