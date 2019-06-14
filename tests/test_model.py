""""""

# Standard library modules.
import dataclasses
import typing

# Third party modules.

# Local modules.
from pipeline_async.model import SqlModel
import mock

# Globals and constants variables.


def test_sqlmodel_exists_notable(sqlmodel):
    data = mock.ArithmeticData(3, 4, 7)
    assert not sqlmodel.exists(data)


def test_sqlmodel_exists_nodata(sqlmodel):
    data = mock.ArithmeticData(3, 4, 7)
    sqlmodel.add(data)

    data = mock.ArithmeticData(3, 4, -1)
    assert sqlmodel.exists(data)

    data = mock.ArithmeticData(3, 99, 102)
    assert not sqlmodel.exists(data)

def test_sqlmodel_exists(sqlmodel):
    data = mock.ArithmeticData(3, 4, 7)
    rowid = sqlmodel.add(data)
    assert rowid == 1
    assert sqlmodel.exists(data)

