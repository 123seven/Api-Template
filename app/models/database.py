from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_DSN,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BaseModel = declarative_base()


def create_db_and_tables():
    BaseModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_session_maker():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
