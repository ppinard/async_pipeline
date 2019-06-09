""""""

# Standard library modules.
import dataclasses
import typing

# Third party modules.

# Local modules.
from pipeline_async.model import SqlModel
import mock

# Globals and constants variables.


def test_sqlmodel_find_notable(sqlmodel):
    inputdata = mock.ArithmeticInput(3, 4)
    list_outputdata = sqlmodel.find("test", inputdata)
    assert len(list_outputdata) == 0


def test_sqlmodel_find_nodata(sqlmodel):
    inputdata = mock.ArithmeticInput(3, 4)
    sqlmodel.add("test", inputdata, [mock.ArithmeticOutput(7)])

    inputdata = mock.ArithmeticInput(3, 99)
    list_outputdata = sqlmodel.find("test", inputdata)
    assert len(list_outputdata) == 0


def test_sqlmodel_find(sqlmodel):
    inputdata = mock.ArithmeticInput(3, 4)
    sqlmodel.add("test", inputdata, [mock.ArithmeticOutput(7)])
    list_outputdata = sqlmodel.find("test", inputdata)

    assert len(list_outputdata) == 1

    outputdata = list_outputdata[0]
    assert outputdata.value == 7
    assert outputdata.x == 3
    assert outputdata.y == 4

    fields = {field.name: field for field in dataclasses.fields(outputdata)}
    assert fields["x"].default is dataclasses.MISSING
    assert fields["x"].metadata.get("key")
    assert fields["y"].default is dataclasses.MISSING
    assert fields["y"].metadata.get("key")
    assert fields["value"].default is None
    assert not fields["value"].metadata.get("key")

    type_hints = typing.get_type_hints(outputdata)
    assert type_hints["x"] is float
    assert type_hints["y"] is float
    assert type_hints["value"] is float

