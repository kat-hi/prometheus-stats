import argparse
import pandas as pd
from influxdb import DataFrameClient


HOST = '127.0.0.1'
PORT = 8086
DB = 'prometheus'

params = {
    "chunked" : True,
    "chunk_size" : 10
}


def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='localhost',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


def main(host='localhost', port=8086):
    client = DataFrameClient(host, port, database=DB)

    # query variables "up" and "node_cpu_frequency_hertz"
    resp_up = client.query("select host, value from up WHERE time > now() - 1h")
    resp_node_cpu_frequency_hertz = client.query(("select cpu, host, value from node_cpu_frequency_hertz WHERE time > now() - 1h"))

    # create pandas dataframe
    df_up = pd.DataFrame(resp_up['up'], columns=['host', 'value'])
    df_node_cpu_frequency_hertz = pd.DataFrame(resp_node_cpu_frequency_hertz['node_cpu_frequency_hertz'],
                                               columns=['cpu', 'host', 'value'])
    # access timestamps with index parameter
    for index in df_node_cpu_frequency_hertz.iterrows():
        print(index)

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





