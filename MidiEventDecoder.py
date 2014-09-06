from MidiParser import MidiParser

#decodes data from the MidiParser into data easier to work with in MidiData
#(will decode each piece of data from midiParser into an event,
#including header chunk pieces)
class MidiEventDecoder:
    def __init__(self, midiFilename):
        self.midiParser = MidiParser(midiFilename)
        return
    def hasMoreEvents(self):
        return self.midiParser.hasMoreData
    #be sure to call this once before calling nextEvent
    def headerData(self):
        return HeaderData(self, self.midiParser.readNextData(),
                          self.midiParser.readNextData())
    #returns a MidiEvent
    def nextEvent(self):
        return MidiEvent(self.midiParser.readNextData())

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
    def __init__(midiData):
        #midi event data
        self.noteNumber = None
        self.velocity = None
        self.controllerNumber = None
        self.programNumber = None
        self.aftertouchValue= None
        self.pitchValue = None
        return

#contains data from the header chunk
class HeaderData:
    def __init__(self, headerChunkID, headerData):
        self.ticksPerBeat = None
        self.framesPerSecond = None
        self.formatType = headerData
        return
    def __str__(self):
        return "Format type: " + str(self.formatType)
