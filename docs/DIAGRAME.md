# Diagrame NeuroDeck

## 1. Diagrama claselor (UML)

```mermaid
classDiagram
    class User {
        +int id
        +str email
        +str hashed_password
        +create_user()
        +get_by_email()
    }

    class StudySession {
        +int id
        +int user_id
        +str title
        +datetime created_at
        +datetime updated_at
        +create()
        +update()
        +delete()
    }

    class Document {
        +int id
        +int user_id
        +int session_id
        +str title
        +str content
        +datetime upload_date
    }

    class Flashcard {
        +int id
        +int document_id
        +int session_id
        +str question
        +str correct_answer
        +datetime created_at
    }

    User "1" --> "0..*" StudySession : detine
    User "1" --> "0..*" Document : incarca
    StudySession "1" --> "0..*" Document : contine
    StudySession "1" --> "0..*" Flashcard : grupeaza
    Document "1" --> "0..*" Flashcard : genereaza
```

---

## 2. Diagrama componentelor

```mermaid
graph TB
    subgraph Frontend["Frontend (React + Vite)"]
        UI[Interfata utilizator]
        API_SVC[api.js - serviciu HTTP]
    end

    subgraph Backend["Backend (FastAPI + Python)"]
        ROUTES[Rute REST]
        CRUD[Strat CRUD]
        DOC_PROC[Document Processor]
        AI_AGENT1[Agent AI 1 - Generare]
        AI_AGENT2[Agent AI 2 - Evaluare]
    end

    subgraph Storage["Stocare"]
        DB[(SQLite neurodeck.db)]
    end

    subgraph AI["Servicii AI"]
        OLLAMA[Ollama - Llama3]
        ST[SentenceTransformer]
    end

    UI --> API_SVC
    API_SVC -->|HTTP REST / JSON| ROUTES
    ROUTES --> CRUD
    ROUTES --> DOC_PROC
    ROUTES --> AI_AGENT1
    ROUTES --> AI_AGENT2
    CRUD --> DB
    DOC_PROC -->|text extras| AI_AGENT1
    AI_AGENT1 -->|prompt| OLLAMA
    OLLAMA -->|Q and A text| AI_AGENT1
    AI_AGENT2 -->|embeddings| ST
    ST -->|scor similaritate| AI_AGENT2
```

---

## 3. Workflow principal — Upload PDF si generare flashcards

```mermaid
sequenceDiagram
    actor U as Utilizator
    participant FE as Frontend
    participant BE as Backend FastAPI
    participant DP as Document Processor
    participant AI as Agent AI (Ollama)
    participant DB as SQLite

    U->>FE: Selecteaza PDF-uri + nr. intrebari
    FE->>BE: POST /upload (multipart/form-data)
    BE->>DB: Verifica sesiunea utilizatorului
    DB-->>BE: Sesiune valida

    loop Pentru fiecare PDF
        BE->>DP: Salveaza fisier temporar
        DP->>DP: Extrage text (pypdf)
        DP->>DP: Imparte in chunks
    end

    BE->>DB: Salveaza Document (titlu + continut)
    DB-->>BE: document_id

    BE->>AI: genereaza_flashcards(text, nr_intrebari)
    AI->>AI: Trimite prompt la Llama3 (Ollama)
    AI-->>BE: Text Q/A brut

    BE->>BE: parseaza_flashcards_din_text()

    loop Pentru fiecare flashcard
        BE->>DB: Salveaza Flashcard (question, answer, session_id)
    end

    BE-->>FE: JSON cu lista de flashcards
    FE->>U: Afiseaza flashcards pentru studiu
    BE->>BE: Sterge fisiere temporare (temp_pdfs/)
```

---

## 4. Workflow evaluare raspuns

```mermaid
sequenceDiagram
    actor U as Utilizator
    participant FE as Frontend
    participant BE as Backend FastAPI
    participant AI2 as Agent AI 2 (SentenceTransformer)

    U->>FE: Scrie raspuns la intrebare
    FE->>BE: POST /evaluate?raspuns_utilizator=...&raspuns_corect=...&severitate=2

    BE->>AI2: evalueaza_raspuns(corect, dat, severitate)
    AI2->>AI2: Encode raspuns_corect -> embedding
    AI2->>AI2: Encode raspuns_dat -> embedding
    AI2->>AI2: cosine_similarity(emb1, emb2)
    AI2->>AI2: Aplica prag severitate (30/40/50)
    AI2->>AI2: Calculeaza scor_final (0-100)
    AI2-->>BE: scor_final (int)

    BE-->>FE: JSON {scor: 85, status: "CORECT"}
    FE->>U: Afiseaza verdict + scor
```

---

## 5. Diagrama de stare — Frontend

```mermaid
stateDiagram-v2
    [*] --> Login
    Login --> SessionSelect : autentificare reusita
    Login --> Login : date gresite
    SessionSelect --> Upload : selectare/creare sesiune
    Upload --> Study : flashcards generate
    Study --> Results : toate raspunsurile trimise
    Results --> Upload : reincepe sesiunea
    SessionSelect --> Upload : sesiune fara flashcards
    Study --> SessionSelect : schimba sesiunea
    Upload --> SessionSelect : schimba sesiunea
```
