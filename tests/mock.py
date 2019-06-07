import asyncio
import dataclasses

from async_pipeline.task import Task

@dataclasses.dataclass
class AdditionInput:
    x: float
    y: float

@dataclasses.dataclass
class AdditionOutput:
    x: float
    y: float
    value: float

@dataclasses.dataclass
class PowerInput:
    x: float

@dataclasses.dataclass
class PowerOutput:
    x: float
    value: float

class AdditionTask(Task):

    async def run(self, inputobj):
        return [AdditionOutput(inputobj.x, inputobj.y, inputobj.x + inputobj.y)]

class AdditionOutputToPowerInputTask(Task):

    async def run(self, inputobj):
        return [PowerInput(inputobj.value)]

class SquarePowerTask(Task):

    def run(self, inputobj):
        return [PowerOutput(inputobj.x, inputobj.x ** 2)]

class FailedTask(Task):

    def run(self, inputobj):
        raise RuntimeError('Task has failed')

class FailedAsyncTask(Task):

    async def run(self, inputobj):
        raise RuntimeError('Task has failed')