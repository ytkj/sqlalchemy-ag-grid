class Const:
    def __setattr__(self, key, value):
        self.__dict__[key] = value
