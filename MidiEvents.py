from Util import Util
import math

#contains data from the header chunk
class HeaderData:
    def __init__(self):
        self.ticksPerBeat = None
        self.framesPerSecond = None
        self.ticksPerFrame = None
        self.formatType = None
        self.numTracks = None
    def __str__(self):
        s = ("Format type: " + str(self.formatType)
                + " Number of tracks: " + str(self.numTracks))
        if self.ticksPerBeat != None:
            s = s + "\nTicks per Beat: " + str(self.ticksPerBeat)
        return s
    def setFromBytes(self, headerDefByts, headerBodyBytes):
        self.formatType = int.from_bytes(headerBodyBytes[0:2], "big")
        self.numTracks = int.from_bytes(headerBodyBytes[2:4], "big")
        timeDivision = headerBodyBytes[4:6]
        if Util.msbIsOne(headerBodyBytes): #frames per second
            self.framesPerSecond = timeDivision[0] & int('7f', 16)
            self.tickesPerFrame = int.from_bytes(timeDivision[1:2], "big")
        else: #ticks per beat
            self.ticksPerBeat = int.from_bytes(timeDivision, "big")
        return
    
class TrackHeader():
    def setFromBytes(self, midiData):
        self.chunkSize = Util.intFromBytes(midiData[4:])
    def __str__(self):
        return "Track Header, Chunk Size: " + str(self.chunkSize)

#parent class for all midi events with delta time information
#deltaTime and all relavent data must be set on all midi events
#(if data is not set, __str__ will fail)
class MidiEvent:
    #set the delta time in clock ticks from the bytes representing delta time
    def setDeltaTimeFromBytes(self, deltaTimeBytes):
        self.deltaTime = Util.varLenVal(deltaTimeBytes)
    #sets the event data from the bytes (bytes should not include delta time)
    #this method is defined in every child class
    def setFromBytes(self, midiDataBytes):
        return print("Set bytes called on parent event class!")
    def __str__(self):
        return ("Midi Event" + " " +
                " deltaTime: " + str(self.deltaTime))
    def setStartTime(self, startTime): #set start time in ms
        self.startTime = startTime    

######################### Meta Events ################################################
class MetaEvent(MidiEvent):
    def setFromBytes(self, midiData):
        print("Set bytes called on parent event class!")
    def __str__(self):
        return "Meta  deltaTime: " + str(self.deltaTime)

class SequenceNumberEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.sequenceNumber = int.from_bytes(eventData, "big")
    def __str__(self):
        return (super().__str__() + ", eventType: Sequence Number" +
            "\n\t Sequence Number: " + str(self.sequenceNumber))

class TextEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.text = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Text" +
            "\n\t Text: " + str(self.text))

class CopyrightNoticeEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.copyrightNotice = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Copyright Notice" +
                "\n\t Copyright Notice: " + str(self.copyrightNotice))

class TrackNameEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.trackName = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Sequence/Track Name" +
            "\n\t Track Name: " + str(self.trackName))

class InstrumentNameEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.instrumentName = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Instrument Name" +
            "\n\t Instrument Name: " + str(self.instrumentName))

class LyricsEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.lyrics = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Lyrics" +
                "\n\t Lyrics: " + str(self.lyrics))

class MarkerEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.marker = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType:Marker" +
                "\n\t Marker: " + str(self.marker))

class CuePointEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.cuePoint = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Cue Point" +
                "\n\t Cue Point: " + str(self.cuePoint))
    
class ProgramNameEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.programName = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Program Name" +
                "\n\t Program Name: " + str(self.programName))

class DeviceNameEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.deviceName = eventData.decode()
    def __str__(self):
        return (super().__str__() + ", eventType: Device Name" +
                "\n\t Device Name: " + str(self.deviceName))

class MidiChannelPrefixEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.channel = Util.intFromBytes(eventData)
    def __str__(self):
        return (super().__str__() + ", eventType: Midi Channel Prefix"
                + "\n\t Channel: " + str(self.channel))

class EndOfTrackEvent(MetaEvent):
    def setFromBytes(self, midiData):
        #nothing to set for end of track
        return
    def __str__(self):
        return super().__str__() + ", eventType: End of Track"

class SetTempoEvent(MetaEvent):
    def setFromBytes(self, midiData):
        #tempo is in microseconds per quarter note
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        self.tempo = Util.intFromBytes(eventData)
    def __str__(self):
        return (super().__str__() + ", eventType: Set Tempo"
                + "\n\t Tempo (microseconds per quarter note): "
                    + str(self.tempo))

class SMPTEOffsetEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        frameRateIdentifier = (eventData[0] & int('e0',16)) / 64
        #frame rate in fps
        self.frameRate = None
        self.dropFrame = False
        if (frameRateIdentifier == 0):
            self.frameRate = 24
        if (frameRateIdentifier == 1):
            self.frameRate = 25
        if (frameRateIdentifier == 10):
            self.frameRate = 30
            self.dropFrame = True
        if (frameRateIdentifier == 11):
            self.frameRate = 30
        self.hour = eventData[0] & int('1f', 16)
        self.minute = Util.intFromBytes(eventData[1:2])
        self.second = Util.intFromBytes(eventData[2:3])
        self.frame = Util.intFromBytes(eventData[3:4] )
        #always 100 sub-frames per frame
        self.subFrame = Util.intFromBytes(eventData[4:])
    def __str__(self):
        return (super().__str__() + ", eventType: SMPTE Offset"
                + "\n\t Frame Rate: " + str(self.frameRate)
                + ", Drop Frame: " + str(self.dropFrame)
                + "\n\t Hour: " + str(self.hour)
                + ", Minute: " + str(self.minute)
                + "\n\t Frame: " + str(self.frame)
                + ", Sub-Frame: " + str(self.subFrame))

class TimeSignatureEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        #default is 4
        self.numerator = Util.intFromBytes(eventData[0:1])
        #default is 4 (or encoded 2 since 2^2 is 4)
        self.denominator = math.pow(2, Util.intFromBytes(eventData[1:2]))
        #default is 1 (or 24 encoded since 24/24 = 1)
        self.beatsPerTick = Util.intFromBytes(eventData[2:3]) / 24
        #default is 8
        self.thirtySecondNotesPerBeat = Util.intFromBytes(eventData[3:])
    def __str__(self):
        return (super().__str__() + ", eventType: Time Signature"
                + "\n\t Time Signature: " + str(self.numerator)
                    + "/" + str(self.denominator)
                + "\n\t Beats per tick: " + str(self.beatsPerTick)
                + ", 32nd notes per beat: " + str(self.thirtySecondNotesPerBeat))

class KeySignatureEvent(MetaEvent):
    def setFromBytes(self, midiData):
        eventData = Util.stripLeadingVariableLength(midiData[2:])
        #True for major, False for minor
        self.majorKey = (Util.intFromBytes(eventData[1:2]) == 0)
        #true for sharps, false for flats
        self.sharpKey = (Util.intFromBytes(eventData[0:1], True) > 0)
        self.numberOfAccidentals = abs(Util.intFromBytes(eventData[0:1], True))
    def __str__(self):
        sharpsOrFlats = "sharps" if self.sharpKey else "flats"
        majorOrMinor = ""
        if (self.numberOfAccidentals > 0):
           majorOrMinor = ", major" if self.majorKey else ", minor" 
        return (super().__str__() + ", eventType: Key Signature"
                + "\n\t Number of " + str(sharpsOrFlats) + ": "
                    + str(self.numberOfAccidentals) + majorOrMinor)

class SequencerSpecificEvent():
    def setFromBytes(self, midiData):
        self.eventData = Util.stripLeadingVariableLength(midiData[2:])
    def __str__(self):
        return (super().__str__() + ", eventType: Sequencer Specific"
                + "\n\t Raw data (without variable-length)" + str(self.eventData))
        

############################ System Exclusice Events #########################################
class SystemExclusiveEvent(MidiEvent):
    def setFromBytes(self, midiData):
        self.eventData = Util.stripLeadingVariableLength(midiData[1:])
    def __str__(self):
        return ("System " + " deltaTime: " + str(self.deltaTime)
                + "\n\t Raw data (without variable-length)" + str(self.eventData))                        

######################### Channel Events ############################################
class ChannelEvent(MidiEvent):
    #when calling this on a child class, midiData should have a status byte
    def setFromBytes(self, midiData):
        return print("Set bytes called on parent event class!")
    def __str__(self):
        return "Channel  deltaTime: " + str(self.deltaTime)

class NoteOffEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        self.noteNumber = midiData[1]
        self.velocity = midiData[2]
    def __str__(self):
        return (super().__str__() + ", eventType: Note Off"
                + ", Channel: " + str(self.channel)
                + "\n\t Note Number: " + str(self.noteNumber)
                + ", Velocity: " + str(self.velocity))

class NoteOnEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        self.noteNumber = midiData[1]
        self.velocity = midiData[2]
    #note on with velocity zero is really note off
    def isNoteOff(self):
        return self.velocity == 0
    def __str__(self):
        eventType = ("Note Off (as Note On)" if self.isNoteOff()
                     else "Note On")
        return (super().__str__() + ", eventType: " + eventType
                + ", Channel: " + str(self.channel)
                + "\n\t Note Number: " + str(self.noteNumber)
                + ", Velocity: " + str(self.velocity))

class NoteAftertouchEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        self.noteNumber = midiData[1]
        self.aftertouchAmount = midiData[2]
    def __str__(self):
        return (super().__str__() + ", eventType: Note Aftertouch"
                + ", Channel: " + str(self.channel)
                + "\n\t Note Number: " + str(self.noteNumber)
                + " Aftertouch: " + str(self.aftertouchAmount))

class ControllerEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        self.controllerType = midiData[1]
        self.value = midiData[2]
    def controllerTypeString(self):
        controllerString = Util.controllerString(self.controllerType)
        if controllerString == None:
            return str(self.controllerType)
        else:
            return controllerString
    def __str__(self):
        return (super().__str__() + ", eventType: Controller"
                + ", Channel: " + str(self.channel)
                + "\n\t Controller Type: " + str(self.controllerTypeString())
                + ", Value: " + str(self.value))

class ProgramChangeEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        self.programNumber = midiData[1]
    def __str__(self):
        return (super().__str__() + ", eventType: Program Change"
                + ", Channel: " + str(self.channel)
                + "\n\t Program Number: " + str(self.programNumber))

class ChannelAftertouchEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        self.aftertouchAmount = midiData[1]
    def __str__(self):
        return (super().__str__() + ", eventType: Channel Aftertouch"
                + ", Channel: " + str(self.channel)
                + "\n\t Aftertouch: " + str(self.aftertouchAmount))

class PitchBendEvent(ChannelEvent):
    def setFromBytes(self, midiData):
        self.channel = midiData[0] & int('0f',16)
        #NOTE: this relies on Util.varLenVal not actually caring if
        #the format is an actual valid varaible length value
        #(and thus completly ignoring the msb of every byte)
        self.bendAmount = Util.varLenVal(midiData[2:3] + midiData[1:2])
    #pitchValue relative to 8192; positive for increase, negative for decrease
    def bendAmount(self):
        return self.bendAmount - 8192
    def __str__(self):
        return (super().__str__() + ", eventType: Pitch Bend"
                + ", Channel: " + str(self.channel)
                + "\n\t Amout (relative to 8192): "
                    + str(self.bendAmount()))

class EventDictionaries:
    #maps a meta event type to its class
    META_EVENT_DICTIONARY = MetaEventDict = {0 : SequenceNumberEvent,
                                             1 : TextEvent,
                                             2 : CopyrightNoticeEvent,
                                             3 : TrackNameEvent,
                                             4 : InstrumentNameEvent,
                                             5 : LyricsEvent,
                                             6 : MarkerEvent,
                                             7 : CuePointEvent,
                                             8 : ProgramNameEvent,
                                             9 : DeviceNameEvent,
                                             32 : MidiChannelPrefixEvent,
                                             47 : EndOfTrackEvent,
                                             81 : SetTempoEvent,
                                             84 : SMPTEOffsetEvent,
                                             88 : TimeSignatureEvent,
                                             89 : KeySignatureEvent,
                                             127: SequencerSpecificEvent}
    #maps [byte with event type and channel] & b'\xf0' to event type
    CHANNEL_EVENT_DICTIONARY = {int('80', 16) : NoteOffEvent,
                        int('90', 16) : NoteOnEvent,
                        int('a0', 16) : NoteAftertouchEvent,
                        int('b0', 16) : ControllerEvent,
                        int('c0', 16) : ProgramChangeEvent,
                        int('d0', 16) : ChannelAftertouchEvent,
                        int('e0', 16) : PitchBendEvent}
