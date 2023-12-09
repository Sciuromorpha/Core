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
    logger.debug("connect_db in db/session.py")

    if settings.service_mode == S.ENV_MODE_DEVELOPMENT:
        # Let sqlalchemy log every SQL in development mode.
        import logging

        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

    from sqlalchemy import create_engine

    engine = create_engine(settings.db, pool_pre_ping=True, future=True)
    SessionFactory = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, future=True
    )

    context.set_global("db_engine", engine)
    context.set_global("db_session", SessionFactory)


@app.before_shutdown
async def disconnect_db(
    context: ContextRepo,
    logger: Logger,
    engine: Engine = Context(),
    db_session: sessionmaker = Context(),
):
    logger.debug("disconnect_db in db/session.py")

    if db_session:
        context.set_global("db_session", None)
        db_session.close_all()
        logger.debug("SessionFactory closed.")

    if engine:
        context.set_global("db_engine", None)
        engine.dispose()
        logger.debug("Engine disposed.")

    logger.debug("disconnect_db done.")
