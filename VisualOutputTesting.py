from MidiParser import MidiParser
from MidiData import MidiData
from Util import Util
from MidiEventDecoder import MidiEventDecoder

midi_file = "TestMidiFile2.mid"
print(midi_file)


def print_hex(_bytes):
    temp = ""
    for i in range(len(_bytes)):
        temp = temp + " " + str(hex(_bytes[i]))
    print(temp)


def print_raw_file():
    print("-----------------raw file-----------------------")
    with open(midi_file, 'rb') as file:
        print_hex(file.read())
    file.close()
    print()
    print()


def test_midi_parser():
    midi_parser = MidiParser(midi_file)
    print("---------------Testing MidiParser--------------")
    print("Header def and size: " + str(midi_parser.read_next_data()))
    header_body = midi_parser.read_next_data()
    print("Body of header chunk: " + str(header_body) + " number of tracks: " +
          str(int.from_bytes(header_body[2:4], "big")))
    while midi_parser.has_more_data():
        track_def = midi_parser.read_next_data()
        print("Track def and size: " + str(track_def) + " track size: "
              + str(int.from_bytes(track_def[4:8], "big")))
        while midi_parser.bytes_left_in_chunk > 0:
            print(str(midi_parser.read_next_data()) + " size left: " +
                  str(midi_parser.bytes_left_in_chunk))
        print()
    midi_parser.close()


def test_event_decoder():
    print("-----Testing MidiEventDecoder---------")
    # testing MidiEventDecoder
    event_decoder = MidiEventDecoder(midi_file)  # testMidiFile.mid
    print(event_decoder.header_data())
    # event_data = event_decoder.next_event().midi_data
    # print(int.from_bytes(event_data[0:1],"big"))
    # print(Util.msb_is_one(event_data))
    # print(type(event_data))
    while event_decoder.has_more_events():
        event = event_decoder.next_event()
        print(event)
    event_decoder.close()
    print()


def test_midi_data():
    print("-----Testing MidiData---------")
    midi_data = MidiData(midi_file)
    for i in range(midi_data.get_num_tracks()):
        track = midi_data.get_track(i)
        print(track.name)
        for note in track.notes:
            print(note)
        print()
    print()
    print("Note F4 329.04s to 339.32s Channel: 11 <-- expected last note (TestMidiFile2.mid)")
    # print("Note A4 12.50s to 13.00s Channel: 1 <-- expected last note (testingrunningstatus.mid)")


# print_raw_file()
# test_midi_parser()
# test_event_decoder()
test_midi_data()
