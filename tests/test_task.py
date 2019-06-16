""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pipeline_async.model import SqlModel
from pipeline_async.task import Task
import mock

# Globals and constants variables.


@pytest.mark.asyncio
async def test_task_run_nomodel():
    task = mock.ArithmeticTask(3, 4)
    assert await task.run()
    assert await task.run() # No check that result was previously calculated


@pytest.mark.asyncio
async def test_task_run(sqlmodel):
    # Run once
    task = mock.ArithmeticTask(3, 4, sqlmodel)
    assert await task.run()

    print(id(mock.ArithmeticData(3, 4)), id(mock.PowerData(3)), id(mock.PowerData(3)))

    assert sqlmodel.exists(mock.ArithmeticData(3, 4))
    print(sqlmodel._get_row(mock.PowerData(3)))
    assert not sqlmodel.exists(mock.PowerData(3))

    # Run again, but no new data is added
    task = mock.ArithmeticTask(3, 4, sqlmodel)
    assert not await task.run()


