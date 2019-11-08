"""TEST - PUBLISH
"""

# # Native # #
from time import sleep

# # Project # #
from mqtt2etcd.settings import etcd_settings
from mqtt2etcd.connectors.mqtt_topics import *

# # Package # #
from .utils import *


class TestPublish(BaseTest):
    """Test publishing to the MQTT topic. The published values should be PUT on ETCD.
    """

    def setup_method(self):
        etcd_settings.listen_all = False
        etcd_settings.listen_prefix = None
        super().setup_method()
        sleep(1)  # TODO Avoid using sleep

    def test_publish(self):
        """When publishing to a key topic, the value should be set on ETCD"""
        key, value = self.get_kv()
        topic = get_topic(ContextTopics.PUT, key)

        self.mqtt_client.publish(topic, value)

        sleep(1)  # TODO Avoid using sleep
        read_value = self.etcd_client.get(key)
        assert read_value == value
