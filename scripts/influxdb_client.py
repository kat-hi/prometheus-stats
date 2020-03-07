from influxdb import DataFrameClient
import pandas

HOST = '127.0.0.1'
PORT = 8086
DB = 'prometheus'

params = {
    "url" : "/query"
}

def get_all_prometheus_measurements():
    all_measurements = []
    response = client.get_list_measurements()
    with open('../ressources/measurements.txt', 'w') as file:
        for item in response:
            all_measurements.append(item['name'])
            file.write(item['name'] + '\n')
    # print(all_measurements)

if __name__ == "__main__":
    client = DataFrameClient(host=HOST, port=PORT, database=DB)
    get_all_prometheus_measurements()