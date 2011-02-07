from events import *
from constants import *
import guid

from brightengine import *

from random import random

import math

class Model:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.world = World(2, .2)

        self.player = Player(dispatcher, self.world)
        #Car(dispatcher, self.world)
        #Tree(dispatcher, self.world)
        Baddie(dispatcher, self.world, array([400,0]), array([0,0]))
        Baddie(dispatcher, self.world, array([200,0]), array([0,0]))
        Baddie(dispatcher, self.world, array([0,0]), array([0,0]))
        #Baddie(dispatcher, self.world, array([0,200]), array([0,0]))
        #Baddie(dispatcher, self.world, array([0,0]), array([0,.05]))

class Actor:

    def __init__(self, dispatcher, world):
        self.dispatcher = dispatcher
        self.dispatcher.Register(self)
        self.guid = guid.next()
        self.world = world

    def Place(self):
        self.dispatcher.Post(PlaceEvent(self))

    def Notify(self, evt):
        if isinstance(evt, TickEvent):
            self.dispatcher.Post(MoveEvent(self))

        if isinstance(evt, SetFrameOfReferenceEvent):
            self.dispatcher.Post(ContractEvent(self))

class Player(Actor):

    def __init__(self, dispatcher, world):
        Actor.__init__(self, dispatcher, world)
        self.time = 0
        self.accelerating = False

    def Prepare(self):
        self.Place()
        self.frameOfReference = LinearFrameOfReference(self.world, array([0,
            0]), array([0.8, 0]))
        self.initialFrame = self.frameOfReference
        self.dispatcher.Post(SetFrameOfReferenceEvent(self.frameOfReference))
        self.dispatcher.Post(SetTimeEvent(0))

    def Notify(self, evt):

        if isinstance(evt, BeginPlayEvent):
            self.Prepare()

        elif isinstance(evt, RequestAccelerateEvent):
            self.accelerating = True
            if evt.direction == UP:
                self.ChangeVelocity(array([0, 0.866]))
                #self.ChangeVelocity(array([0, 0.01]))
            elif evt.direction == DOWN:
                self.ChangeVelocity(array([0, -0.866]))
                #self.ChangeVelocity(array([0, -0.01]))
            elif evt.direction == LEFT:
                #self.ChangeVelocity(array([-.866, 0]))
                self.ChangeVelocity(array([-.01, 0]))
            elif evt.direction == RIGHT:
                #self.ChangeVelocity(array([.866, 0]))
                self.ChangeVelocity(array([.01, 0]))

        elif isinstance(evt, RequestDecelerateEvent):
            self.accelerating = False

        elif isinstance(evt, TickEvent):
            self.time += evt.time
            self.dispatcher.Post(SetTimeEvent(self.time))

            #if self.accelerating:
            #    pass #self.SetVelocity(self.frameOfReference.GetLabV() * .999)
            #else:
            #    pass
            #    #self.SetVelocity(self.frameOfReference.GetLabV() * .92)

            r = self.frameOfReference
            v = r.GetLabV()
            x = r.GetLabX() + v * self.time * self.world.c
            if x[1] > 0:
                self.ChangeVelocity(array([0, -0.01]))
            else:
                #self.SetVelocity(array([v[0], 0]))
                self.frameOfReference = LinearFrameOfReference(self.world,
                        array([r.GetLabX()[0], 0]),
                        array([v[0], 0]))
                self.dispatcher.Post(SetFrameOfReferenceEvent(self.frameOfReference))

        Actor.Notify(self, evt)

    def Gravity(self):
        pass

    def ChangeVelocity(self, dv):
        v = self.frameOfReference.GetLabV()
        x = self.frameOfReference.GetLabX()
        nv = self.world.AddVelocities(v, dv)
        self.SetVelocity(nv)

    def SetVelocity(self, v):
        self.frameOfReference, self.time = self.frameOfReference.ChangeVelocity(v, self.time)
        self.dispatcher.Post(SetFrameOfReferenceEvent(self.frameOfReference))

class Baddie(Actor):

    def __init__(self, dispatcher, world, x0, v0):
        Actor.__init__(self, dispatcher, world)
        self.frameOfReference = LinearFrameOfReference(self.world, 
                x0, v0)

    def Notify(self, evt):
        if isinstance(evt, BeginPlayEvent):
            self.Place()

        Actor.Notify(self, evt)

class RandBaddie(Baddie):

    def __init__(self, dispatcher, world, x0):

        r1 = array([random() / 3, 0])
        r2 = array([0, random() / 3])

        v = world.AddVelocities(r1, r2)

        Baddie.__init__(self, dispatcher, world, x0, v)

class Car(Actor):

    def __init__(self, dispatcher, world):
        Actor.__init__(self, dispatcher, world)
        self.frameOfReference = LinearFrameOfReference(self.world,
                array([0,0]), array([.05,0]))

    def Notify(self, evt):
        if isinstance(evt, BeginPlayEvent):
            self.Place()

        Actor.Notify(self, evt)

class Tree(Actor):

    def __init__(self, dispatcher, world):
        Actor.__init__(self, dispatcher, world)
        self.frameOfReference = StationaryFrameOfReference(self.world,
                array([0,0]))

    def Notify(self, evt):
        if isinstance(evt, BeginPlayEvent):
            self.Place()

        Actor.Notify(self, evt)
