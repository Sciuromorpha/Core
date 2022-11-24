import sciuromorpha_core.static as S
from sciuromorpha_core.config import config

if config[S.CONFIG_SECTION_SCIUROMORPHA]["mode"] == S.ENV_MODE_DEVELOPMENT:
    # We are in development mode, enable logs for SQL.
    import logging

    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    config[S.CONFIG_SECTION_DATABASE]["url"], pool_pre_ping=True, future=True
)
SessionFactory = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, future=True
)
