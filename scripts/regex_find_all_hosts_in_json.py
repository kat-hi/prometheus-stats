import re
import json

with open('../data/node_cpu_core_throttles_total01-34-20.json', 'r') as file:
		data = json.load(file)

regex = '\"host\":'






