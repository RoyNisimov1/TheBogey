import pygame


class CardsAssetManager:

    def __init__(self, src: str):
        self.src = src

    def get(self, index: int = 0, scale=1):
        img = pygame.image.load(self.src + f"/{index}.png").convert_alpha()
        img = pygame.transform.scale_by(img, scale)
        return img
