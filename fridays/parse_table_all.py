# reads a matrix from a file into a dict
f = open('matrix.txt', 'r')
a_matrix = dict()
i = 0
for line in f:
	a_matrix[i] = map(str, line.split(' '))
	i+=1
state = 0
i = 0
input = raw_input('Enter a string to validate')
final_state = raw_input('Enter the final state')

next_letter = input[i]
while i != len(input):
	try:
		next_state = a_matrix[state].index(next_letter)
		print 'received ' + next_letter + ' in state ' + str(state) + ' going to state ' + str(next_state) + '. index is ' + str(i)
		state = next_state
	except ValueError:
		print 'passing in state ' + str(state) + ' with letter at ' + str(next_letter) 
		pass
	i += 1
	try:
		next_letter = input[i]
		print 'next letter set to ' + next_letter
	except IndexError:
		print 'index error ' + str(i) 
		if state == final_state:
			print input + ' is a valid string!'
		else:
			print input + ' is not a valid string!'

		input = raw_input('Enter another string to validate: ')
		i = 0
		state = 0
		final_state = raw_input('Enter the final state')
		next_letter = input[i]