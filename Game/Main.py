
import pygame
from pygame import BLEND_RGB_ADD, BLEND_RGBA_MULT, BLEND_RGB_SUB

from Game.GLOBAL import GLOBAL
from Game.Blob import Blob
from Game.Card import Card
from Game.Deck import Deck
from Game.Color import COLORS
from Button import Button

pygame.init()
pygame.font.init()
infoObject = pygame.display.Info()
current_w, current_h = infoObject.current_w, infoObject.current_h


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("The Bogey")


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

in_hand = Deck([], start_pos=[20, current_h - 300])
discard_deck = Deck([])
save_deck = []

torque = 30
space = 20
t_width = ((Card.WIDTH + space) * 5 - space) + 60
vicinity_rect = pygame.rect.Rect([current_w / 2 - (t_width + space)/2, current_h - (Card.HEIGHT + 50), t_width, Card.HEIGHT + 100])
vicinity_surface = pygame.image.load(GLOBAL().BG_SURFACE_LOC).convert_alpha()
vicinity_surface = pygame.transform.smoothscale(vicinity_surface, (vicinity_rect.width, vicinity_rect.height))
vicinity_surface.set_alpha(256)

is_card_in_vicinity = False
draw_cards = True
cards_in_place = 0
clicked_button = False


color_bg_sys = COLORS()

button_size_normal = [250, 90]
BUTTON_SPRITE = pygame.image.load(GLOBAL().BG_SURFACE_LOC).convert_alpha()
keep_cards = Button(text="Keep Cards", font_size=10, size=button_size_normal, pos=[current_w-300, current_h-100], bg_sprite=BUTTON_SPRITE)


main_screen_bg_color = (97, 81, 79)
main_menu_quit = Button(text="Quit", font_size=10, size=button_size_normal, bg_sprite=BUTTON_SPRITE)
def quite():
    GLOBAL().running = False
main_menu_quit.set_f(quite)
main_menu_resume = Button(text="Resume", font_size=10, size=button_size_normal, bg_sprite=BUTTON_SPRITE)
def resume():
    GLOBAL().current_screen = 0
main_menu_resume.set_f(resume)

main_menu_holder = [main_menu_resume, main_menu_quit]

def save_later_wrapper():
    for card in in_hand.deck:
        if card.selected:
            card.selected = False
            save_deck.append(card)
    return True


keep_cards.set_f(save_later_wrapper)




back_design_surface = pygame.image.load(GLOBAL().BACK_DESIGN_LOC).convert_alpha()
back_design_surface = pygame.transform.smoothscale_by(back_design_surface, 0.5)

card_count_font_obj = pygame.font.Font(GLOBAL().FONT_LOC, 32)





while GLOBAL().running:



    mouse_pos = pygame.mouse.get_pos()
    GLOBAL().is_mouse_moving = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GLOBAL().running = False
        if event.type == pygame.MOUSEMOTION:
            GLOBAL().is_mouse_moving = True
        if event.type == pygame.KEYDOWN:
            # key handling
            if event.key == pygame.K_ESCAPE:
                if GLOBAL().current_screen == 1:
                    GLOBAL().current_screen = 0
                else: GLOBAL().current_screen = 1

    card_speed = GLOBAL().get_dt_base()
    card_rot_speed = GLOBAL().get_dt_rot_speed()
    # SCREEN COLOR LERP

    c = color_bg_sys.update()

    screen.fill(c)
    #

    screen.blit(vicinity_surface, vicinity_rect)

    if GLOBAL().current_screen == 1:
        screen.fill(main_screen_bg_color)
        # draw buttons
        for i, button in enumerate(main_menu_holder):
            button.set_pos([((current_w - button.size[0]) / 2), ((current_h - len(main_menu_holder) *(space + button.size[1]))/ 2 + i * (space + button.size[1]))])
            button.update(screen)



        pygame.display.flip()

        delta_time = clock.tick(fps) / 1000
        delta_time = max(0.001, min(0.1, delta_time))
        GLOBAL().set_dt(delta_time)
        GLOBAL().update_mouse()
        is_card_in_vicinity = False
        continue

    # GAME

    # Makes sure there are enough cards:
    if len(draw_deck) <= 5:
        # combine discard and draw deck and reshuffle
        draw_deck.add_cards(discard_deck.deck)
        discard_deck.clear()
        draw_deck.shuffle_deck()

    if len(draw_deck) == 0:
        running = False
        print("IMPLEMENT FINISH CONDITION")

    # Drawing the deck
    for i in range(len(draw_deck)):
        screen.blit(back_design_surface, [20, (current_h - Card.HEIGHT) / 2 - i])
    card_hover_rect = pygame.Rect(20, (current_h - Card.HEIGHT) / 2 - len(draw_deck) - 1, Card.WIDTH , Card.HEIGHT)
    if card_hover_rect.collidepoint(mouse_pos):
        card_count_font_obj_s = card_count_font_obj.render(f"{len(draw_deck)} / 52", True, (0,0,0))
        screen.blit(card_count_font_obj_s, GLOBAL().get_center([20, (current_h - Card.HEIGHT) / 2 - 51, Card.WIDTH - card_count_font_obj_s.get_size()[0], Card.HEIGHT]))

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
        else:
            # CHECK IF THE BOGEY CAN BE ADDED TO ANY DECK
            dont_stop_game = False
            for i, d in enumerate(decks):
                if d.can_add_card(in_hand.deck[0]):
                    dont_stop_game = True
            if not dont_stop_game:
                # IMPLEMENT LOSE CONDITION
                GLOBAL().running = False
    elif draw_cards:
        for _ in range(5 - len(in_hand)):
            c = draw_deck.draw_card()
            c.lerp_pos(in_hand.start_pos, 0, rot_speed=0)
            in_hand.add_card(c)
        draw_cards = False
        in_hand.order_deck()

    if GLOBAL().is_card_active:
        is_card_in_vicinity = vicinity_rect.colliderect(GLOBAL().get_current().get_rect())

    poses = in_hand.draw_deck([current_w // 2 - (Card.WIDTH + space) * in_hand.get_len_not_active() * 0.5, current_h - 300], space, skip=not is_card_in_vicinity)
    for i in range(len(in_hand)):
        card = in_hand.deck[i]
        if not card.active:
            card.rest_pos = poses[i].copy()
            card.lerp_pos(poses[i], 1, rot_speed=0)
        else:
            new_pos = [mouse_pos[0] - Card.WIDTH / 2, mouse_pos[1] - Card.HEIGHT / 2]
            is_rough_eq = card.collides_with_mouse()
            card.lerp_pos(new_pos, 4, rot_speed=int(not is_rough_eq) * card_rot_speed)

    for i, deck in enumerate(decks):
        succeeded = deck.check_mouse_events()
        if succeeded:
            in_hand.remove_card_data(GLOBAL().current)
            GLOBAL().current.active = False
            GLOBAL().set_current(None)
            GLOBAL().set_is_active(False)

    if not is_bogey_turn:
        clicked_button = keep_cards.update(screen)


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
    is_card_in_vicinity = False
pygame.quit()



