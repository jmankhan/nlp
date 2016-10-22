# figure out why using <s> doesnt work
import nltk, math, pprint
import operator

class WordElement():
	# static dictionary of all words and counts
	words = {}

	# static dictionary of all tags and counts
	tags = {}

	# static dict of all lexical bigrams and counts 
	lexical_bigrams = {}

	# static dict of all tags that appear next to each other and counts
	tag_bigrams = {}

	@classmethod
	def add_lexical_bigram(c, word, tag):
		tup = (word, tag)
		if tup in c.lexical_bigrams:
			c.lexical_bigrams[tup] = c.lexical_bigrams[tup]+1
		else:
			c.lexical_bigrams[tup] = 1

	# increment all applicable dictionaries, lists, and counters
	@classmethod
	def increment(c, word, tag):
		c.words[word] = c.words[word]+1 if word in c.words else 1
		c.tags[tag] = c.tags[tag]+1 if tag in c.tags else 1

		c.add_lexical_bigram(word, tag)

	@classmethod
	def add_tag_bigram(c, tag1, tag2):
		tup = (tag1, tag2)
		if tup in c.tag_bigrams:
			c.tag_bigrams[tup] = c.tag_bigrams[tup]+1
		else:
			c.tag_bigrams[tup] = 1

def prepare_corpus(corpus):
	processed = [ ]
	for sentence in corpus.tagged_sents():
		processed.append(("<s>", "START"))
		processed.extend([(word, tag) for (word, tag) in sentence])
		processed.append(("</s>", "END"))

	return processed

# expected input: [(word, tag), (word, tag)...]
def construct(training_corpus):
	previous_tag = None

	# construct list of unique words, tags, and counts for each
	for i, (word, tag) in enumerate(training_corpus):
		WordElement.increment(word, tag)
		
		if previous_tag is None:
			previous_tag = tag
		else:
			WordElement.add_tag_bigram(previous_tag, tag)
			previous_tag = tag

def viterbi(data):
	if data.split()[0] == "<s>":
		data = data[3:]
	# initialize both matrix with all 0s
	len_words = len(data.split())
	len_tags = len(WordElement.tags)

	score = [[0.0 for y in range(len_tags)] for x in range(len_words)]
	backptr = [[0 for y in range(len_words)] for x in range(len_tags)]

	word = data.split()[0] 
	# first step
	# for every tag in T (the master tag list), calculate the probability that the first word will have that tag
	for i, tag in enumerate(WordElement.tags):
		try:
			count_lex = float(WordElement.lexical_bigrams[(word, tag)])
			count_tag0 = WordElement.tags[tag]

			# naming things is hard
			count_tag_tag = float(WordElement.tag_bigrams[("START", tag)])
			count_tag = WordElement.tags["START"]

			pr = ((count_lex + 1) / (count_tag0 + len(WordElement.tags)))*((count_tag_tag + 1) / (count_tag + len(WordElement.tags)))

			score[0][i] = pr
		except Exception as e:
			continue

	# iteration step
	for w, word in enumerate(data.split()[1:], start=1):
		for t, tag in enumerate(WordElement.tags):
			try:
				# do the max thing
				max_j = 0.0
				max_j_index = -1
				for j, tag_j in enumerate(WordElement.tags):
					try:
						count_tag_j = float(WordElement.tags[tag_j])
						count_tagj_tagt = float(WordElement.tag_bigrams[(tag_j, tag)])

						newmax = score[w-1][j]*((count_tagj_tagt + 1) / (count_tag_j + len(WordElement.tags)))

						if newmax > max_j:
							print "here"
							max_j = newmax
							max_j_index = j
						
					except Exception as e:
						continue
				count_word_tag = float(WordElement.lexical_bigrams[(word, tag)])
				count_tag = WordElement.tags[tag]

				pr = ((count_word_tag + 1) / (count_tag + len(WordElement.tags))) * max_j
				score[w][t] = pr
				backptr[t][w] = max_j_index
				# print 'max found for', word, tag, 'was', max_j
			except Exception as e:
				continue

	pretty_print(score)

	seq = list()
	last_word = data.split()[-1]
	score_tag_index = score[len_words-2].index(max(score[len_words-1]))
	score_tag = WordElement.tags.items()[score_tag_index][0]
	seq.append(score_tag)
	for w in range(len_words-3, 0, -1):
		current_word = data.split()[w]
		current_tag_index = backptr[list(WordElement.tags).index(seq[-1])][w+1]
		#print current_tag_index, current_word
		seq.append(WordElement.tags.items()[current_tag_index][0])
		#print seq
	return seq


def pretty_print(matrix):
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	
	print '\n'.join(table)

corpus = prepare_corpus(nltk.corpus.brown)
training_corpus = corpus[0:30000]

construct(training_corpus)

pp = pprint.PrettyPrinter(indent=4)
# print WordElement.words
# print WordElement.tags
# pp.pprint( WordElement.lexical_bigrams)
# pp.pprint( WordElement.tag_bigrams)


# test = "<s> The Grand Jury said no </s>"
test = ""
# for sent in nltk.corpus.brown.sents()[57339]:
# 	test += ' '.join(sent)
test = ' '.join(nltk.corpus.brown.sents()[57339])
t = test
print t
seq = viterbi(t)

correct = 0
for i, s in enumerate(reversed(seq)):
	print list(WordElement.tags)[s], nltk.corpus.brown.tagged_sents()[57339][i][1], t.split()[i]
	if list(WordElement.tags)[s] == nltk.corpus.brown.tagged_sents()[57339][i][1]:
		correct += 1.0

print 'accuracy', correct/len(seq)

