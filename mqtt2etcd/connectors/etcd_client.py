"""
"""

# # Installed # #
from etcd3 import Etcd3Client

# # Project # #
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

        self.add_watch_callback(**kwargs)
