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
            cls._instance.high_to_low = True
            cls._instance.BUTTON_OR_BG_SURFACE_LOC = "Game/Assets/General/button or surface.png"
            cls._instance.BG_SURFACE_LOC = "Game/Assets/General/Wide bg.png"
            cls._instance.BACK_DESIGN_LOC = "Game/Assets/General/Back Design.png"
            cls._instance.BLOB_LOC = "Game/Assets/General/Blob.png"
            cls._instance.FONT_LOC = "Game/Assets/Fonts/Barriecito-Regular.ttf"
            cls._instance.CLUBS_ASSET_LOC = "Game/Assets/Clubs"
            cls._instance.CLUBS_MANAGER = CardsAssetManager(cls._instance.CLUBS_ASSET_LOC)
            cls._instance.HEARTS_ASSET_LOC = "Game/Assets/Hearts"
            cls._instance.HEARTS_MANAGER = CardsAssetManager(cls._instance.HEARTS_ASSET_LOC)
            cls._instance.BASE_SPEED = 10
            cls._instance.ROTATION_SPEED = 20
            cls._instance.TORQUE = 30
            cls._instance.delta_time = 0.1
            cls._instance.CLICK_TIME = 0.09
            cls._instance.is_mouse_moving = False
            cls._instance.current_screen = 0
            cls._instance.running = True
        return cls._instance

    def get_dt_base(self):
        return self.BASE_SPEED * self.get_dt()



    def get_dt_rot_speed(self):
        return self.ROTATION_SPEED * self.get_dt()

    def set_dt(self, dt: float):
        self.delta_time = dt

    def get_dt(self): return self.delta_time

    def set_is_active(self, v: bool):
        self.is_card_active: bool = v

    def get_is_active(self):
        return self.is_card_active

    def set_current(self, card):
        self.current = card

    def get_current(self):
        return self.current

    @staticmethod
    def get_center(r: list[int]):
        return [r[0] + r[2] / 2, r[1] + r[3] / 2]




    def update_mouse(self):
        delta_time = self.delta_time
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]: self.time_held += delta_time
        else:
            self.time_held = 0
