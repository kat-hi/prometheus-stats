# prometheus-stats

## what is this project about?
using the prometheus api for statistical analysis of its metrics

## How to fetch data from prometheus api 
### prerequisite
```
$ kubectl port-forward podname 9100:9100
```
### scripts / execution
scripts/metrics_cmd.py [arg1] [arg2] [arg3]

- arg1 : ressource ( e.g. "/api/v1/query" or "/api/v1/query_range"
- arg2 : parameter ( e.g. "node_cpu_seconds_total", use items from ressources/queries.txt )
- arg3 : filename ( e.g "node_cpu_seconds_total.json" )


### ressources 
queries.txt | contains queries you may use to request data from /api/v1/

### notes
app.py is just a dummy application to run a container inside k8s. not necessary, just from the very beginning.
