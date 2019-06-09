import asyncio
import dataclasses

from pipeline_async.task import Task


@dataclasses.dataclass
class ArithmeticInput:
    x: float = dataclasses.field(metadata={"key": True})
    y: float = dataclasses.field(metadata={"key": True})


@dataclasses.dataclass
class ArithmeticOutput:
    value: float = None


@dataclasses.dataclass
class PowerInput:
    x: float = dataclasses.field(metadata={"key": True})


@dataclasses.dataclass
class PowerOutput:
    value: float


class ArithmeticTask(Task):
    def run(self, inputdata):
        return [
            ArithmeticOutput(inputdata.x + inputdata.y),
            ArithmeticOutput(inputdata.x - inputdata.y),
        ]


class ArithmeticOutputToPowerInputTask(Task):
    def run(self, inputdata):
        return [PowerInput(inputdata.value)]


class PowerTask(Task):
    def run(self, inputdata):
        return [PowerOutput(inputdata.x ** 2), PowerOutput(inputdata.x ** 3)]


class FailedTask(Task):
    def run(self, inputdata):
        raise RuntimeError("Task has failed")

