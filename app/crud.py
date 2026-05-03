from sqlalchemy.orm import Session
from . import models, schemas

#FUNCȚII PENTRU UTILIZATORI
def get_user_by_email(db: Session, email: str):
    # Caută un utilizator după adresa de email
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    # În viața reală parola trebuie criptată! Pentru MVP MDS o lăsăm așa ca să o putem testa ușor.
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# FUNCȚII PENTRU DOCUMENTE
def get_user_documents(db: Session, user_id: int):
    #Returnează toate documentele unui anumit utilizator
    return db.query(models.Document).filter(models.Document.user_id == user_id).all()

def create_user_document(db: Session, document: schemas.DocumentCreate, user_id: int):
    #Salvează un document nou încărcat de utilizator
    db_document = models.Document(**document.model_dump(), user_id=user_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

#FUNCȚII PENTRU FLASHCARDS
def create_flashcard(db: Session, flashcard: schemas.FlashcardCreate, document_id: int):
    #Adaugă un flashcard nou generat de Agentul AI
    db_flashcard = models.Flashcard(**flashcard.model_dump(), document_id=document_id)
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

def get_document_flashcards(db: Session, document_id: int):
    #Extrage toate cardurile pentru a începe sesiunea de studiu
    return db.query(models.Flashcard).filter(models.Flashcard.document_id == document_id).all()