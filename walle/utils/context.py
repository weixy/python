#!/usr/bin/env python

import logging

import robot_settings as settings


def singleton(class_, *args, **kw):
    instances = {}

    def _singleton():
        if class_ not in instances:
            instances[class_] = class_(*args, **kw)
        return instances[class_]
    return _singleton


def get_driver():
    if settings.WEB_DRIVER == 'firefox':
        from selenium.webdriver.firefox.webdriver import WebDriver
        return WebDriver()
    elif settings.WEB_DRIVER == 'chrome':
        from selenium.webdriver.chrome.webdriver import WebDriver
        return WebDriver()
    return None


def config_logging():
    logging.basicConfig(level=settings.LOG_LEVEL,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='test_result.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


@singleton
class Context(object):

    def __init__(self):
        self.driver = get_driver()
        config_logging()


if __name__ == '__main__':
    contxt1 = Context()
    contxt2 = Context()

    print id(contxt1)
    print id(contxt2)

    contxt1.driver.get('http://www.google.com')

    print contxt2.driver.current_url

    contxt2.driver.quit()
