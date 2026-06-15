"""Teste pentru stratul CRUD (operatii pe baza de date)."""
from app import crud, schemas


# ─── UTILIZATORI ───────────────────────────────────────────────
def test_create_user(db):
    user = crud.create_user(db, schemas.UserCreate(email="ana@test.com", password="secret"))
    assert user.id is not None
    assert user.email == "ana@test.com"
    # Parola NU trebuie stocata in clar
    assert user.hashed_password != "secret"


def test_get_user_by_email_gaseste_si_lipsa(db):
    crud.create_user(db, schemas.UserCreate(email="bob@test.com", password="pw"))
    gasit = crud.get_user_by_email(db, "bob@test.com")
    assert gasit is not None
    assert gasit.email == "bob@test.com"
    # Email inexistent -> None
    assert crud.get_user_by_email(db, "lipsa@test.com") is None


# ─── SESIUNI DE STUDIU ─────────────────────────────────────────
def test_create_si_listare_sesiuni(db):
    user = crud.create_user(db, schemas.UserCreate(email="c@test.com", password="pw"))
    sesiune = crud.create_study_session(db, schemas.StudySessionCreate(title="Informatica"), user.id)
    assert sesiune.id is not None
    assert sesiune.title == "Informatica"

    sesiuni = crud.get_user_study_sessions(db, user.id)
    assert len(sesiuni) == 1
    assert sesiuni[0].title == "Informatica"


def test_update_sesiune(db):
    user = crud.create_user(db, schemas.UserCreate(email="d@test.com", password="pw"))
    sesiune = crud.create_study_session(db, schemas.StudySessionCreate(title="Vechi"), user.id)
    actualizat = crud.update_study_session(db, sesiune.id, schemas.StudySessionCreate(title="Nou"))
    assert actualizat is not None
    assert actualizat.title == "Nou"


def test_delete_sesiune(db):
    user = crud.create_user(db, schemas.UserCreate(email="e@test.com", password="pw"))
    sesiune = crud.create_study_session(db, schemas.StudySessionCreate(title="De sters"), user.id)
    sters = crud.delete_study_session(db, sesiune.id)
    assert sters is not None
    # Dupa stergere lista e goala
    assert crud.get_user_study_sessions(db, user.id) == []


def test_update_sesiune_inexistenta_returneaza_none(db):
    assert crud.update_study_session(db, 999, schemas.StudySessionCreate(title="x")) is None


# ─── DOCUMENTE SI FLASHCARDS ───────────────────────────────────
def test_document_si_flashcards(db):
    user = crud.create_user(db, schemas.UserCreate(email="f@test.com", password="pw"))
    sesiune = crud.create_study_session(db, schemas.StudySessionCreate(title="Biologie"), user.id)
    doc = crud.create_user_document(
        db, schemas.DocumentCreate(title="Curs 1", content="Continut text"), user.id, sesiune.id
    )
    assert doc.id is not None
    assert doc.session_id == sesiune.id

    fc = crud.create_flashcard(
        db, schemas.FlashcardCreate(question="Ce este ADN?", correct_answer="Acid nucleic"),
        doc.id, sesiune.id,
    )
    assert fc.id is not None

    flashcards = crud.get_session_flashcards(db, sesiune.id)
    assert len(flashcards) == 1
    assert flashcards[0].question == "Ce este ADN?"
