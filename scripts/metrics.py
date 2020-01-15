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


query = HOST + ':' + str(PORT) + '/api/v1/query'

for q in queries:
	r = requests.get(query, allow_redirects=True, params ={'query': q})
	file = open('../data/'+q+time+'.json', 'w')
	file.write(simplejson.dumps(simplejson.loads(r.text), indent=4))
	file.close()
