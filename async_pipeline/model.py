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
    def find(self, task_name, inputdata):
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, task_name, inputdata, list_outputdata):
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

    def _create_outputdataclass(self, table, column_names):
        fields = []
        for column_name in column_names:
            column = table.c[column_name]
            fields.append(self._create_field(column))

        return dataclasses.make_dataclass('Dummy', fields)

    def _create_field(self, column):
        SQLTYPE_TO_TYPE = {v: k for k, v in self.TYPE_TO_SQLTYPE.items()}
        type_ = SQLTYPE_TO_TYPE.get(column.type.__class__)
        if type_ is None:
            raise ValueError('Cannot convert SQL column {}'.format(column.type.__class__.__name__))

        name = column.name

        metadata = {}
        if column.info.get('key'):
            metadata['key'] = True

        default = dataclasses.MISSING
        if column.nullable:
            default = None

        return (name, type_, dataclasses.field(default=default, metadata=metadata))

    def find(self, task_name, inputdata):
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

        statement = sqlalchemy.sql.select(table.columns).where(sqlalchemy.sql.and_(*clauses))
        logger.debug('Find statement: {}', str(statement.compile()).replace('\n', ''))

        # Execute
        list_outputdata = []
        with self.engine.begin() as conn:
            resultproxy = conn.execute(statement)

            # Create dummy dataclass.
            dataclass = self._create_outputdataclass(table, resultproxy.keys())

            # Create outputdata.
            for row in resultproxy:
                list_outputdata.append(dataclass(**row))

        return list_outputdata

    def add(self, task_name, inputdata, list_outputdata):
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
