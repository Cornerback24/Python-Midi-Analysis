from MidiParser import MidiParser

midiParser = MidiParser("testMidiFile.mid")
a = (midiParser.readNextData() + midiParser.readNextData()
    + midiParser.readNextData() + midiParser.readNextData())
print(str(a))
while midiParser.hasMoreData():
    print(midiParser.readNextData())
midiParser.close()