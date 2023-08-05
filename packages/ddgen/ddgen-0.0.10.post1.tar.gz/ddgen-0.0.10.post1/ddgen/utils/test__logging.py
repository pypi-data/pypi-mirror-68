import logging
import os
import unittest

from pkg_resources import resource_filename

from ._logging import setup_logging


@unittest.skip("These tests are not meant to be run now")
class TestLogging(unittest.TestCase):

    def setUp(self) -> None:
        self.log_file = resource_filename(__name__, 'test_data/test.log')

    def tearDown(self) -> None:
        if os.path.isfile(self.log_file):
            os.remove(self.log_file)

    def test_logging_to_file(self):
        self.assertFalse(os.path.isfile(self.log_file))
        setup_logging(filename=self.log_file)
        logger = logging.getLogger(__name__)
        logger.info('bla bla bla')

        self.assertTrue(os.path.isfile(self.log_file))

        with open(self.log_file) as fh:
            bla = fh.read()

        self.assertTrue('bla bla bla' in bla)

    def test_logging_without_file(self):
        self.assertFalse(os.path.isfile(self.log_file))
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info('bla bla bla')

        self.assertFalse(os.path.isfile(self.log_file))
