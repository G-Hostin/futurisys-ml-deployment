import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv() # charge les variables

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data.db")

engine = create_engine(DATABASE_URL) # crée la connexion avec PostgreSQL
SessionLocal = sessionmaker(bind=engine) # fabrique les sessions


class Base(DeclarativeBase): # Base → classe parente de toutes les tables
    pass