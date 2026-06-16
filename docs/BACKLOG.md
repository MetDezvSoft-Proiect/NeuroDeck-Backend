# 📋 Backlog de produs — NeuroDeck

> **Produs:** NeuroDeck — generator de flashcards din PDF cu AI
> **Tip document:** Product Backlog (metodologie agilă / Scrum)
> **Ultima actualizare:** 2026-06-15

Acest backlog conține toate **epicele** și **user story-urile** produsului NeuroDeck. Story-urile marcate cu 🟢 sunt finalizate, 🟡 în lucru, ⚪ planificate. Estimarea folosește **story points** (scară Fibonacci), iar prioritizarea folosește metoda **MoSCoW** (*Must / Should / Could / Won't*).

> 💡 Fiecare user story de mai jos devine un **Issue** pe GitHub și este urmărit pe **Project board**. Vezi planificarea pe sprinturi în [`SPRINTURI.md`](SPRINTURI.md).

---

## Legendă

| Simbol | Status | | Prioritate | Semnificație |
|---|---|---|---|---|
| 🟢 | Done | | **Must** | Esențial pentru MVP |
| 🟡 | In Progress | | **Should** | Important, dar nu blocant |
| ⚪ | To Do | | **Could** | De dorit dacă rămâne timp |
| | | | **Won't (now)** | Amânat pentru o iterație viitoare |

**Story points:** `1` = trivial · `2` = mic · `3` = mediu · `5` = mare · `8` = foarte mare · `13` = epic de spart

---

## 🧩 EPIC-1 — Fundație & infrastructură backend
*Configurarea bazei de proiect: bază de date, modele, scheme, operații CRUD.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-01 | Ca **dezvoltator**, vreau o configurare SQLAlchemy + SQLite ca să am persistență a datelor. | Must | 3 | 🟢 |
| US-02 | Ca **dezvoltator**, vreau modele pentru User, StudySession, Document, Flashcard ca să reflect domeniul. | Must | 5 | 🟢 |
| US-03 | Ca **dezvoltator**, vreau scheme Pydantic pentru request/response ca să validez datele. | Must | 3 | 🟢 |
| US-04 | Ca **dezvoltator**, vreau operații CRUD reutilizabile ca să separ logica de acces la date. | Must | 5 | 🟢 |

**Criterii de acceptare (exemplu US-02):** modelele au relații corecte (User→Session→Document→Flashcard); `Base.metadata.create_all` creează tabelele fără erori.

---

## 🧩 EPIC-2 — Autentificare utilizatori
*Crearea conturilor și autentificarea.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-05 | Ca **vizitator**, vreau să îmi creez un cont cu email și parolă ca să îmi salvez progresul. | Must | 3 | 🟢 |
| US-06 | Ca **sistem**, vreau să resping email-urile duplicate ca să păstrez conturile unice. | Must | 2 | 🟢 |
| US-07 | Ca **utilizator**, vreau să mă autentific ca să accesez sesiunile mele. | Must | 3 | 🟢 |

**Criterii de acceptare (US-07):** login cu date corecte → 200 + identitatea utilizatorului; date greșite → 400 cu mesaj clar.

---

## 🧩 EPIC-3 — Procesare documente PDF
*Upload, extragere și pregătire text.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-08 | Ca **utilizator**, vreau să încarc unul sau mai multe PDF-uri ca să generez flashcards din ele. | Must | 5 | 🟢 |
| US-09 | Ca **sistem**, vreau să validez că fișierele sunt PDF-uri ca să evit erorile de procesare. | Must | 2 | 🟢 |
| US-10 | Ca **sistem**, vreau să extrag textul din toate PDF-urile ca să am conținut pentru AI. | Must | 5 | 🟢 |
| US-11 | Ca **sistem**, vreau să împart textul în bucăți ca să respect limitele modelului AI. | Should | 3 | 🟢 |
| US-12 | Ca **sistem**, vreau să șterg fișierele temporare după procesare ca să nu ocup spațiu inutil. | Should | 2 | 🟢 |

---

## 🧩 EPIC-4 — Generare flashcards cu AI
*Integrarea cu Ollama / Llama3.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-13 | Ca **utilizator**, vreau să aleg numărul de întrebări generate ca să controlez dimensiunea setului. | Must | 3 | 🟢 |
| US-14 | Ca **sistem**, vreau să generez flashcards din text cu Ollama ca să automatizez crearea întrebărilor. | Must | 8 | 🟢 |
| US-15 | Ca **sistem**, vreau să parsez outputul AI în întrebări/răspunsuri structurate ca să le pot salva. | Must | 5 | 🟢 |
| US-16 | Ca **utilizator**, vreau un mesaj clar dacă Ollama nu e pornit ca să știu cum să rezolv. | Should | 2 | 🟢 |
| US-17 | Ca **sistem**, vreau să salvez flashcards-urile în DB ca să fie disponibile ulterior. | Must | 3 | 🟢 |

---

## 🧩 EPIC-5 — Evaluare răspunsuri
*Scor semantic și verdict.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-18 | Ca **utilizator**, vreau să trimit un răspuns la o întrebare ca să fiu evaluat. | Must | 3 | 🟢 |
| US-19 | Ca **sistem**, vreau să calculez similaritatea semantică ca să evaluez corectitudinea. | Must | 8 | 🟢 |
| US-20 | Ca **utilizator**, vreau să aleg un nivel de severitate ca să ajustez exigența evaluării. | Could | 3 | 🟢 |
| US-21 | Ca **utilizator**, vreau un verdict CORECT/INCORECT ca să înțeleg rapid rezultatul. | Must | 2 | 🟢 |

---

## 🧩 EPIC-6 — Sesiuni de studiu
*Organizarea materialelor pe materii/teme.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-22 | Ca **utilizator**, vreau să creez sesiuni de studiu ca să-mi organizez materiile. | Must | 3 | 🟢 |
| US-23 | Ca **utilizator**, vreau să-mi listez sesiunile ca să navighez între ele. | Must | 2 | 🟢 |
| US-24 | Ca **utilizator**, vreau să văd flashcards-urile dintr-o sesiune ca să reiau recapitularea. | Must | 3 | 🟢 |
| US-25 | Ca **utilizator**, vreau să redenumesc o sesiune ca să o țin organizată. | Could | 2 | 🟢 |
| US-26 | Ca **utilizator**, vreau să șterg o sesiune ca să elimin materialele de care nu mai am nevoie. | Should | 2 | 🟢 |

---

## 🧩 EPIC-7 — Securitate & pregătire pentru producție *(viitor)*
*Hardening-ul necesar înainte de deploy real.*

| ID | User story | Prioritate | Pts | Status |
|---|---|---|---|---|
| US-27 | Ca **utilizator**, vreau ca parola mea să fie hash-uită criptografic (bcrypt/argon2) ca să fie protejată. | Should | 3 | ⚪ |
| US-28 | Ca **utilizator**, vreau autentificare pe bază de token (JWT) ca să am sesiuni sigure. | Should | 5 | ⚪ |
| US-29 | Ca **dezvoltator**, vreau configurare externă (variabile de mediu) pentru Ollama și DB ca să schimb ușor mediile. | Could | 3 | ⚪ |
| US-30 | Ca **dezvoltator**, vreau containerizare cu Docker ca să rulez identic pe orice mașină. | Could | 5 | ⚪ |
| US-31 | Ca **dezvoltator**, vreau un pipeline CI/CD ca să automatizez testarea și build-ul. | Could | 5 | ⚪ |
| US-32 | Ca **dezvoltator**, vreau teste automate (unit + integrare) ca să previn regresiile. | Should | 8 | ⚪ |
| US-33 | Ca **dezvoltator**, vreau logging și monitoring ca să depanez probleme în producție. | Could | 3 | ⚪ |
| US-34 | Ca **utilizator**, vreau suport pentru DOCX/PPTX ca să încarc și alte formate. | Won't (now) | 8 | ⚪ |

---

## 📊 Sumar backlog

| Epic | Story-uri | Total puncte | Done |
|---|---|---|---|
| EPIC-1 Fundație | 4 | 16 | 🟢 100% |
| EPIC-2 Autentificare | 3 | 8 | 🟢 100% |
| EPIC-3 Procesare PDF | 5 | 17 | 🟢 100% |
| EPIC-4 Generare AI | 5 | 21 | 🟢 100% |
| EPIC-5 Evaluare | 4 | 16 | 🟢 100% |
| EPIC-6 Sesiuni | 5 | 12 | 🟢 100% |
| EPIC-7 Producție *(viitor)* | 8 | 40 | ⚪ 0% |
| **Total** | **34** | **130** | **~69% livrat** |

---

## 🔗 Documente conexe
- 📑 [Specificații (SRS)](SPECIFICATII.md)
- 🏃 [Planificare sprinturi](SPRINTURI.md)
- 📊 [Diagrame UML si workflow-uri](DIAGRAME.md)
- 🤖 [Raport folosire instrumente AI](RAPORT_AI_TOOLS.md)
- 🧩 [Design Patterns aplicate](DESIGN_PATTERNS.md)
