import pygame
from Game.CardsAssetManager import CardsAssetManager


class GLOBAL:
    _instance = None



    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.is_card_active = False
            cls._instance.current = None
            cls._instance.time_held = 0.0
            cls._instance.CLUBS_ASSET_LOC = "Game/Assets/Clubs"
            cls._instance.CLUBS_MANAGER = CardsAssetManager(cls._instance.CLUBS_ASSET_LOC)
        return cls._instance

    def set_is_active(self, v: bool):
        self.is_card_active: bool = v

    def get_is_active(self):
        return self.is_card_active

    def set_current(self, card):
        self.current = card

    def get_current(self):
        return self.current

    def update_mouse(self, delta_time: float):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]: self.time_held += delta_time
        else:
            self.time_held = 0
