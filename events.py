from constants import *

class Event:
    def __init__(self, n):
        self.name = n

class PrepareEvent(Event):
    def __init__(self):
        Event.__init__(self, "PrepareEvent")

class BeginPlayEvent(Event):
    def __init__(self):
        Event.__init__(self, "BeginPlayEvent")


class TickEvent(Event):
    def __init__(self, time):
        self.time = time
        Event.__init__(self, "TickEvent")


class QuitEvent(Event):
    def __init__(self):
        Event.__init__(self, "QuitEvent")


class RequestAccelerateEvent(Event):
    def __init__(self, dir):
        self.direction = dir
        if dir == LEFT:
            dirstr = "LEFT"
        elif dir == RIGHT:
            dirstr = "RIGHT"
        elif dir == UP:
            dirstr = "UP"
        elif dir == DOWN:
            dirstr = "DOWN"
        Event.__init__(self, "AccelerateEvent (" + dirstr + ")")

class RequestDecelerateEvent(Event):
    def __init__(self):
        Event.__init__(self, "DecelerateEvent")

class SetFrameOfReferenceEvent(Event):
    def __init__(self, fr):
        self.frameOfReference = fr
        Event.__init__(self, "SetFrameOfReferenceEvent (" + str(fr) + ")")

class SetTimeEvent(Event):
    def __init__(self, time):
        self.time = time
        Event.__init__(self, "SetTimeEvent (" + str(time) + ")")

class PlaceEvent(Event):
    def __init__(self, actor):
        self.actor = actor
        Event.__init__(self, "PlaceEvent (" + str(actor) + ")")

class MoveEvent(Event):
    def __init__(self, actor):
        self.actor = actor
        Event.__init__(self, "MoveEvent (" + str(actor) + ")")

class ContractEvent(Event):
    def __init__(self, actor):
        self.actor = actor
        Event.__init__(self, "ContractEvent (" + str(actor) + ")")
