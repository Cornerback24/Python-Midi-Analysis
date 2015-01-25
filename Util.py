class Util:
    #returns a hex value for use in fromhex
    @staticmethod
    def paddedHex(sourceNum):
        returnVal = hex(sourceNum)[2:]
        if (len(returnVal) % 2) != 0:
            returnVal = '0' + returnVal
        return returnVal

    #returns a bytes object shifted left by numBits bits
    @staticmethod
    def lshiftBytes(sourceBytes, numBits):
        return bytes.fromhex(Util.paddedHex(
            int.from_bytes(sourceBytes, "big") << numBits))

    #returns a byte array shifted left by numBits bits
    @staticmethod
    def lshiftByteArray(sourceByteArray, numBits):
        return bytearray.fromhex(Util.paddedHex(
            int.from_bytes(sourceByteArray, "big") << numBits))

    #takes a bytes object formatted in variable length and
    #returns the int value represented
    @staticmethod
    def varLenVal(varLenBytes):
        if len(varLenBytes) == 0:
            return 0
        varLenArray = bytearray(varLenBytes)
        returnValBytes = bytearray.fromhex(
            Util.paddedHex(varLenArray[0] & b'\x7f'[0]))
        for i in range(len(varLenBytes) - 1):
            nextByte = varLenArray[i+1] & b'\x7f'[0]
            returnValBytes = Util.lshiftByteArray(returnValBytes, 7)
            returnValBytes[len(returnValBytes)-1] = (
                returnValBytes[len(returnValBytes)-1] | nextByte)
        return int.from_bytes(returnValBytes, "big")

    @staticmethod
    def msbIsOne(byte): #returns true if the msb of a bytes object is 1
        return (byte[0] & int('80',16)) > 0

    #maps [byte with event type and channel] & b'\xf0' to event type
    ChannelEventDict = {int('80', 16) : "NoteOff",
                        int('90', 16) : "NoteOn",
                        int('a0', 16) : "NoteAftertouch",
                        int('b0', 16) : "Controller",
                        int('c0', 16) : "ProgramChange",
                        int('d0', 16) : "ChannelAftertouch",
                        int('e0', 16) : "PitchBend"}
