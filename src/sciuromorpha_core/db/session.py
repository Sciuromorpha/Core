from sciuromorpha_core import S, Settings, app
from faststream import FastStream, Context
from faststream.rabbit.annotations import (
    Logger,
    ContextRepo,
    RabbitMessage,
    RabbitBroker as BrokerAnnotation,
    RabbitProducer,
    NoCast,
)

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker


@app.on_startup
async def connect_db(
    context: ContextRepo, logger: Logger, settings: Settings = Context()
):
    if settings.service_mode == S.ENV_MODE_DEVELOPMENT:
        # Let sqlalchemy log every SQL in development mode.
        import logging

        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    from sqlalchemy import create_engine

    db_engine = create_engine(str(settings.db), pool_pre_ping=True, future=True)
    db_session = sessionmaker(
        autocommit=False, autoflush=False, bind=db_engine, future=True
    )

    context.set_global("db_engine", db_engine)
    context.set_global("db_session", db_session)
    logger.info("db connected.")


@app.on_shutdown
async def disconnect_db(
    context: ContextRepo,
    logger: Logger,
    db_engine: Engine = Context(),
    db_session: sessionmaker = Context(),
):
    logger.debug("disconnect_db in db/session.py")

    if db_session:
        context.reset_global("db_session")
        db_session.close_all()
        logger.debug("SessionFactory closed.")

    if db_engine:
        context.reset_global("db_engine")
        db_engine.dispose()
        logger.debug("Engine disposed.")

    logger.info("disconnect_db done.")
