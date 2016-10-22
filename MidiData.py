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
        tempoChanges = TempoChanges()
        self.trackZeroEvents = []
        self.tracks = []

        deltaTimeTotal = 0
        self.msPerBeat = 500 #default 120 bpm
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
                tempoChanges.addTempoChange(deltaTimeTotal, event)
                

        #read in each track
        tracknum = 0 #used to create temporary track names
        while self.eventDecoder.hasMoreEvents():
            tracknum = tracknum + 1
            trackName = "Track" + str(tracknum)
            #should be a track header
            event = self.eventDecoder.nextEvent()
            trackData = TrackData(trackName)
            #set up tempoChanges
            tempoChanges.reset()
            deltaTimeTotal = 0
            nextTotal = 0
            msTotal = 0 #current time in ms
            while (tempoChanges.hasMore() and
                   tempoChanges.deltaTimeTotal() == 0):
                self.msPerBeat = tempoChanges.usPerQuarter()*.001
                tempoChanges.findNext()
            #add events
            while not(event.eventClass == "Meta"
                and event.eventType == "EndOfTrack"):
                event = self.eventDecoder.nextEvent()
                nextTotal = deltaTimeTotal + event.deltaTime
                #calcaute absolute start time for event in ms
                if self.isTicksPerBeat:
                    while (tempoChanges.hasMore() and
                           nextTotal > tempoChanges.deltaTimeTotal()):
                        msTotal = msTotal + ((tempoChanges.deltaTimeTotal() -
                                     deltaTimeTotal)*self.msPerBeat/self.ticksPerBeat)
                        deltaTimeTotal = (tempoChanges.deltaTimeTotal() -
                                     deltaTimeTotal) + deltaTimeTotal
                        tempoChanges.findNext()
                        self.msPerBeat = tempoChanges.usPerQuarter()*.001
                    msTotal = (msTotal +
                           ((nextTotal-deltaTimeTotal)*self.msPerBeat/self.ticksPerBeat))
                else:
                    msTotal = (event.deltaTime/self.ticksPerSecond)*.001
                #add event to trackData
                deltaTimeTotal = nextTotal
                event.setStartTime(msTotal)
                trackData.addEvent(event)
            self.tracks.append(trackData)
#this line just for testing
            ''''
midiData = MidiData("testMidiFile.mid")
for x in midiData.trackZeroEvents:
    print(x)
for y in midiData.tracks:
    print("\n\n----------------------")
    for x in y.events:
        print(x)
'''
        
