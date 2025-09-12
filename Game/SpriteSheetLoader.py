import pygame

class SpriteSheetLoader:


    def __init__(self, sprite_sheet_location: str, dim: list[int]):
        self.sprite_sheet = pygame.image.load(sprite_sheet_location).convert_alpha()
        self.dim = dim




    def get_image(self, index, scale=1):
        img = pygame.Surface(self.dim, pygame.SRCALPHA).convert_alpha()
        img.blit(self.sprite_sheet.convert_alpha(), (0, 0), (index * self.dim[0], 0, self.dim[0], self.dim[1]))
        img = pygame.transform.scale_by(img, scale).convert_alpha()
        return img

    def get_image_2_index(self, index, scale=1):
        img = pygame.Surface(self.dim, pygame.SRCALPHA).convert_alpha()
        img.blit(self.sprite_sheet, (0, 0), (index[0] * self.dim[0], index[1] * self.dim[1], self.dim[0], self.dim[1]))
        img = pygame.transform.scale_by(img, scale)
        return img




