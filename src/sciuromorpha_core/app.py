import os
from sciuromorpha_core import static as S
from sciuromorpha_core import Settings
from faststream import FastStream, Context
from faststream.rabbit import RabbitBroker
from faststream.rabbit.annotations import (
    Logger, ContextRepo, RabbitMessage,
    RabbitBroker as BrokerAnnotation, RabbitProducer, NoCast,
)

broker = RabbitBroker()
app = FastStream(broker)


@app.on_startup
async def setup(context: ContextRepo, env: str = ".env"):
    settings = Settings(_env_file=os.environ.get(S.ENV_DOT_FILE, env))
    context.set_global("settings", settings)


@app.on_startup
async def connect_db(
        logger: Logger,
        settings: Settings = Context()):
    # TODO: migration db struct here.
    logger.debug("connect_db in app.py")
    pass


@app.on_startup
async def connect_mq(settings: Settings = Context()):
    # Everything is OK, let's connect to mq and start service.
    await broker.connect(str(settings.mq))


@app.after_startup
async def publish_online(
    logger: Logger,
    broker: BrokerAnnotation,
):
    # Publish online message to broker.
    await broker.publish({
        "status": "ONLINE",
    }, queue="service-core")
    logger.info("Core service startup success.")
