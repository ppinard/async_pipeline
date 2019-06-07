import pytest

from async_pipeline.pipeline import Pipeline
import mock

@pytest.mark.parametrize('pipeline,expected_value', [
    (Pipeline([mock.AdditionTask('addition')]), 7),
    (Pipeline([mock.AdditionTask('addition'), mock.AdditionOutputToPowerInputTask('convert'), mock.SquarePowerTask('power')]), 49)
])
@pytest.mark.asyncio
async def test_pipeline_run(pipeline, expected_value):
    inputdata = mock.AdditionInput(3, 4)
    list_outputdata = await pipeline.run(inputdata)

    assert len(list_outputdata) == 1
    assert list_outputdata[0].value == expected_value

@pytest.mark.parametrize('pipeline', [
    Pipeline([mock.FailedTask('failed')]),
    Pipeline([mock.FailedAsyncTask('failed')])
])
@pytest.mark.asyncio
async def test_pipeline_run_failed(pipeline):
    with pytest.raises(RuntimeError):
        inputdata = mock.AdditionInput(3, 4)
        await pipeline.run(inputdata)