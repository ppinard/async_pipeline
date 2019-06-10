""""""

# Standard library modules.
import abc

# Third party modules.

# Local modules.
from .model import PassThroughModel

# Globals and constants variables.

class Task(metaclass=abc.ABCMeta):

    def __init__(self, name, model=None, outputdataclass=None):
        self.name = name

        if model is None:
            model = PassThroughModel()
        self.model = model

        self.outputdataclass = outputdataclass

    def run(self, inputdata):
        """
        Executes the task based on the provided *inputdata* and returns a :class:`list` of *outputdata*.
        """
        # Check if already exists.
        list_outputdata = self.model.find(self.name, inputdata, self.outputdataclass)
        if list_outputdata:
            return list_outputdata

        # Run.
        list_outputdata = self._run(inputdata)

        # Add to model.
        self.model.add(self.name, inputdata, *list_outputdata)

        return list_outputdata

    @abc.abstractmethod
    def _run(self, inputdata): # pragma: no cover
        raise NotImplementedError