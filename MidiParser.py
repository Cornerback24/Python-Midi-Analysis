#returns elements of a midi file (in raw form)
#elements returned:
    #Chuck ID along with chunk size
    #The rest of the header chunk
    #Midi Channel events, including delta time
    #Meta Event
    #System Exclusive Event

class MidiParser:
    def __init__(self, midiFilename):
        self.midiFile = open(midiFilename, "rb")
        return
    def __hasMoreData(self):
        return True
    def __readNextData(self):
        return
    def close(self):
        self.midiFile.close()
