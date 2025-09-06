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

#dragability
currently_dragging = None
start_drag = [0, 0]



while running:


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

    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if currently_dragging is not None:
                currently_dragging.set_pos([mouse_pos[0] - Card.WIDTH / 2, mouse_pos[1] - Card.HEIGHT / 2])
                currently_dragging.update(screen)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                currently_dragging.set_pos(start_drag)
                currently_dragging = None

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: running = False

    # GAME

    # Makes sure there are enough cards:
    if len(draw_deck) >= 5:
        # combine discard and draw deck and reshuffle
        draw_deck.add_cards(discard_deck.deck)
        discard_deck.clear()
        draw_deck.shuffle_deck()

    if len(draw_deck) == 0:
        running = False
        print("IMPLEMENT FINISH CONDITION")

    # Draw cards up to 5
    if is_bogey_turn:
        ...
    elif len(in_hand) < 5:
        for _ in range(5 - len(in_hand)):
            in_hand.add_card(draw_deck.draw_card())

    poses = in_hand.draw_deck([current_w // 2 - 525, current_h - 300], 10)
    mouse_buttons = pygame.mouse.get_pressed()
    for i in range(len(in_hand)):
        card = in_hand.deck[i]
        if card == currently_dragging:
            card.update(screen)
            continue
        card.set_pos(poses[i])
        if card.get_rect().collidepoint(mouse_pos) and currently_dragging is None:
            card.set_pos([card.x, card.y - 15])
            if mouse_buttons[0]:
                currently_dragging = card
                start_drag = [card.x, card.y]
        card.update(screen)



    pygame.display.flip()

    delta_time = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()



