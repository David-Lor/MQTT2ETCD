"""
"""

# # Package # #
from .connectors.mqtt_client import MQTTClient

__all__ = ("run",)


def run():
    client = MQTTClient()

    try:
        client.run()
    except (KeyboardInterrupt, InterruptedError):
        pass

    print("Bye!")


if __name__ == "__main__":
    run()
