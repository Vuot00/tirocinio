# 🎯 Approfondimento: Assegnazione Ottimale delle Risorse

Nel modello di pianificazione deterministica, il concetto di "ottimalità" è focalizzato sulla **stabilità** e sulla **garanzia di consegna** dei progetti a più alta priorità, evitando le oscillazioni tipiche dei sistemi dinamici.

L'ottimizzazione si raggiunge attraverso due passaggi chiave: l'ordinamento prioritario dei progetti e il criterio di selezione delle risorse.

---

## 1. La Massima Ottimalità (Priorità e Stabilità)

L'algoritmo garantisce la massima probabilità di successo al progetto più urgente, rispettando il principio di determinismo:

* **Ottimalità per la Scadenza:** I progetti sono processati in ordine di scadenza (più vicina ==> priorità più alta). Questo assicura che le risorse vengano allocate in modo da **proteggere per prime le scadenze più critiche**.
* **Stabilità del Piano:** Quando le ore di una risorsa sono assegnate a un progetto prioritario (P1), esse vengono **sottratte permanentemente** dalla disponibilità residua per i progetti meno urgenti (P2, P3). In questo modo, il piano di P1 è stabile e immune da future riassegnazioni o "furti" di risorse da parte di progetti successivi.

## 2. Criterio di Selezione della Risorsa

Dopo aver scelto il progetto più urgente, il sistema seleziona le risorse basandosi su un criterio semplice e trasparente: **risorse con maggiore disponibilità residua** (e che soddisfano eventuali *skill\_richieste*).

| Vantaggio | Spiegazione |
| :--- | :--- |
| **Massimizzazione della Copertura** | Si sfrutta al meglio chi ha più ore libere, **minimizzando** il numero di risorse complessive da coinvolgere per progetto, operando entro il limite massimo imposto dal budget. |
| **Sostenibilità a Lungo Termine** | Evitando di "bruciare" le risorse con poca disponibilità residua, si preservano potenzialmente le risorse uniche o quelle con skill rare per progetti futuri (non ancora processati). |
| **Trasparenza** | Il criterio è oggettivo (`ore_residue`), eliminando la necessità di metriche complesse e soggettive che potrebbero destabilizzare l'accordo tra i team. |

---

## 3. 🏗️ Approfondimento: Algoritmo di Gestione delle Ore

Una volta che il sistema identifica la risorsa ottimale (quella con maggiore disponibilità residua), deve assegnare le ore necessarie. Questo processo di assegnazione si svolge iterativamente:

### A. Calcolo del Fabbisogno Giornaliero
Per ogni progetto, il sistema calcola il fabbisogno medio di ore:

$$\text{Fabbisogno Medio Giornaliero} = \frac{\text{Ore richieste dal progetto}}{\text{Giorni disponibili fino alla consegna}}$$

Questo valore (es. 4 ore/giorno) definisce quante ore al giorno devono essere coperte per completare il progetto in tempo.

### B. Ciclo di Assegnazione (Pseudocodice Dettagliato)

Il sistema assegna le ore giornaliere finché il totale delle ore del progetto è coperto o si raggiunge il limite di risorse.

```pseudocode
// Dati iniziali:
// Progetto P: ore_residuo_progetto, max_risorse_da_budget
// Fabbisogno: ore_richieste_giorno
// Risorsa R: disponibilita_residua_totale

ordina progetti per data_consegna crescente

per ogni progetto P:
    risorse_assegnate_correnti = 0
    ore_residuo_progetto = P.ore_richieste
    
    while ore_residuo_progetto > 0 AND risorse_assegnate_correnti < P.max_risorse_da_budget:
        
        // 1. Seleziona la risorsa (R) migliore
        seleziona R con la maggiore disponibilita_residua_totale E P.skill_richiesta soddisfatta
        
        se R non esiste O limite budget raggiunto:
             progetto P NON fattibile
             richiedi intervento umano
             esci dal loop del progetto
        
        // 2. Determina quante ore assegnare
        ore_da_assegnare = MIN(P.ore_richieste_giorno, R.disponibilita_residua_giornaliera)
        
        // 3. Esegui l'allocazione
        assegna ore_da_assegnare alla risorsa R sul progetto P per ogni giorno del periodo
        
        // 4. Aggiorna i totali
        ore_residuo_progetto -= (ore_da_assegnare * giorni_nel_periodo)
        R.disponibilita_residua_totale -= (ore_da_assegnare * giorni_nel_periodo)
        R.ore_già_assegnate += (ore_da_assegnare * giorni_nel_periodo)
        
        // Solo la prima volta che la risorsa viene allocata:
        if R è stata allocata per la prima volta:
            risorse_assegnate_correnti += 1

```
