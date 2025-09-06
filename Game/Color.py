import pygame
import random

class COLORS:

    BG_GREEN = (29, 145, 64)
    BG_CYAN = (87, 158, 194)
    BG_ORANGE = (204, 124, 82)
    BG_YELLOW = (183, 191, 31)
    BG_BLUE = (46, 31, 163)
    BG_RED = (194, 94, 87)

    BG_COLORS = [BG_GREEN, BG_ORANGE, BG_CYAN, BG_YELLOW, BG_BLUE, BG_RED]

    def __init__(self, fps=60):
        self.BG_C = COLORS.BG_COLORS.copy()
        self.t = 0.0
        self.direction = 0.1
        self.dir = 1
        self.fps = fps

    def update(self, delta_time: float) -> pygame.Color:
        screen_color = COLORS.lerp_colors(self.BG_C, self.t)
        self.t += self.direction
        if screen_color in self.BG_C:
            old_color_index = 0
            self.direction = delta_time / (self.fps * 100) * self.dir
            for i, c in enumerate(self.BG_C):
                if c == screen_color:
                    old_color_index = i
                    break
            random.shuffle(self.BG_C)
            for i, c in enumerate(self.BG_C):
                if c == screen_color:
                    self.BG_C[i] = self.BG_C[old_color_index]
                    self.BG_C[old_color_index] = screen_color
        else:
            self.direction = delta_time / self.fps * self.dir

        if self.t >= 1.0 or self.t <= 0.0:
            self.dir *= -1

        return screen_color



    @staticmethod
    def lerp_color(color1, color2, t):

        t = max(0.0, min(1.0, t))

        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)

        return pygame.Color(r, g, b)

    @staticmethod
    def lerp_colors(colors: list[pygame.Color], t):
        t = max(0.0, min(1.0, t))  # Clamp t between 0 and 1

        num_colors = len(colors)
        if num_colors < 2:
            return colors[0] if num_colors > 0 else pygame.Color(0, 0, 0)  # Return black if no colors

        segment_length = 1.0 / (num_colors - 1)

        # Determine which segment we are in
        segment_index = int(t / segment_length)

        # Handle the case where t is exactly 1.0
        if segment_index >= num_colors - 1:
            return pygame.Color(colors[num_colors - 1])

        # Calculate local t within the current segment
        local_t = (t % segment_length) / segment_length

        color1 = pygame.Color(colors[segment_index])
        color2 = pygame.Color(colors[segment_index + 1])

        return color1.lerp(color2, local_t)