""""""

# Standard library modules.
import dataclasses

# Third party modules.

# Local modules.

# Globals and constants variables.

def iskeyfield(field):
    return field.name.startswith('key') or field.metadata.get('key', False)

def keyfields(dataclass):
    return tuple(field for field in dataclasses.fields(dataclass) if iskeyfield(field))

