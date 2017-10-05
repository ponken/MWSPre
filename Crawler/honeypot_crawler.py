# -*- coding: utf-8 -*-

import sys
import time
from selenium import webdriver

class GoogleWebCrawler:
	def __init__(self, search_wait_time=2.5):
#		self.browser = selenium.webdriver.Ie()
		self.browser = webdriver.Firefox()
		self.current_pagenum = 0
		self.search_wait_time = search_wait_time

	def __del__(self):
		self.browser.close()

	def search(self, search_words):
		self.browser.get("http://www.google.com/")
		element = self.browser.find_element_by_name("q")
		element.send_keys(search_words)
		element.submit()
		time.sleep(self.search_wait_time)
		self.raw_url = self.browser.current_url

	def restore(self, raw_url, current_pagenum):
		self.raw_url = raw_url
		self.current_pagenum = current_pagenum
		self.browser.get(self.raw_url + "&start=" + str(self.current_pagenum*10))
		time.sleep(self.search_wait_time)

	def get_links(self):
		links = self.browser.find_elements_by_xpath("//div/h3/a")
		links = [link.get_attribute("href") for link in links]
		return links

	def open_links(self, links=[], load_wait_time=2.5):
		for link in links:
			self.browser.get(link)
			try:
				self.browser.switch_to_alert().accept()
			except:
				pass
			time.sleep(load_wait_time)

	def goto_next_page(self):
		self.current_pagenum += 1
		self.browser.get(self.raw_url + "&start=" + str(self.current_pagenum*10))
		time.sleep(self.search_wait_time)

	def get_raw_url(self):
		return self.raw_url

	def get_current_pagenum(self):
		return self.current_pagenum
