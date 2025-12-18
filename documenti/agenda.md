# 📅 Agenda di Sviluppo: Pianificatore Risorse (WIP)

**Stato Progetto:** 🚧 IN CORSO  
**Ultimo aggiornamento:** 18 Dicembre 2025

---

## 📘 FASE 1: ANALISI, STUDIO E PROGETTAZIONE
**Periodo:** 19 Novembre – 02 Dicembre  
**Obiettivo:** Definizione modello matematico e requisiti (No Code).

### Settimana 1

* **19 Novembre (Mar): Analisi Preliminare e Concettualizzazione**
    * *Attività:* Analisi del problema di allocazione risorse. Definizione dei pilastri del modello deterministico (priorità fissa, non riassegnazione).
    * *Rif:* `[01] Idea di fondo.md`

* **20 Novembre (Mer): Definizione Algoritmo Core**
    * *Attività:* Studio della logica di assegnazione "Greedy" e criterio selezione risorse (disponibilità residua).
    * *Rif:* `[02] Approfondimento su algoritmo di assegnazione ore.md`

* **21 Novembre (Gio): Studio Margini di Sicurezza**
    * *Attività:* Analisi rischio stime e introduzione teorica del buffer per mitigare falsi negativi.
    * *Rif:* `[03] Sviluppo con introduzione di margine di sicurezza sulle stime.md`

* **22 Novembre (Ven): Analisi Impatto sui Ruoli**
    * *Attività:* Studio matematico sulla riduzione delle percentuali operative reali (Dev/Tester) a parità di ore contrattuali.
    * *Rif:* `[04] Ripercussioni sulle percentuali di lavoro per ruolo.md`

### Settimana 2

* **25 Novembre (Lun): Definizione Vincoli Temporali**
    * *Attività:* Formalizzazione regola 8h lavorative e invarianza orario contrattuale rispetto al margine.
    * *Rif:* `[05] Ore lavorative.md`

* **26 Novembre (Mar): Progettazione Architettura MVC**
    * *Attività:* Scelta stack (Flask, SQLAlchemy) e bozza architettura tecnica.

* **27 Novembre (Mer): Pianificazione Roadmap**
    * *Attività:* Stesura fasi di sviluppo (Core > DB > Web > Advanced) e definizione funzionalità.
    * *Rif:* `[06] Documentazione progetto.md`

* **28 Novembre (Gio): Modellazione Database (ER)**
    * *Attività:* Disegno schema relazioni (Risorse ↔ Assenze, Progetti).

* **29 Novembre (Ven): Raffinamento Logiche Business**
    * *Attività:* Analisi casi limite (load balancing, skill multiple).

### Settimana 3 (Inizio)

* **02 Dicembre (Lun): Revisione Documentale e Setup**
    * *Attività:* Chiusura documenti analisi e preparazione ambiente Python (venv, git init).

---

## 💻 FASE 2: SVILUPPO SOFTWARE (Core & Web App)
**Periodo:** 03 Dicembre – Oggi  
**Obiettivo:** Implementazione Codice Python, Database e Interfaccia.

### Settimana 3 (Continuazione)

* **03 Dicembre (Mar): Implementazione Modelli Dati**
    * *Attività:* Traduzione entità in classi Python (`Risorsa`, `Progetto`) e setup `config_modelli.py`.
    * *Commit:* Core Logic & Algoritmo.

* **04 Dicembre (Mer): Sviluppo Motore Allocazione**
    * *Attività:* Scrittura logica `assegna_risorse`, ordinamento prioritario e calcolo fattore pianificazione.
    * *File:* `motore.py`.

* **05 Dicembre (Gio): Testing Algoritmico (Mock Data)**
    * *Attività:* Verifica matematica algoritmo tramite script test isolato (senza DB).
    * *File:* `test_manuale.py`.

* **06 Dicembre (Ven): Implementazione Persistenza Dati**
    * *Attività:* Configurazione SQLAlchemy, creazione tabelle DB e metodi mapping oggetto-relazionale.
    * *File:* `db_manager.py`.

### Settimana 4

* **09 Dicembre (Lun): Setup Framework Web**
    * *Attività:* Inizializzazione Flask (`app.py`), routing base e layout `base.html`.

* **10 Dicembre (Mar): Modulo Gestione Risorse**
    * *Attività:* CRUD Risorse, gestione Assenze e visualizzazione grafica barre di carico.
    * *File:* `templates/risorse.html`.

* **11 Dicembre (Mer): Modulo Gestione Progetti**
    * *Attività:* Form inserimento progetti con validazione JS percentuali skill dinamiche.
    * *File:* `templates/progetti.html`.

* **12 Dicembre (Gio): Dashboard e Stati Automatici**
    * *Attività:* Logica aggiornamento stati (Pianificato → In Corso) e visualizzazione dettagli assegnazioni.

* **13 Dicembre (Ven): UI Design e Styling**
    * *Attività:* Refactoring CSS (`style.css`), miglioramento UX (card, badge, messaggi errore).

### Settimana 5

* **16 Dicembre (Lun): Integrazione Calendario**
    * *Attività:* Implementazione FullCalendar.js e API JSON eventi backend.
    * *File:* `templates/calendario.html`.

* **17 Dicembre (Mar): Logica Festività Italiana**
    * *Attività:* Integrazione libreria `holidays`, filtro giorni lavorativi in `motore.py`.

# 📅 Agenda di Sviluppo: Pianificatore Risorse (WIP)

**Stato Progetto:** 🚧 IN CORSO  
**Ultimo aggiornamento:** 18 Dicembre 2025

---

## 📘 FASE 1: ANALISI, STUDIO E PROGETTAZIONE
**Periodo:** 19 Novembre – 02 Dicembre  
**Obiettivo:** Definizione modello matematico e requisiti (No Code).

### Settimana 1

* **19 Novembre (Mar): Analisi Preliminare e Concettualizzazione**
    * *Attività:* Analisi del problema di allocazione risorse. Definizione dei pilastri del modello deterministico (priorità fissa, non riassegnazione).
    * *Rif:* `[01] Idea di fondo.md`

* **20 Novembre (Mer): Definizione Algoritmo Core**
    * *Attività:* Studio della logica di assegnazione "Greedy" e criterio selezione risorse (disponibilità residua).
    * *Rif:* `[02] Approfondimento su algoritmo di assegnazione ore.md`

* **21 Novembre (Gio): Studio Margini di Sicurezza**
    * *Attività:* Analisi rischio stime e introduzione teorica del buffer per mitigare falsi negativi.
    * *Rif:* `[03] Sviluppo con introduzione di margine di sicurezza sulle stime.md`

* **22 Novembre (Ven): Analisi Impatto sui Ruoli**
    * *Attività:* Studio matematico sulla riduzione delle percentuali operative reali (Dev/Tester) a parità di ore contrattuali.
    * *Rif:* `[04] Ripercussioni sulle percentuali di lavoro per ruolo.md`

### Settimana 2

* **25 Novembre (Lun): Definizione Vincoli Temporali**
    * *Attività:* Formalizzazione regola 8h lavorative e invarianza orario contrattuale rispetto al margine.
    * *Rif:* `[05] Ore lavorative.md`

* **26 Novembre (Mar): Progettazione Architettura MVC**
    * *Attività:* Scelta stack (Flask, SQLAlchemy) e bozza architettura tecnica.

* **27 Novembre (Mer): Pianificazione Roadmap**
    * *Attività:* Stesura fasi di sviluppo (Core > DB > Web > Advanced) e definizione funzionalità.
    * *Rif:* `[06] Documentazione progetto.md`

* **28 Novembre (Gio): Modellazione Database (ER)**
    * *Attività:* Disegno schema relazioni (Risorse ↔ Assenze, Progetti).

* **29 Novembre (Ven): Raffinamento Logiche Business**
    * *Attività:* Analisi casi limite (load balancing, skill multiple).

### Settimana 3 (Inizio)

* **02 Dicembre (Lun): Revisione Documentale e Setup**
    * *Attività:* Chiusura documenti analisi e preparazione ambiente Python (venv, git init).

---

## 💻 FASE 2: SVILUPPO SOFTWARE (Core & Web App)
**Periodo:** 03 Dicembre – Oggi  
**Obiettivo:** Implementazione Codice Python, Database e Interfaccia.

### Settimana 3 (Continuazione)

* **03 Dicembre (Mar): Implementazione Modelli Dati**
    * *Attività:* Traduzione entità in classi Python (`Risorsa`, `Progetto`) e setup `config_modelli.py`.
    * *Commit:* Core Logic & Algoritmo.

* **04 Dicembre (Mer): Sviluppo Motore Allocazione**
    * *Attività:* Scrittura logica `assegna_risorse`, ordinamento prioritario e calcolo fattore pianificazione.
    * *File:* `motore.py`.

* **05 Dicembre (Gio): Testing Algoritmico (Mock Data)**
    * *Attività:* Verifica matematica algoritmo tramite script test isolato (senza DB).
    * *File:* `test_manuale.py`.

* **06 Dicembre (Ven): Implementazione Persistenza Dati**
    * *Attività:* Configurazione SQLAlchemy, creazione tabelle DB e metodi mapping oggetto-relazionale.
    * *File:* `db_manager.py`.

### Settimana 4

* **09 Dicembre (Lun): Setup Framework Web**
    * *Attività:* Inizializzazione Flask (`app.py`), routing base e layout `base.html`.

* **10 Dicembre (Mar): Modulo Gestione Risorse**
    * *Attività:* CRUD Risorse, gestione Assenze e visualizzazione grafica barre di carico.
    * *File:* `templates/risorse.html`.

* **11 Dicembre (Mer): Modulo Gestione Progetti**
    * *Attività:* Form inserimento progetti con validazione JS percentuali skill dinamiche.
    * *File:* `templates/progetti.html`.

* **12 Dicembre (Gio): Dashboard e Stati Automatici**
    * *Attività:* Logica aggiornamento stati (Pianificato → In Corso) e visualizzazione dettagli assegnazioni.

* **13 Dicembre (Ven): UI Design e Styling**
    * *Attività:* Refactoring CSS (`style.css`), miglioramento UX (card, badge, messaggi errore).

### Settimana 5

* **16 Dicembre (Lun): Integrazione Calendario**
    * *Attività:* Implementazione FullCalendar.js e API JSON eventi backend.
    * *File:* `templates/calendario.html`.

* **17 Dicembre (Mar): Logica Festività Italiana**
    * *Attività:* Integrazione libreria `holidays`, filtro giorni lavorativi in `motore.py`.

* **18 Dicembre (Mer - OGGI): Integrazione Logiche Temporali**
    * *Attività:* Test e verifica calcolo ore nette su calendario reale. Aggiornamento documentazione tecnica.
    * *Stato:* **Fase 3 Completata.**

---

## 🚀 PROSSIMI PASSI (Roadmap - Fase 4)
*Attività previste (da confermare in base al repository):*

* [ ] **Visualizzazione Gantt:** Diagramma temporale progetti.
* [ ] **Simulazione What-If:** Creazione progetti "bozza" senza salvataggio.
* [ ] **Export Dati:** Reportistica in PDF/Excel.
* [ ] **Refactoring Skill:** Livelli competenza (Junior/Senior).

*In attesa di istruzioni per le attività di domani (19 Dicembre)...*

---

## 🚀 PROSSIMI PASSI (Roadmap - Fase 4)
*Attività previste (da confermare in base al repository):*

* [ ] **Visualizzazione Gantt:** Diagramma temporale progetti.
* [ ] **Simulazione What-If:** Creazione progetti "bozza" senza salvataggio.
* [ ] **Export Dati:** Reportistica in PDF/Excel.
* [ ] **Refactoring Skill:** Livelli competenza (Junior/Senior).

*In attesa di istruzioni per le attività di domani (19 Dicembre)...*