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
    list_outputdata = sqlmodel.find("test", inputdata, mock.ArithmeticOutput)
    assert len(list_outputdata) == 0


def test_sqlmodel_find_nodata(sqlmodel):
    inputdata = mock.ArithmeticInput(3, 4)
    sqlmodel.add("test", inputdata, mock.ArithmeticOutput(7))

    inputdata = mock.ArithmeticInput(3, 99)
    list_outputdata = sqlmodel.find("test", inputdata, mock.ArithmeticOutput)
    assert len(list_outputdata) == 0


def test_sqlmodel_find(sqlmodel):
    inputdata = mock.ArithmeticInput(3, 4)
    sqlmodel.add("test", inputdata, mock.ArithmeticOutput(7))
    list_outputdata = sqlmodel.find("test", inputdata, mock.ArithmeticOutput)

    assert len(list_outputdata) == 1

    outputdata = list_outputdata[0]
    assert isinstance(outputdata, mock.ArithmeticOutput)
    assert outputdata.value == 7

