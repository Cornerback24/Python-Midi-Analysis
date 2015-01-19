from MidiParser import MidiParser
from Util import Util

#decodes data from the MidiParser into data easier to work with in MidiData
#(will decode each piece of data from midiParser into an event,
#including header chunk pieces)
class MidiEventDecoder:
    def __init__(self, midiFilename):
        self.midiParser = MidiParser(midiFilename)
        return
    def hasMoreEvents(self):
        return self.midiParser.hasMoreData()
    #be sure to call this once before calling nextEvent
    def headerData(self):
        return HeaderData(self.midiParser.readNextData(),
                          self.midiParser.readNextData())
    #returns a MidiEvent
    def nextEvent(self):
        return MidiEvent(self.midiParser.readNextData())
    def close(self):
        self.midiParser.close()

#contains all data about and event
#values not used will be set to None
#(it is MidiData's responsibilty to know what data is valid)
class MidiEvent:
    #data contained:
    #eventType
    #   chunkID
    #   (midi): Note off, Note on, Note aftertouch, Controller, Program Change
    #   Channel Aftertouch, Pitch Bend
    #   meta
    #   sysEx
    def __init__(self, midiData):
        #midi event data
        self.midiData = midiData
        self.deltaTime = None
        self.noteNumber = None
        self.velocity = None
        self.controllerNumber = None
        self.programNumber = None
        self.aftertouchValue= None
        self.pitchValue = None
        #analyze data
        tempData = midiData
        temp = 0
        while Util.msbIsOne(tempData[temp:]):
            temp = temp+1
        deltaTime = tempData[:temp]
        tempData = tempData[temp:]
        self.deltaTime = Util.varLenVal(deltaTime)
        
        return
    def __str__(self):
        return ("MidiEvent " + str(self.midiData) +
                " deltaTime: " + str(self.deltaTime))

#contains data from the header chunk
class HeaderData:
    def __init__(self, headerChunkID, headerData):
        self.ticksPerBeat = None
        self.framesPerSecond = None
        self.ticksPerFrame = None
        self.formatType = int.from_bytes(headerData[0:2], "big")
        self.numTracks = int.from_bytes(headerData[2:4], "big")
        timeDivision = headerData[4:6]
        if Util.msbIsOne(headerData): #frames per second
            self.framesPerSecond = timeDivision[0] & int('7f', 16)
            self.tickesPerFrame = int.from_bytes(timeDivision[1:2], "big")
        else: #ticks per beat
            self.ticksPerBeat = int.from_bytes(timeDivision, "big")
        return
    def __str__(self):
        s = ("Format type: " + str(self.formatType)
                + " Number of tracks: " + str(self.numTracks))
        if self.ticksPerBeat != None:
            s = s + "\nTicks per Beat: " + str(self.ticksPerBeat)
        return s
