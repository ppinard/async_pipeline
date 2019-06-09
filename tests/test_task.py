""""""

# Standard library modules.

# Third party modules.

# Local modules.
from pipeline_async.model import SqlModel
from pipeline_async.task import ModelTask
import mock

# Globals and constants variables.


class ArithmeticModelTask(ModelTask):
    def _run(self, inputdata):
        return [
            mock.ArithmeticOutput(inputdata.x + inputdata.y),
            mock.ArithmeticOutput(inputdata.x - inputdata.y),
        ]


def test_modeltask_run(sqlmodel):
    task = ArithmeticModelTask("arithmetic", sqlmodel)

    inputdata = mock.ArithmeticInput(3, 4)
    list_outputdata = task.run(inputdata)
    assert len(list_outputdata) == 2

    list_outputdata = sqlmodel.find("arithmetic", inputdata)
    assert len(list_outputdata) == 2

