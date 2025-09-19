import pygame

from Game.GLOBAL import GLOBAL


class COLORS:

    BG_GREEN = (70, 128, 87)
    BG_CYAN = (94, 142, 166)
    BG_ORANGE = (176, 126, 100)
    BG_YELLOW = (165, 168, 93)
    BG_BLUE = (98, 90, 166)
    BG_RED = (158, 90, 85)

    BG_COLORS = [BG_GREEN, BG_CYAN,BG_BLUE, BG_ORANGE, BG_YELLOW, BG_RED]
    WAIT_TIME = 60
    SPEED = 18

    def __init__(self):
        self.BG_C = COLORS.BG_COLORS.copy()
        self.t = 0.0
        self.direction = 0.1
        self.dir = 1
        self.current_color = self.BG_C[0]
        self.to_color_index = 1
        self.state = 0
        # 0 is stay
        # 1 is transitioning

    def update(self) -> pygame.Color:
        if self.state > 1: self.state = 1
        screen_color = (0, 0, 0)
        if self.state == 1:
            screen_color = COLORS.lerp_color(self.current_color, self.BG_C[self.to_color_index], GLOBAL().get_dt() * COLORS.SPEED)
            if screen_color == self.BG_C[self.to_color_index]:
                self.to_color_index = (self.to_color_index + 1) % len(self.BG_COLORS)
                self.state = 0
            self.current_color = screen_color
        elif 0 <= self.state < 1:
            screen_color = self.current_color
            self.state += (1 / COLORS.WAIT_TIME) * GLOBAL().get_dt()
        return screen_color



    @staticmethod
    def lerp_color(color1, color2, t):
        t = max(0.0, min(1.0, t))


        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)

        return r, g, b

