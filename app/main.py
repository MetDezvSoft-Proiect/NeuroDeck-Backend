from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os

# Importuri relative din pachetul 'app'
from . import crud, models, schemas, database
from .document_processor import extrage_text_dintr_un_pdf, imparte_text_in_bucati
from .ai_agents import genereaza_flashcards, evalueaza_raspuns
from .utils import parseaza_flashcards_din_text

# Crearea tabelelor la pornirea aplicației
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="NeuroDeck API", 
    description="API-ul pentru platforma de micro-learning și evaluare AI", 
    version="1.0.0"
)

# --- CONFIGURARE CORS (Esențial pentru React) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporar permitem toate originile
    allow_credentials=False,  # Trebuie False când folosim "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTE GENERALE ---
@app.get("/")
def citeste_status():
    return {"mesaj": "Salut! Backend-ul NeuroDeck funcționează perfect!"}

# --- RUTE UTILIZATORI ---
@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email-ul este deja înregistrat")
    return crud.create_user(db=db, user=user)

# --- RUTE AI & DOCUMENTE (LOGICA DE DRAG & DROP) ---
@app.post("/upload")
async def upload_si_genereaza_flashcards(file: UploadFile = File(...)):
    """
    Această rută primește PDF-ul de la Frontend, extrage textul 
    și generează flashcards folosind Llama 3.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Te rog încarcă un fișier PDF.")

    # Salvare temporară a fișierului pentru procesare
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Extragere text din PDF temporar
        text_document = extrage_text_dintr_un_pdf(temp_path)
        
        if not text_document:
            raise HTTPException(status_code=500, detail="Nu s-a putut extrage text din PDF.")

        # 2. Chunking & Generare (Limităm la un segment pentru test rapid)
        bucati = imparte_text_in_bucati(text_document, dimensiune_chunk=4000)
        flashcards_text = genereaza_flashcards(bucati[0], numar_intrebari=5)
        flashcards_finale = parseaza_flashcards_din_text(flashcards_text)

        return {
            "filename": file.filename,
            "flashcards": flashcards_finale
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Curățenie: ștergem fișierul temporar
        if os.path.exists(temp_path):
            os.remove(temp_path)

# --- RUTE EVALUARE ---
@app.post("/evaluate")
def evalueaza_raspuns_utilizator(
    intrebare_id: int,
    raspuns_utilizator: str,
    raspuns_corect: str,
    severitate: int = 2
):
    """
    Primește un răspuns și îl evaluează folosind modelul NLP local.
    """
    scor = evalueaza_raspuns(raspuns_corect, raspuns_utilizator, severitate)
    return {
        "scor": scor,
        "status": "CORECT" if scor >= 70 else "INCORECT"
    }