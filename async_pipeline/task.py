""""""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class Task:

    def __init__(self, name):
        self.name = name

    def run(self, inputobj):
        raise NotImplementedError