from sklearn.linear_model import LogisticRegression
from influxdb_client import Influxfetcher, INFLUX_VARS
import pandas as pd
import numpy as np
import logging as log
from sklearn.metrics import classification_report, confusion_matrix
import statsmodels.api as sm

log.basicConfig(level=log.INFO, format='%(message)s')
influxfetcher = Influxfetcher()

def logit_model_one_predictor(df_all, var):
    # MODEL ESTIMATION
    log.info('LOGIT: up & ' + var )
    logit_model = sm.Logit(df_all['up'], df_all[var])
    result = logit_model.fit()

    #log.info(result.summary())
    #log.info(result.summary2())

    get_odds(result)


def logit_model_all(df_all):
    predictors = df_all.drop(columns="up")
    logit_model = sm.Logit(df_all['up'], predictors)
    result = logit_model.fit()

    log.info(result.summary())
    log.info(result.summary2())
    get_odds(result)

def get_odds(result):
    # odds ratios and 95% CI
    log.info('\nOdds:')
    params = result.params
    conf = result.conf_int()
    conf['OR'] = params
    conf.columns = ['2.5%', '97.5%', 'Odds']
    log.info(np.exp(conf))

def estimate_logit_model(df_all):
    for var in INFLUX_VARS:
        if var is 'up':
            continue
        logit_model_one_predictor(df_all, var)

def estimate_multiple_logit_model(df_all):
    logit_model_all(df_all)


if __name__ == "__main__":
    df_up = influxfetcher.create_dataframes_with_value_col('up')
    df_ceph_osd_op_r = influxfetcher.create_dataframes_with_value_col('ceph_osd_op_r')
    df_ceph_osd_op_w = influxfetcher.create_dataframes_with_value_col('ceph_osd_op_w')
    df_ceph_osd_op_rw = influxfetcher.create_dataframes_with_value_col('ceph_osd_op_rw')
    df_node_ipmi_power_watts = influxfetcher.create_dataframes_with_value_col('node_ipmi_power_watts')

    df_up['up'].values[df_up['up'] < 0.99] = 0
    df_up['up'].values[df_up['up'] >= 0.99] = 1

    #df_all_cleaned = influxfetcher.concat_and_clean_dataset([df_up, df_ceph_osd_op_r, df_ceph_osd_op_w, df_ceph_osd_op_rw])
    #influxfetcher.clean_and_describe_dataset(df_all_cleaned)

    #df_all = influxfetcher.concat_and_clean_dataset([df_up, df_node_ipmi_power_watts])
    #influxfetcher.clean_and_describe_dataset(df_all)

    #estimate_logit_model(df_all)
    df_all = influxfetcher.concat_and_clean_dataset([df_up, df_ceph_osd_op_r, df_ceph_osd_op_w, df_ceph_osd_op_rw, df_node_ipmi_power_watts])
    estimate_multiple_logit_model(df_all)

    #influxfetcher.get_node_vs_cluster_metrics_as_csv()





