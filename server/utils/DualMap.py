from bidict import bidict


class DualMap:
    def __init__(self, data):
        self.__map = bidict(data)

    def is_valid_key(self, key):
        return key in self.__map

    def is_valid_value(self, value):
        return value in self.__map.inverse

    def to_key_either(self, value):
        if value in self.__map:
            return value

        if value in self.__map.inverse:
            return self.to_key(value)

        return None

    def to_key(self, value):
        return self.__map.inverse[value]

    def to_value(self, key):
        return self.__map[key]

    def values(self):
        return self.__map.values()

    def keys(self):
        return self.__map.keys()

    def minimum_key(self):
        return min(self.__map.keys())

    def maximum_key(self):
        return max(self.__map.keys())

    def to_dict(self):
        return {k: v for k, v in self.__map.items()}

    def to_reverse_dict(self):
        return {v: k for k, v in self.__map.items()}
