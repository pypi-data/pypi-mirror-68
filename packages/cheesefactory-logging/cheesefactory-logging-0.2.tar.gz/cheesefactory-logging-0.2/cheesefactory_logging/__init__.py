# __init__.py

LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

STANDARD_LOG_FORMAT = '%(asctime)s %(levelname)-8s %(filename)-16s %(name)-16s line:%(lineno)-4s ' \
                      '%(process)-5s:%(processName)-19s %(message)s'


class CfLogConfigBuilder:

    def __init__(self, root_log_level: str = 'DEBUG', disable_existing_loggers: int = 0):

        self.level_sanity_check(log_level=root_log_level)
        self.root_log_level = root_log_level
        self.disable_existing_loggers = disable_existing_loggers

        self.handler_list = []
        self.handlers = {}
        self.formatters = {}

        self.add_formatter('standard', STANDARD_LOG_FORMAT)

    def get_config(self) -> dict:

        if len(self.handler_list) == 0 or len(self.handlers) == 0:
            raise ValueError('No handlers have been defined!')

        return {
            'version': 1,
            'disable_existing_loggers': self.disable_existing_loggers,
            'root': {
                'level': self.root_log_level,
                'handlers': self.handler_list,
            },
            'handlers': self.handlers,
            'formatters': self.formatters
        }

    def add_formatter(self, name, log_format) -> None:
        self.formatters[name] = {'format': log_format}

    @staticmethod
    def level_sanity_check(log_level: str = None) -> None:
        if log_level not in LOG_LEVELS:
            raise ValueError(
                f'Invalid log_level value ({log_level}). Valid values: {str(LOG_LEVELS)}'
            )

    def sanity_check(self, handler_name: str = None, log_level: str = None) -> None:
        self.level_sanity_check(log_level)
        if handler_name in self.handler_list or handler_name in self.handlers:
            raise ValueError(
                f'Handler already exists: {handler_name}'
            )

    def add_console_handler(self, log_level: str = 'DEBUG', formatter: str = 'standard',
                            stream: str = 'ext://sys.stdout') -> None:
        """Add a handler that streams logging output to sys.stdout

        Args:
            log_level: Logging level.
            formatter: Logging formatter.
            stream: ext://sys.stdout or ext://sys.stderr
        """
        handler_name = 'console'
        self.sanity_check(handler_name=handler_name, log_level=log_level)

        self.handlers[handler_name] = {
            'class': 'logging.StreamHandler',
            'level': log_level,
            'formatter': formatter,
            'stream': stream,
        }
        self.handler_list.append(handler_name)

    def add_file_handler(self, log_level: str = 'DEBUG', formatter: str = 'standard',
                         filename: str = 'log.txt', mode: str = 'a', encoding: str = None, delay: bool = False) -> None:
        """Add a handler that sends logging output to a disk file.

        Args:
            log_level: Logging level.
            formatter: Logging formatter.
            filename: Filename to output logging to.
            mode: The mode used when opening the log file. Default mode is append.
            encoding: The encoding to use when opening the log file.
            delay: If True, then file opening is deferred until the first call to emit() (the first write).
        """
        handler_name = 'log_file'
        self.sanity_check(handler_name=handler_name, log_level=log_level)

        self.handlers[handler_name] = {
            'class': 'logging.FileHandler',
            'level': log_level,
            'formatter': formatter,
            'filename': filename,
            'mode': mode,
            'encoding': encoding,
            'delay': delay
        }
        self.handler_list.append(handler_name)

    def add_rotating_file_handler(self, log_level: str = 'DEBUG', formatter: str = 'standard',
                                  filename: str = 'log.txt', mode: str = 'a', max_bytes: int = 1024*10,
                                  backup_count: int = 1, encoding: str = None, delay: bool = False) -> None:
        """Add a handler that sends logging output to a file and rotates the file based on size.

        Args:
            log_level: Logging level.
            formatter: Logging formatter.
            filename: Filename to output logging to.
            mode: The mode used when opening the log file. Default mode is append.
            max_bytes: Roll the log files at a predetermined byte size. If 0, then rollover never occurs
            backup_count: Save this many old log fils. If 0, then rollover never occurs.
            encoding: The encoding to use when opening the log file.
            delay: If True, then file opening is deferred until the first call to emit() (the first write).
        """
        handler_name = 'rotating_log_file'
        self.sanity_check(handler_name=handler_name, log_level=log_level)

        self.handlers[handler_name] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': log_level,
            'formatter': formatter,
            'filename': filename,
            'mode': mode,
            'maxBytes': max_bytes,
            'backupCount': backup_count,
            'encoding': encoding,
            'delay': delay
        }
        self.handler_list.append(handler_name)

    def add_buffered_postgres_handler(self, log_level: str = 'DEBUG', host: str = '127.0.0.1', port: str = '5432',
                                      database: str = None, user: str = None, password: str = None,
                                      encoding: str = 'utf8', table: str = None) -> None:
        """Add a handler that sends aggregated logs to a database table. The aggregation is output, as a single record,
        to the table, when the logger is fed an "extra", where 'end' = 1:

        logger.debug('This is test.', extra={'end': 1})

        Args:
            log_level: Logging level.
            host: Database server hostname or IP.
            port: Database server port.
            database: Database name.
            user: Database server account username.
            password: Database server account password.
            encoding: Postgres client encoding.
            table: Log table in <<schema>>.<<table>> format
        """
        handler_name = 'buffered_postgres_handler'
        self.sanity_check(handler_name=handler_name, log_level=log_level)

        self.handlers[handler_name] = {
            'class': 'cheesefactory_logging.buffered_postgres_handler.BufferedPostgresHandler',
            'level': log_level,
            'host': host,
            'port': port,
            'database': database,
            'user': user,
            'password': password,
            'encoding': encoding,
            'table': table
        }
        self.handler_list.append(handler_name)

    # def add_timed_rotating_file_handler(self, log_level: str = 'DEBUG', formatter: str = 'standard',
    #                                    filename: str = 'log.txt', when: str = 'h', interval: int = 1,
    #                                    backup_count: int = 1, encoding: str = None, delay: bool = False,
    #                                    utc: bool = False, at_time: datetime.time = None):
    #    """Add a handler that sends logging output to a file and rotates the file based on time (when) and interval.

    #    Args:
    #        log_level: Logging level.
    #        formatter: Logging formatter.
    #        filename: Filename to output logging to.
    #        when: The type of interval. For valid value types, reference
    #              https://docs.python.org/3/library/logging.handlers.html#logging.handlers.TimedRotatingFileHandler
    #        interval: Used with "when" to determin rotation. Refer to the above URL for more detail.
    #        backup_count: Save this many old log fils. If 0, then rollover never occurs.
    #        encoding: The encoding to use when opening the log file.
    #        delay: If True, then file opening is deferred until the first call to emit() (the first write).
    #        utc: If true, use UTC time. If False, use local time.
    #        at_time: Computes time of first rollover, then rely on "interval" for future rollovers.
    #    """
    #    handler_name = 'timed_rotating_log_file'
    #    self.sanity_check(handler_name=handler_name, log_level=log_level)

    #    self.handlers[handler_name] = {
    #        'class': 'logging.handlers.TimedRotatingFileHandler',
    #        'level': log_level,
    #        'formatter': formatter,
    #        'filename': filename,
    #        'when': when,
    #        'interval': interval,
    #        'backupCount': backup_count,
    #        'encoding': encoding,
    #        'delay': delay,
    #        'utc': utc,
    #        'atTime': at_time
    #    }
    #    self.handler_list.append(handler_name)

    # def add_mp_rotating_file_handler(self, log_level: str = 'DEBUG', formatter: str = 'standard',
    #                                 filename: str = 'log.txt', mode: str = 'a', max_bytes: int = 1024*10,
    #                                 backup_count: int = 1, encoding: str = None, delay: bool = False):
    #    """Add a file handler to be used by multiple processes.

    #    Uses MemoryHandler() to collect the logs, then flushes them to a RotatingFileHandler.
    #    """
    #    handler_name = 'rotating_log_file'
    #    self.sanity_check(handler_name=handler_name, log_level=log_level)

    #    self.handlers[handler_name] = {
    #        'class': 'logging.RotatingFileHandler',
    #        'level': log_level,
    #        'formatter': formatter,
    #        'filename': filename,
    #        'mode': mode,
    #        'maxBytes': max_bytes,
    #        'backupCount': backup_count,
    #        'encoding': encoding,
    #        'delay': delay
    #    }
    #    self.handler_list.append(handler_name)

# todo: log trace dumps

#   queue_listener:
#    class:
#      QueueListenerHandler
#    handlers:
#      - cfg: // handlers.console
#      - cfg: // handlers.file
#
