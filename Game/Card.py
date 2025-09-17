
import math
from typing import Any

import pygame

from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs

class Card:

    WIDTH = 200
    HEIGHT = 280
    SELECTED_SCALE_UP = 1.1
    BASE_SCALE = 0.5
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
        self.surface = self.get_surface_og()
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
        self.scale_up_speed = scale_up_speed
        self.rotation = 0 # in degs




    def collides_with_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.get_rect().collidepoint(mouse_pos)

    def set_active(self, v: bool):
        self.active = v


    def set_pos(self, pos: list[int], priority: int = 0):
        if priority < self.priority: return
        self.x = pos[0]
        self.y = pos[1]
        self.priority = priority




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

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_buttons_release = pygame.mouse.get_just_released()
        if mouse_buttons_release[0] == 1:
            self.on_mouse_release()
            self.clicked = False

        if self.collides_with_mouse():
            self.on_mouse_hover()
            if mouse_buttons[0] == 1:
                move = False
                if GLOBAL().is_mouse_moving:
                    self.on_mouse_hold()
                    move = True
                if GLOBAL().time_held < GLOBAL().CLICK_TIME and not move:
                    self.on_mouse_click()
                    if not self.clicked:
                        self.selected = not self.selected
                        self.clicked = True
        s = self.surface
        center_s = self.get_center()

        if self.selected:
            self.lerp_pos((self.rest_pos[0], self.rest_pos[1] - 40), 3, rot_speed=0)

        s = pygame.transform.rotate(s, self.rotation)
        rect = s.get_rect(center=center_s)
        screen.blit(s, rect)
        self.priority = 0

    def lerp_pos(self, pos, priority, speed=0.1, rot_speed=GLOBAL().get_dt_rot_speed()):
        if priority < self.priority:
            return
        p = LerpFuncs.LERPPos(self.get_pos(), pos, speed)
        r = 0
        if rot_speed != 0:
            diff = pos[0] - self.get_center()[0]
            if diff > 0:
                r = -GLOBAL().TORQUE
            elif diff < 0:
                r = GLOBAL().TORQUE
        if rot_speed == 0:
            rot_speed = GLOBAL().get_dt_rot_speed()
        self.rotation = LerpFuncs.LERP(self.rotation, r, rot_speed)
        self.set_pos(p, priority)

    def on_mouse_hover(self):
        if not GLOBAL().get_is_active():
            self.lerp_pos([self.rest_pos[0], self.rest_pos[1]-30], priority=3, rot_speed=0)
        return

    def __lt__(self, other) -> bool:
        if type(other) != type(self):
            return False
        if self.suit > other.suit: return False
        if self.suit < other.suit: return True
        if GLOBAL().high_to_low:
            return self.value > other.value
        return self.value < other.value


    def get_surface_size(self, size):
        s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
        s.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"{self.value}, {self.suit}", True, (0,0,0))
        s.blit(text, [100, 140])

        if self.suit == 0:
            s = GLOBAL().CLUBS_MANAGER.get(self.value, size)
        elif self.suit == 1:
            s = GLOBAL().HEARTS_MANAGER.get(self.value, size)
        return s

    def get_surface_og(self):
        s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
        s.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"{self.value}, {self.suit}", True, (0,0,0))
        s.blit(text, [100, 140])

        if self.suit == 0:
            s = GLOBAL().CLUBS_MANAGER.get(self.value, 0.5)
        elif self.suit == 1:
            s = GLOBAL().HEARTS_MANAGER.get(self.value, 0.5)
        return s


    def get_pos(self):
        return self.x, self.y

    def get_rect(self):
        return pygame.Rect([self.get_pos()[0], self.get_pos()[1], Card.WIDTH, Card.HEIGHT])

    def get_center(self):
        return self.x+Card.WIDTH/2, self.y+Card.HEIGHT/2

    def load_surface(self) -> pygame.Surface:
        # Card aspect ratio is 2.5/3.5
        s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
        s.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"{self.value}, {self.suit}", True, (0, 0, 0))
        s.blit(text, [100, 140])

        if self.suit == 0:
            s = GLOBAL().CLUBS_MANAGER.get(self.value, 0.5)
        elif self.suit == 1:
            s = GLOBAL().HEARTS_MANAGER.get(self.value, 0.5)
        return s

    def __repr__(self):
        return f"Value: {self.value}, Suit: {self.suit}"