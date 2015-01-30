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
        self.eventType = None
        self.dataLength = midiData[2:3]
        i = 2
        while Util.msbIsOne(midiData[i:i+1]):
            self.dataLength = self.dataLength + midiData[i+1:i+2]
            i = i+1
        i = i+1
        self.data = midiData[i:]
        #coverts bytes to a string
        self.data = str(self.data)[2:len(str(self.data))-1]
        if midiData[1] in Util.MetaEventDict:
            self.eventType = Util.MetaEventDict[midiData[1]]
        if self.eventType == "SequenceNumber":
            self.sequenceNumber = int.from_bytes(midiData[3:], "big")
        if self.eventType == "SetTempo":
            #micro seconds per quarter note
            self.usPerQuarter = int.from_bytes(midiData[4:], "big")
    def __str__(self):
        s = ("Meta " + str(self.midiData) + " deltaTime: "
                + str(self.deltaTime) + " eventType: " + self.eventType)
        if self.eventType == "SetTempo":
            s = s + "\n\t usPerQuarter: " + str(self.usPerQuarter)
        return s

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
        self.eventType = None
        self.noteNumber = None
        self.velocity = None
        self.aftertouchValue = None
        self.controllerNumber = None
        self.controllerValue = None
        self.programNumber = None #use for ProgramChange
        self.pitchValue = None #used for PitchBend
        #read eventType and channel
        if Util.msbIsOne(midiData):
            self.runningStatus = False
            if midiData[0] & int('f0',16) in Util.ChannelEventDict:
                self.eventType = Util.ChannelEventDict[midiData[0] & int('f0',16)]
                self.channel = midiData[0] & int('0f',16)
                ChannelEvent.prevEventData = (self.eventType, self.channel)
        else:
            self.eventType, self.channel = ChannelEvent.prevEventData
            self.runningStatus = True
        #set applicable values
        if self.runningStatus:
            #so that the indicies of the data are correct
            midiData = b'\x00' + midiData
        if (self.eventType == "NoteOff" or self.eventType == "NoteOn"):
            self.noteNumber = midiData[1]
            self.velocity = midiData[2]
        if self.eventType == "NoteAfterTouch":
            self.noteNumber = midiData[1]
            self.aftertouchValue = midiData[2]
        if self.eventType == "Controller":
            self.controllerNumber = midiData[1]
            self.controllerValue = midiData[2]
        if self.eventType == "ProgramChange":
            self.programNumber = midiData[1]
        if self.eventType == "ChannelAftertouch":
            self.aftertouchValue = midiData[1]
        if self.eventType == "PitchBend":
            #NOTE: this relies on Util.varLenVal not actually caring if
            #the format is an actual valid varaible length value
            #(and thus completly ignoring the msb of every byte)
            self.pitchValue = Util.varLenVal(midiData[2:3] + midiData[1:2])
            
    def __str__(self):
        if self.eventType == "Controller":
            return ("Channel " + str(self.midiData) + " deltaTime: "
            + str(self.deltaTime) + " (Controller)")
        return ("Channel " + str(self.midiData) + " deltaTime: "
                + str(self.deltaTime) + " eventType: " + self.eventType +
                " channel: " + str(self.channel) + "\n\t" +
                "runningStatus: " + str(self.runningStatus) +
                " noteNumber: " + str(self.noteNumber) +
                " velocity: " + str(self.velocity) + "\n\t" +
                "aftertouchValue: " + str(self.aftertouchValue) +
                " controllerNumber: " + str(self.controllerNumber) +
                " controllerValue: " + str(self.controllerValue) + "\n\t" +
                "programNumber: " + str(self.programNumber))

    #used for running status
    prevEventData = ()



