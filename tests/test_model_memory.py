""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
import mock
from pipeline_async.model.memory import MemoryModel

# Globals and constants variables.

@pytest.fixture
def model():
    return MemoryModel()


def test_memorymodel(model, treedata):
    assert not model.exists(treedata)

    # Add once
    assert model.add(treedata)
    assert model.exists(treedata)

    # Add twice
    assert not model.add(treedata)

    assert len(model.get_alldata(mock.TreeData)) == 1
    assert len(model.get_alldata(mock.TaxonomyData)) == 1
