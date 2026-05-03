from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

#Această linie creează efectiv fișierul neurodeck.db și tabelele la pornirea aplicației
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="NeuroDeck API", description="API-ul pentru platforma de micro-learning", version="1.0.0")
#Rută simplă pentru a verifica dacă serverul e activ
@app.get("/")
def citeste_status():
    return {"mesaj": "Salut! Backend-ul NeuroDeck funcționează perfect!"}

#RUTE PENTRU UTILIZATORI
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    #Verificăm dacă email-ul există deja în baza de date
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email-ul este deja înregistrat")
    #Dacă nu există, chemăm funcția din crud.py să îl creeze
    return crud.create_user(db=db, user=user)

# RUTE PENTRU DOCUMENTE
@app.post("/users/{user_id}/documents/", response_model=schemas.DocumentResponse)
def create_document_for_user(user_id: int, document: schemas.DocumentCreate, db: Session = Depends(database.get_db)):
    #Chemăm funcția care adaugă documentul în baza de date
    return crud.create_user_document(db=db, document=document, user_id=user_id)

@app.get("/users/{user_id}/documents/", response_model=list[schemas.DocumentResponse])
def read_user_documents(user_id: int, db: Session = Depends(database.get_db)):
    #Returnăm lista de documente a unui anumit utilizator
    return crud.get_user_documents(db=db, user_id=user_id)