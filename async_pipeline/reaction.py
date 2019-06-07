""""""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class Reaction:

    def __init__(self, name):
        self.name = name

    def process(self, reactant):
        raise NotImplementedError