""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pipeline_async.pipeline import Pipeline
import mock

# Globals and constants variables.

@pytest.mark.parametrize('pipeline,expected_success', [
    (Pipeline([mock.PlantMagnoliaTask(1, 'Magnolia grandiflora')]), 1),
    (Pipeline([mock.PlantMagnoliaTask(1, 'Magnolia grandiflora'), mock.PlantMagnoliaTask(2, 'Magnolia iltisiana')]), 2),
    (Pipeline([mock.FailedTask()]), 0),
    (Pipeline([mock.PlantMagnoliaTask(1, 'Magnolia grandiflora'), mock.FailedTask()]), 1),
])
@pytest.mark.asyncio
async def test_pipeline_run(pipeline, expected_success):
    success_tasks = await pipeline.run(progress=False)

    assert len(success_tasks) == expected_success
