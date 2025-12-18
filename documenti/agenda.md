# 📅 Agenda di Sviluppo: Pianificatore Risorse

**Periodo:** 19 Novembre 2025 – 18 Dicembre 2025  
**Oggetto:** Diario delle attività giornaliere (Analisi e Sviluppo Software)

---

## 📘 FASE 1: ANALISI, STUDIO E PROGETTAZIONE
**Periodo:** 19 Novembre – 02 Dicembre  
**Focus:** Stesura documentazione, definizione algoritmi e requisiti.

### Settimana 1

* **19 Novembre (Mar): Analisi Preliminare e Concettualizzazione**
    * *Attività:* Analisi del problema di allocazione risorse. Definizione dei pilastri del modello deterministico (priorità fissa, non riassegnazione).
    * *Output:* Stesura bozza documento `[01] Idea di fondo.md`.

* **20 Novembre (Mer): Definizione Algoritmo Core**
    * *Attività:* Studio della logica di assegnazione "Greedy". Definizione del criterio di selezione risorse basato sulla disponibilità residua.
    * *Output:* Stesura `[02] Approfondimento su algoritmo di assegnazione ore.md`.

* **21 Novembre (Gio): Studio Margini di Sicurezza**
    * *Attività:* Analisi delle problematiche di stima e rischio. Introduzione teorica del buffer per mitigare i falsi negativi.
    * *Output:* Stesura `[03] Sviluppo con introduzione di margine di sicurezza sulle stime.md`.

* **22 Novembre (Ven): Analisi Impatto sui Ruoli**
    * *Attività:* Studio matematico di come il margine riduce le percentuali operative reali dei ruoli (Dev/Tester) pur mantenendo le 8 ore contrattuali.
    * *Output:* Stesura `[04] Ripercussioni sulle percentuali di lavoro per ruolo.md`.

### Settimana 2

* **25 Novembre (Lun): Definizione Vincoli Temporali**
    * *Attività:* Formalizzazione delle regole sulle ore lavorative (8h/die, Lun-Ven). Conferma che il margine agisce solo sul pianificato.
    * *Output:* Stesura `[05] Ore lavorative.md`.

* **26 Novembre (Mar): Progettazione Architettura MVC**
    * *Attività:* Decisione sullo stack tecnologico: Flask (Controller), SQLAlchemy (Model), Jinja2 (View). Inizio stesura specifiche tecniche.

* **27 Novembre (Mer): Pianificazione Roadmap**
    * *Attività:* Definizione delle fasi di implementazione (Core Logic -> Database -> Web App). Pianificazione feature "Must Have".
    * *Output:* Integrazione roadmap in `[06] Documentazione progetto.md`.

* **28 Novembre (Gio): Modellazione Database (ER)**
    * *Attività:* Disegno dello schema Entità-Relazione. Definizione relazioni tra Tabelle Risorse, Progetti e Assenze.

* **29 Novembre (Ven): Raffinamento Logiche di Business**
    * *Attività:* Studio dei casi limite per l'algoritmo (gestione multi-skill, load balancing tra risorse equivalenti).

### Settimana 3 (Inizio)

* **02 Dicembre (Lun): Revisione Documentale e Setup**
    * *Attività:* Revisione finale di tutti i file Markdown. Preparazione ambiente di sviluppo Python (IDE, venv). Chiusura fase di analisi.

---

## 💻 FASE 2: SVILUPPO SOFTWARE
**Periodo:** 03 Dicembre – 18 Dicembre  
**Focus:** Scrittura codice Python, Database e Interfaccia Web.

### Settimana 3 (Continuazione)

* **03 Dicembre (Mar): Implementazione Modelli Dati**
    * *Attività:* Traduzione delle entità in classi Python. Definizione template best practice.
    * *File lavorati:* `modelli.py`, `config_modelli.py`.

* **04 Dicembre (Mer): Sviluppo Motore di Allocazione**
    * *Attività:* Scrittura della funzione `assegna_risorse`, logica di ordinamento e calcolo del `fattore_pianificazione`.
    * *File lavorati:* `motore.py`.

* **05 Dicembre (Gio): Testing Algoritmico e Debug**
    * *Attività:* Verifica matematica dell'algoritmo tramite script di test isolati (Mock Data).
    * *File lavorati:* `test_manuale.py`.

* **06 Dicembre (Ven): Implementazione Persistenza Dati**
    * *Attività:* Configurazione ORM SQLAlchemy. Creazione tabelle `RisorsaDB`, `ProgettoDB` e mapping oggetti logici.
    * *File lavorati:* `db_manager.py`, `instance/pianificatore.db`.

### Settimana 4

* **09 Dicembre (Lun): Setup Framework Web**
    * *Attività:* Inizializzazione Flask. Creazione struttura base layout HTML e routing.
    * *File lavorati:* `app.py`, `templates/base.html`.

* **10 Dicembre (Mar): Sviluppo Modulo Risorse**
    * *Attività:* Implementazione CRUD Risorse e gestione Assenze. Visualizzazione barre di carico.
    * *File lavorati:* `templates/risorse.html`, `templates/modifica_risorsa.html`.

* **11 Dicembre (Mer): Sviluppo Modulo Progetti**
    * *Attività:* Implementazione form di inserimento progetti con gestione dinamica percentuali skill.
    * *File lavorati:* `templates/progetti.html`, `templates/modifica_progetto.html`.

* **12 Dicembre (Gio): Logica Dashboard e Stati**
    * *Attività:* Implementazione aggiornamento automatico stati (Pianificato/In corso). Visualizzazione dettagli assegnazioni.
    * *File lavorati:* `app.py`, `templates/progetti.html`.

* **13 Dicembre (Ven): Design UI e Styling**
    * *Attività:* Miglioramento CSS (Card, Badge, Tabelle). Feedback utente (Flash messages).
    * *File lavorati:* `static/style.css`.

### Settimana 5

* **16 Dicembre (Lun): Integrazione Calendario Visuale**
    * *Attività:* Integrazione FullCalendar.js e creazione API JSON per eventi.
    * *File lavorati:* `templates/calendario.html`, `app.py`.

* **17 Dicembre (Mar): Gestione Festività e Orari Reali**
    * *Attività:* Integrazione libreria `holidays`. Filtro giorni lavorativi nel motore di calcolo.
    * *File lavorati:* `motore.py`, `app.py`.

* **18 Dicembre (Mer): Finalizzazione e Documentazione Tecnica**
    * *Attività:* Stesura README, pulizia codice, verifica coerenza finale tra documenti e software.
    * *File lavorati:* `README.md`, `.gitignore`.