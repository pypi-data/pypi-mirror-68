import json

from is_url import is_url

from .file import File


class P:
    def __init__(self, input):
        self._input = input

    @property
    def input(self):
        return self._input

    @property
    def is_string(self):
        return isinstance(self.input, str)

    @property
    def file(self):
        """
        :rtype: pobject.file.File
        """
        return File(self.input)

    @property
    def is_url(self):
        return is_url(self.input)

    @property
    def is_file_path(self):
        if self.is_string and ".yaml" in self.input:
            return True
        else:
            raise NotImplementedError

    def to_dict(self):
        if self.is_file_path:
            return self.file.to_dict()

    def to_json_string(self):
        output = json.dumps(self.input)
        return output
