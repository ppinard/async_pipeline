""""""

# Standard library modules.
import re

# Third party modules.

# Local modules.

# Globals and constants variables.


def camelcase_to_words(text):
    return re.sub("([a-z0-9])([A-Z])", r"\1 \2", text)
