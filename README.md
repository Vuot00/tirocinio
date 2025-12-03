# 📑 PoC – Micro-Servizio di Allocazione Risorse

## 1. Obiettivo del Progetto
Realizzare un **Proof of Concept** per un motore di allocazione risorse capace di:

- Gestire risorse assegnate a più progetti contemporaneamente  
- Identificare automaticamente sovraccarichi e problemi di disponibilità  
- Garantire modularità, portabilità e piena testabilità

---

## 2. Contesto e Finalità
Il sistema fa parte del futuro **Workforce Management System** e si concentra sui requisiti:

- **RF-10**: controllo disponibilità delle risorse  
- **RF-11**: segnalazione sovraccarichi  
- **RF-16**: ricalcolo automatico delle allocazioni

---

## 3. Concetti Fondamentali

### 3.1 Modelli di Dati Principali

#### ✔ Risorsa (Chi)
Rappresenta la persona allocata a uno o più progetti.  
**Campi tipici:**
- ID
- Competenza/skill
- Capacità totale (es. 40h o 100%/settimana)
- Assenze/limitazioni (opzionale)

#### ✔ Progetto (Cosa)
Contiene le attività che consumano capacità.  
**Campi:**
- ID
- Data inizio/fine
- Sforzo/ore richieste
- Skill necessarie

#### ✔ Allocazione (Quando + Quanto)
Associazione tra risorsa e progetto.  
**Campi:**
- Resource_ID
- Project_ID
- Start_date
- End_date
- Effort_percentage (0–100%)

> Il motore verifica che la somma dell’effort giornaliero non superi il 100%.

---

## 4. Architettura Generale
Modello **3-tier**, totalmente containerizzato con Docker.

### 4.1 Backend (Core)
- **FastAPI + Pydantic**
- Implementa logiche:
  - Calcolo carico risorse
  - Verifica sovraccarichi
  - API REST

### 4.2 Data Layer
- **SQLAlchemy**
- Database-agnostic:
  - PostgreSQL (sviluppo)
  - SQLite (demo portabile)

### 4.3 Frontend
- **Vue.js + TypeScript**
- Mostra:
  - Timeline assegnazioni
  - Evidenziazione sovraccarichi

### 4.4 Containerizzazione
- **Docker / Docker Compose**
- Garantisce:
  - Portabilità (RNF-24)
  - Setup uniforme

---

## 5. Logica di Calcolo (Core Engine)

### Per ogni risorsa:
1. Estrarre tutte le allocazioni attive nel periodo
2. Per ogni giorno sommare gli `effort_percentage`
3. Se la somma > 100%:
   - Generare un alert

### Output del motore (esempi):
- Nessun problema
- Sovraccarico lieve
- Sovraccarico grave

---

## 6. Test e Qualità (RNF-22)

### 6.1 Unit Test
- `pytest` (backend)
- `vitest/jest` (frontend)

### 6.2 Integration Test
- Verificano:
  - FastAPI ↔ SQLAlchemy ↔ DB

### 6.3 E2E Test
- **Cypress o Playwright**
- Simulano:
  - Inserimento allocazioni
  - Visualizzazione UI
  - Identificazione sovraccarichi

---

## 7. Piano di Lavoro

### **Fase 1 – Setup**
- Configurazione Docker
- Definizione entità SQLAlchemy

### **Fase 2 – Motore di Calcolo**
- Implementazione algoritmi:
  - Verifica disponibilità (RF-10)
  - Ricalcolo automatico (RF-16)
- Alta copertura di test unitari

### **Fase 3 – Frontend**
- UI timeline in Vue.js
- Evidenziazione sovraccarichi (RF-11)

### **Fase 4 – Validazione**
- E2E test
- Dimostrazione portabilità tramite SQLite

---

## 8. Vantaggi della Soluzione

### Tecnici
- Architettura moderna e scalabile  
- Codice tipizzato e manutenibile  
- Backend disaccoppiato dal database

### Operativi
- Individuazione immediata dei sovraccarichi  
- Supporto reale al multi-progetto  
- Interfaccia chiara e visuale

### Organizzativi
- Pronto per evolvere in microservizio  
- Perfettamente dimostrabile in presentazione

---

## 9. Fuori dallo Scope
- Nessun algoritmo avanzato di ottimizzazione
- Nessuna gestione ferie/turni complessi
- Nessun controllo ruoli/permessi avanzato

---

## 10. Risultato Atteso
Un prototipo funzionante che:

- calcola correttamente il carico giornaliero delle risorse  
- segnala i sovraccarichi  
- è portabile, testabile e ingegnerizzato in modo professionale
