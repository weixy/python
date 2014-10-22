__author__ = 'y981821'

import logging
from browsermobproxy import Server
import config.config_settings as settings

auto_globals = {'proxy': None, 'selenium': None, 'server': None}


def setup():
    global selenium
    server = Server(path=settings.BROWSERMOB_PROXY_PATH, options={'port': settings.BROWSERMOB_PROXY_PORT})
    server.start()
    proxy = server.create_proxy()
    proxy.selenium_proxy()
    if settings.WEB_DRIVER == 'firefox':
        from selenium.webdriver.firefox.webdriver import WebDriver
    elif settings.WEB_DRIVER == 'chrome':
        from selenium.webdriver.chrome.webdriver import WebDriver

    selenium = WebDriver(proxy=proxy)
    logging.info('Automation configuration has been completed.')
    return selenium, proxy, server


def execute(selenium, proxy, server):
    proxy.new_har("YELLOW")
    selenium.get(settings.SERVER_URL_TO_TEST)
    har = proxy.har
    harFile.write('%s' % har)
    harFile.close()
    server.stop()
    selenium.quit()


if __name__ == '__main__':
    har_file = 'results/yol.har'
    harFile = open(har_file, 'w')
    auto_globals['selenium'], auto_globals['proxy'], auto_globals['server'] = setup()
    execute(auto_globals['selenium'], auto_globals['proxy'], auto_globals['server'])
