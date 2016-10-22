"""
	Jalal Khan
	09/21/16
	This program will read a file and calculate the probability of certain words of phrases using unigrams and bigrams
"""
import re, sys

# Global variables
unigrams = dict()
bigrams = dict()

# Display options and prompt for input
prompt = '\n'.join([
'1. Create unigram and bigram',
'2. Search for unigram',
'3. Search for bigram',
'4. Exit'])

print 'Hello, welcome to the unigram/bigram creator'
print prompt

# compile corpus into dictionaries of unigrams and bigrams
# unigrams stores a word as a key and its counts as a value
# bigrams stores a tuple of words as a key and its counts as a value
def create_gram():
	filename = raw_input("Enter file name:")
	try:
		content = preprocess('<s> ' + open(filename, 'r').read() + ' </s>')
	except IOError:
		print "File not found"
		return

	corpus = content.split(' ')

	for i in range(len(corpus)):
		word = corpus[i]
		word2 = corpus[i+1] if corpus[i] != '</s>' else None
		unigrams[word] = unigrams[word]+1 if word in unigrams else 1

		if word2 is not None:
			b = (word, word2)
			bigrams[b] = bigrams[b]+1 if b in bigrams else 1

	print "Unigram and bigram created successfully"
	print unigrams

# search for a unigram in the corpus and print its count. 
# also print the top 5 bigrams each that contain this word in the beginning and at the end 
def search_unigram():
	key = raw_input('Enter unigram: ')
	if not key in unigrams:
		print "That unigram doesn't exist in the corpus"
	else:
		print '"{}" occurs {} times in the corpus'.format(key, unigrams[key])
		
		# returns a filtered dictionary where the keys contains the desired key as a subset 
		# the first list contains key as the first word, and the second list as the second word
		sub_bigrams_start = {k:v for k,v in bigrams.iteritems() if key in k and k[0] == key}
		sub_bigrams_end = {k:v for k,v in bigrams.iteritems() if key in k and k[1] == key}

		# sorts the filtered dictionary by value using lambda expressions! LISP did come in handy after all...
		# returns a list of (k:v) tuples
		start = sorted(sub_bigrams_start.items(), key=lambda x: x[1])
		end = sorted(sub_bigrams_end.items(), key=lambda x: x[1])

		print 'Top 5 bigrams with ' + key + ' at the beginning:'
		bigram_printer(start)

		print 'Top 5 bigrams with ' + key + ' at the end:'
		bigram_printer(end)


# search for a bigram in the corpus and print its count and probability
def search_bigram():
	query = raw_input('Enter bigram: ')
	if len(query.split(' ')) == 2:
		key = (query.split(' ')[0], query.split(' ')[1])
		if not key in bigrams:
			print "That bigram doesn't exist in the corpus"
		else:
			p = float(count(key)) / float(count(key[1]))
			print '"{}" occurs {} times with a probability of {:1.3f}'.format(query, bigrams[key], p)

def exit():
	print "Bye"
	sys.exit()

# Helper functions
# counts the amount of times the key appears in the corpus. accepts a string or tuple, for unigrams and bigrams respectively
def count(key):
	if isinstance(key, tuple):
		return bigrams[key] if key in bigrams else 0
	else:
		return unigrams[key] if key in unigrams else 0

# Helper function
# Expects a list of tuples
def bigram_printer(bigram):
	r = 5 if len(bigram) >= 5 else len(bigram)

	for i in range(r):
		p = float(count(bigram[i][0])) / float(count(bigram[i][0][1]))
		print str(bigram[i][0]) + ' appeared ' + str(bigram[i][1]) + ' times with p = {:.3f}'.format(p)

# Helper function
# Preprocesses the corpus to normalize the data a bit
# How functional!
def preprocess(raw):
	processed = raw.replace('\n', ' ')

	return processed

# Main loop
option = int(raw_input("Pick an option\n"))
while option:
	if option == 1:
		create_gram()
	elif option == 2:
		search_unigram()
	elif option == 3:
		search_bigram()
	elif option == 4:
		exit()
	print prompt
	option = int(raw_input("Pick an option\n"))
