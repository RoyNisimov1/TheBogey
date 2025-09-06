import pygame

class LerpFuncs():

    @staticmethod
    def LERPPos(start_pos: list[int], end_pos: list[int], speed: float = 0.1) -> list[float]:
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * speed
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * speed
        return [x, y].copy()








