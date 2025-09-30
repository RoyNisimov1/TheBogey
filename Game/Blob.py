import math
from random import choice

import pygame
import random

from pygame import SRCALPHA

from Game.Color import COLORS
from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs

class Blob(pygame.sprite.Sprite):
    BLOB_SPEED = 1
    MAX_SIZE = 400
    MIN_SIZE = 100
    BLUR_RAD = 20


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = [random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE), random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE)]
        infoObject = pygame.display.Info()
        self.current_w, self.current_h = infoObject.current_w, infoObject.current_h
        self.x = random.randint(0, self.current_w)
        self.y = random.randint(0, self.current_h)
        self.alpha = random.randint(0, 50)
        r = self.alpha / 255
        c = random.choice(COLORS.BG_COLORS)
        c = (math.floor(c[0] * r), math.floor(c[1] * r), math.floor(c[2] * r))
        self.color = (c[0], c[1], c[2], self.alpha)
        self.move_to = [self.x, self.y]
        self.timer = 0
        self.image = self.get_surface()
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)


    def get_surface(self):
        surface = pygame.Surface([self.size[0] + 4 * Blob.BLUR_RAD, self.size[1] + 4 * Blob.BLUR_RAD], pygame.SRCALPHA).convert_alpha()
        r = pygame.Rect(Blob.BLUR_RAD, Blob.BLUR_RAD * 2, self.size[0], self.size[1])
        pygame.draw.ellipse(surface, self.color, r)
        blurred = pygame.transform.gaussian_blur(surface, Blob.BLUR_RAD).convert_alpha()
        return blurred



    def update(self, *args, **kwargs):
        if self.timer >= random.randint(3, 10):
            self.move_to = [random.randint(0, self.current_w), random.randint(0, self.current_h)]
            self.timer = 0
        self.rect.topleft = LerpFuncs.LERPPos(self.rect.topleft, self.move_to, GLOBAL().get_dt())
        self.timer += GLOBAL().get_dt()

class BlobParent:
    BLUR_RAD = 10

    def __init__(self, blobs: list[Blob]):
        self.blobs = blobs



    def update_s(self, screen):
        for b in self.blobs:
            b.update()
        s = pygame.Surface((GLOBAL().current_w, GLOBAL().current_h), SRCALPHA)
        s.fblits([(blob.image, blob.rect) for blob in self.blobs])
        # pygame.transform.box_blur(s, BlobParent.BLUR_RAD)
        return s


