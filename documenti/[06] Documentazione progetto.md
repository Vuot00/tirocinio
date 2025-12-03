# 📘 Progetto: Sistema di Allocazione Deterministica Risorse (v2.0 Web)

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

## 4. Architettura Tecnica (Web App Flask)

Il progetto è evoluto da script CLI a **Web Application MVC**.

### 📂 Struttura File
```text
📁 pianificatore_progetti/
│
├── 📄 app.py            # (CONTROLLER) Server Flask. Gestisce rotte, input utenti e coordinamento.
├── 📄 db_manager.py     # (DATABASE LAYER) Gestisce tabelle SQLite (SQLAlchemy) e traduzione dati.
├── 📄 modelli.py        # (PURE LOGIC) Classi Risorsa/Progetto usate per il calcolo in memoria.
├── 📄 motore.py         # (ALGORITHM) Il cuore del calcolo. Contiene la logica di assegnazione.
│
├── 📁 templates/        # (VIEWS) Pagine HTML
│   ├── index.html              # Dashboard principale (Input + Tabelle).
│   ├── risultato.html          # Report pianificazione.
│   ├── modifica_progetto.html  # Pagina edit progetti.
│   └── modifica_risorsa.html   # Pagina edit risorse e assenze.
│
└── 📁 static/
    └── style.css        # Fogli di stile CSS.
```

# 🗺️ Roadmap di Sviluppo

Questa roadmap traccia l'evoluzione del **Pianificatore Risorse Deterministico**, dallo script iniziale alla Web App completa.

## ✅ Fase 1: Core Logic & Algoritmo (`modelli.py`, `motore.py`)
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

## ✅ Fase 2: Database & Persistenza (`db_manager.py`)
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

## ✅ Fase 3: Web Application (`app.py`, Templates)
*Obiettivo: Interfaccia utente completa per la gestione quotidiana.*

- [x] **Dashboard (`index.html`)**
    - [x] Form inserimento Risorse.
    - [x] Form inserimento Assenze (collegato alla risorsa).
    - [x] Form inserimento Progetti (con gestione quantità e percentuali).
    - [x] **Validazione JS**: Controllo somma percentuali = 100%.
    - [x] Visualizzazione code: Ordinamento decrescente (ultimi inseriti in alto).
- [x] **Gestione CRUD (Modifica/Elimina)**
    - [x] Pagina `modifica_progetto.html` (precompilazione dati esistenti).
    - [x] Pagina `modifica_risorsa.html` (gestione anagrafica e storico assenze).
    - [x] Eliminazione singole assenze, risorse e progetti.
- [x] **Reportistica (`risultato.html`)**
    - [x] Visualizzazione esito (Fattibile ✅ / Non Fattibile ⛔).
    - [x] Visualizzazione barre di carico per ogni risorsa.
    - [x] Dettaglio ore assegnate per progetto.

---

## 🔜 Fase 4: Futuri Miglioramenti (Backlog)
*Idee per le prossime versioni del software.*

- [ ] **Sicurezza**: Aggiungere Login e gestione utenti.
- [ ] **Export**: Scaricare il piano in Excel o PDF.
- [ ] **Visualizzazione Avanzata**: Grafico di Gantt temporale.
- [ ] **Storico**: Salvare i piani calcolati in passato per confronto.
- [ ] **Deploy**: Containerizzazione con Docker.