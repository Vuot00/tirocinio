from modelli import Risorsa, Progetto

# ==============================================================================
# ⚙️ CONFIGURAZIONE E COSTANTI
# ==============================================================================
TOLLERANZA_ERRORE_FLOAT = 0.5  # Tolleranza per arrotondamenti (ore)
MIN_ORE_ASSEGNABILI = 0.1      # Minimo blocco di tempo assegnabile

def ordina_progetti(lista_progetti):
    """
    Ordina i progetti per Priorità (1=Alta) e poi per Data di Consegna.
    """
    return sorted(lista_progetti, key=lambda p: (p.priorita, p.data_consegna))

def calcola_fattore_pianificazione(margine_percentuale):
    """
    Restituisce il moltiplicatore per il Buffer Interno.
    Es. Margine 10% -> Fattore 0.9 (Pianifichiamo solo il 90% delle ore disponibili)
    """
    return 1 - (margine_percentuale / 100)

# ==============================================================================
# 🧠 ALGORITMO DI ASSEGNAZIONE
# ==============================================================================
def assegna_risorse(progetti, risorse):
    
    progetti_ordinati = ordina_progetti(progetti)
    print(f"--- 🚀 Avvio Pianificazione Deterministica (Load Balancing attivo) ---")

    for progetto in progetti_ordinati:
        print(f"\n🔹 [P{progetto.priorita}] {progetto.nome} (Totale Richiesto: {progetto.ore_totali_richieste}h)")
        
        # 1. Calcolo Buffer Interno per questo progetto
        fattore_pianificazione = calcola_fattore_pianificazione(progetto.margine_percentuale)
        progetto_completamente_coperto = True
        
        # 2. Iterazione sui Ruoli (Skills)
        for skill_richiesta, skill_data in progetto.requisiti.items():
            
            # Estrazione dati requisito
            qty_necessaria = skill_data['qty']
            percentuale_carico = skill_data['perc']
            
            # Calcolo ore dedicate a questo specifico ruolo
            ore_target_ruolo = progetto.ore_totali_richieste * (percentuale_carico / 100)
            ore_ancora_da_coprire = ore_target_ruolo
            
            print(f"   🔎 Ruolo {skill_richiesta}: {percentuale_carico}% del tot -> Servono {ore_target_ruolo}h (Min {qty_necessaria} persone)")

            # 3. Selezione Candidati
            # Filtriamo chi ha la skill e ordiniamo per chi è più scarico (maggior residuo)
            candidati = [r for r in risorse if r.skill == skill_richiesta]
            candidati.sort(key=lambda r: r.ore_residue, reverse=True)

            persone_trovate = 0

            # 4. Assegnazione (Ciclo Greedy con Load Balancing)
            for risorsa in candidati:
                # Condizioni di uscita
                if ore_ancora_da_coprire <= 0: break
                
                # --- LOGICA LOAD BALANCING ---
                # Quante persone mancano per raggiungere il quorum?
                persone_mancanti = qty_necessaria - persone_trovate
                if persone_mancanti < 1: persone_mancanti = 1 
                
                # Calcoliamo il fabbisogno "Scontato" (Buffer Interno)
                # È la quantità di spazio che vogliamo occupare sul calendario della risorsa
                fabbisogno_scontato_rimanente = ore_ancora_da_coprire * fattore_pianificazione
                
                # Dividiamo il carico rimanente per le persone che mancano
                # Questo evita che il primo prenda tutto il lavoro
                quota_massima_per_persona = fabbisogno_scontato_rimanente / persone_mancanti
                
                # Verifica disponibilità risorsa
                if risorsa.ore_residue <= 0: continue

                # Decidiamo quanto assegnare:
                # Non più della quota calcolata E non più di quanto la risorsa ha libero
                ore_da_impegnare = min(quota_massima_per_persona, risorsa.ore_residue)
                ore_da_impegnare = round(ore_da_impegnare, 2)
                
                if ore_da_impegnare <= MIN_ORE_ASSEGNABILI: continue

                # --- APPLICAZIONE ---
                # 1. Scaliamo le ore dal calendario della risorsa (ore "scontate")
                risorsa.assegna_ore(ore_da_impegnare)
                
                # 2. Calcoliamo quanto progresso REALE abbiamo fatto sul progetto
                # (Dobbiamo "rigonfiare" le ore per tornare al valore di progetto)
                if fattore_pianificazione > 0:
                    progresso_reale = ore_da_impegnare / fattore_pianificazione
                else:
                    progresso_reale = ore_da_impegnare

                ore_ancora_da_coprire -= progresso_reale
                progetto.risorse_assegnate.append(risorsa)
                persone_trovate += 1
                
                print(f"      ✅ {risorsa.nome}: Impegna {ore_da_impegnare}h (Copre {round(progresso_reale, 1)}h reali)")

            # 5. Verifica Esito per questo Ruolo
            if ore_ancora_da_coprire > TOLLERANZA_ERRORE_FLOAT:
                print(f"      ⚠️  Mancano {round(ore_ancora_da_coprire, 1)}h per il ruolo {skill_richiesta}")
                progetto_completamente_coperto = False
            elif persone_trovate < qty_necessaria:
                print(f"      ⚠️  Team sottodimensionato per {skill_richiesta} (Trovati {persone_trovate}/{qty_necessaria})")
                progetto_completamente_coperto = False
        
        # 6. Verifica Finale Progetto
        if not progetto_completamente_coperto:
            progetto.fattibile = False
            print("   ⛔ NON FATTIBILE: Risorse insufficienti o requisiti non soddisfatti.")
        else:
            progetto.fattibile = True
            print("   ✨ Progetto Completamente Coperto!")