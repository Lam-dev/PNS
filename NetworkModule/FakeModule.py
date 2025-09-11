FALLING = 0
PCPCPLUS = 1
BCM = 1
LOW = 1
HIGH = 1
OUT = 1
IN = 1
PUD_UP = 1
BOTH = 2
def setwarnings(*args):
    pass

def setboard(*args):
    pass

def setmode(*args):
    pass

def output(*args):
    pass

def setup(*args, pull_up_down = 1):
    pass

def input(*args):
    return 1

def cleanup(*args):
    pass

def remove_event_detect(*args):
    pass

def add_event_detect(*args):
    pass

def PWM(*args):
    return pwm()

def add_event_callback(*args, callback = None):
    pass

class pwm:
    def  __init__(self):
        pass

    def start(self, *args):
        pass

    def stop(self, *args):
        pass

    def ChangeDutyCycle(self, *args):
        pass

 