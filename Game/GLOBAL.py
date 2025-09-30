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
            cls._instance.BUTTON_LOC = "Game/Assets/General/Button.png"
            cls._instance.BUTTON_SURFACE = pygame.image.load(cls._instance.BUTTON_LOC).convert_alpha()
            cls._instance.BUTTON_250_90_LOC = "Game/Assets/General/Button250-90.png"
            cls._instance.BUTTON_250_90_SURFACE = pygame.image.load(cls._instance.BUTTON_250_90_LOC).convert_alpha()
            cls._instance.BG_SURFACE_LOC = "Game/Assets/General/Wide bg.png"
            cls._instance.BACK_DESIGN_LOC = "Game/Assets/General/Back Design.png"
            cls._instance.EMPTY_DECK_DESIGN_LOC = "Game/Assets/General/Empty Deck.png"
            cls._instance.EMPTY_DECK_SURFACE = pygame.image.load(cls._instance.EMPTY_DECK_DESIGN_LOC).convert_alpha()
            cls._instance.EMPTY_DECK_SURFACE_SCALED_DOWN_05 = pygame.transform.smoothscale_by(cls._instance.EMPTY_DECK_SURFACE, 0.5)
            cls._instance.BLOB_LOC = "Game/Assets/General/Blob.png"
            cls._instance.FONT_LOC = "Game/Assets/Fonts/Barriecito-Regular.ttf"
            cls._instance.CLUBS_ASSET_LOC = "Game/Assets/Clubs"
            cls._instance.CLUBS_MANAGER = CardsAssetManager(cls._instance.CLUBS_ASSET_LOC)
            cls._instance.HEARTS_ASSET_LOC = "Game/Assets/Hearts"
            cls._instance.HEARTS_MANAGER = CardsAssetManager(cls._instance.HEARTS_ASSET_LOC)
            cls._instance.SPADES_ASSET_LOC = "Game/Assets/Spades"
            cls._instance.SPADES_MANAGER = CardsAssetManager(cls._instance.SPADES_ASSET_LOC)
            cls._instance.BASE_SPEED = 10
            cls._instance.ROTATION_SPEED = 20
            cls._instance.TORQUE = 30
            cls._instance.delta_time = 0.1
            cls._instance.CLICK_TIME = 0.09
            cls._instance.is_mouse_moving = False
            cls._instance.current_screen = 0
            cls._instance.running = True

            cls._instance.camera_offset = (0,0)

        return cls._instance

    def create_rect(self, rect: pygame.rect.Rect):
        r = pygame.rect.Rect([rect.topleft[0] + self.camera_offset[0], rect.topleft[1] + self.camera_offset[1], rect.size[0], rect.size[1]])
        return r

    def set_dim(self, w, h):
        self.current_w = w
        self.current_h = h

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
