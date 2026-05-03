from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 1. SCHEME PENTRU FLASHCARDS
class FlashcardBase(BaseModel):
    question: str
    correct_answer: str
#Schema folosită când creăm un flashcard nou
class FlashcardCreate(FlashcardBase):
    pass
#Schema folosită când trimitem datele înapoi către Frontend (include ID-ul)
class FlashcardResponse(FlashcardBase):
    id: int
    document_id: int
    class Config:
        from_attributes = True  #Permite lui Pydantic să citească din SQLAlchemy

#SCHEME PENTRU DOCUMENTE
class DocumentBase(BaseModel):
    title: str
    content: str
class DocumentCreate(DocumentBase):
    pass
class DocumentResponse(DocumentBase):
    id: int
    upload_date: datetime
    user_id: int
    flashcards: List[FlashcardResponse] = [] #Un document vine la pachet cu cardurile lui
    class Config:
        from_attributes = True

#SCHEME PENTRU UTILIZATORI
class UserBase(BaseModel):
    email: EmailStr #Validează automat dacă este un email corect
class UserCreate(UserBase):
    password: str #Când creăm contul, cerem parola
class UserResponse(UserBase):
    id: int
    documents: List[DocumentResponse] = [] #Nu trimitem parola înapoi la Frontend, doar datele sigure
    class Config:
        from_attributes = True