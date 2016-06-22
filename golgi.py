from flask import Flask, render_template
from influxdb import InfluxDBClient
from datetime import datetime
import random

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

@app.route("/")
def chart():
    result = db.query(query)
    data = []
    for r in result.get_points():
        print r
        data.append(r["value"])
    return render_template('chart.html', data=data)

if __name__ == "__main__":
    app.run( debug=True)
