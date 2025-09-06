import pygame
import random

from Game.Color import COLORS

pygame.init()
infoObject = pygame.display.Info()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

running: bool = True
clock = pygame.time.Clock()
fps: int = 60
delta_time: float = 0.1
#BG Colors
t = 0.0
direction = delta_time / fps
dir = 1
BG_C = COLORS.BG_COLORS.copy()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: running = False

    screen_color = COLORS.lerp_colors(BG_C, t)
    t += direction
    if screen_color in BG_C:
        old_color_index = 0
        direction = delta_time / (fps * 100) * dir
        for i, c in enumerate(BG_C):
            if c == screen_color:
                old_color_index = i
                break
        random.shuffle(BG_C)
        for i, c in enumerate(BG_C):
            if c == screen_color:
                BG_C[i] = BG_C[old_color_index]
                BG_C[old_color_index] = screen_color


    else:
        direction = delta_time / fps * dir
    if t >= 1.0 or t <= 0.0:
        dir *= -1


    screen.fill(screen_color)

    pygame.display.flip()

    delta_time = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()



