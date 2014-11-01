#!/usr/bin/env python
import logging
import unittest
import pytest
import time


@pytest.mark.usefixtures('context')
class TestContext(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(type(self).__name__)

    def test_driver1(self):
        self.logger.info('Open the web page of yellow online ...')
        self.context.driver.get('http://www.yellow.co.nz')

    def test_driver2(self):
        self.logger.info('Open the google web page ...')
        print '#########'
        self.context.driver.get('http://www.google.co.nz')
        self.logger.debug('Sleep 3 seconds ...')
        time.sleep(3)
        self.context.driver.quit()


if __name__ == '__main__':
    unittest.main()