"""MQTT TOPICS
Helpers to get MQTT topics from settings
"""

# # Native # #
from typing import Optional

# # Project # #
from ..settings import mqtt_settings as settings

__all__ = ("ContextTopics", "get_topic")


class ContextTopics:
    PUT = settings.topic_put
    """MQTT > ETCD. External clients publish messages here. MQTT2ETCD is subscribed to this topic."""
    WATCH = settings.topic_watch
    """ETCD > MQTT. The MQTT2ETCD app publishes watched key changes here."""
    STATUS = settings.topic_status


def get_topic(context: str, key: Optional[str] = None):
    levels = [settings.topic_base, context]
    if key is not None:
        levels.append(key)

    return "/".join(levels)
