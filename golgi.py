from flask import Flask, render_template
from influxdb import InfluxDBClient
from datetime import datetime
import random
import time

app = Flask(__name__)

user = 'root'
password = 'root'
dbname = 'example'
dbuser = 'smly'
dbuser_password = 'my_secret_password'
query = 'select value from cpu_load_short;'
host = '192.168.65.2'
port = 8086

db = InfluxDBClient(host, port, user, password, dbname)

db.create_database(dbname, if_not_exists=True)

@app.route("/w")
def write():
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": datetime.now(),
            "fields": {
                "value": random.randint(0, 100)
            }
        }
    ]

    db.write_points(json_body)
    return "wrote"

epoch = datetime.utcfromtimestamp(0)

def unix_time_millis(dts):
    parts = dts.split('.')
    dt = datetime.strptime(parts[0], '%Y-%m-%dT%H:%M:%S')
    ms = int((dt - epoch).total_seconds() * 1000.0)
    us = int(parts[1].replace('.','').replace('Z',''))
    return (ms * 1000) + us

@app.route("/")
def chart():
    result = db.query(query)
    data = []
    since = []
    for r in result.get_points():
        print r
        data.append(r["value"])
        since.append(unix_time_millis(r["time"]))
    return render_template('chart.html', data=data, since=since)

@app.route("/latest/<since>")
def latest():
    result = db.query('select value from cpu_load_short where time>=' + since)
    data = []
    for r in result.get_points():
        data.append(r["value"])
    return data

if __name__ == "__main__":
    app.run( debug=True)
