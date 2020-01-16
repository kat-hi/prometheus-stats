import requests
import sys

HOST = 'http://localhost'
PORT = 9090

RESSOURCE = sys.argv[1]
PARAM = sys.argv[2]
FILENAME = sys.argv[3]

query = HOST + ':' + str(PORT) + RESSOURCE

print(query)

r = requests.get(query, allow_redirects=True, params ={'query': PARAM})

text = r.text
print(text)

file = open(FILENAME, 'w')
file.write(text)
file.close()