"""Put data on an ETCD key. MQTT2ETCD watching the key should publish the data on MQTT.
"""

from time import sleep, time
from mqtt2etcd.connectors.etcd_client import ETCDClient


if __name__ == '__main__':
    client = ETCDClient()

    while True:
        try:
            client.put("foo", str(time()).encode())
            sleep(1)
        except (KeyboardInterrupt, InterruptedError):
            break
