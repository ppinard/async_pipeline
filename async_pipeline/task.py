""""""

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class Task:

    def __init__(self, name):
        self.name = name

    def run(self, inputdata):
        """
        Executes the task based on the provided *inputdata* and returns a :class:`list` of *outputdata*.
        The :meth:`run` method can be made `async` if needed.
        """
        return []