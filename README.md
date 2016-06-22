# Setup

## Docker

https://docs.docker.com/engine/installation/

## Influx DB

```
docker run -d -p 8083:8083 -p 8086:8086 tutum/influxdb
```

## Website

```
python golgi.py
```