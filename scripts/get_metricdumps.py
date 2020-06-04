import logging as log
import pandas as pd
import pars_args as parser
from influxdb import DataFrameClient
import multiprocessing

log.basicConfig(level=log.INFO, format='%(message)s')

client = DataFrameClient(host=parser.parse_args().host, port=parser.parse_args().port,
                         database='prometheus')

def request_data(variable, metric_type):

    log.info(metric_type)
    log.info(variable)
    query_keys = ['node', 'ceph_daemon', 'host', 'none_key']
    for query_key in query_keys:
        if query_key == 'none_key':
            resp = client.query(
                "select mean(%s) from %s WHERE time >= '2020-04-14T08:00:00.00Z' AND time < '2020-04-14T23:00:00.00Z'"
                "GROUP BY time(360m)" % ('value', variable))
        else:
            resp = client.query(
            "select mean(%s) from %s WHERE time >= '2020-04-01T08:00:00.00Z' AND time < '2020-04-14T23:00:00.00Z'"
            "GROUP BY time(5m), %s" % ('value', variable, query_key))
        current_key_names = resp.keys()
        for key in current_key_names:
            if query_key == 'none_key' or key[1][0][1] != '':
                log.info('create dataframe for | ' + variable + ' | with query_key: ' + query_key)
                df_all = create_dataframe(resp, query_key, current_key_names)
                return df_all
            elif key[1][0][1] == '':
                log.info('key' + str(key) + ' is empty string')
                break


def create_dataframe(resp, query_key, current_key_names):
    global all_key_names
    df_list_raw = []
    for key_name in current_key_names:
        column_name = get_column_name(query_key, key_name)
        df = pd.DataFrame(resp[key_name])
        df.rename(columns={'mean': column_name}, inplace=True)
        df_list_raw.append(df)
    df_all = pd.concat(df_list_raw, axis=1)
    return df_all  # dataframe of one metric for all keys (OSDs, nodes, hosts..)


def get_column_name(query_key, key_name):
    column_name = ''
    if query_key == 'host':
        column_name = key_name[1][0][1]
    elif query_key == 'ceph_daemon':
        column_name = key_name[1][0][1]
    elif query_key == 'node':
        column_name = key_name[1][0][1]
    return column_name


def get_avg_metrics():
    log.info('get avg metrics')
    df = pd.ExcelFile('../metric_semantics/test_avg.xlsx').parse('Sheet1')
    sum_results = {}
    count_results = {}
    for row in df['Name InfluxDB']:  # column in avg.xlsx
        full_metric_name = str(row)  # contains _sum or _count
        simple_metric_name = full_metric_name.rsplit('_', 1)[0]  # does not contain _sum or _count
        df = request_data(full_metric_name, metric_type='AVG METRIC')
        if '_sum' in full_metric_name:
            sum_results[simple_metric_name] = df
        elif '_count' in full_metric_name:
            count_results[simple_metric_name] = df
        else:
            log.info('Strange metric name, not containing sum or count: ' + str(row))
    for key, value in sum_results.items():  # geht vermutlich auch mit map()
        try:
            df = value.div(count_results[key])
            dir_name = '../datadump_avg/'
            filename = str(key)
            log.info('write ' + dir_name + filename)
            df.to_csv(dir_name + filename + '.csv', index=True, header=True)
        except KeyError as ke:
            log.info(ke.__cause__)
            continue

def get_count_metrics():
    log.info('get count metrics')
    df = pd.ExcelFile('../metric_semantics/test_counter.xlsx').parse('Sheet1')
    results = {}
    for row in df['Name InfluxDB']:  # column in counter.xlsx
        full_name = str(row)
        df_temp = request_data(full_name, metric_type='COUNT METRIC')
        results[full_name] = df_temp
    write_results_into_csv(results, dir_name='../datadump_count/')


def get_point_metrics():
    df = pd.ExcelFile('../metric_semantics/test_point.xlsx').parse('Sheet1')
    results = {}
    for row in df['Name InfluxDB']:  # column in counter.xlsx
        metric_name = str(row)
        if ':' in metric_name:
            continue
        df_temp = request_data(metric_name, metric_type='POINT METRIC')
        try:
            log.info(df_temp.head(2))
        except AttributeError as e:
            log.info(e.__cause__)
            continue
        results[metric_name] = df_temp
    write_results_into_csv(results, dir_name='../datadump_point/')


def write_results_into_csv(results, dir_name):
    for key, value in results.items():  # geht vermutlich auch mit map()
        filename = str(key)
        df_result = results[key]
        log.info('write ' + dir_name+filename)
        try:
            df_result.to_csv(dir_name + filename + '.csv', index=True, header=True)
        except AttributeError as e:
            log.info(e.__cause__)
            continue


if __name__ == "__main__":
    get_avg_process = multiprocessing.Process(target=get_avg_metrics)
    get_count_process = multiprocessing.Process(target=get_count_metrics)
    get_point_process = multiprocessing.Process(target=get_point_metrics)
    get_avg_process.start()
    get_count_process.start()
    get_point_process.start()
    get_avg_process.join()
    get_count_process.join()
    get_point_process.join()
