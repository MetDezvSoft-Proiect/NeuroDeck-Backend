from typing import List
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os

from . import crud, models, schemas, database
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
    """Creează un utilizator nou"""
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email-ul este deja înregistrat")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """Verifică datele de logare"""
    db_user = crud.get_user_by_email(db, email=user.email)
    fake_hashed_password = user.password + "notreallyhashed"
    
    if not db_user or db_user.hashed_password != fake_hashed_password:
        raise HTTPException(status_code=400, detail="Email sau parolă incorectă")
    
    return {"mesaj": "Logare cu succes", "user_id": db_user.id, "email": db_user.email}

# --- RUTE STUDY SESSIONS (NOU) ---
@app.post("/sessions")
def create_session(
    title: str = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(database.get_db)
):
    """Creează o nouă sesiune de studiu"""
    try:
        session_data = schemas.StudySessionCreate(title=title)
        return crud.create_study_session(db, session_data, user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sessions/{user_id}")
def get_user_sessions(user_id: int, db: Session = Depends(database.get_db)):
    """Listează toate sesiunile unui utilizator"""
    sessions = crud.get_user_study_sessions(db, user_id)
    return {"sessions": sessions}

@app.get("/sessions/detail/{session_id}", response_model=schemas.StudySessionWithFlashcards)
def get_session_detail(session_id: int, db: Session = Depends(database.get_db)):
    """Obține detalii sesiune cu flashcards"""
    session = crud.get_study_session_with_flashcards(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sesiune nu găsită")
    return session

@app.put("/sessions/{session_id}", response_model=schemas.StudySessionResponse)
def update_session(session_id: int, session_update: schemas.StudySessionCreate, db: Session = Depends(database.get_db)):
    """Actualizează titlul unei sesiuni"""
    updated = crud.update_study_session(db, session_id, session_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Sesiune nu găsită")
    return updated

@app.delete("/sessions/{session_id}")
def delete_session(session_id: int, db: Session = Depends(database.get_db)):
    """Șterge o sesiune și flashcards-urile ei"""
    deleted = crud.delete_study_session(db, session_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sesiune nu găsită")
    return {"mesaj": "Sesiune ștearsă cu succes"}

# --- RUTE AI & DOCUMENTE MULTIPLE (MODIFICAT) ---
@app.post("/upload")
async def upload_si_genereaza_flashcards(
    files: List[UploadFile] = File(...),
    numar_intrebari: int = Form(...),
    session_id: int = Form(...),
    user_id: int = Form(...),
    db: Session = Depends(database.get_db)
):
    """Upload PDF și generează flashcards salvate în DB"""
    temp_folder = "temp_pdfs"
    os.makedirs(temp_folder, exist_ok=True)
    
    try:
        # Verifică dacă sesiunea există și aparține utilizatorului
        session = crud.get_study_session(db, session_id)
        if not session or session.user_id != user_id:
            raise HTTPException(status_code=403, detail="Acces interzis la această sesiune")

        nume_fisiere = []
        # Salvează toate PDF-urile
        for file in files:
            if file.filename and file.filename.endswith(".pdf"):
                nume_fisiere.append(file.filename)
                file_path = os.path.join(temp_folder, file.filename)
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
        
        if not nume_fisiere:
            raise HTTPException(status_code=400, detail="Nu ai încărcat niciun PDF valid.")

        # Extrage textul din toate fișierele
        text_document = extrage_text_din_toate_pdf(temp_folder)
        
        if not text_document or not text_document.strip():
            raise HTTPException(status_code=500, detail="Nu s-a putut extrage text din PDF-uri.")

        # Salvează documentul în DB
        doc_schema = schemas.DocumentCreate(
            title=", ".join(nume_fisiere),
            content=text_document
        )
        db_document = crud.create_user_document(db, doc_schema, user_id, session_id)

        # Generează flashcards
        try:
            bucati = imparte_text_in_bucati(text_document, dimensiune_chunk=4000)
            if not bucati:
                raise HTTPException(status_code=500, detail="Nu s-a putut procesa textul.")
            
            flashcards_text = genereaza_flashcards(bucati[0], numar_intrebari=numar_intrebari)
            flashcards_finale = parseaza_flashcards_din_text(flashcards_text)
            
            if not flashcards_finale:
                raise HTTPException(status_code=500, detail="AI-ul nu a putut genera flashcards. Asigură-te că Ollama e pornit.")
        except Exception as ai_error:
            raise HTTPException(
                status_code=500, 
                detail=f"Eroare AI: {str(ai_error)}. Asigură-te că Ollama (ollama serve) e pornit și că modelul llama3 e disponibil."
            )

        # Salvează flashcards în DB
        saved_flashcards = []
        for fc in flashcards_finale:
            try:
                fc_schema = schemas.FlashcardCreate(
                    question=fc.get("intrebare", ""),
                    correct_answer=fc.get("raspuns", "")
                )
                db_fc = crud.create_flashcard(db, fc_schema, db_document.id, session_id)
                saved_flashcards.append({
                    "id": db_fc.id,
                    "intrebare": db_fc.question,
                    "raspuns": db_fc.correct_answer
                })
            except Exception as fc_error:
                print(f"Eroare salvare flashcard: {fc_error}")
                continue

        return {
            "filenames": nume_fisiere,
            "document_id": db_document.id,
            "session_id": session_id,
            "flashcards": saved_flashcards
        }

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        print(f"Eroare upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Eroare: {str(e)}")
    
    finally:
        shutil.rmtree(temp_folder, ignore_errors=True)

# --- RUTE EVALUARE ---
@app.post("/evaluate")
def evalueaza_raspuns_utilizator(intrebare_id: int, raspuns_utilizator: str, raspuns_corect: str, severitate: int = 2):
    scor = evalueaza_raspuns(raspuns_corect, raspuns_utilizator, severitate)
    return { "scor": scor, "status": "CORECT" if scor >= 70 else "INCORECT" }