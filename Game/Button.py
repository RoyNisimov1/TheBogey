import pygame

from Game.GLOBAL import GLOBAL


class Button:

    @staticmethod
    def void_func_wrapper(*args, **kwargs):
        return

    def __init__(self, pos=None, text="", font="freesansbold.ttf", font_size=32, f=void_func_wrapper, bg_sprite = None, size=None):


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

    def set_f(self, f):
        self.function = f

    def update(self, screen: pygame.Surface, *args, **kwargs):
        if self.bg_sprite is None:
            s = pygame.Surface(self.size)
            s.fill((255, 255, 255))
        else:
            s = self.bg_sprite
        font = pygame.font.Font(self.font, self.font_size)
        text = font.render(self.text, True, (0, 0, 0), wraplength=400)
        s.blit(text, [(self.size[0]-len(self.text)*5)//2, self.size[1]//2])
        mouse_pos = pygame.mouse.get_pos()
        r = None
        if self.get_rect().collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                if self.function is not None:
                    r = self.function(*args, **kwargs)
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        if self.clicked:
            s = pygame.transform.scale_by(s, 0.95)
        scaled_rect = s.get_rect(center=self.get_center())
        screen.blit(s, GLOBAL().create_rect(scaled_rect))
        return r

    def set_pos(self, pos: list[int]):
        self.pos = pos

    def get_center(self):
        return [self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2]

    def get_rect(self):
        if self.bg_sprite is not None:
            return self.bg_sprite.get_rect(center=[self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2])
        return pygame.Rect([self.pos[0], self.pos[1], self.size[0], self.size[1]])
