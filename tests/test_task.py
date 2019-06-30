""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pipeline_async.task import Task
import mock

# Globals and constants variables.


@pytest.mark.asyncio
async def test_task_run_nomodel():
    task = mock.PlantMagnoliaTask(1, 'Magnolia grandiflora')
    assert await task.run()
    assert await task.run() # No check that result was previously calculated



