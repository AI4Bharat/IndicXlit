# Hosting

## Pre-requisites
1. [Install Caddy](https://caddyserver.com/docs/install)
2. `sudo apt install libnss3-tools`

## Running server

```
python start_server.py
```

## Reverse-proxying and connecting to a domain

Non-blocking:
```
sudo caddy start
sudo caddy stop
```

Blocking:
```
sudo caddy run
```
