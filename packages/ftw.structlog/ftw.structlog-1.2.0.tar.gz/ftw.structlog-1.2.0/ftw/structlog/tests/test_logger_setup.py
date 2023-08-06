from contextlib import contextmanager
from ftw.structlog.logger import setup_logger
from StringIO import StringIO
from unittest2 import TestCase
import logging
import os


class TestSetupLogger(TestCase):

    def testSetUp(self):
        logger = logging.getLogger('ftw.structlog')
        # If the functional tests are executed before these tests, the log handlers
        # are already there and no setup happens.
        map(logger.removeHandler, logger.handlers)

    def test_logs_errors_when_eventlog_is_missing(self):
        """
        When the event log is missing in the zope configuration, ftw.structlog
        noisily complains since it will result in missing log data.

        In test setups we sometimes do not have an eventlog configured and we do not
        care about ftw.structlog. In this situation we want to be able to mute the errors.
        This can be done with an environment variable.
        """

        with self.expect_log_output(
                "ftw.structlog: Couldn't find eventlog configuration in order to"
                " determine logfile location!\n"
                "ftw.structlog: No request logfile will be written!"):
            setup_logger()

        with self.expect_log_output(''):
            with self.env_variable_set('FTW_STRUCTLOG_MUTE_SETUP_ERRORS', 'true'):
                setup_logger()

    @contextmanager
    def expect_log_output(self, expected):
        with self.captured_log() as output:
            yield

        self.assertEquals(expected.strip(), output.getvalue().strip())

    @contextmanager
    def captured_log(self):
        output = StringIO()
        handler = logging.StreamHandler(output)
        logging.root.addHandler(handler)
        try:
            yield output
        finally:
            logging.root.removeHandler(handler)

    @contextmanager
    def env_variable_set(self, name, value):
        assert name not in os.environ, \
            'Unexpectedly found the variable {} in the environment.'.format(name)
        os.environ[name] = value
        try:
            yield
        finally:
            os.environ.pop(name)
