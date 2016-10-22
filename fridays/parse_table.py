# Receives a string and determines if the pattern is valid, print 'received ' + next + ' in state ' + str(state) + ' to state ' + str(next_state)
a_matrix = dict()
a_matrix[0] = ['-', 'a', '-']
a_matrix[1] = ['c', 'a', 'b']
a_matrix[2] = ['c', '-', '-']
input = 'aacab'
i = 0
state = 0
next = input[i]
while i != len(input):
	try:
		index = a_matrix[state].index(next)
		next_state = index
		state = next_state
	except ValueError:
		pass
	i+=1
	try:
		next = input[i]
	except IndexError:
		if state == 2:
			print input + ' is a valid string'
		else:
			print input + ' is not a valid string'