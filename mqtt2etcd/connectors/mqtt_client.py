"""MQTT CLIENT
MQTTClient runs the MQTT client that listen and publish ETCD keys.
The MQTTClient class inherits from paho.mqtt.client.Client, and instantiates an ETCDClient instance to
watch and put ETCD keys.
"""

# # Installed # #
from paho.mqtt.client import Client, MQTTMessage

# # Project # #
from ..logger import *
from ..settings import mqtt_settings as settings

# # Package # #
from .mqtt_topics import *
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
        logger.debug(f"Connecting to MQTT on {settings.broker}:{settings.broker_port}...")
        super().connect(host=settings.broker, port=settings.broker_port, **kwargs)

    def _on_connect_callback(self, *args):
        self.publish(get_topic(ContextTopics.STATUS), settings.payload_online)
        self.will_set(get_topic(ContextTopics.STATUS), settings.payload_offline)
        self.subscribe(get_topic(ContextTopics.PUT, "#"))
        logger.info("MQTT connected!")

    def _on_message_callback(self, *args):
        message = next(a for a in args if isinstance(a, MQTTMessage))
        topic, payload = message.topic, message.payload.decode()
        logger.debug(f"RX @ MQTT (topic={topic}): {payload}")

        key = topic.replace(get_topic(ContextTopics.PUT, ""), "")

        self.etcd_client.put(key, payload)

    def _etcd_watch_callback(self, event):
        key, value = event.key.decode(), event.value.decode()
        logger.debug(f"RX @ ETCD (key={key}): {value}")
        self.publish(get_topic(ContextTopics.WATCH, key), value, retain=settings.retain)

    def run(self):
        self.connect()
        self.etcd_client.start_watch(self._etcd_watch_callback)
        self.loop_forever()
