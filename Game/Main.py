import math

import pygame

from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs
from Game.Card import Card
from Game.Deck import Deck
from Game.Color import COLORS
from Button import Button

pygame.init()
infoObject = pygame.display.Info()
current_w, current_h = infoObject.current_w, infoObject.current_h


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("The Bogey")

running: bool = True
clock = pygame.time.Clock()
fps: int = 60
delta_time: float = 0.1


# Game related
draw_deck = Deck(Deck.get_new_deck())
draw_deck.shuffle_deck()
is_bogey_turn = False
space_between_decks = [20, 30]
decks_start_pos = [(current_w - (space_between_decks[0] + Card.WIDTH) * 6) / 2, 30]
decks = []
for i in range(12):
    pos = [decks_start_pos[0] + (space_between_decks[0] + Card.WIDTH) * i, decks_start_pos[1]]
    if i > 5:
        pos = [decks_start_pos[0] + (space_between_decks[0] + Card.WIDTH) * (i-6), decks_start_pos[1] + space_between_decks[1] + Card.HEIGHT]
    decks.append(Deck([], pos))

firstCard = draw_deck.draw_card()
in_hand = Deck([], start_pos=[20, current_h - 300])
discard_deck = Deck([])
base_speed = 10
space = 10
draw_cards = True
cards_in_place = 0



color_bg_sys = COLORS(fps)




while running:

    card_speed = base_speed*delta_time

    # SCREEN COLOR LERP

    c = color_bg_sys.update(delta_time)
    screen.fill(c)

    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False






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
    elif draw_cards:
        for _ in range(5 - len(in_hand)):
            c = draw_deck.draw_card()
            c.set_pos(in_hand.start_pos)
            in_hand.add_card(c)
        draw_cards = False


    poses = in_hand.draw_deck([current_w // 2 - (Card.WIDTH + space) * in_hand.get_len_not_active() * 0.5, current_h - 300], space)
    for i in range(len(in_hand)):
        card = in_hand.deck[i]
        card.rest_pos = poses[i]
        l = LerpFuncs.LERPPos(card.get_pos(), poses[i], card_speed)
        card.set_pos(l, 1)
        if card.active:
            card.set_pos([mouse_pos[0] - Card.WIDTH / 2, mouse_pos[1] - Card.HEIGHT / 2], 3)

    for i, deck in enumerate(decks):
        succeeded = deck.check_mouse_events()
        if succeeded:
            in_hand.remove_card_data(GLOBAL().current)
            GLOBAL().current.active = False
            GLOBAL().set_current(None)
            GLOBAL().set_is_active(False)




    for deck in decks:
        deck.gyzmos(screen)

    for card in in_hand.deck:
        if card is not None:
            card.update(screen, delta_time)



    pygame.display.flip()

    delta_time = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    GLOBAL().update_mouse(delta_time)
pygame.quit()



