""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
import mock
from pipeline_async.model.memory import MemoryModel
from pipeline_async.model.chain import ChainModel

# Globals and constants variables.

@pytest.fixture
def model():
    model1 = MemoryModel()
    model2 = MemoryModel()
    return ChainModel(model1, model2)

def test_chainmodel(model, treedata):
    assert not model.exists(treedata)

    # Add once
    assert model.add(treedata)
    assert model.exists(treedata)

    # Add twice
    assert not model.add(treedata)

    assert len(model.models[0].get_alldata(mock.TreeData)) == 1
    assert len(model.models[0].get_alldata(mock.TaxonomyData)) == 1
    assert len(model.models[1].get_alldata(mock.TreeData)) == 1
    assert len(model.models[1].get_alldata(mock.TaxonomyData)) == 1

def test_chainmodel_alreadyexists_firstmodel(model, treedata):
    model.models[0].add(treedata)

    # Add once
    assert model.exists(treedata)
    assert not model.add(treedata)

    assert len(model.models[0].get_alldata(mock.TreeData)) == 1
    assert len(model.models[0].get_alldata(mock.TaxonomyData)) == 1
    assert len(model.models[1].get_alldata(mock.TreeData)) == 0
    assert len(model.models[1].get_alldata(mock.TaxonomyData)) == 0

def test_chainmodel_alreadyexists_secondmodel(model, treedata):
    model.models[1].add(treedata)

    # Add once
    assert not model.exists(treedata)
    assert not model.add(treedata)

    # Add twice
    assert not model.add(treedata)

    assert len(model.models[0].get_alldata(mock.TreeData)) == 1
    assert len(model.models[0].get_alldata(mock.TaxonomyData)) == 1
    assert len(model.models[1].get_alldata(mock.TreeData)) == 1
    assert len(model.models[1].get_alldata(mock.TaxonomyData)) == 1