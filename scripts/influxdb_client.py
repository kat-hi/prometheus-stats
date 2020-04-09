import pandas as pd
from influxdb import DataFrameClient
import matplotlib.pyplot as plt
import seaborn as sns
import logging as log
import json

INFLUX_VARS = ['up', 'ceph_osd_op_r', 'ceph_osd_op_w', 'ceph_osd_op_rw']

log.basicConfig(level=log.INFO, format='%(message)s')
resp = ""
node_metrics = []
cluster_metrics = []
exception_metrics = []
no_data_metrics = []

import pars_args as parser

class Influxfetcher:
    client = DataFrameClient(host=parser.parse_args().host, port=parser.parse_args().port, database='prometheus')

    def __get_raw_data_from_single_var_as_dataframe(self, predictor):
        log.info('get predictor: ' + predictor)

        resp = self.client.query(
            "select mean(%s) from %s WHERE time >= '2020-03-01T08:00:00.00Z' AND time <= '2020-03-20T20:00:00.00Z' "
            "GROUP BY time(10s)" % ('value', predictor))

        if not resp:
            log.info('no data for predictor: ' + predictor + ' and queried colname: value')
        else:
            df = pd.DataFrame(resp[predictor], columns=['mean'])
            return df

    def get_node_vs_cluster_metrics_as_csv(self):
        global node_metrics, cluster_metrics, exception_metrics, no_data_metrics
        metricfiles = ['cluster_metrics','node_metrics','exception_metrics','no_data_metrics']
        with open('ressources/metrics.txt', 'r') as file:
            f = file.read().split('\n')

        global resp
        for item in f:
            try:
                resp = self.client.query(
                    "select * from %s WHERE time >= '2020-03-01T08:00:00.00Z' AND time <= '2020-03-01T08:01:00.00Z' " % item
                )
                if not resp:
                    log.info('no data ' + item)
                    no_data_metrics.append(item)
                elif 'host' in resp[item]:
                    log.info('host in  ' + item)
                    node_metrics.append(item)
                elif 'node' in resp[item]:
                    log.info('node in ' + item)
                    node_metrics.append(item)
                else:
                    log.info('cluster ' + item)
                    cluster_metrics.append(item)
            except:
                log.info('except ' + item)
                exception_metrics.append(item)

        for metricgroup in metricfiles:
            df = pd.DataFrame(metricgroup, columns=[metricgroup])
            df.to_csv(metricgroup + '.csv', index=True, header=True)



    def create_dataframes_with_value_col(self, variable):
        df = self.__get_raw_data_from_single_var_as_dataframe(variable)
        df.rename(columns={'mean': variable}, inplace=True)
        return df


    def dump_create_and_use_multiple_dataframes(self):
        df_up = self.create_dataframes_with_value_col(INFLUX_VARS[0])
        df_ceph_osd_op_r = self.create_dataframes_with_value_col(INFLUX_VARS[1])
        df_ceph_osd_op_w = self.create_dataframes_with_value_col(INFLUX_VARS[2])
        df_ceph_osd_op_rw = self.create_dataframes_with_value_col(INFLUX_VARS[3])


        # DATA EXPLORATION WITH SINGLE VARIABLE
        self.raw_data_exploration_single_variable(df_up, INFLUX_VARS[0])
        # self.raw_data_exploration(df_ceph_osd_op_r, INFLUX_VARS[1])
        # self.raw_data_exploration(df_ceph_osd_op_w, INFLUX_VARS[2])
        # self.raw_data_exploration(df_ceph_osd_op_rw, INFLUX_VARS[3])

        df_list = [df_up, df_ceph_osd_op_w, df_ceph_osd_op_r, df_ceph_osd_op_rw]
        self.concat_and_clean_dataset(df_list)

        #for var in INFLUX_VARS:
        #    self.cleaned_dataset_exploration(df_all, var)

        #for var in INFLUX_VARS:
        #    self.dump_data_to_csv(df_all, var)

    def get_all_prometheus_measurements(self):
        all_measurements = []
        response = self.client.get_list_measurements()
        with open('../ressources/metrics.txt', 'w') as file:
            for item in response:
                all_measurements.append(item['name'])
                file.write(item['name'] + '\n')


    def concat_and_clean_dataset(self, df_list):
        df_all = pd.concat(df_list, axis=1)
        df_all = df_all.dropna()
        return df_all

    def get_simple_plot(self, df, predictor):
        if predictor is 'up':
            df['mean'].values[df['mean'] < 0.99] = 0
        axes = df['mean'].plot(marker='.', markersize=1, linewidth=0.00, alpha=0.9, color="g", figsize=(25, 4))
        axes.set_ylabel(predictor)
        axes.set_xlabel('time')
        plt.show()

    def raw_data_exploration_single_variable(self, df, predictor):
        log.info('\n predictor: ' + predictor)
        self.get_simple_plot(df, predictor)
        df.rename(columns={'mean': predictor}, inplace=True)

        # DATAEXPLORATION
        log.info(df.describe())

        # df['date'] = df.index.date
        # df['day'] = df.index.day
        # df['time'] = df.index.time
        # df['index'] = df.index
        return df

    def dump_data_to_csv(self, df, variable):
        df.to_csv(r'../data/' + variable +'.csv', index=True, header=True)

    def clean_and_describe_dataset(self, df):
        df = df.dropna()
        log.info(df.describe())


if __name__ == "__main__":
    influxfetcher = Influxfetcher()
    influxfetcher.dump_create_and_use_multiple_dataframes()
    # get_all_prometheus_measurements()
