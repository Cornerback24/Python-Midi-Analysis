from MidiParser import MidiParser


midiParser = MidiParser("testMidiFile.mid")

'''
a = (midiParser.readNextData() + midiParser.readNextData()
    + midiParser.readNextData() + midiParser.readNextData())
print(str(a))
while midiParser.hasMoreData():
    print(midiParser.readNextData())
'''
print("Header def and size: " + str(midiParser.readNextData()))
print("Body of header chunk: " + str(midiParser.readNextData()))
print("Track def and size: " + str(midiParser.readNextData()))
print(str(midiParser.readNextData()))
midiParser.close()
