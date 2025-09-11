class Event:
    def __init__(self):
        self.lstCallbackMethod = []

    def __iadd__(self, other):
        self.lstCallbackMethod.append(other)
        return self
    
    def __isub__(self, other):
        self.lstCallbackMethod.remove(other)
        return self

    def emit(self, *args):
        for callbackMethod in self.lstCallbackMethod:
            callbackMethod(*args)