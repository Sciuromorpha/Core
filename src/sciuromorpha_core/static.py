from enum import Enum

# Config sections
CONFIG_SECTION_SCIUROMORPHA = "sciuromorpha"
CONFIG_SECTION_DATABASE = "db"
CONFIG_SECTION_MESSAGEQUEUE = "mq"

# ENV variables
ENV_DOT_FILE = "ENV"
ENV_CONFIG_PREFIX = "SCIUROMORPHA_"
ENV_CONFIG_MODE = ENV_CONFIG_PREFIX + "MODE"
ENV_CONFIG_FILE = ENV_CONFIG_PREFIX + "CONFIG"
ENV_CONFIG_FILES = ENV_CONFIG_PREFIX + "CONFIG_FILES"

# Enviroment modes.
ENV_MODE_DEVELOPMENT = "development"
ENV_MODE_PRODUCTION = "production"
ENV_MODE_TEST = "test"

# Meta data keys.
META_KEY_STUB = "_"
META_KEY_ORIGIN_URL = "origin_url"

SERVICE_STATUS_ONLINE = "online"
SERVICE_STATUS_OFFLINE = "offline"


class TASK_STATUS(Enum):
    PENDING = "pending"
    WAITING = "waiting"
    RUNNING = "running"
    PROCESSING = "running"
    SUCCESS = "success"
    FAILED = "failed"


TASK_STATUS_PENDING = "pending"
TASK_STATUS_WAITING = "waiting"
TASK_STATUS_RUNNING = "running"
TASK_STATUS_PROCESSING = "running"
TASK_STATUS_SUCCESS = "success"
TASK_STATUS_FAILED = "failed"
