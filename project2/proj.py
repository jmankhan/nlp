# Jalal Khan
# 10/21/16
# This program will randomly generate a sentence based on a grammar file that is provided
# It will also display the grammar in a user-friendly manner

import re, random

class Grammar:
	def __init__(self):
		self.table = dict()

	def addProduction(self, nonterminal, definition):
		if not self.hasNonTerminal(nonterminal):
			self.table[nonterminal] = list()
		self.table[nonterminal].append(definition.replace(';', ''))

	def getRandomRHS(self, nonterminal):
		return random.choice(self.table[nonterminal]).split()

	def hasNonTerminal(self, nonterminal):
		return nonterminal in self.table

	def printGrammar(self):
		for p in self.table:
			rules = ""
			for rule in self.table[p]:
				rules += rule + "| "

			print p + " <- " + rules[:-2]

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
		
		print self.randomSentence()		
		# self.grammar.printGrammar()
	
	def getData(self):
		return self.data

	def randomSentence(self):
		return self.randomSentenceHelper(0, self.grammar.getRandomRHS('<start>'))

	def randomSentenceHelper(self, i, prod):
		if i >= len(prod):
			return ''
		elif prod[i].strip().startswith('<') and prod[i].strip().endswith('>'):
			return self.randomSentenceHelper(0, self.grammar.getRandomRHS(prod[i])) + self.randomSentenceHelper(i+1, prod)
		else:
			return prod[i] + " " + self.randomSentenceHelper(i+1, prod)

def main():
	# RandomSentenceGenerator('conspiracy_theory.g')
	RandomSentenceGenerator('jalal.g')

main()