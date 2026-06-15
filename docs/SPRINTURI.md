# 🏃 Planificare sprinturi — NeuroDeck

> **Metodologie:** Scrum / dezvoltare iterativă
> **Durată sprint:** ~1 săptămână
> **Ultima actualizare:** 2026-06-15

Acest document mapează [backlog-ul](BACKLOG.md) pe sprinturi. Fiecare sprint corespunde unei iterații livrate (vizibilă în istoricul de branch-uri și commit-uri al repository-ului).

---

## 🗺️ Roadmap general

```text
Sprint 1  ██████████  Fundație & infrastructură        [DONE]
Sprint 2  ██████████  Autentificare                    [DONE]
Sprint 3  ██████████  Procesare PDF + Generare AI       [DONE]
Sprint 4  ██████████  Evaluare răspunsuri               [DONE]
Sprint 5  ██████████  Sesiuni de studiu + UI            [DONE]
Sprint 6  ░░░░░░░░░░  Securitate & producție            [PLANIFICAT]
```

---

## Sprint 1 — Fundație & infrastructură 🟢
**Obiectiv:** schelet funcțional al backend-ului (DB, modele, scheme, CRUD).

| Story | Pts | Branch asociat |
|---|---|---|
| US-01 Configurare DB | 3 | `feature/database-setup` |
| US-02 Modele | 5 | `feature/create-models` |
| US-03 Scheme | 3 | `feature/create-schemas` |
| US-04 CRUD | 5 | `feature/create-crud` |

**Velocity:** 16 pts · **Livrare:** schelet de date complet.

---

## Sprint 2 — Autentificare 🟢
**Obiectiv:** conturi de utilizator funcționale.

| Story | Pts | Branch asociat |
|---|---|---|
| US-05 Înregistrare | 3 | `feature/setup-api-routes` |
| US-06 Email unic | 2 | `feature/setup-api-routes` |
| US-07 Login | 3 | *commit `added login`* |

**Velocity:** 8 pts · **Livrare:** register + login.

---

## Sprint 3 — Procesare PDF + Generare AI 🟢
**Obiectiv:** de la PDF la flashcards.

| Story | Pts | Branch asociat |
|---|---|---|
| US-08…US-12 Procesare PDF | 17 | `feature/ai-agents` |
| US-13…US-17 Generare AI | 21 | `feature/ai-agents` |

**Velocity:** 38 pts · **Livrare:** pipeline complet PDF → flashcards.

---

## Sprint 4 — Evaluare răspunsuri 🟢
**Obiectiv:** scor semantic și verdict.

| Story | Pts | Branch asociat |
|---|---|---|
| US-18…US-21 Evaluare | 16 | `feature/ai-agents` |

**Velocity:** 16 pts · **Livrare:** evaluare semantică funcțională.

---

## Sprint 5 — Sesiuni de studiu + UI 🟢
**Obiectiv:** organizarea materialelor pe materii.

| Story | Pts | Branch asociat |
|---|---|---|
| US-22…US-26 Sesiuni | 12 | `feature/menu` |

**Velocity:** 12 pts · **Livrare:** CRUD sesiuni + meniu lateral.

---

## Sprint 6 — Securitate & producție ⚪ *(planificat)*
**Obiectiv:** hardening înainte de deploy real.

| Story | Pts | Status |
|---|---|---|
| US-27 Hash parole | 3 | ⚪ |
| US-28 Token JWT | 5 | ⚪ |
| US-29 Config externă | 3 | ⚪ |
| US-30 Docker | 5 | ⚪ |
| US-31 CI/CD | 5 | ⚪ |
| US-32 Teste automate | 8 | ⚪ |
| US-33 Logging/monitoring | 3 | ⚪ |

**Capacitate planificată:** ~32 pts.

---

## 📈 Burn-down (sumar)

| Sprint | Puncte planificate | Puncte livrate | Cumulativ livrat |
|---|---|---|---|
| 1 | 16 | 16 | 16 |
| 2 | 8 | 8 | 24 |
| 3 | 38 | 38 | 62 |
| 4 | 16 | 16 | 78 |
| 5 | 12 | 12 | 90 |
| 6 | 32 | — | (în desfășurare) |

**Total livrat până acum:** 90 / 130 story points (~69%).

---

## 🔗 Documente conexe
- 📑 [Specificații (SRS)](SPECIFICATII.md)
- 📋 [Backlog de produs](BACKLOG.md)
