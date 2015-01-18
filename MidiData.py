from MidiParser import MidiParser

#contains the finalized data after anylisis
class MidiData:
    def __init__(self, midiFilename):
        #variables
        self.midiParser = MidiParser(midiFilename)
        self.notes = list()
        noteMap = dict()
        self.format = 0
        self.numTracks = 0
        
        #read in header chunk
        headerChunkDef = self.midiParser.readNextData()
        if headerChunkDef[0:4] != b'MThd':
            raise Exception("expected MThd header chuck ID",
                            headerChunkDef[0:4])
        headerChunkSize = int.from_bytes(headerChunkDef[4:8], "big")
        if(headerChunkSize != 6):
            raise Exception("expected header chunk size of 6", headerChunkSize)
        print(headerChunkDef[0:4])
        print(headerChunkSize)
        headerChunk = self.midiParser.readNextData()
        self.format = int.from_bytes(headerChunk[0:2], "big")
        self.numTracks = int.from_bytes(headerChunk[2:4], "big")
        print(self.format)
        print(self.numTracks)
        print(headerChunk[4:5])

        #read in track chunks
        while self.midiParser.hasMoreData():
            trackChunkDef = self.midiParser.readNextData()
            print(trackChunkDef)
            while self.midiParser.chunkHasMoreData():            
                self.midiParser.readNextData()
        return
