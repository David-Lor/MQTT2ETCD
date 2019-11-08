"""TESTS - UTILS - BASE TEST
Base test to be inherited by all tests of the project
"""

# # Native # #
import contextlib
from uuid import uuid4
from threading import Thread
from typing import List, Tuple

# # Project # #
from mqtt2etcd.connectors import ETCDClient
from mqtt2etcd.connectors import MQTTClient as MQTT2ETCDClient

# # Package # #
from .mqtt_test_client import MQTTTestClient

__all__ = ("BaseTest",)


class BaseTest:
    timeout = 5
    mqtt_client: MQTTTestClient
    etcd_client: ETCDClient
    app_client: MQTT2ETCDClient
    app_thread: Thread
    inserted_keys: List[str]

    def setup_method(self):
        self.inserted_keys = list()

        self.app_client = MQTT2ETCDClient()
        self.app_thread = Thread(target=self.app_client.run, daemon=True)
        self.app_thread.start()
        self.app_client.connected_event.wait(timeout=self.timeout)

        self.etcd_client = ETCDClient()
        self.mqtt_client = MQTTTestClient()
        self.mqtt_client.start()

    def teardown_method(self):
        for key in self.inserted_keys:
            with contextlib.suppress(Exception):
                self.etcd_client.delete(key)
        self.mqtt_client.stop()
        self.app_client.stop()
        self.app_thread.join(timeout=self.timeout)

    def get_kv(self, register=True) -> Tuple[str, str]:
        key, value = str(uuid4()), str(uuid4())
        if register:
            self.inserted_keys.append(key)
        return key, value
