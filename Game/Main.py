# --------------------- PYGAME INIT ----------------------------- #
import pygame
pygame.init()
pygame.font.init()
infoObject = pygame.display.Info()
current_w, current_h = infoObject.current_w, infoObject.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("The Bogey")
# --------------------- Imports --------------------------------- #
from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs
from Game.Card import Card
from Game.Deck import Deck
from Game.Color import COLORS
from Button import Button

# --------------------- GLOBAL AND CAMERA INIT ------------------ #
GLOBAL().set_dim(current_w, current_h)
CENTER = current_w/2, current_h/2
CAM_DRAG_OFFSET = 0.1
CAM_SPEED = 15


# --------------------- CLOCK, DELTATIME, FPS CAP INIT ---------- #


clock = pygame.time.Clock()
fps: int = 240
delta_time: float = 0.1

# --------------------- DECKS INIT ------------------------------ #

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

# --------------------- VICINITY RECT INIT ---------------------- #
torque = 30
space = 20
t_width = ((Card.WIDTH + space) * 5 - space) + 60
vicinity_rect = pygame.rect.Rect([current_w / 2 - (t_width + 30)/2, current_h - (Card.HEIGHT + 50), t_width, Card.HEIGHT + 100])
vicinity_surface = pygame.image.load(GLOBAL().BG_SURFACE_LOC).convert_alpha()
vicinity_surface = pygame.transform.smoothscale(vicinity_surface, (vicinity_rect.width, vicinity_rect.height))
vicinity_surface.set_alpha(256)

is_card_in_vicinity = False
draw_cards = True
cards_in_place = 0
clicked_button = False

# --------------------- BG INIT ----------------------------- #
color_bg_sys = COLORS()

# --------------------- BUTTONGS INIT ----------------------------- #
button_size_normal = [250, 90]
# BUTTON_SPRITE = GLOBAL().BUTTON_250_90_SURFACE
BUTTON_SPRITE = None
BUTTON_COLOR = "#4298BD"
#BUTTON_COLOR = "#71738E"
BUTTON_COLOR_HOVER = "#BD6742"
FONT_SIZE = 40
COLOR = (255, 255, 255)

FONT = GLOBAL().FONT_LOC
keep_cards = Button(text="Keep Cards", font=FONT, font_size=FONT_SIZE, size=button_size_normal, pos=[current_w-300, current_h-100], bg_sprite=BUTTON_SPRITE, color=BUTTON_COLOR, hover_color=BUTTON_COLOR_HOVER)


# --------------------- Escape Menu INIT ----------------------------- #
MAIN_MENU_SPACING = 40
main_screen_bg_color = (97, 81, 79)
main_menu_quit = Button(text="Quit", font=FONT, font_size=FONT_SIZE, size=button_size_normal, bg_sprite=BUTTON_SPRITE, color=BUTTON_COLOR, hover_color=BUTTON_COLOR_HOVER)
def quite():
    GLOBAL().running = False
main_menu_quit.set_f(quite)
main_menu_resume = Button(text="Resume", font=FONT, font_size=FONT_SIZE, size=button_size_normal, bg_sprite=BUTTON_SPRITE, color=BUTTON_COLOR, hover_color=BUTTON_COLOR_HOVER)
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

for i, button in enumerate(main_menu_holder):
    button.set_pos([((current_w - button.size[0]) / 2), (
                (current_h - len(main_menu_holder) * (MAIN_MENU_SPACING + button.size[1])) / 2 + i * (MAIN_MENU_SPACING + button.size[1]))])



# --------------------- DECK SPRITE INIT ----------------------------- #
back_design_surface = pygame.image.load(GLOBAL().BACK_DESIGN_LOC).convert_alpha()
back_design_surface = pygame.transform.smoothscale_by(back_design_surface, 0.5)

card_count_font_obj = pygame.font.Font(GLOBAL().FONT_LOC, 32)
# --------------------- VIGNETTE INIT ----------------------------- #
VIGNETTE_FILE_LOC = "Game/Assets/General/Vignette.png"
vignette_surf = pygame.image.load(VIGNETTE_FILE_LOC).convert_alpha()
vignette_surf = pygame.transform.smoothscale(vignette_surf, [current_w, current_h]).convert_alpha()
vignette_surf.set_alpha(100)



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

    # CAM

    rect_cam_offset = pygame.Rect([75, 80, current_w-150, current_h])
    rect_cam_offset = GLOBAL().create_rect(rect_cam_offset)
    if not (rect_cam_offset.collidepoint(mouse_pos)):
        cam_to = ((mouse_pos[0] - CENTER[0]) * -CAM_DRAG_OFFSET, (mouse_pos[1] - CENTER[1]) * -CAM_DRAG_OFFSET)
        GLOBAL().camera_offset = (LerpFuncs.LERP(GLOBAL().camera_offset[0], cam_to[0], CAM_SPEED * GLOBAL().get_dt())), (
            LerpFuncs.LERP(GLOBAL().camera_offset[1], cam_to[1], CAM_SPEED * GLOBAL().get_dt()))

    else:
        GLOBAL().camera_offset = (LerpFuncs.LERP(GLOBAL().camera_offset[0], 0, CAM_SPEED * GLOBAL().get_dt())), (LerpFuncs.LERP(GLOBAL().camera_offset[1], 0, CAM_SPEED * GLOBAL().get_dt()))


    # SCREEN COLOR LERP

    c = color_bg_sys.update()

    screen.fill(c)
    screen.blit(vignette_surf, [0, 0])
    #

    screen.blit(vicinity_surface, GLOBAL().create_rect(vicinity_rect))

    if GLOBAL().current_screen == 1:
        screen.fill(main_screen_bg_color)
        # draw buttons
        for i, button in enumerate(main_menu_holder):
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
    if len(draw_deck.deck) <= 5:
        # combine discard and draw deck and reshuffle
        draw_deck.add_cards(discard_deck.deck)
        discard_deck.deck.clear()
        draw_deck.shuffle_deck()

    if len(draw_deck) == 0:
        running = False
        print("IMPLEMENT FINISH CONDITION")

    # Drawing the draw deck
    r = None
    for i in range(len(draw_deck)):
        r = pygame.Rect([20, (current_h - Card.HEIGHT) / 2 - i, Card.WIDTH, Card.HEIGHT])
        screen.blit(back_design_surface, GLOBAL().create_rect(r))
    card_hover_rect = r
    if card_hover_rect.collidepoint(mouse_pos):
        card_count_font_obj_s = card_count_font_obj.render(f"{len(draw_deck)} / 52", True, (0, 0, 0))
        r = pygame.Rect([card_hover_rect.topleft[0] + Card.WIDTH / 2 - card_count_font_obj_s.size[0] / 2, card_hover_rect.topleft[1] + Card.HEIGHT / 2 - card_count_font_obj_s.size[1] / 2, card_count_font_obj_s.size[0], card_count_font_obj_s.size[1]])
        screen.blit(card_count_font_obj_s, GLOBAL().create_rect(r))

    # Checking if clicked the button
    if clicked_button and not is_bogey_turn:
        not_selected = [].copy()
        not_selected.clear()
        for c in in_hand.deck:
            if c not in save_deck:
                not_selected.append(c)
        discard_deck.add_cards(not_selected.copy())
        in_hand.clear()
        in_hand.add_card(draw_deck.draw_card())
        is_bogey_turn = True


    # Draw cards and checking if the bogey has finished the turn
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
    else:
        is_card_in_vicinity = True

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



