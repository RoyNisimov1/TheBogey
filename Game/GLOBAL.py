

class GLOBAL:
    _instance = None



    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.is_card_active = False
            cls._instance.current = None
        return cls._instance

    def set_is_active(self, v: bool):
        self.is_card_active: bool = v

    def get_is_active(self):
        return self.is_card_active

    def set_current(self, card):
        self.current = card

    def get_current(self):
        return self.current
