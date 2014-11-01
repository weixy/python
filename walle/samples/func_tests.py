#!/usr/bin/env python

from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://sem.yellow.co.nz')
print browser.title
assert 'Murray' in browser.title
