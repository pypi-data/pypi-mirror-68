# coding=utf8


class Mapper:
    __keys = None

    def __init__(self):
        self._data = {}

    def register(self, key):
        def _inner(obj):
            self._data[key] = obj
            return obj

        return _inner

    def get(self, key):
        return self._data.get(key)


mr = Mapper()


@mr.register('hello')
class A:
    """XXX"""
    pass


print(A.__name__)
print(A.__doc__)
