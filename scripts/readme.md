### influxdb_client.py
- provides Influxfetcher-class and methods to fetch data from influxdb

### parse_args.py
- helper module that is used by influxdb_client.py

### logit.py
- running regression analysis or whatever


## How to Dataexploration 

## Build your own env
```
python3 -m venv env

pip3 install -r requirements.txt
```

### prerequisite
```
$ kubectl port-forward influxdb-669bb8c4cb-6445d 8086:8086
```

## Run the script

```
source env/bin/activate
python3 influxdb_client.py
```

