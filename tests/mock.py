# Standard library modules.
import asyncio
import dataclasses
import datetime

# Third party modules.

# Local modules.
from pipeline_async.task import Task

# Globals and constants variables.


@dataclasses.dataclass
class TaxonomyData:
    kingdom: str = dataclasses.field(metadata={"key": True})
    order: str = dataclasses.field(metadata={"key": True})
    family: str = dataclasses.field(metadata={"key": True})
    genus: str = dataclasses.field(metadata={"key": True})

@dataclasses.dataclass
class TreeData:
    serial_number: int = dataclasses.field(metadata={"key": True})
    taxonomy: TaxonomyData = dataclasses.field(metadata={"key": True})
    specie: str = dataclasses.field(metadata={'key': True})
    diameter_m: float = None
    long_description: bytes = None
    has_flower: bool = None
    plantation_datetime: datetime.datetime = None
    last_pruning_date: datetime.date = None


class PlantMagnoliaTask(Task):
    def __init__(self, serial_number, specie, model=None):
        super().__init__(model)
        self.serial_number = serial_number
        self.specie = specie

    async def run(self):
        taxonomy = TaxonomyData('plantae', 'magnoliales', 'magnoliaceae', 'magnolia')
        treedata = TreeData(self.serial_number, taxonomy, self.specie)

        if self.model.exists(treedata):
            return False

        treedata.diameter_m = 0.1
        treedata.long_description = 'As with all Magnoliaceae, the perianth is undifferentiated, with 9–15 tepals in 3 or more whorls. The flowers are bisexual with numerous adnate carpels and stamens are arranged in a spiral fashion on the elongated receptacle. The fruit dehisces along the dorsal sutures of the carpels. The pollen is monocolpate, and the embryo development is of the Polygonum type.'.encode('utf8')
        treedata.has_flower = True
        treedata.plantation_date = datetime.datetime.now()
        treedata.last_pruning = datetime.datetime.now().date

        self.model.add(treedata)

        return True

    @property
    def name(self):
        return 'Planting {}'.format(self.specie)


class FailedTask(Task):
    async def run(self):
        raise RuntimeError("Task has failed")

    @property
    def name(self):
        return "failed"

