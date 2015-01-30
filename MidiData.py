from MidiParser import MidiParser

#contains the finalized data after anylisis
class MidiData:
    def __init__(self, midiFilename):
        #variables
        self.format = 0
        self.numTracks = 0
