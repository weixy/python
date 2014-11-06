#!/usr/bin/env python
import logging
import unittest
import pytest
import time

# Method 1: Use singleton and fixture to inject driver
@pytest.mark.usefixtures('context')
class TestContext(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(type(self).__name__)

    def test_driver1(self):
        self.logger.info('Open the web page of yellow online ')
        self.context.driver.get('http://www.yellow.co.nz')

    def test_driver2(self):
        self.logger.info('Open the google web page ')
        self.context.driver.get('http://www.google.co.nz')
        self.logger.debug('Sleep 3 seconds ')
        time.sleep(3)
        self.context.driver.quit()


# Method 2: Use generator to build driver
@pytest.mark.usefixtures('browser')
class TestDriverOtherWay(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger(type(self).__name__)

    def test_driver3(self):
        self.logger.info('Open the white pages ')
        self.driver.get('http://www.whitepages.co.nz')


def test_driver_yield(browser):
    print 'Open google.com'
    browser.get('http://www.google.com')


def test_driver_yield2(browser):
    print 'Open white pages again'
    browser.get('http://www.whitepages.co.nz')


if __name__ == '__main__':
    unittest.main()
