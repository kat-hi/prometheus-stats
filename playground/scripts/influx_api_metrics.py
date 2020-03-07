import requests
import datetime
import simplejson
import threading

HOST = 'http://localhost'
PORT = 8086

time = (str(datetime.datetime.now().time()).split('.')[0]).replace(':', '-')
# GET /query?db=prometheus&q=SELECT%20%2A%20FROM%20up

items = []

with open('../ressources/queries_bug_report.txt', 'r') as file:
	f = file.read().split('\n')

for item in f:
	items.append(item)

query = HOST + ':' + str(PORT)


def quer(chunkstart, chunkend):
	chunk = items[chunkstart:chunkend]
	for q in chunk:
		qu = 'query?db=prometheus&q=select%20%2A%20from%20' + q + '%20where%20time%3Cnow%28%29%2B1m'
		print(query + '/' + qu)
		try:
			r = requests.get(query + '/' + qu, allow_redirects=True)
			print(r)
			file = open('../data/' + q + time + '.json', 'w')
			file.write(simplejson.dumps(simplejson.loads(r.content), indent=4))
			file.close()
		except:

			print('error: ' + q)


if __name__ == '__main__':
	'''
	t1 = threading.Thread(target=quer, args=(0, 65))
	t2 = threading.Thread(target=quer, args=(65, 130))
	t3 = threading.Thread(target=quer, args=(130, 195))
	t4 = threading.Thread(target=quer, args=(195, 260))
	'''
	t1 = threading.Thread(target=quer, args=(0, 1))
	t2 = threading.Thread(target=quer, args=(1, 2))
	t3 = threading.Thread(target=quer, args=(2, 3))
	t4 = threading.Thread(target=quer, args=(3, 4))
	threads = [t1, t2, t3, t4]

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()
