import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.secrets import Secrets

engine = create_engine(Secrets.get_secret('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()