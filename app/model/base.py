class BaseModel:
    def __init__(self, **kwargs):
        self.prepare()

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(self.__dict__)
