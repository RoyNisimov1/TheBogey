
import pygame
import math
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
fps: int = 1000
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
save_deck = []
base_speed = 10
card_rotation_speed = 10
torque = 10
space = 20
draw_cards = True
cards_in_place = 0
clicked_button = False


color_bg_sys = COLORS(fps)


b = Button(text="Keep Cards", font_size=10, size=[100, 90], pos=[current_w-110, current_h-100])

def save_later_wrapper():
    for card in in_hand.deck:
        if card.selected:
            card.selected = False
            save_deck.append(card)
    return True


b.set_f(save_later_wrapper)
while running:

    card_speed = base_speed*delta_time
    card_rot_speed = card_rotation_speed * delta_time
    # SCREEN COLOR LERP

    c = color_bg_sys.update(delta_time)
    screen.fill(c)

    mouse_pos = pygame.mouse.get_pos()
    GLOBAL().is_mouse_moving = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            GLOBAL().is_mouse_moving = True


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

    if clicked_button and not is_bogey_turn:
        discard_deck.add_cards(in_hand.deck.copy())
        in_hand.clear()
        in_hand.add_card(draw_deck.draw_card())
        is_bogey_turn = True


    # Draw cards up to 5
    if is_bogey_turn:
        if len(in_hand) == 0:
            is_bogey_turn = False
            clicked_button = False
            in_hand.add_cards(save_deck.copy())
            save_deck.clear()
            draw_cards = True
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
        if not card.active:
            card.rest_pos = poses[i].copy()
            l = LerpFuncs.LERPPos(card.get_pos(), poses[i], card_speed)
            card.set_pos(l, 1)
            card.rotation = LerpFuncs.LERP(card.rotation, 0, card_rot_speed)
        else:
            new_pos = LerpFuncs.LERPPos(start_pos=card.get_pos(), end_pos=[mouse_pos[0] - Card.WIDTH / 2, mouse_pos[1] - Card.HEIGHT / 2], speed=card_speed)
            is_rough_eq = card.collides_with_mouse()
            card.set_pos(new_pos, 4)
            if not is_rough_eq:
                diff = [mouse_pos[0] - card.get_center()[0], (mouse_pos[1] - card.get_center()[1])//1]
                # Normalising the vector
                len_v = math.sqrt(pow(diff[0], 2) + pow(diff[1], 2))
                if len_v == 0: len_v = 1
                diff = diff[1] // len_v, diff[0] // len_v
                r = math.atan2(diff[1], diff[0]) * -torque
                card.rotation = LerpFuncs.LERP(card.rotation, math.floor(r), card_rot_speed)
            else:
                card.rotation = LerpFuncs.LERP(card.rotation, 0, card_rot_speed)

    for i, deck in enumerate(decks):
        succeeded = deck.check_mouse_events()
        if succeeded:
            in_hand.remove_card_data(GLOBAL().current)
            GLOBAL().current.active = False
            GLOBAL().set_current(None)
            GLOBAL().set_is_active(False)

    if not is_bogey_turn:
        clicked_button = b.update(screen)


    for deck in decks:
        deck.gyzmos(screen)

    for card in in_hand.deck:
        if card is not None:
            card.update(screen)



    pygame.display.flip()

    delta_time = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
    GLOBAL().set_dt(delta_time)
    GLOBAL().update_mouse()

pygame.quit()



