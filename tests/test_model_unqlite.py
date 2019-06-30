""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
import mock
from pipeline_async.model.unqlite import UnqliteModel

# Globals and constants variables.

@pytest.fixture
def model(tmp_path_factory):
    return UnqliteModel(tmp_path_factory.mktemp("test").joinpath("unqlitemodel.db"))


def test_unqlitemodel(model, treedata):
    assert not model.exists(treedata)

    # Add once
    assert model.add(treedata)
    assert model.exists(treedata)

    # Add twice
    assert not model.add(treedata)
