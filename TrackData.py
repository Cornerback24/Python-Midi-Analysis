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

#this is basiclly and ordered dictionary
class TempoChanges:
    def __init__(self):
        self.deltaTimeTotal = []
        self.tempoChangeEvents = []
        self.index = 0
        return
    #tempo changes need to be added in order
    def addTempoChange(self, deltaTimeTotal, event):
        self.deltaTimeTotal.append(deltaTimeTotal)
        self.tempoChangeEvents.append(event)
    #so that class can be used as a stream
    def current(self):
        return (self.deltaTimeTotal[self.index],
                self.tempoChangeEvets[self.index])
    def findNext(self):
        self.index = self.index + 1
    def hasMoreTempoChanges(self):
        return self.index < len(self.tempoChangeEvents)
    def reset(self): #go back to first task
        self.index = 0
