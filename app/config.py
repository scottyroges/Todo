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
        if not os.environ.get("name"):
            file = file_project_path('../config.json')
            print("WARNING: no config found so trying to load from local")
            print("looking for file at %s" % file)
            with open(file) as f:
                file_config = json.load(f)
                for key, val in file_config.items():
                    os.environ[key] = val

    def get(self, key):
        return os.environ.get(key)


config = Config()
