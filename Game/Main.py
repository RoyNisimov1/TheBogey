import pygame

from Game.LerpFuncs import LerpFuncs
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


# Game related
draw_deck = Deck(Deck.get_new_deck())
draw_deck.shuffle_deck()
is_bogey_turn = False
decks = []
firstCard = draw_deck.draw_card()
in_hand = Deck([])
discard_deck = Deck([])
card_speed = 20
#dragability
currently_dragging = None
start_drag_index = 0

color_bg_sys = COLORS(fps)
while running:


    # SCREEN COLOR LERP

    c = color_bg_sys.update(delta_time)
    screen.fill(c)

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
                in_hand.add_card_index(currently_dragging, start_drag_index)
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
    elif len(in_hand) < 5 and currently_dragging is None:
        for _ in range(5 - len(in_hand)):
            in_hand.add_card(draw_deck.draw_card())

    space = 10
    poses = in_hand.draw_deck([current_w // 2 - (Card.WIDTH + space) * len(in_hand) * 0.5, current_h - 300], space)
    mouse_buttons = pygame.mouse.get_pressed()
    for i in range(len(in_hand)):
        card = in_hand.deck[i]
        if card == currently_dragging:
            continue

        if currently_dragging is None:
            l = LerpFuncs.LERPPos(card.get_pos(), poses[i], delta_time * card_speed)
            #l = poses[i]
            card.set_pos(l)

        if card.get_rect().collidepoint(mouse_pos) and currently_dragging is None:
            l = LerpFuncs.LERPPos(card.get_pos(), [poses[i][0], poses[i][1] - 15], delta_time * card_speed * 0.5)
            #l = [poses[i][0], poses[i][1] - 50]
            card.set_pos(l)
            if mouse_buttons[0]:
                currently_dragging = card
                start_drag_index = i

    if currently_dragging is not None and len(in_hand) == 5:
        in_hand.remove(start_drag_index)

    for card in in_hand.deck:
        if card is not None:
            card.update(screen)
    if currently_dragging is not None: currently_dragging.update(screen)

    pygame.display.flip()

    delta_time = clock.tick(fps) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()



