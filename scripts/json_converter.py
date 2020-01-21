import simplejson
import json
import os
import re

regex = "(\D)*"
colnames_cum = []
data_cum = {}


def extract_values_from_json():
	for file in os.listdir('../data/'):
		colname = re.search(regex, file).group()
		colnames_cum.append(colname)

		filename = '../data/'+file
		print(filename)
		f = open(filename, 'r')
		dat_temp = json.load(f)
		results = dat_temp['results'][0]['series'][0]['values']

		col_values = []
		for item in results:
			col_values.append(item[8])
		data_cum[colname] = col_values


def write_csv_data_file():
	with open('../ressources/data.csv', 'w') as file:
		for key_col in colnames_cum:
			file.write(key_col + " " + str(data_cum[key_col].strip('[]')))
		file.close()


if __name__ == '__main__':
	extract_values_from_json()
	write_csv_data_file()
