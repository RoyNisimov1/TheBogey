import pygame
import random

from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs

class Blob(pygame.sprite.Sprite):
    BLOB_SPEED = 1
    MAX_SIZE = 1000
    MIN_SIZE = 200



    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = [random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE), random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE)]
        infoObject = pygame.display.Info()
        self.current_w, self.current_h = infoObject.current_w, infoObject.current_h
        self.x = random.randint(0, self.current_w)
        self.y = random.randint(0, self.current_h)
        self.alpha = random.randint(0, 255)
        self.move_to = [self.x, self.y]
        self.og_img = pygame.image.load(GLOBAL().BLOB_LOC).convert_alpha()
        self.image = self.og_img
        self.image.set_alpha(self.alpha)
        self.to_size = [random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE), random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE)]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self, *args, **kwargs):

        self.image = pygame.transform.smoothscale(self.og_img, self.size)
        if self.x != self.move_to[0] and self.y != self.move_to[1]:
            l = LerpFuncs.pyLerp([self.x, self.y], self.move_to, GLOBAL().get_dt() * Blob.BLOB_SPEED)
            self.rect.topleft = l
            self.x = l[0]
            self.y = l[1]
        else:
            self.move_to = [random.randint(0, self.current_w), random.randint(0, self.current_h)]

        if self.size != self.to_size:
            w = LerpFuncs.LERP(self.size[0], self.to_size[0], GLOBAL().get_dt() * Blob.BLOB_SPEED)
            h = LerpFuncs.LERP(self.size[1], self.to_size[1], GLOBAL().get_dt() * Blob.BLOB_SPEED)
            self.size = [w, h]
        else:
            self.to_size = [random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE), random.randint(Blob.MIN_SIZE, Blob.MAX_SIZE)]


