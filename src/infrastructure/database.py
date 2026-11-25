import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.domain.models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./buzdolabi_local.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Tüm SQL tablolarını veritabanında oluşturur."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI ve servisler için güvenli veritabanı oturumu sağlar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        