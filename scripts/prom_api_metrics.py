import sys
import requests
import datetime
import simplejson

HOST = 'http://localhost'
PORT = 9090

time = (str(datetime.datetime.now().time()).split('.')[0]).replace(':','-')

'''
# use command-line arguments 
RESSOURCE = sys.argv[1]
PARAM = sys.argv[2]
FILENAME = sys.argv[3]

'''

queries=[]
with open('../ressources/queries_reduced.txt', 'r') as file:
	f = file.read().split('\n')

for item in f:
	queries.append(item)


query = HOST + ':' + str(PORT) + '/api/v1/query_range'

for q in queries:
	qu = q+'&start=2020-01-05T10:10:10-01:00&end=2020-01-13T11:11:11-01:00&step=120s'
	print(query+'?query='+qu)
	r = ""
	try:
		r = requests.get(query+'?query='+qu, allow_redirects=True)
	except:
		pass

	file = open('../data/' + q + time + '.json', 'w')
	file.write(simplejson.dumps(simplejson.loads(r.content), indent=4))
	file.close()