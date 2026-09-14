from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.infrastructure.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=settings.DEBUG,)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """Base ORM model that all database tables inherit from."""
    pass

def get_db() -> Generator[Session, None, None]:
    """Provides a database session per HTTP request and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()