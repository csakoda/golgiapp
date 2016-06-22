# Setup

## Docker

https://docs.docker.com/engine/installation/

## Influx DB

```
docker run -d -p 8083:8083 -p 8086:8086 tutum/influxdb
```

This will start an influxDB for storing our votes in docker.

## Website

```
pip install -r requirements.txt
python golgi.py
```

You can access the site by browsing to <http://localhost:5000>

You can add a test vote by going to <http://localhost:5000/w>

# TODO

- [ ] Buttons (dial?) for voting
- [ ] Proper rollup and aggregation on the graph
- [ ] Proper timestamps on the graph
- [ ] Rolling graph updates
