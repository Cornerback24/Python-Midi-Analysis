#returns elements of a midi file (in raw form as a bytes object)
#elements returned:
    #Chuck ID along with chunk size
    #The rest of the header chunk
    #Midi Channel events, including delta time
    #Meta Event
    #System Exclusive Event
from Util import Util

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
        if self.state == "chunkStart": #return ID along with chunk size
            returnVal = self.readNextBytes(8)
            if returnVal[0:4] == b'MThd':
                self.state = "inHeader"
            if returnVal[0:4] == b'MTrk':
                self.state = "inTrack"
            self.bytesLeftInChunk = int.from_bytes(returnVal[4:8], "big")
            return returnVal
        if self.state == "inHeader": #return body of header
            return self.readNextBytes(self.bytesLeftInChunk)
        if self.state == "inTrack": #return an event
            return self.readEvent()
        print("Internal State Error!")

    def readEvent(self):
        deltaTime = self.readVariableLength()
        firstByte = self.readNextByte()
        if firstByte == b'\xff':
            return deltaTime + self.readMetaEvent(firstByte)
        elif firstByte ==  b'\xf0' or firstByte == b'\xf7':
            return deltaTime + self.readSysExEvent(firstByte)
        else:
            return deltaTime + self.readChannelEvent(firstByte)
    def readChannelEvent(self, firstByte):
        dataLength = 1
        if msbIsOne(firstByte): #not running status
            num = dataLength = 2
        return b'CHNL' + firstByte + self.readNextBytes(dataLength)
    def readMetaEvent(self, firstByte):
        metaEventType = self.readNextByte()
        metaEventLength = self.readVariableLength()
        metaEventData = self.readNextBytes(Util.varLenVal(
            metaEventLength))
        return (b'META ' + firstByte + metaEventType +
                metaEventLength + metaEventData)
    def readSysExEvent(self, firstByte):
        #TODO write this method
        dataLength = self.readVariableLength()
        return (b'SYEX' + firstByte + dataLength +
                self.readNextBytes(Util.varLenVal(dataLength)))
    
    def readNextByte(self):
        if self.bytesLeftInChunk > -500: #TODO change value
            self.bytesLeftInChunk = self.bytesLeftInChunk - 1
        if self.bytesLeftInChunk == 0:
            self.state = "chunkStart"
        returnVal = self.nextByte
        if returnVal == b'': #TODO remove print statment
            print("PAST EOF")
        #print(" " + hex((int.from_bytes(returnVal, "big"))))
        self.nextByte = self.midiFile.read(1)
        return returnVal
    def readNextBytes(self, numBytes):
        returnBytes = b''
        for i in range(numBytes):
            returnBytes = returnBytes + self.readNextByte()
        return returnBytes

    
    def readVariableLength(self):
        curByte = self.readNextByte()
        first = curByte
        returnVal = curByte
        while(msbIsOne(curByte)):
            curByte = self.readNextByte()
            returnVal = returnVal + curByte
        return returnVal
    def close(self):
        self.midiFile.close()

def msbIsOne(byte): #returns true of the msb of a single byte is 1
    return (byte[0] & int('80',16)) > 0
