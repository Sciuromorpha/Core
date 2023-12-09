import os
from uuid import uuid4
from sciuromorpha_core import static as S
from sciuromorpha_core import Settings
from faststream import FastStream, Context
from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import (
    Logger,
    ContextRepo,
    RabbitMessage,
    RabbitBroker as BrokerAnnotation,
    RabbitProducer,
    NoCast,
)

broker = RabbitBroker()
app = FastStream(broker)
app_id = str(uuid4())


@app.on_startup
async def setup(context: ContextRepo, logger: Logger, env: str = ".env"):
    settings = Settings(_env_file=os.environ.get(S.ENV_DOT_FILE, env))
    context.set_global("settings", settings)

    await broker.connect(str(settings.mq))
    logger.debug("connect to mq success")


@app.after_startup
async def publish_online(
    logger: Logger,
    broker: BrokerAnnotation,
):
    # Publish online message to broker.
    await broker.publish(
        {
            "status": "ONLINE",
            "app_id": app_id,
        },
        queue="service-core",
    )
    logger.info("Core service startup success.")


@app.on_shutdown
async def publish_offline(
    logger: Logger,
    broker: BrokerAnnotation,
):
    # Publish online message to broker.
    await broker.publish(
        {
            "status": "OFFLINE",
            "app_id": app_id,
        },
        queue="service-core",
    )
    logger.info("Core service startup success.")
