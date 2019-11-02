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
    WATCH = settings.topic_watch
    STATUS = settings.topic_status


def get_topic(context: str, key: Optional[str] = None):
    levels = [settings.topic_base, context]
    if key is not None:
        levels.append(key)

    return "/".join(levels)
