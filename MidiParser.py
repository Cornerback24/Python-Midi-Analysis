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
        self.bytesLeftInChunk = 0
        self.nextByte = self.midiFile.read(1)
        self.state = "chunkStart" #chunkStart, inHeader, inTrack
        return
    def hasMoreData(self):
        return self.nextByte != b''
    def readNextData(self):
        if self.nextByte == b'':
            print("Tried to read end of file!")
            return self.nextByte
        if self.state == "chunkStart":
            returnVal = self.readNextBytes(8)
            if returnVal[0:4] == b'MThd':
                self.state = "inHeader"
            if returnVal[0:4] == b'MTrk':
                self.state = "inTrack"
            self.bytesLeftInChunk = int.from_bytes(returnVal[4:8], "big")
            return returnVal
        if self.state == "inHeader":
            return self.readNextBytes(self.bytesLeftInChunk)
        if self.state == "inTrack":
            return self.readEvent()
        return self.readNextByte()

    def readEvent(self):
        return "event"
    
    def readNextByte(self):
        if self.bytesLeftInChunk > 0:
            self.bytesLeftInChunk = self.bytesLeftInChunk - 1
        if self.bytesLeftInChunk == 0:
            self.state = "chunkStart"
        returnVal = self.nextByte
        self.nextByte = self.midiFile.read(1)
        return returnVal
    def readNextBytes(self, numBytes):
        returnBytes = b''   
        for i in range(numBytes):
            returnBytes = returnBytes + self.readNextByte()
        return returnBytes
    def close(self):
        self.midiFile.close()
        
