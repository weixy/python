#!/usr/bin/env python

import time

from selenium.webdriver.support.ui import WebDriverWait


class Page(object):

    def __init__(self, testsetup):
        self.testsetup = testsetup
        self.base_url = testsetup.base_url
        self.selenium = testsetup.selenium
        self.timeout = testsetup.timeout
        self._selenium_root = hasattr(self, '_root_element') and self._root_element or self.selenium

    def open(self, url_fragment):
        self.selenium.get(self.base_url + url_fragment)
        self.is_the_current_page
