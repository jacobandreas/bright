from dispatcher import *
from events import *
from models import *
from views  import *
from controllers import *

import pygame, sys, os

class Game:

    REFRESH_RATE = 60

    STATE_PREPARING = 0
    STATE_PLAYING = 1
    STATE_STOPPED = 2
    STATE_PAUSED = 3

    def Prepare(self):

        self.dispatcher = Dispatcher()
        self.model = Model(self.dispatcher)
        self.view = View(self.dispatcher)

        self.keyController = KeyController(self.dispatcher)

        self.dispatcher.Register(self)

        self.state = Game.STATE_PREPARING
        self.dispatcher.Post(PrepareEvent())

    def Play(self):

        self.Prepare()

        clock = pygame.time.Clock()

        self.state = Game.STATE_PLAYING
        self.dispatcher.Post(BeginPlayEvent())

        time = 0

        while self.state == Game.STATE_PLAYING:
            time += clock.tick(Game.REFRESH_RATE)
            self.dispatcher.Post(TickEvent(clock.get_time()))

    def Notify(self, evt):
        if isinstance(evt, QuitEvent):
            self.state = Game.STATE_STOPPED
            
if __name__ == "__main__":
    Game().Play()
