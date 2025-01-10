# this may be the most useless class ever
# :(
class Store:
    def __init__(self, init=None):
        if not init:
            init = {}
        self.main_dict = init

    def set(self, key: str, value: any):
        self.main_dict[key] = value
        return value

    def get(self, key: str):
        return self.main_dict.get(key)

    def __len__(self):
        return len(self.main_dict)

    def __iter__(self):
        return iter(self.main_dict)

    def __getitem__(self, item):
        return self.main_dict.get(item)

    def __setitem__(self, key, value):
        self.main_dict.__setitem__(key, value)

    def get_strict(self, key: str):
        return self.main_dict[key]

    def remove(self, key: str):
        del self.main_dict[key]

    def __contains__(self, item):
        return item in self.main_dict

    def has(self, key: str):
        return key in self.main_dict

    def clear(self):
        self.main_dict.clear()

    @property
    def size(self):
        return len(self.main_dict)
