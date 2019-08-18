""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
import mock
from pipeline_async.model.sql import SqlModel

# Globals and constants variables.

@pytest.fixture
def model(tmp_path_factory):
    return SqlModel.from_filepath(
        tmp_path_factory.mktemp("test").joinpath("sqlmodel.db")
    )


def test_sqlmodel(model, treedata):
    assert not model.exists(treedata)

    # Add once
    assert model.add(treedata)
    assert model.exists(treedata)

    # Add twice
    assert not model.add(treedata)

def test_sqlmodel_fetch(model, treedata):
    assert model.add(treedata)

    newtreedata = mock.TreeData(treedata.serial_number, treedata.taxonomy, treedata.specie)
    assert newtreedata.diameter_m is None

    model.fetch(newtreedata)
    assert newtreedata.diameter_m == pytest.approx(3.0, abs=1e-3)