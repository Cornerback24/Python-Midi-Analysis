class Note:    
    def __init__(self):
        self.bank = 0
        self.pitch = 0
        self.chan = 0
        self.startTime = 0
        self.endTime = 0
        return
    #returns a vaule used in sorting the notes
    def sortVal(self):
        return ((self.time + 1)*1000 + self.bank*20 + self.chan
                + self.pitch*.001)
        
