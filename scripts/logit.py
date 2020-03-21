from sklearn.linear_model import LogisticRegression
from influxdb_client import Influxfetcher, INFLUX_VARS
import pandas as pd
import numpy as np
import logging as log
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import statsmodels.api as sm

log.basicConfig(level=log.INFO, format='%(message)s')
influxfetcher = Influxfetcher()

def logit_model_estimation(df_all):
    # MODEL ESTIMATION
    model = LogisticRegression(solver='liblinear', random_state=0).fit(df_all['up'], df_all['ceph_osd_op_rw'])
    log.info(str(model.classes_))
    log.info(str(model.intercept_))
    log.info(str(model.coef__))


if __name__ == "__main__":
    df_up = influxfetcher.create_dataframe('up')
    df_ceph_osd_op_r = influxfetcher.create_dataframe('ceph_osd_op_r')
    df_ceph_osd_op_w = influxfetcher.create_dataframe('ceph_osd_op_w')
    df_ceph_osd_op_rw = influxfetcher.create_dataframe('ceph_osd_op_rw')

    df_all = pd.concat([df_up, df_ceph_osd_op_r, df_ceph_osd_op_w, df_ceph_osd_op_rw], axis=1)

    logit_model_estimation(df_all)




