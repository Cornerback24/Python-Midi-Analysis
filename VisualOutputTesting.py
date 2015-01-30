from MidiParser import MidiParser
from MidiData import MidiData
from Util import Util
from MidiEventDecoder import MidiEventDecoder
from MidiEventDecoder import MidiEvent
from MidiEventDecoder import HeaderData

midi_file = "one_note.mid" #testMidiFile.mid
print(midi_file)
midiParser = MidiParser(midi_file)

def printHex(_bytes):
    temp = ""
    for i in range (len(_bytes)):
        temp = temp + " " + str(hex(_bytes[i]))
    print(temp)

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
midiParser.close()
b = b'\x81\x7f'
b = bytearray(b)
print(Util.varLenVal(b))

print("------------")
midiData = MidiData(midi_file)

print("--------------")
#testing MidiEventDecoder
eventDecoder = MidiEventDecoder(midi_file) #testMidiFile.mid
print(eventDecoder.headerData())
eventData = eventDecoder.nextEvent().midiData
#print(int.from_bytes(eventData[0:1],"big"))
#print(Util.msbIsOne(eventData))
#print(type(eventData))
while eventDecoder.hasMoreEvents():
    print(eventDecoder.nextEvent())
eventDecoder.close()
