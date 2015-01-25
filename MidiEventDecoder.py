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
        return self.midiEvent(self.midiParser.readNextData())
    def midiEvent(self, midiData):
        #check if TrackHeader
        if midiData[0:4] == b'MTrk':
            return TrackHeader(midiData)#MidiEvent(b'\x00', midiData)
        #find deltaTime
        tempData = midiData
        temp = 0
        while Util.msbIsOne(tempData[temp:]):
            temp = temp+1
        temp = temp + 1
        deltaTime = tempData[:temp]
        tempData = tempData[temp:]
        if tempData[0:1] == b'\xff':
                return MetaEvent(deltaTime, tempData)
        if midiData[0:1] == b'\xf0' or midiData[0:1] == b'\xf7':
                return SystemEvemt(deltaTime, tempData)
        return ChannelEvent(deltaTime, tempData)
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
    def __init__(self, deltaTime, midiData):
        #midi event data
        self.midiData = midiData
        self.eventClass = "Channel" #Channel, Meta, System, #TrackHeader
        self.eventType = None
        self.deltaTime = Util.varLenVal(deltaTime)
        self.noteNumber = None
        self.velocity = None
        self.controllerNumber = None
        self.programNumber = None
        self.aftertouchValue= None
        self.pitchValue = None
        return
    
    def __str__(self):
        return (self.eventClass + " " + str(self.midiData) +
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
    
class TrackHeader(MidiEvent):
    def __init__(self, midiData):
        self.midiData = midiData
        self.eventClass = "TrackHeader"
    def __str__(self):
        return "Track Header " + str(self.midiData)

class MetaEvent(MidiEvent):
    def __init__(self, deltaTime, midiData):
        self.eventClass = "Meta"
        self.midiData = midiData
        self.deltaTime = Util.varLenVal(deltaTime)
    def __str__(self):
        return ("Meta " + str(self.midiData) + " deltaTime: "
                + str(self.deltaTime))

class SystemEvent(MidiEvent):
    def __init__(self, deltaTime, midiData):
        self.eventClass = "System"
        self.midiData = midiData
        self.deltaTime = Util.varLenVal(deltaTime)
    def __str__(self):
        return ("System " + str(self.midiData) + " deltaTime: "
                + str(self.deltaTime))

class ChannelEvent(MidiEvent):
    def __init__(self, deltaTime, midiData):
        self.midiData = midiData
        self.eventClass = "Channel"
        self.deltaTime = Util.varLenVal(deltaTime)
        if Util.msbIsOne(midiData):
            self.runningStatus = False
            if midiData[0] & int('f0',16) in Util.ChannelEventDict:
                self.eventType = Util.ChannelEventDict[midiData[0] & int('f0',16)]
                self.channel = midiData[0] & int('0f',16)
                ChannelEvent.prevEventData = (self.eventType, self.channel)
            else:
                self.eventType = "Unknown"
        else:
            self.eventType, self.channel = ChannelEvent.prevEventData
            self.runningStatus = True
    def __str__(self):
        return ("Channel " + str(self.midiData) + " deltaTime: "
                + str(self.deltaTime) + " eventType: " + self.eventType +
                " channel: " + str(self.channel) + "\n\t" +
                "runningStatus: " + str(self.runningStatus))

    #used for running status
    prevEventData = ()



