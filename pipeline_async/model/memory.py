""""""

# Standard library modules.
import dataclasses

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

        # Add data from fields
        for field in dataclasses.fields(data):
            name = field.name
            value = getattr(data, name)

            if dataclasses.is_dataclass(value):
                self.add(value, check_exists)

        # Add actual data
        key = self._get_table_name(data)
        self.storage.setdefault(key, []).append(data)
        return True

    def get_alldata(self, dataclass):
        key = self._get_table_name(dataclass)
        return tuple(self.storage.get(key, []))