"""TESTS - UTILS - MQTT TEST CLIENT
MQTT Client instance for PUB/SUB during tests
"""

# # Native # #
from queue import Queue

# # Installed # #
import pydantic
from paho.mqtt import client as mqtt

# # Project # #
from mqtt2etcd.settings import mqtt_settings as settings
from mqtt2etcd.connectors.mqtt_topics import *


__all__ = ("MQTTTestClient", "MQTTMessage")


class MQTTMessage(pydantic.BaseModel):
    topic: str
    payload: str


class MQTTTestClient(mqtt.Client):
    def __init__(self, **kwargs):
        kwargs["client_id"] = "TEST_" + settings.client_id
        super().__init__(**kwargs)
        self.on_connect = self._on_connect_callback
        self.on_message = self._on_message_callback
        self.received_messages = Queue()

    def _on_connect_callback(self, *args):
        self.subscribe(get_topic(ContextTopics.WATCH, "#"))

    def _on_message_callback(self, *args):
        message = next(a for a in args if isinstance(a, mqtt.MQTTMessage))
        topic, payload = message.topic, message.payload.decode()
        message = MQTTMessage(topic=topic, payload=payload)
        self.received_messages.put(message)

    def start(self):
        self.connect(host=settings.broker, port=settings.broker_port)
        self.loop_start()

    def stop(self):
        self.loop_stop(force=True)
        self.disconnect()
