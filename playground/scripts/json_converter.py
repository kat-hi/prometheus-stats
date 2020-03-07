import simplejson
import json
import os
import re
import csv

regex = "(\D)*"
colnames_cum = []
data_cum = {}


def extract_values_from_json():
    for file in os.listdir('../data/'):
        colname = re.search(regex, file).group()
        colnames_cum.append(colname)

        filename = '../data/' + file
        print(filename)
        f = open(filename, 'r')
        dat_temp = json.load(f)
        results = dat_temp['results'][0]['series'][0]['values']

        col_values = []
        for item in results:
            col_values.append(item[8])
        data_cum[colname] = col_values


def write_data_file():
    with open('../ressources/data.txt', 'w') as file:
        for key in colnames_cum:
            file.write(key + ",")
            for value in data_cum[key]:
                file.write(str(value) + ",")
            file.write('\n')
        file.close()


def write_many_data_files():
    for key in colnames_cum:
        with open('../ressources/' + key + '.txt', 'w') as file:
            file.write(key + ",")
            for value in data_cum[key]:
                file.write(str(value) + ",")
        file.close()

def write_np_x_array(file):
        f = open('../'+file, 'r')
        dat_temp = json.load(f)
        results = dat_temp['results'][0]['series'][0]['values']
        x = []
        for item in results:
            x.append(item[8])
        return x




if __name__ == '__main__':
    extract_values_from_json()
    # write_data_file()
    write_many_data_files()
