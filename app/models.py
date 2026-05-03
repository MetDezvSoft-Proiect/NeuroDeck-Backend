from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

#Tabelul pentru Utilizatori
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # Relația:un utilizator are mai multe documente
    documents = relationship("Document", back_populates="owner")


#Tabelul pentru Documentele încărcate (Cursuri/PDF-uri)
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String) # Aici salvăm textul brut extras din PDF
    upload_date = Column(DateTime, default=datetime.utcnow)
    #Cheia externă: leagă documentul de ID-ul utilizatorului
    user_id = Column(Integer, ForeignKey("users.id"))
    #Relațiile bidirecționale
    owner = relationship("User", back_populates="documents")
    flashcards = relationship("Flashcard", back_populates="document")


#Tabelul pentru Flashcards (Generat de AI)
class Flashcard(Base):
    __tablename__ = "flashcards"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    correct_answer = Column(String)
    # Cheia externă:leagă flashcard-ul de ID-ul documentului
    document_id = Column(Integer, ForeignKey("documents.id"))
    #Relația inversă
    document = relationship("Document", back_populates="flashcards")