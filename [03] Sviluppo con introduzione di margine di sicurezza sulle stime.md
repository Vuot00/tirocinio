# Introduzione del margine di sicurezza nelle stime

# 1. Funzionamento del sistema senza margine

Il sistema originale:

* conosce in anticipo per ogni progetto:

  * data di consegna,
  * ore richieste,
  * numero massimo di risorse (vincolo di budget),
* conosce per ogni risorsa:

  * disponibilità totale,
  * ore già assegnate,
  * assenze e ferie.

Il processo:

1. I progetti vengono ordinati in base alla scadenza (prima quelli più urgenti).
2. Per ciascun progetto si assegnano risorse con maggiore disponibilità residua.
3. Se non ci sono abbastanza ore disponibili:

   * il progetto viene dichiarato non fattibile,
   * il sistema si ferma senza riassegnazioni.

Questo modello è **deterministico e stabile**, con soli due scenari critici inevitabili:

* mancanza reale di risorse,
* stime iniziali errate.

---

# 2. Introduzione del margine di sicurezza

## 2.1 Come viene applicato

Si modifica il calcolo delle ore richieste:

```
ore_effettive = ore_stimate × (1 + margine_sicurezza)
```

Esempio:

* Ore stimate: 120
* Margine: 20%

```
120 × 1.2 = 144 ore
```

Le ore effettive con margine sostituiscono le stime nella pianificazione.

---

## 2.2 Dove si inserisce nel processo

La pipeline aggiornata è:

```
Input progetto →
Applicazione del margine →
Allocazione risorse →
Verifica fattibilità →
Output piano
```

Nulla cambia nelle altre fasi.

---

# 3. Vantaggi dell’introduzione del margine

* Riduce il rischio che un progetto finisca corto di ore.
* Copre errori di stima, ritardi imprevisti e imprecisioni.
* Aumenta la probabilità che il progetto sia completato nei tempi.

---

# 4. Nuovi scenari critici introdotti

L’introduzione del margine elimina il rischio di sottostima, ma genera **nuovi scenari critici**:

---

## 4.1 Progetti dichiarati non fattibili pur essendo fattibili

A causa del margine:

* cresce il fabbisogno teorico di ore,
* il sistema potrebbe bloccare progetti che in realtà sarebbero eseguibili.

Questo genera **falsi negativi**.

---

## 4.2 Meno progetti eseguibili con lo stesso budget

Il margine aumenta:

* ore richieste dai progetti,
* uso delle risorse.

A parità di capacità:

* meno progetti possono essere accettati,
* aumenta la probabilità di rigetto.

---

## 4.3 Penalizzazione dei progetti con scadenza lontana

Poiché il sistema pianifica in ordine di scadenza:

* i primi progetti assorbono più ore (grazie al margine),
* i progetti con consegna più distante trovano disponibilità ridotta.

---

## 4.4 Inefficienza se il margine è troppo elevato

Se il margine è:

* troppo conservativo,
* applicato indiscriminatamente,

il risultato può essere:

* risorse sottoutilizzate,
* minor produttività complessiva.

---

## 4.5 Margine uniforme non adatto a tutti i tipi di lavoro

Se si applica lo stesso margine a:

* attività ripetitive e consolidate,
* attività incerte e ad alto rischio,

il modello diventa **poco accurato**.

Soluzione futura: margini differenziati per tipologia o complessità.

---

# 5. In sintesi

## Prima

* Sistema stabile.
* Pochi scenari critici.
* Rischio principale: sottostima delle ore reali.

## Dopo l’introduzione del margine

### Vantaggi

* Ridotto rischio di mancanza ore durante l’esecuzione.

### Nuovi rischi

1. Progetti giudicati non fattibili anche se lo sono.
2. Meno progetti che rientrano nel budget.
3. Progetti con scadenza lontana penalizzati.
4. Rischio di inefficienza per margine troppo alto.
5. Margine uniforme può essere poco accurato.

---

# Conclusione

L’introduzione del margine:

* migliora la sicurezza operativa,
* riduce uno dei principali rischi,
* ma rende il sistema più conservativo,
* e introduce nuovi scenari critici legati alla sovrastima.

È un compromesso classico nei sistemi di pianificazione:

> meno rischio di sorpresa → più rischio di inefficienza.
