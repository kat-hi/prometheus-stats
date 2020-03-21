from sklearn.linear_model import LogisticRegression
from influxdb_client import Influxfetcher, INFLUX_VARS
import pandas as pd
import numpy as np
import logging as log
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import statsmodels.api as sm

log.basicConfig(level=log.INFO, format='%(message)s')
influxfetcher = Influxfetcher()

def logit_model_estimation(df_all, var):
    # MODEL ESTIMATION
    log.info('LOGIT: up & ' + var )
    logit_model = sm.Logit(df_all['up'], df_all[var])
    result = logit_model.fit()

    #log.info(result.summary())
    #log.info(result.summary2())

    get_odds(result)


def logit_model_all(df_all):
    log.info('LOGIT: up & r & w')
    #predictors = df_all.drop(columns="up")
    #predictors = predictors.drop(columns="ceph_osd_op_rw")
    logit_model = sm.Logit(df_all['up'], df_all)

    #logit_model = sm.Logit(df_all['up'], predictors)
    result = logit_model.fit()

    #log.info(result.summary())
    #log.info(result.summary2())

    get_odds(result)

def get_odds(result):
    # odds ratios and 95% CI
    log.info('\nOdds:')
    params = result.params
    conf = result.conf_int()
    conf['OR'] = params
    conf.columns = ['2.5%', '97.5%', 'Odds']
    log.info(np.exp(conf))


if __name__ == "__main__":
    df_up = influxfetcher.create_dataframe('up')
    df_ceph_osd_op_r = influxfetcher.create_dataframe('ceph_osd_op_r')
    df_ceph_osd_op_w = influxfetcher.create_dataframe('ceph_osd_op_w')
    df_ceph_osd_op_rw = influxfetcher.create_dataframe('ceph_osd_op_rw')

    df_up['up'].values[df_up['up'] < 0.99] = 0
    df_up['up'].values[df_up['up'] >= 0.99] = 1

    df_all = pd.concat([df_up, df_ceph_osd_op_r, df_ceph_osd_op_w, df_ceph_osd_op_rw], axis=1)
    df_all = df_all.dropna()

    for var in INFLUX_VARS:
        if var is 'up':
            continue
        logit_model_estimation(df_all, var)

    logit_model_all(df_all)




