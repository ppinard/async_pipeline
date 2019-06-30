""""""

__all__ = ['PassThroughModel']

# Standard library modules.

# Third party modules.

# Local modules.
from .base import ModelBase

# Globals and constants variables.

class PassThroughModel(ModelBase):
    def exists(self, data, check_exists=True):
        return False

    def add(self, data):
        return []