class WordElement():
	# static list of all tags
	tags = {}

	def __init__(self, w, c, t):
		# the word as a string. e.g. "hello"
		self.word = w

		# the number of ocurrences of this word in the corpus
		self.count = c

		# a dict of tuples of each tag associated with this word
		# as well as the ocurrences of each tag. e.g. {'NN':4, 'VB', 2}
		self.t = t

	# append a tag as a tuple 
	def add_tag(self, tag):
		if tag in self.t:
			self.t[tag] += 1 
		else:
			self.t[tag] = 1

	def __str__(self):
		return self.word

	def __eq__(self, other):
		return self.word == other.word

	def __hash__(self):
		return hash(self.word)

w = WordElement('hello', 1, {'NN':1, 'VB':2})
words = [WordElement('hello', 1, {'NN':1, 'VB':2})]

if w in words:
	print "in words"
else:
	print "not in words"

