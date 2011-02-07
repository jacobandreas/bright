from events import *
from constants import *

import pygame
from pygame.locals import *

class Controller:

    def __init__(self, em):
        self.dispatcher = em
        self.dispatcher.Register(self)

class KeyController(Controller):

    def __init__(self, em):
        Controller.__init__(self, em)
        self.down = None

    def Notify(self, evt):
        if isinstance(evt, TickEvent):
            for pgevt in pygame.event.get():
                if pgevt.type == KEYDOWN:
                    #print "keydown"
                    if pgevt.key == K_LEFT:
                        self.down = LEFT
                    elif pgevt.key == K_RIGHT:
                        self.down = RIGHT
                    elif pgevt.key == K_UP:
                        self.down = UP
                    elif pgevt.key == K_DOWN:
                        self.down = DOWN
                elif pgevt.type == KEYUP:
                    #print "keyup"
                    if self.down:
                        #self.dispatcher.Post(RequestAccelerateEvent(self.down))
                        self.dispatcher.Post(RequestDecelerateEvent())
                        self.down = None
                elif pgevt.type == QUIT:
                    self.dispatcher.Post(QuitEvent())
            if self.down:
                #pass
                self.dispatcher.Post(RequestAccelerateEvent(self.down))

class MouseController(Controller):

    def __init__(self, em):
        Controller.__init__(self, em)

    def Notify(self, evt):
        if isinstance(evt, TickEvent):
            for pgevt in pygame.event.get():
                revt = None
                if pgevt.type == MOUSEBUTTONDOWN:
                    pass
                elif pgevt.type == MOUSEBUTTONUP:
                    pass
                elif pgevt.type == MOUSEMOTION:
                    pass

            if revt:
                self.dispatcher.Post(revt)
