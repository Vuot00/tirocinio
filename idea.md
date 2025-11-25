# 🧠 IDEA DI FONDO

Costruiamo un sistema che:

* per ogni progetto conosce a priori:
    * **data di consegna**,
    * **ore richieste**,
    * **numero massimo di risorse disponibili da budget**,
    * eventuali **skill richieste**.
* per ogni risorsa conosce a priori:
    * **disponibilità totale** nel periodo,
    * **ore già occupate** da altri progetti,
    * **ferie**,
    * **assenze** note.

Il sistema deve solo:
* ✔ assegnare risorse in modo ottimale,
* ✔ verificare se si riesce a consegnare il progetto in tempo,
* ✔ **senza riassegnare, spostare, oppure rivalutare in continuo**.

In questo modo abbiamo un modello **deterministico e stabile**.

---

# 🧩 1. Come funzionerebbe passo‐per‐passo

## Fase 1 – Ordinamento dei progetti

I progetti vengono **ordinati una volta sola** in base a un criterio semplice:

> più la scadenza è vicina → **più alta la priorità**

**Esempio:**

| Progetto | Scadenza | Priorità |
| :------- | :------- | :------- |
| P1       | 10 dicembre | 1        |
| P2       | 15 dicembre | 2        |
| P3       | 30 dicembre | 3        |

Niente aggiornamento dinamico.

## Fase 2 – Si processa ogni progetto in ordine

Il sistema prende i progetti uno alla volta, **dal più urgente al meno urgente**.

Per ogni progetto:

1.  **Si calcola il fabbisogno**
    * `Ore richieste dal progetto / giorni disponibili`
    * `= numero medio di ore/giorno`

2.  **Si verificano le risorse disponibili**
    Il motore verifica:
    * **disponibilità residua** della risorsa nel periodo,
    * rispetto delle **ferie/assenze**,
    * carichi già assegnati ad altri progetti **prioritari**.

3.  **Si assegnano le migliori risorse**
    Criterio semplice:
    > risorse con **maggiore disponibilità residua**

    Finché:
    * tutte le ore del progetto sono coperte
    * oppure
    * il numero massimo di risorse da budget è raggiunto.

## Fase 3 – Se l’allocazione non è possibile

Il sistema **non cerca soluzioni complesse**, ma:
* **interrompe** la schedulazione
* registra che il progetto **non è fattibile**
* richiede **intervento umano**.

Niente oscillazioni, niente ricalcoli infiniti.

---

# ⚙️ 2. Perché questo modello elimina la maggior parte dei problemi

Perché dice:

> “Io calcolo la soluzione migliore **UNA VOLTA** e basta.”

Quindi non possono accadere:
* **riassegnazioni continue**,
* progetti che **rubano risorse a vicenda**,
* priorità che **cambiano ogni settimana**,
* soluzioni che si rincorrono.

Il sistema è come una foto scattata in un istante, molto **stabile**.

---

# 📉 3. Quali problemi risolve automaticamente

| Problema reale | Perché non si verifica |
| :------------- | :--------------------- |
| Progetti che si bloccano a catena | I progetti non si influenzano tra loro |
| Continua oscillazione delle priorità | Le priorità sono fisse |
| Ricalcoli e ripianificazioni infinite | Il piano si calcola una sola volta |
| Effetto “sempre le stesse risorse” | Il modello assegna solo fino al limite massimo |
| Disaccordi operativi fra team | Il modello è semplice da leggere e discutere |

---

# 🔢 4. Parametri fondamentali del sistema

Per funzionare, bastano pochi dati:

* **Per ogni progetto:**
    * `data_consegna`
    * `ore_richieste`
    * `max_risorse_da_budget`
    * `eventuale skill_richiesta`
* **Per ogni risorsa:**
    * `ore_totali_disponibili`
    * `ore_già_assegnate`
    * `ferie/permessi`
    * `impegni su altri progetti`

Questi dati **non devono cambiare** durante il calcolo, o il modello perderebbe stabilità.

---

# 🏗️ 5. Schema di implementazione logica

In pseudocodice semplice:

```pseudocode
ordina progetti per data_consegna crescente

per ogni progetto:
    calcola ore_residuo_progetto
    while ore_residuo_progetto > 0:
        seleziona risorsa con maggiore disponibilità residua
        se nessuna risorsa disponibile o limite budget raggiunto ->
             progetto NON fattibile
             esci
        assegna ore giornaliere alla risorsa
        aggiorna disponibilità della risorsa
# ⚠️ 6. Gli unici due scenari critici rimasti
Scenario critico 1 – Risorse insufficienti
Se:


somma ore disponibili < ore richieste
allora il progetto non può essere fatto, punto.
Non è colpa del sistema: è una condizione reale.
Scenario critico 2 – Stime iniziali errate
Se un progetto richiede più ore del previsto:

nessun algoritmo al mondo può salvarlo.
Per attenuare questo, puoi aggiungere:

margine di sicurezza del 10–20% sulle stime,
stima basata su esperienza storica,
complessità parametrica (“se progetto harder → +30%”).
