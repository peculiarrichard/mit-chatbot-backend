from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
from src.config import settings
import logging


DATABASE_URL = settings.DATABASE_URL

logger = logging.getLogger(__name__)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    logger.info("DB session created")
    try:
        yield db
        logger.info("DB session closed")
    finally:
        db.close()
