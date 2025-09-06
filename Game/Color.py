import pygame
class COLORS:

    BG_GREEN = (29, 145, 64)
    BG_CYAN = (87, 158, 194)
    BG_ORANGE = (204, 124, 82)
    BG_YELLOW = (183, 191, 31)
    BG_BLUE = (46, 31, 163)
    BG_RED = (194, 94, 87)

    BG_COLORS = [BG_GREEN, BG_ORANGE, BG_CYAN, BG_YELLOW, BG_BLUE, BG_RED]
    @staticmethod
    def lerp_color(color1, color2, t):

        t = max(0.0, min(1.0, t))

        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)

        return pygame.Color(r, g, b)

    @staticmethod
    def lerp_colors(colors: [pygame.Color], t):
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