""""""

# Standard library modules.

# Third party modules.
import pytest
import attr

# Local modules.
from pipeline_async.task import Task

# Globals and constants variables.

@attr.s
class ArithmeticData:
    x: float = attr.ib(metadata={"key": True})
    y: float = attr.ib(metadata={"key": True})
    value: float = attr.ib(default=None)


@attr.s
class PowerData:
    x: float = attr.ib(metadata={"key": True})
    value: float = attr.ib(default=None)


class ArithmeticTask(Task):
    def __init__(self, x, y, model=None):
        super().__init__(model)
        self.x = x
        self.y = y

    async def run(self):
        if self.model.exists(ArithmeticData(self.x, self.y)):
            return False

        self.model.add(ArithmeticData(self.x, self.y, self.x + self.y))
        self.model.add(ArithmeticData(self.x, self.y, self.x - self.y))

        return True

    @property
    def name(self):
        return '{}+{}'.format(self.x, self.y)


class PowerTask(Task):
    def __init__(self, x, model=None):
        super().__init__(model)
        self.x = x

    async def run(self):
        if self.model.exists(PowerData(self.x)):
            return False

        self.model.add(PowerData(self.x ** 2))

        return True

    @property
    def name(self):
        return '{}**2'.format(self.x)

class FailedTask(Task):
    async def run(self):
        raise RuntimeError("Task has failed")

    @property
    def name(self):
        return 'failed'

