Python-midi-analysis
====================
The idea here is to decode midi files into objects that are easy to extract data from, primary by making tracks into objects that contains notes, which are objects themselves. 
This will probably only work with type one midi files which are organized so that each track contains data for a separate instrument.

(This isn't meant to create or manipulate midi files; it is just to get data from them.)
Current work in progress is generating note objects from the midi file, with start and stop times.

At this point, this script should be able to take a format one midi file that has one channel per track,
and create Notes with start and stop times.  To do this, create a MidiData (ex midiData = MidiData("testMidiFile.mid")).  
All the data should be initialized by the constructor.  The number of tracks created can be checked by calling midiData.getNumTracks().

A TrackData can be retrieved by calling midiData.getTrack(index).  If trackData = midiData.getTrack(index) then
trackData.notes is a list containing the notes for that track, sorted by start time.  Each Note has a startTime and endTime field, defined in 
milliseconds (as well as a length() function that returns the length in milliseconds).  Each Note also has a pitch
field in the range 0 - 127.  trackData.name contains the name of the track, which may be the name of the instrument on that track.  
trackData.events contains the midi events in the track, and each event has a startTime field in milliseconds. Midi events are defined in
MidiEvents.py.
TrackData, MidiData, and Note may need to imported.
