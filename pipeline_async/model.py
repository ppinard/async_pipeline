""""""

__all__ = ['Model', 'PassThroughModel', 'SqlModel']

# Standard library modules.
import abc
import datetime
import dataclasses
import inspect

# Third party modules.
import sqlalchemy
import sqlalchemy.sql
from loguru import logger

# Local modules.
from .datautil import iskeyfield, keyfields
from .util import camelcase_to_words

# Globals and constants variables.


class Model(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def exists(self, data):  # pragma: no cover
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, data):  # pragma: no cover
        raise NotImplementedError


class PassThroughModel(Model):
    def exists(self, data):
        return False

    def add(self, data):
        return []


class SqlModel(Model):

    TYPE_TO_SQLTYPE = {int: sqlalchemy.Integer, float: sqlalchemy.Float, str: sqlalchemy.String, bytes: sqlalchemy.LargeBinary, datetime.datetime: sqlalchemy.DateTime, bool: sqlalchemy.Boolean}

    def __init__(self, engine):
        self.engine = engine

        self.metadata = sqlalchemy.MetaData()
        self.metadata.reflect(engine)

    @classmethod
    def from_filepath(cls, filepath):
        engine = sqlalchemy.create_engine("sqlite:///" + str(filepath))
        return cls(engine)

    def _get_table_name(self, data_or_dataclass):
        if not inspect.isclass(data_or_dataclass):
            data_or_dataclass = type(data_or_dataclass)

        name = data_or_dataclass.__name__.lower()
        return "_".join(camelcase_to_words(name).split())

    def _require_table(self, data_or_dataclass):
        table_name = self._get_table_name(data_or_dataclass)
        table = self.metadata.tables.get(table_name)

        if table is None:
            table = self._create_table(table_name, data_or_dataclass)

        return table

    def get_table(self, data_or_dataclass):
        table_name = self._get_table_name(data_or_dataclass)
        table = self.metadata.tables.get(table_name)

        if table is None:
            raise ValueError('No table named: {}'.format(table_name))

        return table

    def _create_table(self, table_name, data_or_dataclass):
        # Add column for key fields of inputdata and all fields of outputdata.
        columns = [sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True)]
        for field in dataclasses.fields(data_or_dataclass):
            columns.append(self._create_column(field))

        # Create table.
        table = sqlalchemy.Table(table_name, self.metadata, *columns)
        self.metadata.create_all(self.engine, tables=[table])
        logger.debug('Create table "{}"'.format(table_name))

        return table

    def _create_column(self, field):
        column_type = self.TYPE_TO_SQLTYPE.get(field.type)
        if column_type is None:
            raise ValueError("Cannot convert {} to SQL column".format(field.name))

        if column_type is sqlalchemy.String and iskeyfield(field):
            column_type = sqlalchemy.String(collation="NOCASE")

        nullable = field.default is None

        return sqlalchemy.Column(field.name, column_type, nullable=nullable)

    def exists(self, data):
        # Find table
        table_name = self._get_table_name(data)
        table = self.metadata.tables.get(table_name)
        if table is None:
            return False

        # Build statement
        clauses = []
        columns = []
        for field in keyfields(data):
            clause = table.c[field.name] == getattr(data, field.name)
            clauses.append(clause)
            columns.append(table.c[field.name])

        # No key fields
        if not columns:
            return False

        statement = sqlalchemy.sql.select(columns).where(sqlalchemy.sql.and_(*clauses))
        logger.debug("Find statement: {}", str(statement.compile()).replace("\n", ""))

        # Execute
        with self.engine.begin() as conn:
            row = conn.execute(statement).first()
            return row is not None

    def add(self, data):
        table = self._require_table(data)
        row = dataclasses.asdict(data)

        with self.engine.begin() as conn:
            result = conn.execute(table.insert(), row)  # pylint: disable=no-value-for-parameter
            logger.debug("Added output to table {}".format(table.name))
            return result.inserted_primary_key[0]
