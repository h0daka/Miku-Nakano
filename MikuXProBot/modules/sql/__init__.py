from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from MikuXProBot import DB_URI, LOGGER
from MikuXProBot.config import Development as Config


def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8", echo=Config.DEBUG)
    LOGGER.info("[PostgreSQL] Connecting to fucking database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=True))


BASE = declarative_base()
try:
    SESSION: scoped_session = start()
except Exception as e:
    LOGGER.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
LOGGER.info("[PostgreSQL] Fuking Connection successful, session started.")
