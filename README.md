# MQTT2ETCD

Bridge between MQTT and ETCD, that can:

- PUT on ETCD by publishing on MQTT
- Watch ETCD keys and Publish changes on MQTT

## Requirements

- Python >= 3.6
- Packages listed on [requirements.txt](requirements.txt)
- Docker recommended for deployment

## Changelog

- 0.1.2 - add logging
- 0.1.1 - add settings to customize MQTT topics
- 0.0.1 - initial version (base functional code, supporting MQTT2ETCD & ETCD2MQTT)

## Settings

Settings can be defined through environment variables or using a `.env` file (located within the `__main__.py` file).

### ETCD Settings

- **MQTT2ETCD_HOST**: ETCD server host (default: `127.0.0.1`)
- **MQTT2ETCD_PORT**: ETCD server port (default: `2379`)
- **MQTT2ETCD_LISTEN_PREFIX**: ETCD key prefix to watch (default=undefined; if undefined, will not watch)
- **MQTT2ETCD_LISTEN_ALL**: if 1, watch ALL ETCD keys (default=0; if 1 will override the LISTEN_PREFIX setting)
- **MQTT2ETCD_PREV_KV**: if 1, publish watched ETCD keys on startup (default=0)

### MQTT Settings

- **MQTT2ETCD_BROKER**: MQTT broker host (default: `127.0.0.1`)
- **MQTT2ETCD_BROKER_PORT**: MQTT broker port (default: `1883`)
- **MQTT2ETCD_CLIENT_ID**: MQTT client ID (default: `MQTT2ETCD-{uuid1}`)
- **MQTT2ETCD_RETAIN**: if 1, publish watched ETCD keys MQTT messages with Retain flag (default=0)
- **MQTT2ETCD_TOPIC_BASE**: Base level topic (default: `mqtt2etcd`)
- **MQTT2ETCD_TOPIC_PUT**: Context level for PUT (publish) keys (default: `put`)
- **MQTT2ETCD_TOPIC_WATCH**: Context level where watched keys get published (default: `stat`)
- **MQTT2ETCD_TOPIC_STATUS**: Context level where MQTT2ETCD service status messages get published (default: `status`)
- **MQTT2ETCD_PAYLOAD_ONLINE**: Payload to send on the Status topic when the service connects to MQTT (default: `Online`)
- **MQTT2ETCD_PAYLOAD_OFFLINE**: Payload to send on the Status topic when the service goes offline, as LWT (default: `Offline`)

### Misc System Settings

- **MQTT2ETCD_LOG_LEVEL**: Log level for the logger (default: `INFO`)

## MQTT Topics

Topics for ETCD keys are split in 3 levels (split by `/`):

1. Base level (default: `mqtt2etcd`)
2. Order/context level (default: `put`, `stat`)
3. ETCD key (it can contain multiple `/`, but shall not contain `#` nor `+`)

Having the order/context level at the end would be (personally) prefered, but would cause trouble with the MQTT wildcard pattern 
  for subscribing to the `put` order topics while supporting ETCD keys with `/`.

An additional topic for status about the MQTT2ETCD service (on-connect and LWT messages) get published on the Status topic
  (`mqtt2etcd/status` by default).

### MQTT2ETCD (PUT)

- Default topic is `mqtt2etcd/put/{key}`, being `{key}` the full ETCD key of the entry
- Payload must be the value to set

### ETCD2MQTT (Watch)

- Default topic is `mqtt2etcd/stat/{key}`, being `{key}` the full ETCD key of the entry
- Payload is the value of the entry

## Installing (via Docker)

The recommended method to install is using the [Python-Autoclonable-App](https://hub.docker.com/r/davidlor/python-autoclonable-app/) image:

```bash
sudo docker run -d \
  -e GIT_REPOSITORY=https://github.com/David-Lor/MQTT2ETCD.git \
  -e GIT_BRANCH=develop \
  -e MQTT2ETCD_BROKER={mqtt_broker_ip} \
  -e MQTT2ETCD_HOST={etcd_server_ip} \
  -v /etc/localtime:/etc/localtime:ro
  --name mqtt2etcd \
  davidlor/python-autoclonable-app
```

If you want to run it locally:

```bash
git clone https://github.com/David-Lor/MQTT2ETCD.git
python MQTT2ETCD
```
