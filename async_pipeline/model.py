""""""

# Standard library modules.
import abc
import datetime
import dataclasses

# Third party modules.
import sqlalchemy
import sqlalchemy.sql
from loguru import logger

# Local modules.

# Globals and constants variables.

class Model(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find(self, inputdata):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, list_outputdata):
        raise NotImplementedError

class SqlModel:

    FIELDS_TO_SQLTYPE = {int: sqlalchemy.Integer,
                         float: sqlalchemy.Float,
                         str: sqlalchemy.String,
                         bytes: sqlalchemy.LargeBinary,
                         datetime.datetime: sqlalchemy.DateTime,
                         bool: sqlalchemy.Boolean}

    def __init__(self, engine, dataclass):
        self.engine = engine
        self.dataclass = dataclass

        metadata = sqlalchemy.MetaData()
        table_name = dataclass.__name__.lower()
        fields = dataclasses.fields(dataclass)
        self.table = self._create_table(metadata, table_name, fields)
        logger.debug('Created table "{}"', table_name)

    @classmethod
    def from_filepath(cls, filepath, dataclass):
        engine = sqlalchemy.create_engine('sqlite:///' + str(filepath))
        return cls(engine, dataclass)

    def _create_table(self, metadata, table_name, fields):
        columns = []
        for field in fields:
            name = field.name
            column_type = self.FIELDS_TO_SQLTYPE.get(field.type)
            if column_type is None:
                raise ValueError('Cannot convert {} to SQL column'.format(name))
            columns.append(sqlalchemy.Column(name, column_type))

        table = sqlalchemy.Table(table_name, metadata, *columns)
        metadata.create_all(self.engine)
        return table

    def find(self, inputdata):
        # Build where clauses
        clauses = []
        for field in dataclasses.fields(inputdata):
            if field.name.startswith('key') or field.metadata.get('key', False):
                clause = self.table.c[field.name] == getattr(inputdata, field.name)
                clauses.append(clause)


    def add(self, list_outputdata):
        logger.debug('Preparing to add {} outputs to database'.format(len(list_outputdata)))

        rows = []
        for outputdata in list_outputdata:
            rows.append(dataclasses.asdict(outputdata))

        with self.engine.begin() as conn:
            conn.execute(self.table.insert(), rows) # pylint: disable=no-value-for-parameter

        logger.debug('{} outputs added to database'.format(len(rows)))
