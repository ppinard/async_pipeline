""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pipeline_async.model import SqlModel
from pipeline_async.task import Task
import mock

# Globals and constants variables.


class ArithmeticModelTask(Task):
    def __init__(self, name, model=None):
        super().__init__(name, model, mock.ArithmeticOutput)

    def _run(self, inputdata):
        return [mock.ArithmeticOutput(inputdata.x + inputdata.y), mock.ArithmeticOutput(inputdata.x - inputdata.y)]


def test_task_run_nomodel():
    task = ArithmeticModelTask("arithmetic")

    inputdata = mock.ArithmeticInput(3, 4)
    list_outputdata = task.run(inputdata)
    assert len(list_outputdata) == 2


def test_task_run(sqlmodel):
    task = ArithmeticModelTask("arithmetic", sqlmodel)

    # Run once
    inputdata = mock.ArithmeticInput(3, 4)
    list_outputdata = task.run(inputdata)
    assert len(list_outputdata) == 2

    list_outputdata = sqlmodel.find("arithmetic", inputdata, mock.ArithmeticOutput)
    assert len(list_outputdata) == 2

    # Run again, but no new data is added
    list_outputdata = task.run(inputdata)
    assert len(list_outputdata) == 2

    list_outputdata = sqlmodel.find("arithmetic", inputdata, mock.ArithmeticOutput)
    assert len(list_outputdata) == 2


