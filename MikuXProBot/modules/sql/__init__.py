from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from MikuXProBot import DB_URI, LOGGER, DEBUG

def start() -> scoped_session:
    engine = create_engine(DB_URI, client_encoding="utf8", echo=DEBUG)
    LOGGER.info("[PostgreSQL] Connecting to database......")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=True))


BASE = declarative_base()
try:
    SESSION: scoped_session = start()
except Exception as e:
    LOGGER.exception(f'[PostgreSQL] Failed to connect due to {e}')
    exit()
   
LOGGER.info("[PostgreSQL] Connection successful, session started.")
