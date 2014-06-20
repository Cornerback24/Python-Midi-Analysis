from MidiParser import MidiParser
from Util import Util

midiParser = MidiParser("testMidiFile.mid")

'''
a = (midiParser.readNextData() + midiParser.readNextData()
    + midiParser.readNextData() + midiParser.readNextData())
print(str(a))
while midiParser.hasMoreData():
    print(midiParser.readNextData())
'''
print("Header def and size: " + str(midiParser.readNextData()))
headerBody = midiParser.readNextData()
print("Body of header chunk: " + str(headerBody) + " number of tracks: " + 
       str(int.from_bytes(headerBody[2:4], "big")))
while midiParser.hasMoreData():
#for i in range(2):
    trackDef = midiParser.readNextData()
    print("Track def and size: " + str(trackDef) + " track size: "
        + str(int.from_bytes(trackDef[4:8], "big")))
    while midiParser.bytesLeftInChunk > 0:
        print(str(midiParser.readNextData()) + " size left: " +
            str(midiParser.bytesLeftInChunk))
    print()

'''
trackDef = midiParser.readNextData()
print("Track def and size: " + str(trackDef) + " track size: "
    + str(int.from_bytes(trackDef[4:8], "big")))
for i in range(65):
    print(str(midiParser.readNextData()) + " size left: " +
        str(midiParser.bytesLeftInChunk))
'''
