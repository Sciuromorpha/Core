import os
import logging
import configparser
from . import static as S
from xmlrpc.client import Boolean

logging.basicConfig()
logger = logging.getLogger("sciuromorpha.core")

config = configparser.ConfigParser(allow_no_value=True, strict=True)

# The DEFAULT configs.
config.read_dict(
    {
        S.CONFIG_SECTION_SCIUROMORPHA: {
            "mode": S.ENV_MODE_DEVELOPMENT,
        },
        S.CONFIG_SECTION_DATABASE: {
            "driver": "postgresql",
            "host": "localhost",
            "port": "5432",
            "user": "postgres",
            "password": "",
            "db": "sciuromorpha",
        },
    }
)

# Try get environ variables.
env_mode = os.environ.get(S.ENV_CONFIG_MODE, S.ENV_MODE_DEVELOPMENT)
config_files = [
    f"../../../config.ini",
    f"../../../{env_mode}.ini",
    f"../../config.ini",
    f"../../{env_mode}.ini",
    f"../config.ini",
    f"../{env_mode}.ini",
    f"./config.ini",
    f"./{env_mode}.ini",
    f"~/.config/sciuromorpha/config.ini",
    f"~/.config/sciuromorpha/{env_mode}.ini",
]

if S.ENV_CONFIG_FILE in os.environ:
    config_files.append(os.environ.get(S.ENV_CONFIG_FILE))

if S.ENV_CONFIG_FILES in os.environ:
    config_files += os.environ.get(S.ENV_CONFIG_FILES).split(":")

# Try to read config files.
config_files = config.read(config_files)

# Setup logger to INFO when mode is development.
if env_mode == S.ENV_MODE_DEVELOPMENT:
    logger.setLevel(logging.INFO)
else:
    logger.setLevel(logging.WARN)

logger.info(
    f"Loaded config files: {':'.join(config_files)}",
)

# Combine ENV variables.
db_section = config[S.CONFIG_SECTION_DATABASE]
db_section.update(
    {
        key.removeprefix("POSTGRES_"): value
        for key, value in os.environ.items()
        if key.startswith("POSTGRES_")
    }
)

if "url" in db_section:
    db_url = db_section["url"]
else:
    db_url = f'{db_section["driver"]}://{db_section["user"]}{":" if db_section["password"] else ""}{db_section["password"]}@{db_section["host"]}{":" if db_section["port"] else ""}{db_section["port"]}/{db_section["db"]}'

config.read_dict(
    {
        S.CONFIG_SECTION_SCIUROMORPHA: {
            "mode": env_mode,
            "config_files": config_files,
        },
        S.CONFIG_SECTION_DATABASE: {
            "url": db_url,
            "sqlalchemy.url": db_url,
        },
    }
)
