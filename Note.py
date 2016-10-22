class Note:    
    def __init__(self, start, pitch, velocity, chan):
        self.pitch = pitch #note number
        self.chan = chan
        self.startTime = start
        self.endTime = None
        self.velocity = velocity
        self.releaseVelocity = None
        return
    def setEndTime(self, endTime):
        self.endTime = endTime
    def setReleaseVelocity(self, releaseVelocity):
        self.releaseVelocity = releaseVelocity
    def length(self):
        return self.endTime - self.startTime
    #returns a vaule used in sorting the notes
    #notes are sorted by time, pitch
    def sortVal(self):
        return (self.startTime + 1)*1000 + self.pitch*.001
    def __lt__(self, other):
        return self.sortVal() < other.sortVal()
        
