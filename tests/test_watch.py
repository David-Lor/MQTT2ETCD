"""TEST - WATCH
"""

# # Native # #
import random

# # Package # #
from .utils import *

# # Project # #
from mqtt2etcd.settings import etcd_settings
from mqtt2etcd.connectors.mqtt_topics import *


class TestWatch(BaseTest):
    """Test watching ETCD keys. Changing keys should get published on MQTT topics."""

    def setup_method(self):
        # Skip setup_method from BaseTest; manually called from tests
        pass

    def _setup(self):
        super().setup_method()

    def test_watch_all(self):
        """Watching all keys, when a key changes, the value should be published on MQTT"""
        etcd_settings.listen_all = True
        etcd_settings.listen_prefix = None
        self._setup()

        key, value = self.get_kv()
        expected_topic = get_topic(ContextTopics.WATCH, key)
        self.etcd_client.put(key, value.encode())

        received: MQTTMessage = self.mqtt_client.received_messages.get(timeout=self.timeout)
        assert received.topic == expected_topic
        assert received.payload == value

    # TODO Failing test
    def test_watch_prefix(self):
        """Watching a prefix, when a key with that prefix changes, the value should be published on MQTT"""
        prefix = str(random.randint(100, 1000))
        key, value = self.get_kv(register=False)
        key = prefix + key

        etcd_settings.listen_all = False
        etcd_settings.listen_prefix = prefix
        self._setup()

        self.inserted_keys.append(key)
        other_key, other_value = self.get_kv(register=True)

        expected_topic = get_topic(ContextTopics.WATCH, key)
        self.etcd_client.put(other_key, other_value.encode())
        self.etcd_client.put(key, value.encode())

        received: MQTTMessage = self.mqtt_client.received_messages.get(timeout=self.timeout)
        assert received.topic == expected_topic
        assert received.payload == value
