import re

# this script is for fetching all values into a list that can be choosen from localhost:9090/graph

regex = 'value = \"(\w)*\" '
values = []
file = open('options.txt', 'r')
for line in file:
	values.append(re.search(regex, line).group().split('= ')[1])

file.close()

with open('../ressources/queries.txt', 'w') as file:
	for value in values:
		file.writelines(value+'\r\n')

file.close()





