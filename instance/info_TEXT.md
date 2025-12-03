# 🗄️ Architettura del Database (`pianificatore.db`)

## 1. Panoramica Tecnica
pianificatore.db è il file di database (in formato SQLite) che funge
da memoria permanente del tuo programma.

Al suo interno sono salvate fisicamente tutte le tabelle con i dati che hai inserito (Anagrafica Risorse, Dettagli Progetti, Calendario Assenze), permettendo al software di ritrovarli e rileggerli ogni volta che lo riavvii, esattamente come un documento Word o Excel salva il tuo lavoro sul disco rigido affinché non vada perso.

* **Tecnologia:** SQLite 3
* **Interfaccia (ORM):** SQLAlchemy (tramite `db_manager.py`)
* **Posizione:** Root del progetto
* **Portabilità:** Il file può essere copiato, spostato o inviato via email mantenendo tutti i dati integri.

---

## 2. Astrazione vs Concretezza
Il sistema utilizza un approccio **ORM (Object-Relational Mapping)** per separare il codice Python dalla gestione SQL diretta.

### A. Livello Astratto (Codice Python)
Nel file `db_manager.py`, lavoriamo con **Classi e Oggetti**:
```python
# Tu scrivi questo nel codice:
nuova_risorsa = RisorsaDB(nome="Mario", skill="Developer")
db.session.add(nuova_risorsa)
# Il sistema esegue questo dietro le quinte:
INSERT INTO risorsa_db (nome, skill) VALUES ('Mario', 'Developer')
```

---

## 3. Schema delle Tabelle (Schema ER)
Il database è composto da 3 tabelle principali collegate tra loro.
* Risorsa 👨‍💻
* Assenza 🏖️
* Progetto 🗺️

---

## 4. Flusso dei Dati
1. **Input**: L'utente inserisce i dati via Web.
2. **Controller** (```app.py```): Riceve i dati e istanzia oggetti ```RisorsaDB```o ```ProgettoDB```.
3. **ORM** (```db_manager.py```): Esegue il salvataggio scrivendo le modifiche sul file ```pianificatore.db```
4. **Lettura e Calcolo**: quando si clicca su elabora piano
    * Il sistema legge le righe dal DB.
    * Le converte in "Oggetti Logici Puri" (modelli.py), calcolando al volo le ore perse per ferie.
    * Le passa al motore.py per l'elaborazione dell'algoritmo.
