class Util:
    #returns a hex value for use in fromhex
    @staticmethod
    def paddedHex(sourceNum):
        returnVal = hex(sourceNum)[2:]
        if (len(returnVal) % 2) != 0:
            returnVal = '0' + returnVal
        return returnVal
