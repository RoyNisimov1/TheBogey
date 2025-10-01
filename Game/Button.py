import pygame

from Game.GLOBAL import GLOBAL
from Game.LerpFuncs import LerpFuncs


class Button:

    UP = 20
    SPEED = 20

    @staticmethod
    def void_func_wrapper(*args, **kwargs):
        return

    def __init__(self, pos=None, text="", font="freesansbold.ttf", font_size=32, f=void_func_wrapper, bg_sprite = None, size=None, color=(0, 0, 0), hover_color=(0, 0, 0), text_color=(0, 0, 0)):
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        if size is None:
            size = [50, 30]
        self.size = size
        self.font_size = font_size
        if pos is None: pos = [0, 0]
        self.pos = pos
        if bg_sprite != None:
            bg_sprite = pygame.transform.smoothscale(bg_sprite, size)
        self.bg_sprite: pygame.Surface = bg_sprite
        self.text = text
        self.function = f
        self.font = font
        self.clicked = False
        font = pygame.font.Font(self.font, self.font_size)
        text = font.render(self.text, True, self.color)
        self.font_surface = text
        self.rendered_bg = None
        self.hover = False
        self.move_to_pos = self.pos.copy()
        self.move_to_pos = (self.move_to_pos[0], self.move_to_pos[1] - Button.UP)
        self.rest_pos = self.pos.copy()


    def create_render_bg(self):
        if self.bg_sprite is None:
            if not self.hover:
                s = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
                r = s.get_rect()
                pygame.draw.rect(s, self.color, r, border_radius=12)
            else:
                s = pygame.Surface(self.size, pygame.SRCALPHA).convert_alpha()
                r = s.get_rect()
                pygame.draw.rect(s, self.hover_color, r, border_radius=12)
        else:
            s = self.bg_sprite
        font = pygame.font.Font(self.font, self.font_size)
        text = font.render(self.text, True, self.text_color)
        r = text.get_rect()
        r.center = self.size[0] / 2, self.size[1] / 2
        s.blit(text, r)
        self.rendered_bg = s


    def set_f(self, f):
        self.function = f

    def update(self, screen: pygame.Surface, *args, **kwargs):
        if self.rendered_bg is None:
            self.create_render_bg()
        s = self.rendered_bg
        mouse_pos = pygame.mouse.get_pos()
        r = None
        colliding = self.get_rect().collidepoint(mouse_pos)
        if self.hover != colliding:
            self.hover = self.get_rect().collidepoint(mouse_pos)
            self.create_render_bg()
        if self.hover:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                if self.function is not None:
                    r = self.function(*args, **kwargs)
            self.pos = LerpFuncs.LERPPos(self.pos, self.move_to_pos, GLOBAL().get_dt()*Button.SPEED)
        else:
            self.pos = LerpFuncs.LERPPos(self.pos, self.rest_pos, GLOBAL().get_dt()*Button.SPEED)


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if self.clicked:
            s = pygame.transform.scale_by(s, 0.95)
        scaled_rect = s.get_rect(center=self.get_center())
        screen.blit(s, GLOBAL().create_rect(scaled_rect))
        return r

    def set_pos(self, pos: list[int]):
        self.pos = pos
        self.move_to_pos = self.pos.copy()
        self.move_to_pos = (self.move_to_pos[0], self.move_to_pos[1] - Button.UP)
        self.rest_pos = self.pos.copy()

    def get_center(self):
        return [self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2]

    def get_rect(self):
        if self.bg_sprite is not None:
            return self.bg_sprite.get_rect(center=[self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2])
        return pygame.Rect([self.pos[0], self.pos[1], self.size[0], self.size[1]])
