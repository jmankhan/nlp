import urllib, urllib2, os
from tinydb import *
from bs4 import BeautifulSoup

# primary_key, url, content
db = TinyDB('db.json')

class Crawler:
	def __init__(self, root_url):

		visited = dict()
		stack = list()
		stack.append(root_url)

		for i in range(5):
			if stack[-1] not in visited:
				self.visit(stack.pop(), visited, stack)
			else:
				stack.pop()


	def visit(self, url, visited, stack):
		if not self.should_visit(url, visited):
			return

		url = self.sanitize_url(url)

		print 'visiting ', url
		html = urllib2.urlopen(url).read()
		db.insert({'address':url, 'content':html})

		soup = BeautifulSoup(html, 'html.parser')
		
		for anchor in soup.find_all('a', href=True):
			stack.append(anchor['href'])

		visited[url] = True

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

	def should_visit(self, url, visited):
		return url not in visited and not url.endswith('.pdf')


Crawler('http://www.muhlenberg.edu')