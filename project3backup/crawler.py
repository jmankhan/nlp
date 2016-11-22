import urllib, urllib2, os, httplib
from tinydb import *
from bs4 import BeautifulSoup

# primary_key, url, content
db = TinyDB('db.json')

class Crawler:
	def __init__(self, root_url):

		stack = list()
		stack.append(root_url)

		while stack:
			if not self.exists(stack[:-1]):
				self.visit(stack.pop(), stack)
			else:
				stack.pop()

	def visit(self, url, stack):
		url = self.sanitize_url(url)
		if not self.should_visit(url):
			return

		print 'visiting ', url
		html = ''
		try:
			html += urllib2.urlopen(url).read()
		except httplib.IncompleteRead as e:
			html += e.partial
		except urllib2.HTTPError as e:
			return

		db.insert({'address':url, 'content':html, 'text':soup.get_text()})

		soup = BeautifulSoup(html, 'html.parser')
		
		for anchor in soup.find_all('a', href=True):
			stack.append(anchor['href'])


	def sanitize_url(self, url):
		# change all relative addresses to absolute
		if url.startswith('/'):
			url = 'http://www.muhlenberg.edu' + url
		# make sure all urls start with http
		if not (url.startswith('http') or url.startswith('https')):
			url = 'http://' + url
		# remove trailing slashes
		if url.endswith('/'):
			url = url[:-1]

		return url

	def exists(self, url):
		URL = Query()
		return db.contains(URL.address == url)

	def should_visit(self, url):
		return (not self.exists(url)) and not url.endswith('.pdf') and not url.endswith('.jpg') \
			and not url.endswith('.png') and not url.startswith('http://#') and not url.startswith('http://mailto') \
			and not url.startswith('http://javascript') and not url.startswith('http://tel') and not url.startswith('http://maps') \
			or url.startswith('http://www.muhlenberg')


db.purge()
Crawler('http://www.muhlenberg.edu')