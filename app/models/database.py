from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine, SQLModel, Session

from app.core.config import settings

# must import model


engine = create_engine(settings.DATABASE_DSN, echo=settings.DEBUG, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_session_maker():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
