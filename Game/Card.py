import pygame

class Card:

    WIDTH = 200
    HEIGHT = 280

    def __init__(self, value: int, suit: int, pos: list[int] = None):
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

        self.x = pos[0]
        self.y = pos[1]

    def draw(self, screen: pygame.Surface, pos: list[int] = None):
        if pos is None: pos = [self.x, self.y]
        screen.blit(self.surface, pos)

    def set_pos(self, pos: list[int]):
        self.x = pos[0]
        self.y = pos[1]

    def update(self, screen):
        pos = [self.x, self.y]
        screen.blit(self.surface, pos)

    def get_pos(self):
        return [self.x, self.y]

    def get_rect(self):
        return self.surface.get_rect(topleft=(self.x, self.y))

    def load_surface(self) -> pygame.Surface:
        # Card aspect ratio is 2.5/3.5
        s = pygame.Surface([Card.WIDTH, Card.HEIGHT])
        s.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f"{self.value}, {self.suit}", True, (0,0,0))
        s.blit(text, [100, 140])
        return s

    def __repr__(self):
        return f"Value: {self.value}, Suit: {self.suit}"