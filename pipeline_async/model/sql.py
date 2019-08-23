""""""

__all__ = ['SqlModel']

# Standard library modules.
import dataclasses
import datetime

# Third party modules.
import sqlalchemy
import sqlalchemy.sql

from loguru import logger

# Local modules.
from .base import ModelBase, iskeyfield, keyfields

# Globals and constants variables.

class SqlModel(ModelBase):

    TYPE_TO_SQLTYPE = {int: sqlalchemy.Integer, float: sqlalchemy.Float, str: sqlalchemy.String, bytes: sqlalchemy.LargeBinary, datetime.datetime: sqlalchemy.DateTime, datetime.date: sqlalchemy.Date, bool: sqlalchemy.Boolean}

    def __init__(self, engine):
        self.engine = engine

        self.metadata = sqlalchemy.MetaData()
        self.metadata.reflect(engine)

    @classmethod
    def from_filepath(cls, filepath):
        engine = sqlalchemy.create_engine("sqlite:///" + str(filepath))
        return cls(engine)

    def _require_table(self, data_or_dataclass):
        table_name = self._get_table_name(data_or_dataclass)
        table = self.metadata.tables.get(table_name)

        if table is None:
            table = self._create_table(table_name, data_or_dataclass)

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
        if dataclasses.is_dataclass(field.type):
            subtable = self._require_table(field.type)
            return sqlalchemy.Column(field.name + '_id', None, sqlalchemy.ForeignKey(subtable.name + '.id'))

        if issubclass(field.type, str) and iskeyfield(field):
            column_type = sqlalchemy.String(collation="NOCASE")
        elif field.type in self.TYPE_TO_SQLTYPE:
            column_type = self.TYPE_TO_SQLTYPE.get(field.type)
        else:
            raise ValueError("Cannot convert {} to SQL column".format(field.name))

        nullable = field.default is None

        return sqlalchemy.Column(field.name, column_type, nullable=nullable)

    def _get_rowid(self, data):
        """
        Returns the row of the dataclass if it exists.
        If not, ``None`` is returned
        Args:
            data (dataclasses.dataclass): instance
        Returns:
            int: row of the dataclass instance in its table, ``None`` if not found
        """
        if hasattr(data, '_rowid'):
            return data._rowid

        table_name = self._get_table_name(data)
        table = self.metadata.tables.get(table_name)
        if table is None:
            return None

        clauses = []
        for field in keyfields(data):
            value = getattr(data, field.name)

            if dataclasses.is_dataclass(field.type):
                row_id = self._get_rowid(value)
                clause = table.c[field.name + '_id'] == row_id
            else:
                clause = table.c[field.name] == value

            clauses.append(clause)

        if not clauses:
            logger.debug('No key fields')
            return None

        statement = sqlalchemy.sql.select([table.c.id]).where(sqlalchemy.sql.and_(*clauses))
        logger.debug("Find statement: {}", str(statement.compile()).replace("\n", ""))

        with self.engine.begin() as conn:
            rowid = conn.execute(statement).scalar()
            if not rowid:
                return None

            data._rowid = rowid
            return rowid

    def get_table(self, data_or_dataclass):
        table_name = self._get_table_name(data_or_dataclass)
        table = self.metadata.tables.get(table_name)

        if table is None:
            raise ValueError('No table named: {}'.format(table_name))

        return table

    def exists(self, data):
        return self._get_rowid(data) is not None

    def add(self, data, check_exists=True):
        # Check if exists
        if hasattr(data, '_rowid'):
            return False

        if check_exists:
            rowid = self._get_rowid(data)
            if rowid is not None:
                return False

        # Create row
        row = {}
        for field in dataclasses.fields(data):
            name = field.name
            value = getattr(data, name)

            if dataclasses.is_dataclass(value):
                self.add(value, check_exists)
                row[name + '_id'] = value._rowid
            else:
                row[name] = value

        # Insert
        table = self._require_table(data)

        with self.engine.begin() as conn:
            result = conn.execute(table.insert(), row)  # pylint: disable=no-value-for-parameter
            logger.debug("Added output to table {}".format(table.name))
            rowid = result.inserted_primary_key[0]
            data._rowid = rowid
            return True

    def fetch(self, data):
        table_name = self._get_table_name(data)
        table = self.metadata.tables.get(table_name)
        if table is None:
            raise ValueError('Data does not exists')

        clauses = []
        if hasattr(data, '_rowid'):
            clauses.append(table.c['id'] == data._rowid)
        else:
            for field in keyfields(data):
                value = getattr(data, field.name)

                if dataclasses.is_dataclass(field.type):
                    row_id = self._get_rowid(value)
                    clause = table.c[field.name + '_id'] == row_id
                else:
                    clause = table.c[field.name] == value

                clauses.append(clause)

        if not clauses:
            raise ValueError('Data does not exists')

        statement = sqlalchemy.sql.select(table.columns).where(sqlalchemy.sql.and_(*clauses))
        logger.debug("Fetch statement: {}", str(statement.compile()).replace("\n", ""))

        with self.engine.begin() as conn:
            row = conn.execute(statement).fetchone()
            if row is None:
                raise ValueError('Data does not exists')

            for column, value in row.items():
                if column.endswith('_id'):
                    pass
                else:
                    setattr(data, column, value)

        return data