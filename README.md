Python-midi-analysis
====================
The idea here is to decode midi files into objects that are easy to extract data from, primary by making tracks into objects that contains notes, which are objects themselves. 
This works with with type one midi and type zero midi files. For type zero midi files, a single track is creating containing all notes.

(This isn't meant to create or manipulate midi files; it is just to get data from them.)

At this point, this script should be able to take a format one midi file that has one channel per track,
and create Notes with start and stop times.

Start by creating a MidiData object with the path to the midi file (ex midiData = MidiData("testMidiFile.mid")). This will parse the midi file and populate the MidiData object.
By default, when note names are printed, middle c (pitch 60) will be C4. This can be changed to either C3 or C5 by passing it to the MidiData (ex midiData = MidiData("testMidiFile.mid", "C3"))
The number of tracks created can be checked by calling midiData.getNumTracks().

The MidiData contains TrackData objects for each track in the midi file. A TrackData can be retrieved by calling midiData.getTrack(index).
TrackData objects have a list of notes in their notes field (ex trackData.notes) sorted by start time.  Each Note has a startTime and endTime field, defined in 
milliseconds (as well as a length() function that returns the length in milliseconds).  Each Note also has a pitch
field in the range 0 - 127.  trackData.name contains the name of the track, which may be the name of the instrument on that track.  
trackData.events contains the midi events in the track, and each event has a startTime field in milliseconds. Midi events are defined in
MidiEvents.py.
TrackData, MidiData, and Note may need to imported.

Structure (only intended output values listed):  
MidiData: contains all data for a midi file (created by calling MidiData("midi_file.mid") where "midi_file.mid" is the path to the midi file)  
  * getNumTracks(): number of tracks in the midi file
  * tracks: list of TrackData (one TrackData for each track in the file)
  * getTrack(index): returns the TrackData with the given index (ex. data.getTrack(1) to get the data for the second track)

TrackData: contains all the data for a single track  
  * notes: list of Note (one Note for each note in the track)
  * channel: channel
  * events: list of MidiEvents that make up the track (see MidiEvents.py for definitions)
  * name: name of the track

Note:
  * pitch: note number  
  * channel: the midi channel
  * startTime: start time in ms
  * startTimeTicks: start time in ticks
  * endTime: end time in ms
  * endTimeTicks: end time in ticks
  * velocity: velocity
  * releaseVelocity: release velocity
  * length(): length of the note in ms
