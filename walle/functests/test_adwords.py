#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.select import Select
import unittest
import time
import csv


class PullTimeZonesFromGoogleAdWords(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		# self.browser.quit()
		pass

	def testPullTimeZones(self):
		self.browser.get('http://adwords.google.com')
		time.sleep(5)
		email_field = self.browser.find_element_by_id('Email')
		email_field.send_keys('adwordsapi@y8.co.nz')
		pawd_field = self.browser.find_element_by_id('Passwd')
		pawd_field.send_keys('JLMRproduction')
		sign_in_butn = self.browser.find_element_by_id('signIn')
		sign_in_butn.click()
		time.sleep(20)
		country_select_element = self.browser.find_element_by_xpath(".//select[contains(@class, '{style.timeZoneSelect')]")
		country_select = Select(country_select_element)
		options = country_select_element.find_elements_by_xpath(".//option")
		
		print '\n'
		list_timezones = []
		for option in options:
			option_value = option.get_attribute("value")
			if len(option_value) != 0:
				option_text = option.text
				country_select.select_by_visible_text(option_text)
				time.sleep(5)
				timezone_select_element = self.browser.find_element_by_xpath(".//select[contains(@class, 'mPAC')]")
				timezone_select = Select(timezone_select_element)
				zones = timezone_select_element.find_elements_by_xpath(".//option")
				for zone in zones:
					zone_value = zone.get_attribute("value")
					if len(zone_value) != 0:
						zone_text = zone.text
						list_timezones.append((zone_value, zone_text, option_value))
						print '%s, %s, %s' % (zone_value, zone_text, option_value)
		list_timezones.sort()
		with open('timezones_upd.csv', 'a') as outcsv:
			writer = csv.writer(outcsv, delimiter=',', lineterminator='\n')
			for zone in list_timezones:
				writer.writerow([zone[0], zone[1], zone[2]])




