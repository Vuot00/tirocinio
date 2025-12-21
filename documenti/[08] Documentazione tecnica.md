# 📚 Documentazione Tecnica del Progetto

Questo documento fornisce una panoramica dettagliata dell'architettura software, descrivendo la struttura dei file, la logica di business e la suite di test del **Sistema di Allocazione Deterministica Risorse**.

Il progetto segue il pattern architetturale **MVC (Model-View-Controller)** ed è modulato tramite **Flask Blueprints**.

---

## 1. ⚙️ File di Avvio e Configurazione (Root)

Questi file si trovano nella directory principale del progetto e gestiscono l'ambiente di esecuzione e l'avvio del server.

### `run.py`
**Ruolo:** Entry Point (Punto di Ingresso).
* **Descrizione:** È lo script da eseguire per avviare l'applicazione web (`python run.py`).
* **Funzionamento:** Importa la funzione `create_app` dal pacchetto `app`, crea l'istanza e avvia il server di sviluppo Flask (con `debug=True`).

### `config.py`
**Ruolo:** Configurazione Globale.
* **Descrizione:** Centralizza le impostazioni dell'applicazione e garantisce la portabilità tra diversi sistemi operativi.
* **Funzionalità Chiave:**
    * **Gestione Percorsi:** Calcola dinamicamente `BASE_DIR` e definisce `INSTANCE_PATH`.
    * **Auto-Fix:** Verifica l'esistenza della cartella `instance/` e la crea automaticamente se mancante (prevenendo errori SQLite su Windows).
    * **Classe `Config`:** Definisce `SQLALCHEMY_DATABASE_URI` (percorso del DB) e `SECRET_KEY` (sicurezza sessioni).

---

## 2. 🧪 Suite di Test (`test/`)

La cartella `test/` contiene la suite di Quality Assurance basata su **Pytest**, garantendo che ogni componente funzioni isolatamente e integrato.

### `test/conftest.py`
**Ruolo:** Configurazione Test & Fixtures.
* **Descrizione:** Definisce le risorse condivise per i test.
* **Fixtures:**
    * `app`: Crea un'istanza dell'app configurata per il testing (`TESTING=True`, database in memoria `:memory:`), che viene creata e distrutta per ogni singolo test.
    * `client`: Client HTTP simulato per testare le rotte web.

### `test/test_unitari.py`
**Ruolo:** Unit Testing (Logica Pura).
* **Descrizione:** Verifica il comportamento delle classi di dominio (`Risorsa`, `Progetto`) senza coinvolgere il database. Testa calcoli matematici e normalizzazione date.

### `test/test_motore.py`
**Ruolo:** Test Algoritmo (Business Logic).
* **Descrizione:** Mette alla prova il cuore del sistema (`engine.py`). Verifica scenari di assegnazione risorse e gestione dei casi limite (risorse insufficienti, progetti non fattibili).

### `test/test_db.py`
**Ruolo:** Integration Testing (Database).
* **Descrizione:** Verifica la persistenza dei dati. Controlla che i modelli (`ProgettoDB`, `RisorsaDB`) scrivano e leggano correttamente dal database SQLite.

### `test/test_routes.py`
**Ruolo:** Functional Testing (Controller Web).
* **Descrizione:** Simula l'interazione utente. Verifica che le pagine (es. Dashboard, Form) rispondano con codice 200 OK e contengano i dati attesi.

---

## 3. 📦 Pacchetto Applicativo (`app/`)

La cartella `app/` contiene il codice sorgente vero e proprio, organizzato in moduli distinti.

### 🛠️ Inizializzazione e Configurazione Interna

* **`app/__init__.py` (Application Factory):**
    * Inizializza Flask, configura le estensioni (DB) e registra i **Blueprint** (`main`, `progetti`, `risorse`).
* **`app/config_modelli.py`:**
    * Contiene costanti di business, come il dizionario `BEST_PRACTICE` usato per pre-compilare i template dei progetti (es. percentuali standard per "Sviluppo Software").

### 🧠 Business Logic Layer (`app/logic/`)

* **`app/logic/engine.py` (Motore):**
    * Implementa l'algoritmo *greedy* di allocazione risorse.
    * Contiene funzioni di utilità come `is_giorno_lavorativo` (usando la libreria `holidays`) e il calcolo della capacità lavorativa netta.
* **`app/logic/services.py` (Service Layer):**
    * Agisce da ponte tra il Database e il Motore.
    * `ServiceProgetti`: Recupera i dati dal DB, lancia il motore di calcolo e prepara i risultati unificati per la visualizzazione.
    * `ServiceCalendario`: Genera i dati JSON per le API del calendario (eventi e festività).

### 💾 Data Layer (`app/models/`)

* **`app/models/database.py` (ORM):**
    * Definisce le tabelle SQL (`RisorsaDB`, `ProgettoDB`, `AssenzaDB`) usando SQLAlchemy. Gestisce le relazioni (es. Risorsa -> Assenze).
* **`app/models/entities.py` (Domain Entities):**
    * Definisce classi Python pure (`Risorsa`, `Progetto`) usate dall'engine per i calcoli in memoria, disaccoppiando la logica dalla persistenza.
* **`app/models/__init__.py`:**
    * Espone i modelli per un'importazione pulita.

### 🌐 Controllers (`app/routes/`)

I Blueprint gestiscono le richieste HTTP e coordinano la risposta.

* **`app/routes/main.py`:**
    * Gestisce la Home Page, la pagina Calendario e le API JSON (`/api/eventi_calendario`) per FullCalendar.
* **`app/routes/progetti.py`:**
    * Gestisce il CRUD dei Progetti: Dashboard, Creazione, Modifica, Cambio Stato (Sospeso/Attivo).
* **`app/routes/risorse.py`:**
    * Gestisce il CRUD delle Risorse e delle Assenze. Include validazione per evitare sovrapposizioni o errori logici.

### 🎨 Presentation Layer (`app/templates/` & `app/static/`)

* **Templates (Jinja2):**
    * `base.html`: Layout master.
    * `progetti.html`: Dashboard principale interattiva.
    * `risorse.html`: Vista carico risorse.
    * `calendario.html`: Wrapper per il calendario grafico.
* **Static:**
    * `style.css`: Stili personalizzati per l'interfaccia utente.