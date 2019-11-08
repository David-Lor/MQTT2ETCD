"""RUNNER
Run the MQTT2ETCD service
"""

# # Package # #
from .logger import *
from .connectors.mqtt_client import MQTTClient

__all__ = ("run",)


def run():
    logger.debug("Starting MQTT2ETCD...")
    client = MQTTClient()

    try:
        client.run()
    except (KeyboardInterrupt, InterruptedError):
        pass

    client.stop()
    logger.debug("Bye!")


if __name__ == "__main__":
    run()
