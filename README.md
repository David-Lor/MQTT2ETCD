# MQTT2ETCD

Bridge between MQTT and ETCD, that can:

- PUT on ETCD by publishing on MQTT
- Watch ETCD keys and Publish changes on MQTT

## Requirements

- Python >= 3.6
- Packages listed on [requirements.txt](requirements.txt)
- Docker recommended for deployment

## Changelog

- 0.0.1 - initial version (base functional code, supporting MQTT2ETCD & ETCD2MQTT)

## Settings

Settings can be defined through environment variables or a `.env` file.

### ETCD Settings

- **MQTT2ETCD_HOST**: ETCD server host (required)
- **MQTT2ETCD_PORT**: ETCD server port (required)
- **MQTT2ETCD_LISTEN_PREFIX**: ETCD key prefix to watch (optional, default=undefined; if undefined, will not watch)
- **MQTT2ETCD_LISTEN_ALL**: if 1, watch ALL ETCD keys (optional, default=0; if 1 will override the LISTEN_PREFIX setting)
- **MQTT2ETCD_PREV_KV**: if 1, publish watched ETCD keys on startup (optional, default=0)

### MQTT Settings

- **MQTT2ETCD_BROKER**: MQTT broker host (required)
- **MQTT2ETCD_BROKER_PORT**: MQTT broker port (required)
- **MQTT2ETCD_CLIENT_ID**: MQTT client ID (optional, default="MQTT2ETCD-{uuid1}")
- **MQTT2ETCD_RETAIN**: if 1, publish watched ETCD keys MQTT messages with Retain flag (optional, default=0) 

## MQTT Topics

Topics are split in 3 levels (split by `/`):

1. Base level (example: `mqtt2etcd`)
2. Order/context level (example: `put`)
3. ETCD key (it can contain multiple `/`, but shall not contain `#` nor `+`)

Having the order/context level at the end would be (personally) prefered, but would cause trouble with the MQTT wildcard pattern 
  for subscribing to the `put` order topics while supporting ETCD keys with `/`.

### MQTT2ETCD (PUT)

- Example topic is `mqtt2etcd/put/{key}`, being `{key}` the full ETCD key of the entry
- Payload must be the value to set

### ETCD2MQTT (Watch)

- Example topic is `mqtt2etcd/stat/{key}`, being `{key}` the full ETCD key of the entry
- Payload is the value of the entry
