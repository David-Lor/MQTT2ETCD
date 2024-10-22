"""SETTINGS
Settings for ETCD, MQTT and the service
"""

# # Native # #
import uuid
from typing import Optional

# # Installed # #
from dotenv import load_dotenv

# # Installed # #
from dotenv_settings_handler import BaseSettingsHandler

__all__ = ("etcd_settings", "mqtt_settings", "system_settings")


class BaseSettings(BaseSettingsHandler):
    class Config:
        env_prefix = "MQTT2ETCD_"
        case_insensitive = True


class ETCDSettings(BaseSettings):
    host: str = "127.0.0.1"
    port: int = 2379
    listen_prefix: Optional[str]
    listen_all: bool = False
    prev_kv: bool = False


class MQTTSettings(BaseSettings):
    broker: str = "127.0.0.1"
    broker_port: int = 1883
    client_id: str = f"MQTT2ETCD-{uuid.uuid1()}"
    retain: bool = False
    topic_base: str = "mqtt2etcd"
    topic_status: str = "status"
    topic_put: str = "put"
    topic_watch: str = "stat"
    payload_online: str = "Online"
    payload_offline: str = "Offline"


class SystemSettings(BaseSettings):
    log_level: str = "INFO"


load_dotenv()

etcd_settings = ETCDSettings()
mqtt_settings = MQTTSettings()
system_settings = SystemSettings()
