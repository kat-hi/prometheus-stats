import logging as log
import pandas as pd
from celery.utils.sysinfo import df
import pars_args as parser
from influxdb import DataFrameClient
import matplotlib.pyplot as plt

log.basicConfig(level=log.INFO, format='%(message)s')

client = DataFrameClient(host=parser.parse_args().host, port=parser.parse_args().port,
                         database='prometheus')

all_key_names = set()


def request_influxdb_data(variable):
    print(variable)
    resp = client.query(
        "select mean(%s) from %s WHERE time >= '2020-02-01T08:00:00.00Z' AND time < '2020-05-01T23:00:00.00Z'"
        "GROUP BY time(5m),ceph_daemon" % ('value', variable))

    if not resp:
        log.info('no data for predictor: ' + variable + ' and queried colname: value')
        return resp
    else:
        df_all = create_dataframe(resp)
        return df_all


def create_dataframe(resp):
    global all_key_names
    df_list_raw = []
    current_key_names = resp.keys()
    all_key_names.update(current_key_names)
    var_name_counter = 0
    for key_name in current_key_names:
        df = pd.DataFrame(resp[key_name])
        if not key_name[1][0][1]:
            column_name = 'values' + str(var_name_counter)
            var_name_counter += 1
        else:
            column_name = key_name[1][0][1]
        df.rename(columns={'mean': column_name}, inplace=True)
        df_list_raw.append(df)
    df_all = pd.concat(df_list_raw, axis=1)
    return df_all  # dataframe of one metric for all keys (OSDs)


def get_avg_metrics():
    df = pd.ExcelFile('../metric_semantics/avg.xlsx').parse('Sheet1')
    sum_results = {}
    count_results = {}
    simple_metric_name = ''
    for row in df['Name InfluxDB']:  # column in avg.xlsx
        full_metric_name = str(row)  # contains _sum or _count
        simple_metric_name = full_metric_name.rsplit('_', 1)[0]  # does not contain _sum or _count
        df = request_influxdb_data(full_metric_name)
        if '_sum' in full_metric_name:
            sum_results[simple_metric_name] = df
            print(df.head(2))
        elif '_count' in full_metric_name:
            count_results[simple_metric_name] = df
            print(df.head(2))
        else:
            print('Strange metric name, not containing sum or count: ' + str(row))
    for key, value in sum_results.items():  # geht vermutlich auch mit map()
        df = value.div(count_results[key])
        df.to_csv(simple_metric_name + '.csv', index=True, header=True)


def get_count_metrics():
    df = pd.ExcelFile('../metric_semantics/counter.xlsx').parse('Sheet1')
    for row in df['Name InfluxDB']:  # column in counter.xlsx
        results = {}
        full_name = str(row)
        df_temp = request_influxdb_data(full_name)
        if str(df_temp) == str({}):
            print('no data: ' + full_name)
            continue
        results[full_name] = df_temp
        for key, value in results.items():  # geht vermutlich auch mit map()
            filename = str(key)
            df_result = results[key]
            df_result.to_csv('../datadump_count/' + filename + '.csv', index=True, header=True)


if __name__ == "__main__":
    get_avg_metrics()
    get_count_metrics()
