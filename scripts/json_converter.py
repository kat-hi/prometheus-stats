import simplejson
import json

with open('../data/node_cpu_core_throttles_total01-34-20.json') as file:
	data = json.load(file)
	print(data['status'])

	print(type(data['data']['result']))
