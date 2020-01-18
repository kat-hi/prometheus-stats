import simplejson
import json
import os
import re

regex = "(\D)*"
colnames = []
values = []

for filename in os.listdir('../data/'):
	colnames.append(re.search(regex, filename).group())
	file = open('../data/'+filename, 'r')
	data = json.load(file)
	results = data['results'][0]['series'][0]['values']
	file.close()


'''
with open('../data/data.csv', 'w') as file:
	for item in res:
		file.writelines(str(item[8]))
file.close()
'''