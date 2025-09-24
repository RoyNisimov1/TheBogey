import math

import pygame

class LerpFuncs():


    @staticmethod
    def LERPPos(start_pos: list[int], end_pos: list[int], speed: float = 0.1) -> list[float]:
        if speed > 1: speed = 1
        if speed < 0: speed = 0

        x = start_pos[0] + (end_pos[0] - start_pos[0]) * speed
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * speed
        if LerpFuncs.rough_eq(start_pos, end_pos):
            return end_pos
        return [round(x), round(y)].copy()

    @staticmethod
    def pyLerp(start_pos: list[int], end_pos: list[int], speed: float = 0.1):
        if speed > 1: speed = 1
        if speed < 0: speed = 0
        x = pygame.math.lerp(start_pos[0], end_pos[0], speed, True)
        y = pygame.math.lerp(start_pos[1], end_pos[1], speed, True)
        if LerpFuncs.rough_eq(start_pos, end_pos):
            return end_pos
        return [x,y].copy()

    @staticmethod
    def rough_eq(a, b, s = 1):
        return abs(b[0] - a[0]) <= s and abs(b[1] - a[1]) <= s
        # return a[0] // 1 == b[0] // 1 and a[1] // 1 == b[1] // 1


    @staticmethod
    def ease_in_sine(t):
        return -math.cos(t * math.pi / 2) + 1

    @staticmethod
    def ease_in_pos(start_pos: list[int], end_pos: list[int], speed: float = 0.1):
       t = LerpFuncs.ease_in_sine(speed)
       return LerpFuncs.LERPPos(start_pos, end_pos, t)

    @staticmethod
    def LERP(a, b, t):
        if t > 1: t = 1
        if t < 0: t = 0

        l =  a + (b - a) * t
        if abs(b - l) <= 1:
            return b
        return l
    @staticmethod
    def interpolate(a0, a1, w):
        return math.ceil((a1 - a0) * (3 - w * 2) * w * w + a0)





