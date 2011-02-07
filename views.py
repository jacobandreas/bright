from events import *
from models import *

import pygame, sys, os

class View(object):

    WIDTH = 640
    HEIGHT = 480

    CENTER = array([WIDTH / 2, HEIGHT / 2])

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.dispatcher.Register(self)

        self.frontSprites = pygame.sprite.RenderUpdates()
        self.backSprites = pygame.sprite.RenderUpdates()

        #bg = BackgroundSprite(-1, self.backSprites)

    def Notify(self, evt):

        if isinstance(evt, PrepareEvent):
            pygame.init()
            self.window = pygame.display.set_mode((View.WIDTH, View.HEIGHT))
            self.background = pygame.Surface(self.window.get_size())

        elif isinstance(evt, PlaceEvent):
            if isinstance(evt.actor, Player):
                self.PlacePlayer(evt.actor)
            elif isinstance(evt.actor, Baddie):
                self.PlaceBaddie(evt.actor)
            elif isinstance(evt.actor, Car):
                self.PlaceCar(evt.actor)
            elif isinstance(evt.actor, Tree):
                self.PlaceTree(evt.actor)

        elif isinstance(evt, SetTimeEvent):
            self.time = evt.time

        elif isinstance(evt, TickEvent):
            self.Paint()

        elif isinstance(evt, MoveEvent):
            self.MoveActor(evt.actor)

        elif isinstance(evt, SetFrameOfReferenceEvent):
            self.frameOfReference = evt.frameOfReference

        elif isinstance(evt, ContractEvent):
            #pass
            self.ContractActor(evt.actor)

    def PlacePlayer(self, player):
        ps = PlayerSprite(player.guid, self.frontSprites)
        ps.center = View.CENTER

    def PlaceBaddie(self, baddie):
        bs = BaddieSprite(baddie.guid, self.frontSprites)
        self.MoveActor(baddie)

    def PlaceCar(self, car):
        cs = CarSprite(car.guid, self.frontSprites)
        self.MoveActor(car)

    def PlaceTree(self, tree):
        ts = TreeSprite(tree.guid, self.frontSprites)
        self.MoveActor(tree)

    def MoveActor(self, actor):
        x = self.frameOfReference.GetApparentX(actor.frameOfReference, self.time)
        s = self.GetFrontSprite(actor)
        s.rect.center = [View.CENTER[0] + int(x[0]), View.CENTER[1] + -x[1]]

    def ContractActor(self, actor):
        s = self.GetFrontSprite(actor)
        s.Contract(self.frameOfReference.GetGamma(actor.frameOfReference),
                   self.frameOfReference.world.AddVelocities(-self.frameOfReference.GetLabV(),
                                            actor.frameOfReference.GetLabV()))

    def Paint(self):

        self.backSprites.clear(self.window, self.background)
        self.frontSprites.clear(self.window, self.background)

        self.backSprites.update()
        self.frontSprites.update()

        dirty1 = self.backSprites.draw(self.window)
        dirty2 = self.frontSprites.draw(self.window)

        dirty = dirty1 + dirty2

        pygame.display.update(dirty)

    def GetFrontSprite(self, sp):
        for s in self.frontSprites:
            if s.guid == sp.guid:
                return s
        return None

    def GetBackSprite(self, sp):
        for s in self.backSprites:
            if s.guid == sp.guid:
                return s
        return None


class BrightSprite(pygame.sprite.Sprite):

    def __init__(self, guid, group=None):
        self.guid = guid
        pygame.sprite.Sprite.__init__(self, group)

    def Contract(self, gamma, dv):

        if isinstance(self, PlayerSprite):
            return

        if not dv.any():
            return

        angle = 90 - degrees(atan(-dv[1] / dv[0]))

        working = pygame.transform.rotate(self.base_image, angle)
        w = working.get_rect().w
        h = working.get_rect().h
        nh = int(h / gamma)

        working = pygame.transform.scale(working, [w, nh]) 
        working = pygame.transform.rotate(working, -angle)

        self.image = working

class BackgroundSprite(BrightSprite):

    def __init__(self, guid, group=None):
        BrightSprite.__init__(self, guid, group)

        self.image = pygame.image.load("map.png")
        self.rect = self.image.get_rect()

class PlayerSprite(BrightSprite):

    def __init__(self, guid, group=None):
        BrightSprite.__init__(self, guid, group)

        surf = pygame.Surface((30, 30))
        surf = surf.convert_alpha()
        surf.fill((0,0,0,0))
        pygame.draw.circle(surf, (255,0,0), (15,15), 15)

        self.base_image = surf
        self.base_rect = surf.get_rect()

        self.image = self.base_image.copy()
        self.rect = pygame.Rect(0, 0, self.base_rect.w, self.base_rect.h)

class BaddieSprite(BrightSprite):

    def __init__(self, guid, group=None):
        BrightSprite.__init__(self, guid, group)

        surf = pygame.Surface((20, 20))
        surf = surf.convert_alpha()
        surf.fill((0,0,0,0))
        pygame.draw.circle(surf, (0,255,0), (10,10), 10)
        pygame.draw.circle(surf, (0,0,0), (10,5), 3)

        self.base_image = surf
        self.base_rect = surf.get_rect()

        self.image = self.base_image.copy()
        self.rect = pygame.Rect(0, 0, self.base_rect.w, self.base_rect.h)

class CarSprite(BrightSprite):

    def __init__(self, guid, group=None):
        BrightSprite.__init__(self, guid, group)

        self.base_image = pygame.image.load("car.png")
        self.base_image = self.base_image.convert()
        self.base_image.set_colorkey((255,0,255))
        self.base_rect = self.base_image.get_rect()

        self.image = self.base_image.copy()
        self.rect = pygame.Rect(0, 0, self.base_rect.w, self.base_rect.h)

class TreeSprite(BrightSprite):

    def __init__(self, guid, group=None):
        BrightSprite.__init__(self, guid, group)

        self.base_image = pygame.image.load("tree.png")
        self.base_image = self.base_image.convert()
        self.base_image.set_colorkey((255,0,255))
        self.base_rect = self.base_image.get_rect()

        self.image = self.base_image.copy()
        self.rect = pygame.Rect(0, 0, self.base_rect.w, self.base_rect.h)
