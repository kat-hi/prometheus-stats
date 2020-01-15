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

# use ressource items from queries.txt
queries=[]
with open('../ressources/queries_reduced.txt', 'r') as file:
	f = file.read().split('\n')

for item in f:
	queries.append(item)


# query = HOST + ':' + str(PORT) + RESSOURCE
query = HOST + ':' + str(PORT) + '/api/v1/query'

for q in queries:
	r = requests.get(query, allow_redirects=True, params ={'query': q})
	file = open('../data/'+q+time+'.json', 'w')
	file.write(simplejson.dumps(simplejson.loads(r.text), indent=4))
	file.close()

#text = r.text
#print(text)

#file = open(FILENAME, 'w')
#file.write(text)
#file.close()

'''
server_adr = (HOST,PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect():
    try:
        sock.connect(server_adr)
        print('Connection established')
        print(HOST, PORT)
    except socket.error:
        print('Something went wrong')

def send_request():
    print('send')
    request = "GET /api/v1/targets?state=active HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\n\r\n" % HOST
    sock.send(request.encode())

def receive():
    print('receive')
    content = b''
    while True:
        response = sock.recv(512)
        print(response)
        if not response:
            print('break')
            break
        content = content + response
    for data in content:
        print('.' + str(data))
    return content

def close():
    sock.close()

#if __name__ == '__main__':
    #connect()
    #send_request()
    #receive()
    #close()

'''