# Jalal Khan
# Due: October 14th, 2016
# Description: This is an implementation of the Viterbi Algorithm. It predicts the POS tag for a set of test data and compares
# the result with a known result set for accuracy. The expected rate of accuracy is 70%+, but I'm aiming for 99% :)
# The default training size is recommended, but the default testing size should be <1000 for a reasonable runtime

import nltk, numpy as np, pprint, string
from collections import defaultdict

pp = pprint.PrettyPrinter(indent=4)

# globals
words           = defaultdict(lambda: 0)
tags            = defaultdict(lambda: 0)
lexical_bigrams = defaultdict(lambda: 0)
tag_bigrams     = defaultdict(lambda: 0)
pr_tag_tag      = defaultdict(lambda: 0)
pr_word_tag     = defaultdict(lambda: 0)

def process_training(corpus, train_size):
	exclude = set(string.punctuation)
	processed = []
	for sent in corpus.tagged_sents(tagset="universal")[0:train_size]:
		processed.append(("<s>", "START"))
		for word in sent:
			if word not in exclude:
				processed.append(word)
			
		processed.append(("</s>", "END"))

	return processed

def train(corpus):
	previous_tag = None

	# collect counts of all words, tags, word_tag pairs, and tag_tag pairs
	for i, (word, tag) in enumerate(corpus):
		words[word] = words[word]+1 
		tags[tag] = tags[tag]+1
		lexical_bigrams[(word, tag)] = lexical_bigrams[(word, tag)]+1

		if i>0:	
			tag_bigrams[(previous_tag, tag)] = tag_bigrams[(previous_tag, tag)]+1

		previous_word = word
		previous_tag = tag

	# find probabilities of EVERY word_tag combination
	# pr(word|tag) = count(word, tag)/count(tag)
	for word in words:
		for tag,count in tags.iteritems():
			pr = np.log10(lexical_bigrams[(word, tag)]) - np.log10(count)
			pr_word_tag[(word, tag)] = pr

	# find probabilities of EVERY tag_tag combination
	# pr(tag_i|tag_i-1) = count(tag_i-1, tag_i)/count(tag_i-1)
	for tag_i in tags:
		for tag_i_1, count in tags.iteritems():
			pr = np.log10(tag_bigrams[(tag_i_1, tag_i)]) - np.log10(count)
			pr_tag_tag[(tag_i_1, tag_i)] = pr

# apply the viterbi algorithm to the input data (expects a list of words)
def test(data):
	score = np.zeros([len(tags), len(data)])
	backptr = np.zeros([len(data), len(tags)])

	# first step
	word1 = data[0]
	for t, tag in enumerate(tags):
		score[t, 0] = pr_word_tag[(word1, tag)] + pr_tag_tag["START", tag]

	# iterative step
	for w, word in enumerate(data[1:], start=1):
		for t, tag in enumerate(tags):
			max_j = np.log(0)
			index_max_j = 0
			for j, tag_j in enumerate(tags):
				newmax = score[j, w-1]+pr_tag_tag[(tag_j, tag)]

				if newmax > max_j:
					max_j = newmax
					index_max_j = j

			score[t, w] = pr_word_tag[(word, tag)]+max_j
			backptr[w, t] = index_max_j

			if score[t, w] == np.log(0):
				print 'unknown word', word

	# sequencing step
	seq = list()
	seq.append(list(tags)[score[0:,len(data)-1].argmax()])

	ptr = backptr[len(data)-1][score[0:,len(data)-1].argmax()]
	for i in range(len(data)-2, 0, -1):
		seq.append(list(tags)[int(ptr)])
		ptr = backptr[i][ptr]

	seq.append(backptr[0][ptr])

	return seq

def setup():
	np.seterr(all="ignore")
	np.set_printoptions(threshold=np.nan)

	train_size = raw_input('Enter size of training corpus [default 1/3]') or len(nltk.corpus.brown.sents())/3

	test_size = raw_input('Enter the size of the testing corpus [default 2/3]') or len(nltk.corpus.brown.sents())*2/3-1

	return int(train_size), int(test_size)

def main():
	train_size, test_size = setup()

	corpus = process_training(nltk.corpus.brown, train_size)
	train(corpus)
	
	print 'Done training'

	f = open('output.txt', 'w+')

	total = long(0)
	total_sent = long(0)

	start = len(nltk.corpus.brown.sents())/3
	stop = len(nltk.corpus.brown.sents())/3+train_size
	cur = start

	while cur < stop:
		seq = test(nltk.corpus.brown.sents()[cur])
		correct = nltk.corpus.brown.tagged_sents(tagset="universal")[cur]
		
		try:
			n_correct = 0.0
			for j, s in enumerate(reversed(seq)):
				if s == correct[j][1]:
					n_correct += 1.0

		except Exception as e:
			print e

		rate = n_correct/len(correct)
		f.write('accuracy for ' +  str(cur-start) + ' is ' + str(rate) + '\n')
		print 'accuracy for ', cur-start, 'is', rate

		total += n_correct
		total_sent += len(correct)

		print 'running total is', total/total_sent 
		cur +=1


	f.write('total accuracy is ' + str((total/total_sent)))
	f.close()

main()