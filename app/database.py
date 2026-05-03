from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#Se creează fișierul bazei de date pe hard disk
SQLALCHEMY_DATABASE_URL = "sqlite:///./neurodeck.db"
#Engine-ul comunică cu baza de date SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#SessionLocal va fi folosit pentru interogări
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#'Base' este clasa părinte cerută de models.py!
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()