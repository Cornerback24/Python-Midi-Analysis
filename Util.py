class Util:
    #returns a hex value for use in fromhex
    @staticmethod
    def paddedHex(sourceNum):
        returnVal = hex(sourceNum)[2:]
        if (len(returnVal) % 2) != 0:
            returnVal = '0' + returnVal
        return returnVal

    #returns a bytes objected shifted left by numBits bits
    @staticmethod
    def lshiftBytes(sourceBytes, numBits):
        return bytes.fromhex(Util.paddedHex(
            int.from_bytes(sourceBytes, "big") << numBits))
