# Impatto del Margine di Sicurezza sulle Ore e sul Carico delle Risorse

## Le 8 Ore Giornaliere non Vengono Intaccate

L’introduzione di un margine di sicurezza nelle stime **non modifica le ore lavorative reali della risorsa**.  
Se una risorsa lavora:

- **8 ore al giorno**
- **40 ore a settimana**

queste rimangono tali.

Il margine di sicurezza non modifica l’orario lavorativo, ma **la quantità di lavoro che viene effettivamente pianificata nel sistema**.

---

## Come Funziona

Se normalmente pianifichi:

- 8 ore al giorno → 100% del carico massimo

con il margine di sicurezza puoi decidere che:

- nel planner ne consideri solo 6–7
- lasciando 1–2 ore libere per margini, imprevisti o assorbimento di errori di stima

### In sintesi:

| Tipo di ora | Valore |
|---|---|
| Ore lavorabili reali | **8h/die** |
| Ore pianificate dopo margine | **es. 6–7h/die** |

---

## Perché Questo Non Sovraccarica?

Perché:

- **non stai aggiungendo lavoro**
- **stai riducendo la quantità pianificata**
- **stai mitigando il rischio di straordinari reali**

Il margine funziona come un “cuscinetto operativo”.

---

## Esempio

### Prima

- Pianificazione: 8h al giorno  
- Carico reale: qualsiasi imprevisto rischia di far sforare e causare straordinari

### Dopo

- Pianificazione: 6.4h al giorno (80%)  
- Ore libere: 1.6h  
- Un imprevisto si assorbe senza superare le 8h reali

---

## Effetto sulle Percentuali di Carico

Applicando il margine:

- il carico pianificato per ruolo si riduce
- le percentuali impegnate formalmente scendono

Esempio:

| Ruolo | Prima | Dopo |
|---|---|---|
| Analista | 100% | 80% |
| Sviluppatore | 100% | 85% |
| Tester | 100% | 75% |

Questo comporta:

- maggior spazio per assorbire imprevisti
- meno rischi di sovraccarico
- riduzione di straordinari e ritardi

---

## Conclusione

- Il margine **non riduce le ore lavorate**, ma **riduce quelle pianificate**.
- Le 8 ore giornaliere restano invariate.
- È una tecnica utile per:

  - mitigare pianificazioni ottimistiche  
  - mantenere un margine operativo realistico  
  - evitare sovraccarichi imprevisti

