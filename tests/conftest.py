""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pipeline_async.model import SqlModel, MongoModel

# Globals and constants variables.


@pytest.fixture
def sqlmodel(tmp_path_factory):
    return SqlModel.from_filepath(
        tmp_path_factory.mktemp("test").joinpath("model.db")
    )

@pytest.fixture
def mongomodel():
    model = MongoModel('test')
    yield model
    model.client.drop_database('test')
