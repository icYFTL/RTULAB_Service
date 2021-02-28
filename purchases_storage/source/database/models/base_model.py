from copy import copy


class BaseModel:
    # def __dict__(self): # Eh, I can't redeclare the __dict__
    #     pass

    def get_dict(self):
        # if not issubclass(self.__class__, Base.__class__):  # https://ru.stackoverflow.com/questions/1242976/python3-sqlalchemy-%d1%8f%d0%b2%d0%bb%d1%8f%d0%b5%d1%82%d1%81%d1%8f-%d0%bb%d0%b8-%d0%ba%d0%bb%d0%b0%d1%81%d1%81-%d0%bc%d0%be%d0%b4%d0%b5%d0%bb%d1%8c%d1%8e
        #     raise TypeError("Not a sqlaclhemy based")

        _vars = copy(vars(self))
        for x in list(_vars):
            if x.startswith('_') or callable(getattr(self, x)) or x == 'metadata':
                _vars.pop(x)

        return _vars
