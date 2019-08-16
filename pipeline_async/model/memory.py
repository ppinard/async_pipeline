""""""

# Standard library modules.

# Third party modules.

# Local modules.
from .base import ModelBase

# Globals and constants variables.

class MemoryModel(ModelBase):

    def __init__(self):
        self.storage = {}

    def exists(self, data):
        key = self._get_table_name(data)
        return data in self.storage.get(key, [])

    def add(self, data, check_exists=True):
        if check_exists and self.exists(data):
            return False

        key = self._get_table_name(data)
        self.storage.setdefault(key, []).append(data)
        return True

    def get_alldata(self, dataclass):
        key = self._get_table_name(dataclass)
        return tuple(self.storage.get(key, []))