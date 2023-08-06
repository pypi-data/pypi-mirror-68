from pathlib import Path
import yaml


class File:
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def path_object(self):
        return Path(self.path)

    @property
    def text(self):
        return self.path_object.read_text()

    @property
    def is_yaml(self):
        return ".yaml" in self.path

    def to_dict(self):
        if self.is_yaml:
            return yaml.safe_load(self.text)
        else:
            raise NotImplementedError
