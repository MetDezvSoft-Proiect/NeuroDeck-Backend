from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

#Tabelul pentru Utilizatori
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relații: un utilizator are mai multe sesiuni de studiu
    study_sessions = relationship("StudySession", back_populates="owner")
    documents = relationship("Document", back_populates="owner")


#Tabelul pentru Sesiuni de Studiu (NOU)
class StudySession(Base):
    __tablename__ = "study_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)  # Ex: "Informatica", "Matematica"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relații
    owner = relationship("User", back_populates="study_sessions")
    documents = relationship("Document", back_populates="session", cascade="all, delete-orphan")
    flashcards = relationship("Flashcard", back_populates="session", cascade="all, delete-orphan")


#Tabelul pentru Documentele încărcate (Cursuri/PDF-uri)
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    #Chei externe
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=True)
    #Relații
    owner = relationship("User", back_populates="documents")
    session = relationship("StudySession", back_populates="documents")
    flashcards = relationship("Flashcard", back_populates="document")


#Tabelul pentru Flashcards (Generat de AI)
class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    correct_answer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Chei externe
    document_id = Column(Integer, ForeignKey("documents.id"))
    session_id = Column(Integer, ForeignKey("study_sessions.id"), nullable=True)
    #Relații
    document = relationship("Document", back_populates="flashcards")
    session = relationship("StudySession", back_populates="flashcards")