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
    model_config = SettingsConfigDict()

    mq: AmqpDsn = Field(
        "amqp://guest:guest@localhost:5672/",
        validation_alias=AliasChoices(
            "rabbit", "rabbmitmq", "rabbitmq_url", "amqp")
    )
    db: PostgresDsn = Field(
        "postgres://user:pass@localhost:5432/core",
        validation_alias=AliasChoices("pg", "pg_url"),
    )
    redis: RedisDsn = Field(
        "redis://user:pass@localhost:6379/1",
        validation_alias=AliasChoices("redis_url"),
    )
    service_name: str = "core"
