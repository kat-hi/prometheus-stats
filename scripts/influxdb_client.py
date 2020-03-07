import argparse
import pandas as pd
from influxdb import DataFrameClient
import threading
import matplotlib.pyplot as plt
import seaborn as sns

HOST = '127.0.0.1'
PORT = 8086
DB = 'prometheus'

params = {
    "chunked" : True,
    "chunk_size" : 10
}


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


def data_preprocessing(predictor, colnames, client):
    print('predictor: ' + predictor)

    resp = client.query("select %s,%s from %s WHERE time >= '2020-03-02T10:00:00.00Z' AND time <= '2020-03-04T10:00:00.00Z'" % (colnames[0], colnames[1], predictor))
    if not resp:
        print('no data for predictor: ' + predictor)
    else:
        df = pd.DataFrame(resp[predictor], columns=colnames)
        df['date'] = df.index.date
        df['day'] = df.index.day
        df['time'] = df.index.time

        sns.set(rc={'figure.figsize': (11, 4)})
        if predictor is not 'up':
            df['value'].plot(linewidth=0.5)
            plt.show()

def main(host='localhost', port=8086):
    client = DataFrameClient(host, port, database=DB)

    t1 = threading.Thread(target=data_preprocessing, args=('up', ['host', 'value'], client))
    t2 = threading.Thread(target=data_preprocessing, args=('node_cpu_frequency_hertz', ['host', 'value'], client))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

# @TODO index matching of different variables and time series analysis
# @TODO running all in multiple threads to parallelize these processes

'''
def get_all_prometheus_measurements():
    all_measurements = []
    response = client.get_list_measurements()
    with open('../ressources/measurements.txt', 'w') as file:
        for item in response:
            all_measurements.append(item['name'])
            file.write(item['name'] + '\n')
    # print(all_measurements)
'''


if __name__ == "__main__":
    args = parse_args()
    main(host=args.host, port=args.port)
    # get_all_prometheus_measurements()





