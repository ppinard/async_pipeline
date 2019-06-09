""""""

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from async_pipeline.model import SqlModel

# Globals and constants variables.


@pytest.fixture
def sqlmodel(tmp_path_factory):
    return SqlModel.from_filepath(
        tmp_path_factory.mktemp("test").joinpath("async_pipeline.db")
    )
