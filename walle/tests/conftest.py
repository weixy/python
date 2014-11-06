#!/usr/bin/env python

import pytest
from utils import context
from selenium import webdriver
from utils.context import Context

BROWSERS = {
    'firefox': webdriver.DesiredCapabilities.FIREFOX,
    'chrome': webdriver.DesiredCapabilities.CHROME,
}

@pytest.fixture
def context(request):
    request.cls.context = Context()

@pytest.yield_fixture()
def browser(request):
    driver = webdriver.Firefox()
    if not isinstance(request.cls, type(None)):
        request.cls.driver = driver
    yield driver
    driver.quit()