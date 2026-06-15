"""Configurare comuna pentru teste (fixtures pytest).

Foloseste o baza de date SQLite in memorie, izolata pentru fiecare test,
ca sa nu atinga fisierul real `neurodeck.db`.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
# Importam models pentru ca tabelele sa fie inregistrate pe Base.metadata
from app import models  # noqa: F401


@pytest.fixture
def db():
    """Returneaza o sesiune de baza de date izolata, curata pentru fiecare test."""
    engine = create_engine(
        "sqlite://",  # baza de date in memorie
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
