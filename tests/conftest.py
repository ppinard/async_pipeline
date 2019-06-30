""""""

# Standard library modules.
import enum
import dataclasses
import datetime

# Third party modules.
import pytest

# Local modules.
import mock
from pipeline_async.model.sql import SqlModel
from pipeline_async.model.unqlite import UnqliteModel

# Globals and constants variables.

@pytest.fixture
def treedata():
    taxonomy = mock.TaxonomyData('plantae', 'malvales', 'malvaceae', 'hibiscus')
    return mock.TreeData(1, taxonomy, 'Hibiscus abelmoschus')
