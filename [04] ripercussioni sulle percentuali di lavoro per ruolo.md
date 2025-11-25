# Effetti del Margine di Sicurezza sulle Percentuali di Ore per Ruolo

## Scenario di partenza

La pianificazione di un progetto può prevedere un totale di **200 ore assegnate a priori**, da distribuire tra diversi ruoli, ad esempio:

| Ruolo           | % allocazione | Ore |
| --------------- | ------------- | --- |
| Project Manager | 10%           | 20  |
| Sviluppatore    | 60%           | 120 |
| Tester          | 30%           | 60  |

Totale: **200 ore**

In questo scenario, le percentuali nascono direttamente sul totale definito.

---

## Introduzione del margine di sicurezza

Se si applica, ad esempio, un **margine del 10%**, le ore del progetto rimangono ufficialmente:

```
Ore progetto totali = 200
```

ma il sistema assegna solo:

```
Ore pianificabili = 200 × 0.9 = 180
```

### Ore ricalcolate mantenendo le stesse percentuali

| Ruolo           | % allocazione | Ore pianificate |
| --------------- | ------------- | --------------- |
| Project Manager | 10%           | 18              |
| Sviluppatore    | 60%           | 108             |
| Tester          | 30%           | 54              |

Totale pianificato: **180 ore**

Le **20 ore mancanti** diventano **buffer interno** per assorbire imprevisti.

---

## Come cambiano le percentuali

### Percentuali interne al piano

Le percentuali tra i ruoli possono **rimanere le stesse** (10%, 60%, 30), quindi:

* la logica di distribuzione non cambia,
* il sistema semplicemente pianifica meno ore.

### Percentuali sul totale progetto

Calcolate ora su 200 ore, risultano più basse:

* Il PM passa da 10% → 9% reale sul totale.
* Il Dev da 60% → 54%.
* Il Tester da 30% → 27%.

Quindi il margine abbassa automaticamente la quota reale di tempo assegnata rispetto al totale dichiarato.

---

## Effetti se i ruoli hanno priorità diverse

Se il margine viene applicato solo ai ruoli considerati meno critici, ad esempio:

* Sviluppatore rimane a 120 ore,
* Tester scende da 60 a 40,

otteniamo:

| Ruolo        | Ore |
| ------------ | --- |
| Sviluppatore | 120 |
| Tester       | 40  |

Totale = 160 ore pianificate

Le percentuali rispetto al nuovo totale cambiano:

| Ruolo        | % reale |
| ------------ | ------- |
| Sviluppatore | 75%     |
| Tester       | 25%     |

Il margine quindi può anche **spostare l'equilibrio tra ruoli**, riflettendo le priorità reali.

---

## Effetti operativi

### 1. Riduzione del rischio di sovraccarico

Pianificando meno del 100% dell’impegno teorico:

* il sistema lascia spazio a ritardi,
* eventuali imprevisti vengono assorbiti internamente,
* si riduce la probabilità di “collisione” tra progetti.

### 2. Il rischio non scompare, ma diventa controllabile

Il sovraccarico può comunque verificarsi se:

* troppi progetti sono attivi contemporaneamente,
* il margine è troppo piccolo,
* le stime iniziali sono troppo ottimistiche,
* mancano risorse perché il budget non permette di aggiungerne.

La differenza è che:

* con il margine ci si accorge dei problemi prima,
* il PM può intervenire in tempo.

### 3. Possibili riallocazioni automatiche

Se un ruolo, sottratti gli imprevisti, scende sotto soglie minime:

* il sistema può generare alert,
* proporre nuove assegnazioni,
* chiedere nuove risorse,
* o ripianificare le percentuali.

---

## Conclusione

Introdurre un margine di sicurezza:

* **non cambia le ore totali del progetto**,
* **riduce quelle pianificabili**,
* **modifica automaticamente le percentuali reali dei ruoli**,
* rende la pianificazione più stabile e realistica.

In sintesi:

> Il margine non crea ore extra: riduce la capacità pianificata per evitare sovraccarichi futuri, mantenendo le percentuali operative interne ma abbassando quelle reali sul totale progetto.
