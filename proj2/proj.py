import re, random

class Grammar:
	def __init__(self):
		self.table = dict()

	def addProduction(self, nonterminal, definition):
		if nonterminal not in self.table:
			self.table[nonterminal] = list()
		self.table[nonterminal].append(definition)

	def getRandomRHS(self, nonterminal):
		return random.choice(self.table[nonterminal]).split()[:-1]

	def hasNonTerminal(self, nonterm):
		return nonterminal in self.table

	def construct(self, productions):
		for production in productions:
			name = production.splitlines()[1]
			children = list()

			for line in production.splitlines():	
				if line != '{' and line != '}' and line != name and len(line.strip()) != 0:
					self.addProduction(name, line)
		
		return self.table



class RandomSentenceGenerator:

	def __init__(self, file_name):
		f = open(file_name, 'r+')
		
		self.data = f.read()

		nonterminals = set(re.findall(r'<(.*?)>', self.data))
		productions = list(re.findall(r'{(.*?)}', self.data, re.DOTALL))
		self.grammar = Grammar()
		self.grammar.construct(productions)
		print(self.randomSentence())
		
		
	
	def getData(self):
		return self.data

	def randomSentence(self):
		return self.randomSentenceHelper(0, self.grammar.getRandomRHS('<start>'))

	def randomSentenceHelper(self, i, prod):
		if i >= len(prod):
			return ""
		elif prod[i].startswith('<') and prod[i].endswith('>'):
			return prod[i] + " (" + self.randomSentenceHelper(0, self.grammar.getRandomRHS(prod[i])) + ") " + self.randomSentenceHelper(i+1, prod)
		else:
			return prod[i] + " " + self.randomSentenceHelper(i+1, prod)

RandomSentenceGenerator('conspiracy_theory.g')