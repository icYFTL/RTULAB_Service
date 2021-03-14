from copy import copy


class BaseModel:
    def get_dict(self):
        _vars = copy(vars(self))
        for x in list(_vars):
            if x.startswith('_') or callable(getattr(self, x)) or x == 'metadata':
                _vars.pop(x)

        return _vars
