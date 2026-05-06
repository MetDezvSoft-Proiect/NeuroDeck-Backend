from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# 1. SCHEME PENTRU FLASHCARDS
class FlashcardBase(BaseModel):
    question: str
    correct_answer: str

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardResponse(FlashcardBase):
    id: int
    document_id: int
    session_id: Optional[int] = None
    created_at: datetime
    class Config:
        from_attributes = True

# SCHEME PENTRU SESIUNI DE STUDIU (NOU)
class StudySessionBase(BaseModel):
    title: str

class StudySessionCreate(StudySessionBase):
    pass

class StudySessionCreateRequest(StudySessionBase):
    user_id: int

class StudySessionResponse(StudySessionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class StudySessionWithFlashcards(StudySessionResponse):
    flashcards: List[FlashcardResponse] = []
    class Config:
        from_attributes = True

# SCHEME PENTRU DOCUMENTE
class DocumentBase(BaseModel):
    title: str
    content: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    upload_date: datetime
    user_id: int
    session_id: Optional[int] = None
    flashcards: List[FlashcardResponse] = []
    class Config:
        from_attributes = True

# SCHEME PENTRU UTILIZATORI
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    study_sessions: List[StudySessionResponse] = []
    documents: List[DocumentResponse] = []
    class Config:
        from_attributes = True