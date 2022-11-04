import os
import configparser
from xmlrpc.client import Boolean

config = configparser.ConfigParser(allow_no_value=True, strict=True)

# The DEFAULT configs.
config.read_dict(
    {
        "sciuromorpha": {
            "mode": "development",
        },
        "db": {
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
env_mode = os.environ.get("SCIUROMORPHA_MODE", "development")
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

if "SCIUROMORPHA_CONFIG" in os.environ:
    config_files.append(os.environ.get("SCIUROMORPHA_CONFIG"))

if "SCIUROMORPHA_CONFIG_FILES" in os.environ:
    config_files += os.environ.get("SCIUROMORPHA_CONFIG_FILES").split(":")

# Try to read config files.
config_files = config.read(config_files)

# Combine ENV variables.
db_section = config["db"]
db_section.update(
    {
        key.removeprefix("POSTGRES_"): value
        for key, value in os.environ.items()
        if key.startswith("POSTGRES_")
    }
)

config.read_dict(
    {
        "sciuromorpha": {
            "mode": env_mode,
            "config_files": config_files,
        },
        "db": {
            "url": f'{db_section["driver"]}://{db_section["user"]}'
            f'{":" if db_section["password"] else ""}{db_section["password"]}'
            f'@{db_section["host"]}{":" if db_section["port"] else ""}'
            f'{db_section["port"]}/{db_section["db"]}',
        },
    }
)
