import pygame


class Button:

    @staticmethod
    def void_func_wrapper():
        return

    def __init__(self, pos=None, text="", font=None, f=void_func_wrapper, bg_sprite = None, size=None):
        self.bg_sprite: pygame.Surface = bg_sprite

        if size is None:
            size = [50, 30]
        self.size = size
        if font is None:
            font = ["freesansbold.ttf", 32]
        if pos is None: pos = [0, 0]
        self.pos = pos
        self.text = text
        self.function = f
        self.font = font
        self.clicked = False

    def update(self, screen: pygame.Surface):
        if self.bg_sprite is None:
            s = pygame.Surface(self.size)
            s.fill((255, 255, 255))
        else:
            s = self.bg_sprite
        font = pygame.font.Font(self.font[0], self.font[1])
        text = font.render(self.text, True, (0, 0, 0))
        s.blit(text, [100, 140])
        mouse_pos = pygame.mouse.get_pos()
        if self.get_rect().collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.function()
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0: self.clicked = False
        screen.blit(s)

    def get_rect(self):
        if self.bg_sprite is not None:
            return self.bg_sprite.get_rect(top_left=self.pos)
        return pygame.Rect([self.pos[0], self.pos[1], self.size[0], self.size[1]])
