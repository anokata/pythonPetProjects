# TODO: Скрывать! _
class Event():
    theme = ''

    def __init__(self, theme, data):
        self.theme = theme
        self.data = data

EventBox = list()

class Publisher():

    def __init__(self):
        self.reigster(EventBox)

    def send(self, theme, data):
        self.sendEvent(Event(theme, data))

    def sendEvent(self, event):
        self.box.append(event)

    def reigster(self, box):
        self.box = box

class Subscriber():
    
    def __init__(self):
        self.boxes = list()
        self.handlers = dict()
        self.subscribe(EventBox)

    def subscribe(self, box):
        self.box = box

    def register(self, eventTheme, fun):
        self.handlers[eventTheme] = fun

    def process(self):
        dispatched = list()
        for event in self.box:
            if event.theme in self.handlers.keys():
                handler = self.handlers[event.theme]
                handler(event)
                dispatched.append(event)
        for e in dispatched:
            self.box.remove(e)

                
if __name__=='__main__':
    p = Publisher()
    s = Subscriber()
    s.register('T', lambda e: print(e.data))
    p.send(Event('T', 1))
    p.send(Event('T', 4))
    s.process()
    p.send(Event('T', 5))
    s.process()




