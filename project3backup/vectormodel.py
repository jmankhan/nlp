from tinydb import *
import json
from collections import defaultdict

db = TinyDB('db.json')
words = defaultdict(int)


class VectorSpaceModel:
	def __init__(self):
		print 'a'

	def create_vector(doc):
		for r in db.all():
			docs = list()
			for word in row['text']:
				words[word] = row.eid
