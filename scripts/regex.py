import re

regex = 'value = \"(\w)*\" '
values = []
file = open('options.txt', 'r')
for line in file:
	values.append(re.search(regex, line).group().split('= ')[1])

file.close()

with open('queries.txt', 'w') as file:
	for value in values:
		file.writelines(value+'\r\n')

file.close()





