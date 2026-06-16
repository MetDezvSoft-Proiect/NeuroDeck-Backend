# Raport — Folosirea instrumentelor AI în dezvoltarea NeuroDeck

> **Proiect:** NeuroDeck — generator de flashcards din PDF cu AI
> **Disciplina:** Metode de Dezvoltare Software
> **Data:** 2026-06-16

---

## 1. Introducere

Acest document descrie instrumentele de inteligenta artificiala folosite in timpul procesului de dezvoltare a aplicatiei NeuroDeck, modul in care au fost integrate in fluxul de lucru si impactul lor asupra productivitatii si calitatii codului.

---

## 2. Instrumente AI folosite

### 2.1 Claude (Anthropic) — Asistent de dezvoltare

**Rol:** Asistent principal de programare si debugging

**Cum a fost folosit:**
- Identificarea si rezolvarea bugurilor din cod (route ordering, cascade delete, UnicodeEncodeError pe Windows)
- Generarea structurii initiale a modulelor (`models.py`, `schemas.py`, `crud.py`)
- Debugging la erori de startup (Python 3.13 incompatibilitati cu socket exceptions)
- Revizuirea codului si identificarea problemelor de securitate sau arhitectura
- Generarea documentatiei tehnice (SRS, backlog, diagrame Mermaid)
- Explicarea conceptelor FastAPI (response_model, Query(), Form(), cascade)

**Exemple concrete:**
- A identificat ca `GET /sessions/{user_id}` si `GET /sessions/detail/{session_id}` sunt in ordine gresita si explica de ce FastAPI face match gresit
- A detectat ca `SentenceTransformer` incarcat la import nivel crapa serverul daca modelul nu e disponibil si a propus lazy loading
- A explicat de ce emoji-urile in `print()` cauzeaza `UnicodeEncodeError` pe Windows cu encoding cp1252

**Limitari observate:**
- Nu cunoaste starea exacta a fisierelor fara sa le citeasca explicit
- Uneori propune solutii care necesita ajustare pentru versiunea specifica de Python sau OS

---

### 2.2 Ollama + Llama3 — Agent AI integrat in produs

**Rol:** Agent AI 1 — generare de flashcards din text

**Cum functioneaza in NeuroDeck:**
- Primeste textul extras din PDF-uri impartit in chunks de ~4000 caractere
- Genereaza perechi intrebare/raspuns in limba romana pe baza unui prompt structurat
- Returneaza text in formatul `Q: ... / A: ...` care este apoi parsat

**Prompt folosit:**
```
Esti un asistent educational expert. Analizeaza urmatorul text si genereaza 
EXACT {numar_intrebari} intrebari esentiale cu raspunsuri scurte.
REGULA STRICTA: EXCLUSIV in limba romana!
```

**Avantaje:**
- Rulare locala — nu trimite date la servere externe
- Gratuit, fara limite de API
- Suport bun pentru limba romana

**Limitari observate:**
- Necesita Ollama instalat si rulat local (`ollama serve`)
- Calitatea intrebarilor depinde de calitatea textului din PDF
- Uneori nu respecta exact numarul de intrebari cerut

---

### 2.3 SentenceTransformer (paraphrase-multilingual-MiniLM-L12-v2) — Agent AI integrat in produs

**Rol:** Agent AI 2 — evaluare semantica a raspunsurilor

**Cum functioneaza in NeuroDeck:**
- Transforma raspunsul corect si raspunsul dat de utilizator in vectori de embeddings
- Calculeaza similaritatea cosinus intre cei doi vectori (valoare 0-1)
- Aplica un prag minim in functie de severitatea aleasa (bland/normal/sever)
- Returneaza un scor 0-100 si un verdict CORECT/INCORECT

**De ce acest model:**
- Suporta nativ limba romana (model multilingv)
- Dimensiune mica (~50MB), rulare rapida pe CPU
- Nu necesita conexiune la internet dupa prima descarcare

**Avantaje fata de comparatia string simpla:**
- Recunoaste raspunsuri corecte formulate diferit ("acid dezoxiribonucleic" vs "ADN")
- Tolereaza greseli de scriere minore
- Evalueaza sensul, nu forma exacta

---

## 3. Impact asupra procesului de dezvoltare

| Activitate | Fara AI (estimat) | Cu AI (real) | Reducere |
|---|---|---|---|
| Structura initiala backend | 3-4 ore | ~1 ora | ~70% |
| Debugging route ordering | 30-60 min | ~5 min | ~90% |
| Scriere documentatie SRS | 4-5 ore | ~1 ora | ~80% |
| Identificare buguri | 2-3 ore | ~20 min | ~85% |
| Generare diagrame Mermaid | 2-3 ore | ~30 min | ~85% |

---

## 4. Lectii invatate

1. **AI-ul nu inlocuieste intelegerea codului** — pentru a valida sugestiile Claude, era necesar sa intelegem ce face fiecare linie. Sugestiile gresite (ex: exceptia socket) trebuiau identificate si corectate manual.

2. **Prompturile conteaza** — calitatea flashcards-urilor generate de Llama3 depinde direct de calitatea promptului. Am iterat de mai multe ori pentru a obtine intrebari relevante in romana.

3. **Modelele locale au avantaje clare** — Ollama si SentenceTransformer ruleaza offline, ceea ce e important pentru date academice potential sensibile.

4. **Limitele contextuale** — Claude nu cunoaste starea sistemului (ce porturi sunt deschise, ce versiune de Python e instalata). Aceste detalii trebuiau furnizate explicit pentru a obtine solutii corecte.

---

## 5. Concluzie

Instrumentele AI au accelerat semnificativ dezvoltarea NeuroDeck, in special in fazele de arhitectura initiala, debugging si documentatie. Cele mai valoroase contributii au fost in identificarea bugurilor subtile (ordinea rutelor FastAPI, problema encoding Windows) care ar fi durat mult mai mult de gasit manual.

In acelasi timp, AI-ul a fost folosit ca un **asistent**, nu ca un inlocuitor al rationamentului tehnic — fiecare sugestie a fost evaluata, testata si adaptata contextului specific al proiectului.
