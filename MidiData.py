from MidiParser import MidiParser

class MidiData:
    def __init__(self, midiFilename):
        self.midiParser = MidiParser(midiFilename)
        self.notes = list()
        noteMap = dict()
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
        return
