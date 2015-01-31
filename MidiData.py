from MidiEventDecoder import MidiEventDecoder

#contains the finalized data after anylisis
class MidiData:
    def __init__(self, midiFilename):
        self.eventDecoder = MidiEventDecoder(midiFilename)
        headerData = self.eventDecoder.headerData()
        #variables
        self.format = headerData.formatType
        self.numTracks = headerData.numTracks
        self.isTicksPerBeat = False
        if headerData.ticksPerBeat == None:
            self.isTicksPerBeat = False
            self.ticksPerSecond = (headerData.framesPerSecond *
                                   headerData.ticksPerFrame)
        else:
            self.isTicksPerBeat = True
            self.ticksPerBeat = headerData.ticksPerBeat

        #maps running total of delta times to microsecondsPerQuarter
        self.tempoChanges = {}
        self.trackZeroEvents = []

        deltaTimeTotal = 0    
        #should be a track header
        event = self.eventDecoder.nextEvent()

        #read in trackZeroEvents
        while not(event.eventClass == "Meta"
                and event.eventType == "EndOfTrack"):
            event = self.eventDecoder.nextEvent()
            deltaTimeTotal = deltaTimeTotal + event.deltaTime
            self.trackZeroEvents.append(event)
            if (event.eventClass == "Meta" and
                event.eventType == "SetTempo"):
                self.tempoChanges[deltaTimeTotal] = event.usPerQuarter
                

        while self.eventDecoder.hasMoreEvents():
            #should be a track header
            event = self.eventDecoder.nextEvent()
            while not(event.eventClass == "Meta"
                and event.eventType == "EndOfTrack"):
                event = self.eventDecoder.nextEvent()
            
#this line just for testing
MidiData("testMidiFile.mid")
        
