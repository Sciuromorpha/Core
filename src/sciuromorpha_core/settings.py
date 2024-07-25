from sciuromorpha_core import static as S
from pydantic import (
    AliasChoices,
    AmqpDsn,
    Field,
    PostgresDsn,
    RedisDsn,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix='',
        extra="ignore",
        case_sensitive=False,
        str_strip_whitespace=True,
    )

    mq: AmqpDsn = Field(
        "amqp://guest:guest@localhost:5672/",
        validation_alias=AliasChoices(
            "mq", "rabbit", "rabbmitmq", "rabbitmq_url", "amqp")
    )
    db: PostgresDsn = Field(
        "postgresql://user:pass@localhost:5432/core",
        validation_alias=AliasChoices("db", "db_url", "pg", "pg_url"),
    )
    redis: RedisDsn = Field(
        "redis://user:pass@localhost:6379/1",
        validation_alias=AliasChoices("redis", "redis_url"),
    )
    service_name: str = "core"
    service_mode: str = Field(
        S.ENV_MODE_DEVELOPMENT,
        validation_alias=AliasChoices(S.ENV_CONFIG_MODE)
    )
