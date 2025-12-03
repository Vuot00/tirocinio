# 📘 Progetto: Sistema di Allocazione Deterministica Risorse

## 1. Scopo del Progetto
Costruire un sistema di pianificazione delle risorse che sia **stabile e deterministico**.
L'obiettivo è evitare riassegnazioni continue, conflitti tra progetti e oscillazioni delle priorità. Il sistema calcola la soluzione migliore **una volta sola**.

---

## 2. I Pilastri del Modello

### A. Filosofia "Foto Statica"
* Il sistema non sposta risorse già assegnate.
* Se un progetto non trova spazio, viene segnalato come **"Non Fattibile"** (intervento umano richiesto), invece di rompere la pianificazione degli altri.

### B. Algoritmo di Priorità (Ordinamento)
I progetti vengono processati in ordine rigoroso di scadenza:
> **Scadenza più vicina = Priorità più alta.**

### C. Algoritmo di Assegnazione (Greedy)
Per coprire le ore di un progetto, il sistema sceglie le risorse secondo questo criterio:
1.  Filtra chi ha la **skill richiesta**.
2.  Ordina le risorse in base alla **maggior disponibilità residua** (chi è più scarico lavora prima).
3.  Assegna le ore fino a coprire il fabbisogno o raggiungere il limite di budget (max risorse).

---

## 3. Il Margine di Sicurezza

Per mitigare il rischio di ritardi e stime errate, introduciamo un fattore di sicurezza **direttamente nel fabbisogno**.

### La Formula
$$\text{Ore Richieste} = \text{Stima Iniziale} \times (1 + \text{Margine \%})$$

### Effetti Operativi
* **Ore Reali vs Pianificate:** Una risorsa continua a lavorare 8 ore al giorno, ma il sistema ne pianifica (ad esempio) solo 6 o 7.
* **Buffer:** Le ore non pianificate fungono da cuscinetto per gli imprevisti.
* **Percentuali:** Le percentuali di allocazione formale diminuiscono (es. dal 100% all'80%), lasciando spazio di manovra.

---

## 4. Architettura Tecnica

Il progetto è strutturato in **3 moduli** Python distinti per separare le responsabilità.

### 📂 Struttura File
```text
📁 pianificatore_progetti/
│
├── 📄 modelli.py        # (LE FONDAMENTA)
│   ├── Class Risorsa: gestisce nome, skill, ore totali e residuo.
│   └── Class Progetto: gestisce dati, scadenze e applica il Margine di Sicurezza.
│
├── 📄 motore.py         # (IL CERVELLO)
│   ├── Funzione ordina_progetti(): stabilisce le priorità.
│   └── Funzione assegna_risorse(): esegue l'algoritmo "greedy" di assegnazione.
│
└── 📄 main.py           # (IL COMANDANTE)
    ├── Caricamento dati (input).
    ├── Avvio del motore.
    └── Stampa dei report finali (output).
```

# 🗺️ Roadmap di Sviluppo

Usa questo file per tracciare lo stato di avanzamento del progetto.
Segna le attività completate mettendo una `x` tra le parentesi quadre (es. `- [x]`).

## 🏗️ Fase 1: Strutture Dati (File: `modelli.py`)
*Obiettivo: Creare le basi del sistema definendo gli oggetti e le regole matematiche.*

- [x] **Definizione classe `Risorsa`**
  - [x] Attributi: nome, skill, ore totali, ore impegnate
  - [x] Proprietà dinamica: `ore_residue`
  - [x] Metodo per assegnare ore
- [x] **Definizione classe `Progetto`**
  - [x] Attributi: nome, scadenza, budget risorse
  - [x] **Logica Margine di Sicurezza**: Calcolo automatico `ore_richieste` aumentate del margine %

---

## 🧠 Fase 2: Motore Logico (File: `motore.py`)
*Obiettivo: Implementare l'algoritmo che prende le decisioni senza intervento umano.*

- [x] **Funzione `ordina_progetti`**
  - [x] Criterio: Data di scadenza crescente (dal più urgente al meno urgente)
- [x] **Funzione `assegna_risorse` (Algoritmo Greedy)**
  - [x] Ciclo sui progetti ordinati
  - [x] Filtro risorse per skill
  - [x] Ordinamento risorse per disponibilità residua (decrescente)
  - [x] Assegnazione ore fino a copertura o fine risorse
  - [x] Gestione stato "Non Fattibile" se le risorse mancano

---

## 🚀 Fase 3: Esecuzione e Test (File: `main.py`)
*Obiettivo: Mettere tutto insieme e verificare il funzionamento con dati simulati.*

- [x] **Setup Dati di Prova**
  - [x] Creazione lista Risorse simulate (es. Mario, Luca, Giulia)
  - [x] Creazione lista Progetti simulati con scadenze diverse
- [x] **Integrazione**
  - [x] Importazione dei moduli `modelli` e `motore`
  - [x] Esecuzione della pianificazione
- [x] **Reportistica**
  - [x] Stampa progetti pianificati con dettagli
  - [x] Stampa progetti scartati
  - [x] Stampa carico finale delle risorse
      * Esecuzione script e verifica output.
      * Tuning dei parametri (margine, budget).
