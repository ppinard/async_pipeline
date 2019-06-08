import asyncio
import dataclasses

from async_pipeline.task import Task

@dataclasses.dataclass
class AdditionInput:
    x: float
    y: float

@dataclasses.dataclass
class AdditionOutput:
    value: float

@dataclasses.dataclass
class PowerInput:
    x: float

@dataclasses.dataclass
class PowerOutput:
    value: float

class ArithmeticTask(Task):

    async def run(self, inputdata):
        return [AdditionOutput(inputdata.x + inputdata.y), AdditionOutput(inputdata.x - inputdata.y)]

class AdditionOutputToPowerInputTask(Task):

    async def run(self, inputdata):
        return [PowerInput(inputdata.value)]

class PowerTask(Task):

    def run(self, inputdata):
        return [PowerOutput(inputdata.x ** 2), PowerOutput(inputdata.x ** 3)]

class FailedTask(Task):

    def run(self, inputdata):
        raise RuntimeError('Task has failed')

class FailedAsyncTask(Task):

    async def run(self, inputdata):
        raise RuntimeError('Task has failed')