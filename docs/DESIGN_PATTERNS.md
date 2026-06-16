# Design Patterns — NeuroDeck Backend

> Acest document descrie pattern-urile de proiectare aplicate in arhitectura backend-ului NeuroDeck, cu referinte concrete la fisierele si liniile de cod unde sunt implementate.

---

## 1. Repository Pattern

**Fisier:** `app/crud.py`

**Descriere:**
Repository Pattern separa logica de acces la date (interogari SQL) de logica de business (rutele API). In loc ca rutele din `main.py` sa scrie direct interogari SQLAlchemy, acestea apeleaza functii din `crud.py` care abstractizeaza complet stratul de date.

**Implementare:**
```python
# app/crud.py — Repository pentru entitatea StudySession
def create_study_session(db: Session, session: schemas.StudySessionCreate, user_id: int):
    db_session = models.StudySession(**session.model_dump(), user_id=user_id)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_study_sessions(db: Session, user_id: int):
    return db.query(models.StudySession).filter(models.StudySession.user_id == user_id).all()

def delete_study_session(db: Session, session_id: int):
    db_session = get_study_session(db, session_id)
    if db_session:
        db.delete(db_session)
        db.commit()
    return db_session
```

**Beneficiu:** Daca schimbam baza de date (ex: de la SQLite la PostgreSQL), modificam doar `crud.py`, nu toate rutele.

---

## 2. DTO Pattern (Data Transfer Object) — prin Pydantic Schemas

**Fisier:** `app/schemas.py`

**Descriere:**
DTO Pattern separa reprezentarea datelor interne (modelele SQLAlchemy din `models.py`) de datele expuse prin API. Fiecare entitate are cel putin 3 scheme: una de baza, una pentru creare (input) si una pentru raspuns (output).

**Implementare:**
```python
# app/schemas.py — DTO-uri pentru StudySession
class StudySessionBase(BaseModel):
    title: str                          # campuri comune

class StudySessionCreate(StudySessionBase):
    pass                                # input: doar titlul

class StudySessionResponse(StudySessionBase):
    id: int                             # output: include ID si timestamps
    user_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True          # permite citirea din obiecte SQLAlchemy

class StudySessionWithFlashcards(StudySessionResponse):
    flashcards: List[FlashcardResponse] = []   # output extins: include relatiile
```

**Beneficiu:** Parola (`hashed_password`) nu apare niciodata in raspunsurile API deoarece `UserResponse` nu o include, chiar daca modelul `User` o contine.

---

## 3. Dependency Injection

**Fisier:** `app/main.py`, `app/database.py`

**Descriere:**
FastAPI implementeaza Dependency Injection prin `Depends()`. Sesiunea de baza de date nu este creata manual in fiecare ruta — este injectata automat de framework, care gestioneaza si ciclul de viata al acesteia (deschidere/inchidere).

**Implementare:**
```python
# app/database.py — definirea dependentei
def get_db():
    db = SessionLocal()
    try:
        yield db        # ofera sesiunea rutei
    finally:
        db.close()      # inchide automat dupa raspuns

# app/main.py — injectarea dependentei in rute
@app.get("/sessions/{user_id}", response_model=schemas.SessionsListResponse)
def get_user_sessions(
    user_id: int,
    db: Session = Depends(database.get_db)   # DI aici
):
    sessions = crud.get_user_study_sessions(db, user_id)
    return {"sessions": sessions}
```

**Beneficiu:** Sesiunile DB sunt garantat inchise dupa fiecare request, eliminand memory leaks. La testare, `get_db` poate fi inlocuit cu o sesiune de test (vezi `tests/conftest.py`).

---

## 4. Lazy Initialization Pattern

**Fisier:** `app/ai_agents.py`

**Descriere:**
Lazy Initialization amana crearea unui obiect costisitor pana in momentul primei utilizari. Modelul `SentenceTransformer` (~500MB) nu este incarcat la pornirea serverului, ci doar la primul apel al endpointului `/evaluate`.

**Implementare:**
```python
# app/ai_agents.py
_evaluator_model = None          # nu e incarcat la import

def _get_evaluator():
    global _evaluator_model
    if _evaluator_model is None:                          # incarcat doar la primul apel
        print("Se incarca modelul NLP pentru evaluare...")
        _evaluator_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    return _evaluator_model                               # returnat din cache la apelurile urmatoare

def evalueaza_raspuns(raspuns_corect, raspuns_student, nivel_severitate):
    model = _get_evaluator()     # accesat prin getter, nu direct
    ...
```

**Beneficiu:** Serverul porneste instant chiar daca modelul NLP nu e descarcat. Utilizatorii care nu folosesc evaluarea nu platesc costul incarcarii modelului.

---

## 5. Facade Pattern

**Fisier:** `app/main.py`

**Descriere:**
Facade Pattern ofera o interfata simplificata peste un subsistem complex. Ruta `POST /upload` din `main.py` ascunde complet complexitatea colaborarii dintre 4 module diferite: `document_processor`, `ai_agents`, `utils` si `crud`.

**Implementare:**
```python
# app/main.py — Facade peste subsistemul de procesare
@app.post("/upload")
async def upload_si_genereaza_flashcards(files, numar_intrebari, session_id, user_id, db):

    # Subsistem 1: procesare document
    text_document = extrage_text_din_toate_pdf(temp_folder)
    bucati = imparte_text_in_bucati(text_document, dimensiune_chunk=4000)

    # Subsistem 2: agent AI generare
    flashcards_text = genereaza_flashcards(bucati[0], numar_intrebari=numar_intrebari)

    # Subsistem 3: parser output AI
    flashcards_finale = parseaza_flashcards_din_text(flashcards_text)

    # Subsistem 4: persistenta in DB
    db_fc = crud.create_flashcard(db, fc_schema, db_document.id, session_id)
```

**Beneficiu:** Frontend-ul face un singur apel `POST /upload` si primeste flashcards gata generate. Nu trebuie sa cunoasca nimic despre Ollama, pypdf sau parsarea textului.

---

## Sumar

| Pattern | Fisier | Problema rezolvata |
|---|---|---|
| **Repository** | `crud.py` | Separa accesul la date de logica de business |
| **DTO / Schema** | `schemas.py` | Separa modelele interne de datele expuse prin API |
| **Dependency Injection** | `main.py` + `database.py` | Gestionare automata a sesiunilor de baza de date |
| **Lazy Initialization** | `ai_agents.py` | Incarcarea modelului NLP doar la primul apel |
| **Facade** | `main.py` (`/upload`) | Interfata simpla peste un subsistem complex de procesare |
