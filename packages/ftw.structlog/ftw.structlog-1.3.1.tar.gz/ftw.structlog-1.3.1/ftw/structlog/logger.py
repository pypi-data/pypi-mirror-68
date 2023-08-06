from App.config import getConfiguration
from logging import FileHandler
from logging import getLogger
import json
import logging
import os


logger = getLogger('ftw.structlog')

root_logger = logging.root


def setup_logger():
    """Set up logger that writes to the JSON based logfile.

    May be invoked multiple times, and must therefore be idempotent.
    """
    if not logger.handlers:
        path = get_logfile_path()
        if path is not None:
            handler = FileHandler(path)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
    return logger


def get_logfile_path():
    """Determine the path for our JSON log.

    This will be derived from Zope2's EventLog location, in order to not
    have to figure out the path to var/log/ and the instance name ourselves.
    """
    zconf = getConfiguration()
    eventlog = getattr(zconf, 'eventlog', None)
    if eventlog is None:
        if os.environ.get('FTW_STRUCTLOG_MUTE_SETUP_ERRORS', '').lower().strip() != 'true':
            root_logger.error('')
            root_logger.error(
                "ftw.structlog: Couldn't find eventlog configuration in order "
                "to determine logfile location!")
            root_logger.error("ftw.structlog: No request logfile will be written!")
            root_logger.error('')
        return None

    handler_factories = eventlog.handler_factories
    eventlog_path = handler_factories[0].section.path
    assert eventlog_path.endswith('.log')
    path = eventlog_path.replace('.log', '-json.log')
    return path


def log_request_data(request_data):
    """Given a Python dict of key/value pairs to be logged, serialize and log
    them to a JSON based logfile.
    """
    json_log = setup_logger()
    msg = json.dumps(request_data, sort_keys=True)
    json_log.info(msg)


setup_logger()
