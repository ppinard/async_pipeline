""""""

# Standard library modules.
import abc
import datetime
import dataclasses
import re

# Third party modules.
import sqlalchemy
import sqlalchemy.sql
from loguru import logger

# Local modules.
from .datautil import iskeyfield, keyfields

# Globals and constants variables.

class Model(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def find(self, task_name, inputdata, outputdataclass):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, task_name, inputdata, *list_outputdata):
        raise NotImplementedError

def camelcase_to_words(text):
    return re.sub('([a-z0-9])([A-Z])', r'\1 \2', text)

class SqlModel(Model):

    TYPE_TO_SQLTYPE = {int: sqlalchemy.Integer,
                       float: sqlalchemy.Float,
                       str: sqlalchemy.String,
                       bytes: sqlalchemy.LargeBinary,
                       datetime.datetime: sqlalchemy.DateTime,
                       bool: sqlalchemy.Boolean}

    def __init__(self, engine):
        self.engine = engine
        self.metadata = sqlalchemy.MetaData()

    @classmethod
    def from_filepath(cls, filepath):
        engine = sqlalchemy.create_engine('sqlite:///' + str(filepath))
        return cls(engine)

    def _require_table(self, task_name, inputdata, outputdata):
        table = self.metadata.tables.get(task_name)

        if table is None:
            table = self._create_table(task_name, inputdata, outputdata)

        return table

    def _create_table(self, table_name, inputdata, outputdata):
        # Add column for key fields of inputdata and all fields of outputdata.
        columns = []
        for field in keyfields(inputdata) + dataclasses.fields(outputdata):
            columns.append(self._create_column(field))

        # Create table.
        table = sqlalchemy.Table(table_name, self.metadata, *columns)
        self.metadata.create_all(self.engine, tables=[table])
        logger.debug('Create table "{}"'.format(table_name))

        return table

    def _create_column(self, field):
        column_type = self.TYPE_TO_SQLTYPE.get(field.type)
        if column_type is None:
            raise ValueError('Cannot convert {} to SQL column'.format(field.name))

        if column_type is sqlalchemy.String and iskeyfield(field):
            column_type = sqlalchemy.String(collation='NOCASE')

        nullable = field.default is None

        info = {}
        if iskeyfield(field):
            info['key'] = True

        return sqlalchemy.Column(field.name, column_type, nullable=nullable, info=info)

    def find(self, task_name, inputdata, outputdataclass):
        # Find table
        table = self.metadata.tables.get(task_name)

        # No output if table does not exists
        if table is None:
            return []

        # Build statement
        clauses = []
        for field in keyfields(inputdata):
            clause = table.c[field.name] == getattr(inputdata, field.name)
            clauses.append(clause)

        columns = []
        for field in dataclasses.fields(outputdataclass):
            if field.name in table.columns:
                columns.append(table.c[field.name])

        statement = sqlalchemy.sql.select(columns).where(sqlalchemy.sql.and_(*clauses))
        logger.debug('Find statement: {}', str(statement.compile()).replace('\n', ''))

        # Execute
        list_outputdata = []
        with self.engine.begin() as conn:
            for row in conn.execute(statement):
                list_outputdata.append(outputdataclass(**row))

        return list_outputdata

    def add(self, task_name, inputdata, *list_outputdata):
        if not list_outputdata:
            logger.debug('No output to add to database')
            return

        logger.debug('Preparing to add {} outputs to database'.format(len(list_outputdata)))

        inputrow = dict((field.name, getattr(inputdata, field.name)) for field in keyfields(inputdata))

        rows = []
        for outputdata in list_outputdata:
            row = {}
            row.update(inputrow)
            row.update(dataclasses.asdict(outputdata))
            rows.append(row)

        # Get or create table.
        table = self._require_table(task_name, inputdata, list_outputdata[0])

        with self.engine.begin() as conn:
            conn.execute(table.insert(), rows) # pylint: disable=no-value-for-parameter

        logger.debug('{} outputs added to database'.format(len(rows)))
