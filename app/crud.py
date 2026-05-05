from sqlalchemy.orm import Session
from . import models, schemas

#FUNCȚII PENTRU UTILIZATORI
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# FUNCȚII PENTRU SESIUNI DE STUDIU (NOU)
def create_study_session(db: Session, session: schemas.StudySessionCreate, user_id: int):
    db_session = models.StudySession(**session.model_dump(), user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_study_sessions(db: Session, user_id: int):
    return db.query(models.StudySession).filter(models.StudySession.user_id == user_id).all()

def get_study_session(db: Session, session_id: int):
    return db.query(models.StudySession).filter(models.StudySession.id == session_id).first()

def get_study_session_with_flashcards(db: Session, session_id: int):
    session = db.query(models.StudySession).filter(models.StudySession.id == session_id).first()
    return session

def update_study_session(db: Session, session_id: int, update_data: schemas.StudySessionCreate):
    db_session = get_study_session(db, session_id)
    if db_session:
        db_session.title = update_data.title
        db.commit()
        db.refresh(db_session)
    return db_session

def delete_study_session(db: Session, session_id: int):
    db_session = get_study_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
    return db_session

# FUNCȚII PENTRU DOCUMENTE
def get_user_documents(db: Session, user_id: int):
    return db.query(models.Document).filter(models.Document.user_id == user_id).all()

def get_session_documents(db: Session, session_id: int):
    return db.query(models.Document).filter(models.Document.session_id == session_id).all()

def create_user_document(db: Session, document: schemas.DocumentCreate, user_id: int, session_id: int = None):
    db_document = models.Document(**document.model_dump(), user_id=user_id, session_id=session_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

#FUNCȚII PENTRU FLASHCARDS
def create_flashcard(db: Session, flashcard: schemas.FlashcardCreate, document_id: int, session_id: int = None):
    db_flashcard = models.Flashcard(**flashcard.model_dump(), document_id=document_id, session_id=session_id)
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def get_document_flashcards(db: Session, document_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.document_id == document_id).all()

def get_session_flashcards(db: Session, session_id: int):
    return db.query(models.Flashcard).filter(models.Flashcard.session_id == session_id).all()