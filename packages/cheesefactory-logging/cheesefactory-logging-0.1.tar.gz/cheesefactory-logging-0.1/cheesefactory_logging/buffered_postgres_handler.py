# buffered_postgres_handler.py

import logging
from logging import Handler
import time
from queue import Queue
from typing import List
from socket import gethostname, gethostbyname
from sys import executable, argv
from cheesefactory_database.postgresql import CfPostgresql

logger = logging.getLogger(__name__)


class BufferedPostgresHandler(Handler):
    def __init__(self, host: str = '127.0.0.1', port: str = '5432', database: str = None, user: str = None,
                 password: str = None, encoding: str = 'utf8', table: str = None, field_list: List = None):
        """Collects logging records into a queue.Queue.

        Logs the queue as a JSON object in a PostgreSQL table, when the extra logging attribute "end" is given a value
        of "True" or when the handler is closed.

        Args:
            host: Database server hostname or IP.
            port: Database server port.
            database: Database name.
            user: Database server account username.
            password: Database server account password.
            encoding: Postgres client encoding.
            table: Log table in <<schema>>.<<table>> format
            field_list: Currently unused.
        """
        Handler.__init__(self)

        self.db = CfPostgresql(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            autocommit=True,
            dictionary_cursor=False,
            encoding=encoding
        )

        if not self.db.table_exists(table):
            raise ValueError(f'Table does not exist: {table}')

        # Currently unused.
        self.field_list = field_list
        # if not self.db.fields_exist(
        #        table_path=table,
        #        table_fields=field_list
        # ):
        #    raise ValueError(f'Table {table} is missing one of these fields: {str(field_list)}')

        self.table = table
        self.duration_start = None
        self.record_queue = Queue()

    def emit(self, record: logging.LogRecord):
        """If the "end" attribute in the current record has been set to True, dump all records that have been stored up
        to this point.

        All records will be reformatted to be output into the JSONB field of one record.

        Notes:
            LogRecord attributes: https://docs.python.org/3/library/logging.html#logrecord-attributes

        Args:
             record: The log record.
        """
        # If this is the first record in the queue, grab the "start" time.
        if self.record_queue.qsize() == 0:
            self.duration_start = record.created  # Returns a float that will be used later to get a time delta.

        self.record_queue.put({
            'args': str(getattr(record, 'args', None)),
            'asctime': str(getattr(record, 'asctime', None)),
            'created': str(getattr(record, 'created', None)),
            'exc_info': str(getattr(record, 'exc_info', None)),
            'exc_text': str(getattr(record, 'exc_text', None)),
            'filename': str(getattr(record, 'filename', None)),
            'funcName': str(getattr(record, 'filename', None)),
            'levelname': str(getattr(record, 'levelname', None)),
            'levelno': getattr(record, 'levelno', None),
            'lineno': getattr(record, 'lineno', None),
            'message': str(getattr(record, 'message', None)),
            'module': str(getattr(record, 'module', None)),
            'msecs': getattr(record, 'msecs', None),
            'msg': str(getattr(record, 'msg', None)),
            'name': str(getattr(record, 'name', None)),
            'pathname': str(getattr(record, 'pathname', None)),
            'process': str(getattr(record, 'process', None)),
            'processName': str(getattr(record, 'processName', None)),
            'relativeCreated': str(getattr(record, 'relativeCreated', None)),
            'stack_info': str(getattr(record, 'stack_info', None)),
            'thread': str(getattr(record, 'thread', None)),
            'threadName': str(getattr(record, 'threadName', None)),
        })

        if getattr(record, 'end', 0) == 1:  # or is it True

            # This is the final record. Compile this and all previous records into one JSON object, to be sent in a
            # database INSERT.
            message = []
            hostname = gethostname()
            duration = time.time() - self.duration_start

            while not self.record_queue.empty():
                message.append(self.record_queue.get())  # Making a list of dicts -- the JSON object.

            query = f'''
                INSERT INTO {self.table} (
                    source_host, source_ip, source_app, source_app_args, event_duration, message
                ) 
                VALUES (
                    '{hostname}', '{gethostbyname(hostname)}', '{executable}', array{argv}, 
                    {duration}, '{str(message).replace("'", '"')}'::jsonb
                )
            '''

            logger.debug(query)
            self.db.execute(query, fetchall=False)

    def close(self):
        self.db.cursor.close()
        self.db.connection.close()
