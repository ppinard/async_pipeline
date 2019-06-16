""""""

# Standard library modules.
import inspect

# Third party modules.
import attr

# Local modules.

# Globals and constants variables.

def fields(data_or_dataclass):
    if not inspect.isclass(data_or_dataclass):
        data_or_dataclass = type(data_or_dataclass)
    return attr.fields(data_or_dataclass)

def iskeyfield(field):
    return field.name.startswith('key') or field.metadata.get('key', False)

def keyfields(data_or_dataclass):
    return tuple(field for field in fields(data_or_dataclass) if iskeyfield(field))

