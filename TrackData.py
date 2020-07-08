class TrackData:
    def __init__(self, name=""):
        self.notes = []
        self.events = []
        self.name = name
        return
    def addEvent(self, event):
        self.events.append(event)
        #print(event)
        if (event.eventClass == "Meta" and
            event.eventType == "Sequence/TrackName"):
            self.name = event.data
        return

#this is kind of like an ordered dictionary
class TempoChanges:
    def __init__(self):
        self.deltaTimeTotals = []
        self.tempoChangeEvents = []
        self.index = 0
        return
    #tempo changes need to be added in order
    def addTempoChange(self, deltaTimeTotal, event):
        self.deltaTimeTotals.append(deltaTimeTotal)
        self.tempoChangeEvents.append(event)
    #so that class can be used as a stream
    def deltaTimeTotal(self):
        return self.deltaTimeTotals[self.index]
    def usPerQuarter(self):
        return self.tempoChangeEvents[self.index].usPerQuarter
    def findNext(self):
        self.index = self.index + 1
    def hasMore(self):
        return self.index + 1 < len(self.tempoChangeEvents)
    def reset(self): #go back to first tempo change
        self.index = 0
