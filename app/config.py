import json
import os


def file_project_path(filename):
    # its important that this lives in the root of the project
    # would be great to find a better way to do this,
    # but for now this works
    # could potentially use flasks built in config
    return os.path.dirname(os.path.abspath(__file__)) + "/" + filename


class Config(object):
    def __init__(self):
        with open(file_project_path('config.json')) as f:
            self.config = json.load(f)

    def get(self, key):
        return self.config.get(key, None)


config = Config()
