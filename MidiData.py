from MidiEventDecoder import MidiEventDecoder
from TrackData import TrackData
from TrackData import TempoChanges

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
        self.tempoChanges = TempoChanges()
        self.trackZeroEvents = []
        self.tracks = []

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
                self.tempoChanges.addTempoChange(deltaTimeTotal, event)
                

        #read in each track
        tracknum = 0 #used to create temprary track names
        while self.eventDecoder.hasMoreEvents():
            tracknum = tracknum + 1
            trackName = "Track" + str(tracknum)
            #should be a track header
            event = self.eventDecoder.nextEvent()
            trackData = TrackData(trackName)
            while not(event.eventClass == "Meta"
                and event.eventType == "EndOfTrack"):
                event = self.eventDecoder.nextEvent()
                trackData.addEvent(event)
            self.tracks.append(trackData)
            
#this line just for testing
MidiData("testMidiFile.mid")


        
