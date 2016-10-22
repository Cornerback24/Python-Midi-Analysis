from MidiParser import MidiParser
from MidiEvents import *
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
        data = HeaderData()
        data.setFromBytes(self.midiParser.readNextData(),
                          self.midiParser.readNextData())
        return data
    #returns a MidiEvent
    def nextEvent(self):
        return self.midiEvent(self.midiParser.readNextData())
    #creates a MidiEvent from the midiData
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
        midiData = tempData[temp:]
        #Meta Event
        if midiData[0:1] == b'\xff':
            return MetaEvent(Util.varLenVal(deltaTime), midiData)
        #System Event
        if midiData[0:1] == b'\xf0' or midiData[0:1] == b'\xf7':
                return SystemEvemt(Util.varLenVal(deltaTime), midiData)
        return ChannelEvent(Util.varLenVal(deltaTime), midiData)
    def close(self):
        self.midiParser.close()






