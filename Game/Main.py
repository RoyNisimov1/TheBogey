import pygame
import random

from Game.Card import Card
from Game.Deck import Deck
from Game.Color import COLORS

pygame.init()
infoObject = pygame.display.Info()
current_w, current_h = infoObject.current_w, infoObject.current_h


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

running: bool = True
clock = pygame.time.Clock()
fps: int = 60
delta_time: float = 0.1
#BG Colors
t = 0.0
direction = delta_time / fps
dir = 1
BG_C = COLORS.BG_COLORS.copy()

# Game related
draw_deck = Deck(Deck.get_new_deck())
draw_deck.shuffle_deck()
is_bogey_turn = False
decks = []
firstCard = draw_deck.draw_card()
in_hand = Deck([])
discard_deck = Deck([])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: running = False

    # SCREEN COLOR LERP
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

    # GAME
    # Makes sure there are enough cards:
    if len(draw_deck) >= 5:
        ... # combine discard and draw deck and reshuffle

    # Draw cards up to 5
    if not is_bogey_turn and len(in_hand) < 5:
        for _ in range(5 - len(in_hand)):
            in_hand.add_card(draw_deck.draw_card())

    in_hand.draw_deck(screen, [current_w // 2 - 525, current_h - 300], 10)




    pygame.display.flip()

    delta_time = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()



