

class GLOBAL:
    _instance = None

    isCardActive = False


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

