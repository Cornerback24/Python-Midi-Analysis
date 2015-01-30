class Note:    
    def __init__(self, start, pitch, velocity, chan):
        self.pitch = pitch #note number
        self.chan = chan
        self.startTime = start
        self.endTime = None
        self.velocity = velocity
        return
    def length(self):
        return self.endTime - self.startTime
    #returns a vaule used in sorting the notes
    #notes are sorted by time, pitch
    def sortVal(self):
        return (self.time + 1)*1000 + self.pitch*.001
    def __lt__(self, other):
        return self.sortVal() < other.sortVal()
        
