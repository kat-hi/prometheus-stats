import pandas as pd
from influxdb import DataFrameClient
import matplotlib.pyplot as plt
import seaborn as sns
import logging as log

INFLUX_VARS = ['up', 'ceph_osd_op_r', 'ceph_osd_op_w', 'ceph_osd_op_rw']

log.basicConfig(level=log.INFO, format='%(message)s')

import pars_args as parser

class Influxfetcher:
    client = DataFrameClient(host=parser.parse_args().host, port=parser.parse_args().port, database='prometheus')

    def __get_raw_data(self, predictor, colnames):
        log.info('get predictor: ' + predictor)

        resp = self.client.query(
            "select mean(%s) from %s WHERE time >= '2020-03-01T08:00:00.00Z' AND time <= '2020-03-12T20:00:00.00Z' "
            "GROUP BY time(15s)" % (colnames[0], predictor))

        if not resp:
            log.info('no data for predictor: ' + predictor + ' and queried colname: ' + colnames[0])
        else:
            df = pd.DataFrame(resp[predictor], columns=['mean'])
            return df

    def create_dataframe(self, influx_var):
        return self.__get_raw_data(influx_var, ['value'])


# TODO REFACTORING
## UNTIL THEN, JUST RUN AND SEE:
    def dump_create_and_use_multiple_dataframes(self):
        df_up = self.create_dataframe(INFLUX_VARS[0])
        df_ceph_osd_op_r = self.create_dataframe(INFLUX_VARS[1])
        df_ceph_osd_op_w = self.create_dataframe(INFLUX_VARS[2])
        df_ceph_osd_op_rw = self.create_dataframe(INFLUX_VARS[3])


        # DATA EXPLORATION WITH SINGLE VARIABLE
        # raw_data_exploration(df_up, INFLUX_VARS[0])
        # raw_data_exploration(df_ceph_osd_op_r, INFLUX_VARS[1])
        # raw_data_exploration(df_ceph_osd_op_w, INFLUX_VARS[2])
        # raw_data_exploration(df_ceph_osd_op_rw, INFLUX_VARS[3])

        # CONCAT DATAFRAMES TO ONE DATASET
        df_all = pd.concat([df_up, df_ceph_osd_op_r, df_ceph_osd_op_w, df_ceph_osd_op_rw], axis=1)

        # DATACLEANING
        df_all = df_all.dropna()

        # DATA EXPLORATION OF CLEANED DATASET
        for var in INFLUX_VARS:
            self.cleaned_dataset_exploration(df_all, var)

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
    def get_all_prometheus_measurements():
        all_measurements = []
        response = client.get_list_measurements()
        with open('../ressources/measurements.txt', 'w') as file:
            for item in response:
                all_measurements.append(item['name'])
                file.write(item['name'] + '\n')
        # print(all_measurements)
    '''

    def raw_data_exploration(self, df, predictor):
        log.info('\n predictor: ' + predictor)
        # PLOTTING
        axes = df['mean'].plot(marker=".", linewidth=0.05, alpha=0.4, color="g", figsize=(25, 4))
        axes.set_ylabel(predictor)
        axes.set_xlabel('time')
        # plt.show()

        df.rename(columns={'mean': predictor}, inplace=True)

        # DATAEXPLORATION
        ## PRINT MEAN, STD AND VAR

        log.info('mean:  ' + str(float(df.mean(axis=0))))
        log.info('std: ' + str(float(df.std(axis=0))))
        log.info('min: ' + str(float(df.min())))
        log.info('max: ' + str(float(df.max())))
        log.info('n: ' + str(float(df.count())))

        # DATAFRAMES TO CSV
        # df.to_csv(r'../data/' + predictor +'.csv', index=True, header=True)

        # df['date'] = df.index.date
        # df['day'] = df.index.day
        # df['time'] = df.index.time
        # df['index'] = df.index
        return df

    def cleaned_dataset_exploration(self, df_all, var):
        log.info('\n var: ' + var)
        log.info('mean:  ' + str(float(df_all[var].mean(axis=0))))
        log.info('std: ' + str(float(df_all[var].std(axis=0))))
        log.info('min: ' + str(float(df_all[var].min())))
        log.info('max: ' + str(float(df_all[var].max())))
        log.info('n: ' + str(float(df_all[var].count())))


if __name__ == "__main__":
    influxfetcher = Influxfetcher()
    influxfetcher.dump_create_and_use_multiple_dataframes()
    # get_all_prometheus_measurements()
