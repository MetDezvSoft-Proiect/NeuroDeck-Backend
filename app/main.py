from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os

from . import crud, models, schemas, database
# Folosim funcția care știe să citească toate PDF-urile dintr-un folder[cite: 4]
from .document_processor import extrage_text_din_toate_pdf, imparte_text_in_bucati
from .ai_agents import genereaza_flashcards, evalueaza_raspuns
from .utils import parseaza_flashcards_din_text

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="NeuroDeck API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def citeste_status():
    return {"mesaj": "Salut! Backend-ul NeuroDeck funcționează!"}

# --- RUTE AUTENTIFICARE ---
@app.post("/users/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Creează un utilizator nou[cite: 2]"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email-ul este deja înregistrat")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Verifică datele de logare"""
    db_user = crud.get_user_by_email(db, email=user.email)
    # Logica MVP de verificare a parolei cu hash-ul falsificat din crud.py[cite: 2]
    fake_hashed_password = user.password + "notreallyhashed"
    
    if not db_user or db_user.hashed_password != fake_hashed_password:
        raise HTTPException(status_code=400, detail="Email sau parolă incorectă")
    
    return {"mesaj": "Logare cu succes", "user_id": db_user.id, "email": db_user.email}

# --- RUTE AI & DOCUMENTE MULTIPLE ---
@app.post("/upload")
async def upload_si_genereaza_flashcards(
    files: List[UploadFile] = File(...), # NOU: Primește o listă de fișiere
    numar_intrebari: int = Form(...)
):
    temp_folder = "temp_pdfs"
    os.makedirs(temp_folder, exist_ok=True)
    
    try:
        nume_fisiere = []
        # Salvăm toate PDF-urile primite în folderul temporar
        for file in files:
            if file.filename.endswith(".pdf"):
                nume_fisiere.append(file.filename)
                file_path = os.path.join(temp_folder, file.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
        
        if not nume_fisiere:
             raise HTTPException(status_code=400, detail="Nu ai încărcat niciun PDF.")

        # Extragem textul combinat din toate fișierele[cite: 4]
        text_document = extrage_text_din_toate_pdf(temp_folder)
        
        if not text_document or not text_document.strip():
            raise HTTPException(status_code=500, detail="Nu s-a putut extrage text din PDF-uri.")

        bucati = imparte_text_in_bucati(text_document, dimensiune_chunk=4000)
        flashcards_text = genereaza_flashcards(bucati[0], numar_intrebari=numar_intrebari)
        flashcards_finale = parseaza_flashcards_din_text(flashcards_text)

        return {
            "filenames": nume_fisiere,
            "flashcards": flashcards_finale
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Ștergem întregul folder temporar
        shutil.rmtree(temp_folder, ignore_errors=True)

# --- RUTE EVALUARE ---
@app.post("/evaluate")
def evalueaza_raspuns_utilizator(intrebare_id: int, raspuns_utilizator: str, raspuns_corect: str, severitate: int = 2):
    scor = evalueaza_raspuns(raspuns_corect, raspuns_utilizator, severitate)
    return { "scor": scor, "status": "CORECT" if scor >= 70 else "INCORECT" }