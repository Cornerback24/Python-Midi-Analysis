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
        self.nextByte = self.midiFile.read(1)
        return
    def hasMoreData(self):
        return self.nextByte != b''
    def readNextData(self):
        if self.nextByte == b'':
            return self.nextByte
        returnVal = self.nextByte
        self.nextByte = self.midiFile.read(1)
        return returnVal
    def close(self):
        self.midiFile.close()
