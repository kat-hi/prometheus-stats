import argparse
import pandas as pd
from influxdb import DataFrameClient
import threading
import queue
import matplotlib.pyplot as plt
import seaborn as sns
import logging as log
HOST = '127.0.0.1'
PORT = 8086
DB = 'prometheus'

log.basicConfig(level=log.INFO, format='%(message)s')

def parse_args():
    """Parse the args from main."""
    parser = argparse.ArgumentParser(description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False, default='localhost', help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086, help='port of InfluxDB http API')
    return parser.parse_args()


def data_exploration(predictor, colnames, client):
    log.info('\n predictor: ' + predictor)

    resp = client.query(
        "select mean(%s) from %s WHERE time >= '2020-03-09T08:00:00.00Z' AND time <= '2020-03-12T20:00:00.00Z' "
        "GROUP BY time(60s)" % (colnames[0], predictor))

    if not resp:
        log.info('no data for predictor: ' + predictor + ' and queried colname: ' + colnames[0])
    else:
        df = pd.DataFrame(resp[predictor], columns=['mean'])

        # PLOTTING
        axes = df['mean'].plot(marker=".", linewidth=0.05, alpha=0.4, color="g", figsize=(25, 4))
        axes.set_ylabel(predictor)
        axes.set_xlabel('time')
        # plt.show()

        # DATACLEANING
        df = df.dropna()

        # DATAEXPLORATION
        ## PRINT MEAN, STD AND VAR
        #log.info('mean: ' + str(float(df.mean())))
        #log.info('sd: ' + str(float(df.std())))
        log.info('mean:  ' + str(float(df.mean(axis=0))))
        log.info('std: ' + str(float(df.std(axis=0))))
        log.info('min: ' + str(float(df.min())))
        log.info('max: ' + str(float(df.max())))
        log.info('n: ' + str(float(df.count())))
        log.info('')

        # DATAFRAMES TO CSV
        df.to_csv(r'../data/' + predictor, index=True, header=True)

        df['date'] = df.index.date
        df['day'] = df.index.day
        df['time'] = df.index.time
        df['index'] = df.index
        return df


def main(host='localhost', port=8086):
    client = DataFrameClient(host, port, database=DB)

    # CREATE DATAFRAMES
    df_up = data_exploration('up', ['value'], client)
    df_ceph_osd_op_r = data_exploration('ceph_osd_op_r', ['value'], client)
    df_ceph_osd_op_w = data_exploration('ceph_osd_op_w', ['value'], client)
    df_ceph_osd_op_rw = data_exploration('ceph_osd_op_rw', ['value'], client)

    # DATAEXPLORATION step by step
    ## PRINT MEAN; STD AND VAR
    '''
    print(str(df_up.values.mean()) + ' ' + str(df_up.values.std()) + ' ' + str(df_up.var()))
    print(str(df_ceph_osd_op_r.values.mean()) + ' ' + str(df_ceph_osd_op_r.values.std()) + ' ' + str(
        df_ceph_osd_op_r.var()))
    print(str(df_ceph_osd_op_rw.values.mean()) + ' ' + str(df_ceph_osd_op_rw.values.std()) + ' ' + str(
        df_ceph_osd_op_rw.var()))
    print(str(df_ceph_osd_op_w.values.mean()) + ' ' + str(df_ceph_osd_op_w.values.std()) + ' ' + str(
        df_ceph_osd_op_w.var()))

    print(df_up.count())
    '''

    # DATAFRAMES TO CSV
    '''
    df_ceph_osd_op_rw.to_csv(r'../data/ceph_osd_op_rw.csv', index=True, header=True)
    df_ceph_osd_op_r.to_csv(r'../data/ceph_osd_op_r.csv', index=True, header=True)
    df_ceph_osd_op_w.to_csv(r'../data/ceph_osd_op_w.csv', index=True, header=True)
    df_up.to_csv(r'../data/up.csv', index=True, header=True)
    '''

'''
  threading
  t1 = threading.Thread(target=data_preprocessing, args=('up', ['host', 'value'], client))
  t2 = threading.Thread(target=data_preprocessing, args=('node_cpu_frequency_hertz', ['host', 'value'], client))
  thread_list = [t1,t2]

  for thread in thread_list:
      thread.start()

  for thread in thread_list:
      thread.join()
  '''

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
