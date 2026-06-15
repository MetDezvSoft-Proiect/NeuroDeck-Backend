# 📑 Specificații software — NeuroDeck Backend

> **Document:** Specificația Cerințelor Software (SRS — *Software Requirements Specification*)
> **Produs:** NeuroDeck — generator inteligent de flashcards din documente PDF
> **Componentă:** Backend (API + procesare AI)
> **Versiune:** 1.0 (MVP)
> **Ultima actualizare:** 2026-06-15

---

## 1. Introducere

### 1.1 Scopul documentului
Acest document descrie cerințele funcționale și non-funcționale ale componentei **backend** a aplicației NeuroDeck. Servește ca referință comună pentru echipa de dezvoltare și ca bază pentru planificarea sprinturilor și a backlog-ului (vezi [`BACKLOG.md`](BACKLOG.md) și [`SPRINTURI.md`](SPRINTURI.md)).

### 1.2 Descrierea produsului
**NeuroDeck** este o aplicație web care transformă materiale de studiu (PDF-uri) în **flashcards** generate automat cu inteligență artificială. Utilizatorul încarcă unul sau mai multe documente, iar sistemul generează întrebări și răspunsuri, apoi evaluează semantic răspunsurile date de utilizator.

Backend-ul expune un **API REST** care gestionează:
- autentificarea utilizatorilor,
- sesiunile de studiu,
- procesarea PDF-urilor și extragerea textului,
- generarea flashcards-urilor cu AI (Ollama + Llama3),
- evaluarea semantică a răspunsurilor.

### 1.3 Public țintă
- Studenți și elevi care vor să învețe eficient pe bază de materiale proprii.
- Oricine dorește să transforme rapid un curs PDF într-un set de întrebări de recapitulare.

---

## 2. Roluri și actori

| Actor | Descriere |
|---|---|
| **Utilizator neautentificat** | Își poate crea cont sau se poate autentifica. |
| **Utilizator autentificat** | Gestionează sesiuni de studiu, încarcă PDF-uri, generează și parcurge flashcards, primește evaluări. |
| **Sistem AI (Ollama/Llama3)** | Generează întrebări/răspunsuri pe baza textului extras. |
| **Model semantic (sentence-transformers)** | Calculează similaritatea dintre răspunsul corect și cel dat de utilizator. |

---

## 3. Cerințe funcționale

Fiecare cerință are un identificator `RF-xx` și este urmărită în [`BACKLOG.md`](BACKLOG.md).

### 3.1 Autentificare
| ID | Cerință |
|---|---|
| **RF-01** | Sistemul permite crearea unui cont nou pe bază de email și parolă. |
| **RF-02** | Sistemul respinge înregistrarea unui email deja existent. |
| **RF-03** | Sistemul permite autentificarea cu email și parolă și returnează identitatea utilizatorului. |

### 3.2 Sesiuni de studiu
| ID | Cerință |
|---|---|
| **RF-04** | Utilizatorul autentificat poate crea o sesiune de studiu cu un titlu (ex: „Informatică”). |
| **RF-05** | Utilizatorul își poate lista toate sesiunile. |
| **RF-06** | Utilizatorul poate vizualiza detaliile unei sesiuni împreună cu flashcards-urile asociate. |
| **RF-07** | Utilizatorul poate redenumi o sesiune. |
| **RF-08** | Utilizatorul poate șterge o sesiune (împreună cu flashcards-urile ei). |

### 3.3 Procesare documente
| ID | Cerință |
|---|---|
| **RF-09** | Utilizatorul poate încărca unul sau mai multe fișiere PDF într-o sesiune. |
| **RF-10** | Sistemul validează că fișierele sunt PDF-uri valide. |
| **RF-11** | Sistemul extrage textul din toate PDF-urile încărcate. |
| **RF-12** | Sistemul împarte textul în bucăți („chunks”) procesabile de AI. |
| **RF-13** | Fișierele temporare sunt șterse după procesare. |

### 3.4 Generare flashcards
| ID | Cerință |
|---|---|
| **RF-14** | Sistemul generează un număr configurabil de flashcards din textul extras. |
| **RF-15** | Flashcards-urile sunt persistate în baza de date, legate de document și sesiune. |
| **RF-16** | Sistemul returnează un mesaj de eroare clar dacă serviciul AI (Ollama) nu este disponibil. |

### 3.5 Evaluare răspunsuri
| ID | Cerință |
|---|---|
| **RF-17** | Utilizatorul poate trimite un răspuns pentru o întrebare. |
| **RF-18** | Sistemul calculează un scor de similaritate semantică între răspunsul corect și cel dat. |
| **RF-19** | Sistemul aplică un nivel de severitate configurabil la calculul scorului. |
| **RF-20** | Sistemul returnează verdictul `CORECT` / `INCORECT` pe baza unui prag. |

---

## 4. Cerințe non-funcționale

| ID | Categorie | Cerință |
|---|---|---|
| **RNF-01** | Performanță | Răspunsul la cererile care nu implică AI trebuie să fie sub 500 ms în condiții normale. |
| **RNF-02** | Compatibilitate | API-ul răspunde în format JSON și permite CORS pentru frontend. |
| **RNF-03** | Portabilitate | Backend-ul rulează pe Python 3.10+ cu dependențe instalabile via `pip`. |
| **RNF-04** | Mentenabilitate | Cod organizat pe module clare (rute, modele, scheme, CRUD, procesare). |
| **RNF-05** | Securitate (MVP) | Parolele nu se stochează în clar. *(Notă: MVP folosește un hash simplificat; producția necesită bcrypt/argon2 — vezi backlog EPIC-8.)* |
| **RNF-06** | Disponibilitate | Sistemul tratează elegant indisponibilitatea Ollama, fără a pica brusc. |
| **RNF-07** | Observabilitate | Erorile relevante sunt logate pentru depanare. |

---

## 5. Arhitectură și stack tehnologic

| Zonă | Tehnologie |
|---|---|
| Framework API | FastAPI + Uvicorn |
| Bază de date | SQLite (MVP) + SQLAlchemy ORM |
| Validare | Pydantic v2 |
| Procesare PDF | pypdf |
| Generare AI | Ollama (Llama3) |
| Similaritate semantică | sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`) |

### 5.1 Fluxul principal
```text
1. Utilizatorul se autentifică / își creează contul
2. Creează o sesiune de studiu
3. Încarcă unul sau mai multe PDF-uri în sesiune
4. Backend-ul salvează fișierele și extrage textul
5. Textul este împărțit în bucăți și trimis la Ollama
6. Ollama generează întrebări + răspunsuri → parsate în flashcards
7. Flashcards-urile sunt salvate în DB
8. Utilizatorul răspunde → backend-ul evaluează semantic → verdict
```

---

## 6. Modelul de date

```text
User 1 ──< StudySession 1 ──< Document 1 ──< Flashcard
  │                                ▲
  └────────────────────────────────┘  (un User are și Documente direct)
```

| Entitate | Câmpuri cheie |
|---|---|
| **User** | `id`, `email` (unic), `hashed_password` |
| **StudySession** | `id`, `user_id`, `title`, `created_at`, `updated_at` |
| **Document** | `id`, `title`, `content`, `upload_date`, `user_id`, `session_id` |
| **Flashcard** | `id`, `question`, `correct_answer`, `created_at`, `document_id`, `session_id` |

---

## 7. Contractul API

| Metodă | Endpoint | Cerință acoperită | Descriere |
|---|---|---|---|
| `GET` | `/` | — | Status check |
| `POST` | `/users/` | RF-01, RF-02 | Creare cont nou |
| `POST` | `/login` | RF-03 | Autentificare |
| `POST` | `/sessions` | RF-04 | Creare sesiune de studiu |
| `GET` | `/sessions/{user_id}` | RF-05 | Listare sesiuni utilizator |
| `GET` | `/sessions/detail/{session_id}` | RF-06 | Detalii sesiune + flashcards |
| `PUT` | `/sessions/{session_id}` | RF-07 | Redenumire sesiune |
| `DELETE` | `/sessions/{session_id}` | RF-08 | Ștergere sesiune |
| `POST` | `/upload` | RF-09 … RF-16 | Upload PDF + generare flashcards |
| `POST` | `/evaluate` | RF-17 … RF-20 | Evaluare răspuns |

---

## 8. Constrângeri și presupuneri

- Ollama trebuie instalat și pornit local (`ollama serve`), cu modelul `llama3` descărcat.
- Modelul semantic trebuie disponibil pentru `sentence-transformers`.
- MVP-ul folosește SQLite (un singur fișier `neurodeck.db`); producția poate migra la PostgreSQL.
- Autentificarea MVP nu este destinată producției (vezi RNF-05).

---

## 9. Documente conexe
- 📋 [Backlog de produs](BACKLOG.md)
- 🏃 [Planificare sprinturi](SPRINTURI.md)
- 📖 [README](../README)
