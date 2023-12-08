from sciuromorpha_core import S, Settings, app
from faststream import FastStream, Context
from faststream.rabbit.annotations import (
    Logger, ContextRepo, RabbitMessage,
    RabbitBroker as BrokerAnnotation, RabbitProducer, NoCast,
)


@app.on_startup
async def connect_db(
        context: ContextRepo,
        logger: Logger,
        settings: Settings = Context()):
    logger.debug("connect_db in db/session.py")

    if settings.core.get("mode", "") == S.ENV_MODE_DEVELOPMENT:
        # Let sqlalchemy log every SQL in development mode.
        import logging

        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine(
        settings.db, pool_pre_ping=True, future=True
    )
    SessionFactory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, future=True
    )

    context.set_global("db_engine", engine)
    context.set_global("db_session", SessionFactory)
