class GlobalStore:
    main_dict = {}

    def set(self, key: str, value: any):
        self.main_dict[key] = value
        return value

    def get(self, key: str):
        return self.main_dict.get(key)

    def get_strict(self, key: str):
        return self.main_dict[key]

    def remove(self, key: str):
        del self.main_dict[key]

    def has(self, key: str):
        return key in self.main_dict

    def clear(self):
        self.main_dict.clear()

    @property
    def size(self):
        return len(self.main_dict)
