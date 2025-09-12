import pygame

from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs

class Card:

    WIDTH = 200
    HEIGHT = 280
    SELECTED_SCALE_UP = 2.5/3.5 * 1.5
    SPEED = 5
    SCALE_UP_SPEED = 5


    def __init__(self, value: int, suit: int, pos: list[int] = None, rest_pos=None, speed=SPEED, scale_up_speed=SCALE_UP_SPEED):
        assert 0 <= suit <= 3
        # Suit will be CHaSeD order:
        #   0: Clubs
        #   1: Hearts
        #   2: Spades
        #   3: Diamonds

        assert 1 <= value <= 13
        # Value will be face value:
        #   1: Ace
        #   11: Jack
        #   12: Queen
        #   13: King
        self.suit = suit
        self.value = value
        self.surface = self.load_surface()
        if pos is None: pos = [0, 0]
        self.active = False
        self.x = pos[0]
        self.y = pos[1]
        self.speed = speed
        if rest_pos is None:
            rest_pos = [0, 0]
        self.rest_pos = rest_pos
        self.delta_time = GLOBAL().get_dt()
        self.priority = 0
        self.selected = False
        self.clicked = False
        self.current_scale = 1
        self.scale_up_speed = scale_up_speed

    def set_active(self, v: bool):
        self.active = v

    def draw(self, screen: pygame.Surface, pos: list[int] = None):
        if pos is None: pos = [self.x, self.y]
        screen.blit(self.surface, pos)

    def set_pos(self, pos: list[int], priority: int = 0):
        if priority < self.priority: return
        self.x = pos[0]
        self.y = pos[1]
        self.priority = priority


    def on_mouse_hover(self):
        if not GLOBAL().get_is_active():
            self.set_pos(LerpFuncs.LERPPos(self.get_pos(), [self.rest_pos[0], self.rest_pos[1]-30], self.speed*self.delta_time), 4)
        return

    def on_mouse_click(self):
        ...

    def on_mouse_release(self):
        self.active = False
        GLOBAL().set_is_active(False)
        GLOBAL().set_current(None)

        return

    def on_mouse_hold(self):
        if not GLOBAL().get_is_active():
            self.active = True
            GLOBAL().set_is_active(True)
            GLOBAL().set_current(self)
            self.selected = False
        return

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.value == other.value

    def update(self, screen):
        self.delta_time = GLOBAL().get_dt()
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_buttons_release = pygame.mouse.get_just_released()
        if self.get_rect().collidepoint(mouse_pos):
            self.on_mouse_hover()
            if mouse_buttons_release[0] == 1:
                self.on_mouse_release()
                self.clicked = False
            if mouse_buttons[0] == 1:
                move = False
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        self.on_mouse_hold()
                        move = True

                        break
                if GLOBAL().time_held < GLOBAL().CLICK_TIME and not move:
                    self.on_mouse_click()
                    if not self.clicked:
                        self.selected = not self.selected
                        self.clicked = True



        s = self.surface
        center_s = self.get_center()
        t = LerpFuncs.LERP(self.current_scale, 1, self.scale_up_speed*GLOBAL().get_dt())
        if self.selected:
            t = LerpFuncs.LERP(self.current_scale, Card.SELECTED_SCALE_UP, self.scale_up_speed*GLOBAL().get_dt())
        s = pygame.transform.scale_by(s, t)
        rect = s.get_rect(center=center_s)
        screen.blit(s, rect)
        self.current_scale = t
        self.priority = 0


    def get_pos(self):
        return [self.x, self.y]

    def get_rect(self):
        return self.surface.get_rect(center=(self.x+Card.WIDTH/2, self.y+Card.HEIGHT/2))

    def get_center(self):
        return self.x+Card.WIDTH/2, self.y+Card.HEIGHT/2

    def load_surface(self) -> pygame.Surface:
        # Card aspect ratio is 2.5/3.5
        if self.suit != 0:
            s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
            s.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(f"{self.value}, {self.suit}", True, (0,0,0))
            s.blit(text, [100, 140])
            return s
        s = GLOBAL().CLUBS_MANAGER.get(self.value, 0.5)

        return s

    def __repr__(self):
        return f"Value: {self.value}, Suit: {self.suit}"