"""ETCD CLIENT
ETCDClient watch and put ETCD keys on the server.
The ETCDClient class inherits etcd3.Etcd3Client, and is instantiated on MQTTClient class, who calls its methods.
"""

# # Installed # #
from etcd3 import Etcd3Client

# # Project # #
from ..logger import *
from ..settings import etcd_settings as settings

__all__ = ("ETCDClient",)


class ETCDClient(Etcd3Client):
    def __init__(self, **kwargs):
        super().__init__(host=settings.host, port=settings.port, **kwargs)

    def start_watch(self, callback):
        kwargs = {
            "callback": callback,
            "prev_kv": settings.prev_kv
        }

        if settings.listen_all:
            kwargs["key"] = kwargs["range_end"] = "\0"
        elif settings.listen_prefix:
            kwargs["key"] = kwargs["listen_prefix"] = settings.listen_prefix
        else:
            logger.debug("No keys to watch on ETCD!")
            return

        self.add_watch_callback(**kwargs)
        logger.info(f"Started watch on ETCD key {kwargs['key']}")

    def put(self, key, value, **kwargs):
        logger.debug(f"PUT @ ETCD (key={key}): {value}")
        super().put(key, value, **kwargs)
