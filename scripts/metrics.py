import requests
import socket
import threading
import json
import sys

#HOST = 'http://prometheus.monitor.svc.cluster.local'
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
                                                                                                                                                                66,1          Bot



def connect():
    try:
        sock.connect(server_adr)
        print('Connection established')
    except socket.error:
        print('Something went wrong')

def send_request():
    request = "GET /api/v1/alerts HTTP/1.1\r\nHost: %s\r\nAccept: */*\r\n\r\n" % HOST
    sock.send(request.encode())

def receive():
    content = b''
    while True:
        response = sock.recv(64000)
        if not response:
            break
        content = content + response
    return content


if __name__ == '__main__':
    connect()
    receive()
    send_request()
    
'''