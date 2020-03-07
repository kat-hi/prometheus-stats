# prometheus-stats

## what is this project about?
using the influxdb api for statistical analysis of its prometheus metrics

## How to fetch data from influxdb api 
### prerequisite
- influxdb is deployed on your k8s cluster and gets data from prometheus
- do port forward to your local machine:

```
$ kubectl port-forward podname 8086:8086
```


