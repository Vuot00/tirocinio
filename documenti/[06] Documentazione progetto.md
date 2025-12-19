# 📘 Progetto: Sistema di Allocazione Deterministica Risorse (v2.5 Refactored)

## 1. Scopo del Progetto
Costruire un sistema di pianificazione delle risorse che sia **stabile, deterministico e accessibile via Web**.
L'obiettivo è evitare riassegnazioni continue e conflitti, calcolando la soluzione migliore **una volta sola** basandosi su vincoli rigidi (Priorità, Competenze, Assenze).

---

## 2. I Pilastri del Modello

### A. Filosofia "Foto Statica"
* Il sistema non sposta risorse già assegnate in precedenti elaborazioni.
* Se un progetto non trova spazio, viene segnalato come **"Non Fattibile"**, richiedendo intervento umano (es. cambio priorità o aggiunta risorse).

### B. Algoritmo di Priorità (Ordinamento)
I progetti vengono processati in ordine rigoroso basato su due chiavi:
1.  **Priorità Manuale** (1 = Massima Urgenza, vince su tutto).
2.  **Data di Scadenza** (A parità di priorità manuale, vince la scadenza più vicina).

### C. Gestione Team Multi-Skill e Percentuali
Un progetto non richiede più una singola risorsa generica, ma definisce una **composizione del team** basata su percentuali del monte ore totale.
* *Esempio:* Progetto da 100 ore → 20% Developer (20h), 80% Tester (80h).
* Il sistema cerca risorse specifiche per ogni ruolo richiesto.

### D. Algoritmo di Assegnazione (Load Balancing)
Per coprire le ore di un ruolo, il sistema:
1.  Filtra chi ha la **skill richiesta**.
2.  Ordina le risorse per **maggior disponibilità residua**.
3.  **Distribuisce il carico**: Invece di saturare una risorsa alla volta, divide il lavoro equamente tra le risorse necessarie (es. se servono 2 Dev per 40 ore, assegna max 20 ore a testa).

### E. Gestione Assenze
Il sistema tiene conto delle **ferie e assenze** registrate. Le ore di assenza vengono sottratte a monte dalla disponibilità della risorsa prima di iniziare la pianificazione.

---

## 3. Il Margine di Sicurezza (Buffer Interno)

Il margine non viene usato per chiedere ore extra al cliente, ma per creare un **cuscinetto interno** sulla disponibilità della risorsa.

### La Logica
Il sistema applica un "Fattore di Pianificazione":

$$\text{Fattore} = 1 - \left( \frac{\text{Margine \%}}{100} \right)$$

*Esempio (Margine 10%):*
Se il progetto richiede 50 ore, il sistema occupa 50 ore "reali" del progetto, ma verifica che la risorsa abbia spazio sufficiente come se ne stessimo occupando di più, oppure "sconta" la capacità di pianificazione per lasciare ore libere non assegnate sul calendario della risorsa.

---

## 4. Architettura Tecnica (Refactoring MVC)

Il progetto è evoluto in una architettura professionale modulare basata su **Blueprint** e **Application Factory Pattern**.

### 📂 Nuova Struttura File
```text
📁 TIROCINIO/
│
├── 📄 run.py              # (ENTRY POINT) Avvia il server Flask.
├── 📄 config.py           # (CONFIG) Impostazioni ambiente e DB.
│
├── 📁 app/                # (PACKAGE PRINCIPALE)
│   ├── 📄 __init__.py     # Application Factory.
│   ├── 📄 config_modelli.py
│   │
│   ├── 📁 logic/          # (BUSINESS LOGIC LAYER)
│   │   ├── 📄 engine.py   # Ex motore.py. Cuore del calcolo allocazione.
│   │   └── 📄 services.py # Logica di coordinamento e servizi (es. Calendario).
│   │
│   ├── 📁 models/         # (DATA LAYER)
│   │   ├── 📄 database.py # Inizializzazione SQLAlchemy.
│   │   └── 📄 entities.py # Ex modelli.py. Classi pure e tabelle DB.
│   │
│   ├── 📁 routes/         # (CONTROLLERS) Gestione rotte web tramite Blueprints.
│   │   ├── 📄 main.py     # Home, API e Calendario.
│   │   ├── 📄 progetti.py # CRUD Progetti.
│   │   └── 📄 risorse.py  # CRUD Risorse e Assenze.
│   │
│   └── 📁 templates/      # (VIEWS) Pagine HTML.
│
├── 📁 instance/           # Contiene il database SQLite fisico.
└── 📁 test/               # Suite di test automatici (Pytest).

# 🗺️ Roadmap di Sviluppo

Questa roadmap traccia l'evoluzione del **Pianificatore Risorse Deterministico**, dallo script iniziale alla Web App completa e strutturata.

## ✅ Fase 1: Core Logic & Algoritmo
*Obiettivo: Costruire il motore decisionale stabile e deterministico.*

- [x] **Modellazione Dati**
    - [x] Classi `Risorsa` e `Progetto` con Type Hinting.
    - [x] Normalizzazione date e gestione tipi.
- [x] **Algoritmo di Ordinamento**
    - [x] Priorità Manuale (1=Max) > Data di Scadenza.
- [x] **Algoritmo di Assegnazione (Engine)**
    - [x] Logica Greedy (assegnazione al migliore candidato).
    - [x] **Buffer Interno**: Calcolo ore "scontate" in base al margine di sicurezza.
    - [x] **Multi-Skill**: Gestione requisiti per ruolo (es. Developer, Tester).
    - [x] **Percentuali**: Input carico lavoro basato su % (es. 20% Dev, 80% Tester).
    - [x] **Load Balancing**: Distribuzione equa del carico tra le risorse (non satura il primo che trova).

---

## ✅ Fase 2: Database & Persistenza
*Obiettivo: Salvare i dati in modo permanente su file.*

- [x] **Setup Database**
    - [x] Configurazione SQLite e SQLAlchemy.
- [x] **Struttura Tabelle**
    - [x] `RisorsaDB`: Anagrafica e skill.
    - [x] `ProgettoDB`: Dati, stringa requisiti (parsing automatico).
    - [x] `AssenzaDB`: Gestione ferie/malattia (Relazione 1-a-Molti).
- [x] **Mapping Dati**
    - [x] Conversione automatica da Oggetti DB a Oggetti Logici puri.
    - [x] Calcolo automatico ore perse per assenza.

---

## ✅ Fase 3: Web Application & UI
*Obiettivo: Interfaccia utente completa per la gestione quotidiana.*

- [x] **Dashboard Progetti**
    - [x] Form inserimento Progetti (con gestione quantità e percentuali).
    - [x] **Validazione JS**: Controllo somma percentuali = 100%.
    - [x] Visualizzazione code: Ordinamento e indicatori di stato (Fattibile/Rischio).
- [x] **Gestione Risorse**
    - [x] Dashboard stato risorse (Carico, Residuo, Ferie).
    - [x] Registrazione Assenze.
- [x] **Gestione CRUD (Modifica/Elimina)**
    - [x] Modifica Progetti e Risorse.
    - [x] Eliminazione singole assenze, risorse e progetti.
- [x] **Reportistica**
    - [x] Visualizzazione esito (Fattibile ✅ / Non Fattibile ⛔).
    - [x] Visualizzazione barre di carico per ogni risorsa dentro il progetto.

---

## ✅ Fase 4: Refactoring, Testing & Calendario
*Obiettivo: Professionalizzazione del codice e strumenti visivi.*

- [x] **Architecture Refactoring**
    - [x] Passaggio a struttura MVC modulare (Cartelle `logic`, `models`, `routes`).
    - [x] Implementazione **Application Factory** (`create_app`) e **Blueprints**.
    - [x] Pulizia della root directory e organizzazione file (`run.py`, `config.py`).
- [x] **Quality Assurance (Testing)**
    - [x] Setup ambiente **Pytest**.
    - [x] Test Unitari (Logica pura).
    - [x] Test Database (Integrità salvataggio).
    - [x] Test Rotte Web (Simulazione client).
- [x] **📅 Calendario Visivo (FullCalendar)**
    - [x] Visualizzazione timeline dei progetti (Start -> End).
    - [x] Color coding dinamico in base allo stato (Pianificato, In Svolgimento, Sospeso).
- [x] **🏖️ Festività Nazionali**
    - [x] Integrazione libreria `holidays` per calcolo automatico giorni festivi italiani.
    - [x] Visualizzazione festività nel calendario.

---

## 🔜 Fase 4: Futuri Miglioramenti 
*Attività previste (da confermare in base al repository):*

* [ ] **Calendario:** Possibilità di visualizzare in formato mese, trimestre, ecc..
* [ ] **Simulazione What-If:** Creazione progetti "bozza" senza salvataggio.
* [ ] **Export Dati:** Reportistica in PDF/Excel. (per giorni o per ruolo)

