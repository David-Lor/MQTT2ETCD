"""
"""

# # Installed # #
from paho.mqtt.client import Client, MQTTMessage

# # Project # #
from ..settings import mqtt_settings as settings

# # Package # #
from .etcd_client import ETCDClient

__all__ = ("MQTTClient",)


class MQTTClient(Client):
    etcd_client: ETCDClient

    def __init__(self, **kwargs):
        super().__init__(client_id=settings.client_id, **kwargs)
        self.etcd_client = ETCDClient()
        self.on_connect = self._on_connect_callback
        self.on_message = self._on_message_callback

    def connect(self, **kwargs):
        super().connect(host=settings.broker, port=settings.broker_port, **kwargs)

    def _on_connect_callback(self, *args):
        self.publish("mqtt2etcd/status", "Online")
        self.will_set("mqtt2etcd/status", "Offline")
        self.subscribe("mqtt2etcd/set/#")

    def _on_message_callback(self, *args):
        message = next(a for a in args if isinstance(a, MQTTMessage))
        topic, payload = message.topic, message.payload.decode()
        print("RX MQTT", topic, payload)

        key = topic.replace("mqtt2etcd/set/", "")

        print("PUT", key, payload)
        self.etcd_client.put(key, payload)

    def _etcd_watch_callback(self, event):
        key, value = event.key.decode(), event.value.decode()
        print("RX ETCD", event)
        self.publish(f"mqtt2etcd/stat/{key}", value, retain=settings.retain)

    def run(self):
        self.connect()
        self.etcd_client.start_watch(self._etcd_watch_callback)
        self.loop_forever()
