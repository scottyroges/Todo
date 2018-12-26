import json


class Config(object):
    def __init__(self):
        with open('app/config.json') as f:
            self.config = json.load(f)

    def get(self, key):
        return self.config.get(key, None)


config = Config()
