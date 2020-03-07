from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello'


# ns: monitor
# svc: prometheus

# 10.98.149.68
# 9090/TCP

# HOST = "10.98.149.68"
# PORT = 9090

