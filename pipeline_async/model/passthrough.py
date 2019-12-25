""""""

__all__ = ['PassThroughModel']

# Standard library modules.

# Third party modules.

# Local modules.
from pipeline_async.model.base import ModelBase

# Globals and constants variables.

class PassThroughModel(ModelBase):
    def exists(self, data):
        return False

    def add(self, data, check_exists=True):
        return False