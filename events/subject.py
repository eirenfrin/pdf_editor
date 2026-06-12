
class Subject():
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, event, data):
        for observer in self.observers:
            observer.update(event, data)
