import pygame

class Card:
    def __init__(self, value: int, suit: int):
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

    def draw(self, screen: pygame.display, pos: list[int] = None):
        if pos is None: pos = [0, 0]
        screen.blit(self.surface, pos)



    def load_surface(self) -> pygame.Surface:
        # Card aspect ratio is 2.5/3.5
        s = pygame.Surface([200, 280])
        s.fill((255, 255, 255))
        return s

    def __repr__(self):
        return f"Value: {self.value}, Suit: {self.suit}"