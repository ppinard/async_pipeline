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
        """
        return []

class ModelTask(Task):

    def __init__(self, name, model, outputdataclass):
        super().__init__(name)
        self.model = model
        self.outputdataclass = outputdataclass

    def run(self, inputdata):
        # Check if already exists.
        list_outputdata = self.model.find(self.name, inputdata, self.outputdataclass)
        if list_outputdata:
            return list_outputdata

        # Run.
        list_outputdata = self._run(inputdata)

        # Add to model.
        self.model.add(self.name, inputdata, *list_outputdata)

        return list_outputdata

    def _run(self, inputdata):
        return []