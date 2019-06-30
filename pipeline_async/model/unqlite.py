""""""

__all__ = ['UnqliteModel']

# Standard library modules.
import hashlib
import dataclasses

# Third party modules.
import unqlite

from loguru import logger

# Local modules.
from .base import ModelBase, keyfields

# Globals and constants variables.


class UnqliteModel(ModelBase):

    def __init__(self, filepath):
        self.db = unqlite.UnQLite(str(filepath))

    def _generate_key(self, data):
        key = hashlib.blake2s()
        key.update(self._get_table_name(data).encode('ascii'))

        for field in keyfields(data):
            value = getattr(data, field.name)

            if dataclasses.is_dataclass(field.type):
                key.update(self._generate_key(value))
            else:
                key.update(str(value).encode('ascii'))

        return key.hexdigest().encode('ascii')

    def _get_rowid(self, data):
        key = self._generate_key(data)
        try:
            return int(self.db.fetch(key))
        except KeyError:
            return None

    def exists(self, data):
        return self._get_rowid(data) is not None

    def add(self, data, check_exists=True):
        # Check if exists
        if hasattr(data, '_rowid'):
            return False

        if check_exists:
            rowid = self._get_rowid(data)
            if rowid is not None:
                return False

        # Create row
        row = {}
        for field in dataclasses.fields(data):
            name = field.name
            value = getattr(data, name)

            if dataclasses.is_dataclass(value):
                row[name + '_id'] = self.add(value, check_exists)
            else:
                row[name] = value

        # Insert
        table_name = self._get_table_name(data)
        collection = self.db.collection(table_name)
        collection.create()

        rowid = collection.store(row, return_id=True)
        logger.debug("Added output to table {}".format(table_name))

        # Insert key
        key = self._generate_key(data)
        self.db.store(key, rowid)

        data._rowid = rowid
        return True