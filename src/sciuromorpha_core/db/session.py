from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sciuromorpha_core.config import config

engine = create_engine(config["db"]["url"], pool_pre_ping=True, future=True)
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
