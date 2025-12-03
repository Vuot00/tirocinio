from modelli import Risorsa, Progetto

def ordina_progetti(lista_progetti):
    return sorted(lista_progetti, key=lambda p: (p.priorita, p.data_consegna))

def assegna_risorse(progetti, risorse):
    
    progetti_ordinati = ordina_progetti(progetti)
    print(f"--- Pianificazione Bilanciata per {len(progetti)} progetti ---")

    for progetto in progetti_ordinati:
        print(f"\n🔹 [P{progetto.priorita}] {progetto.nome} (Scad: {progetto.data_consegna})")
        
        # Fattore 0.9 se margine è 10% (buffer interno)
        fattore_pianificazione = 1 - (progetto.margine_percentuale / 100)
        
        progetto_completamente_coperto = True

        for skill_richiesta, quantita_necessaria in progetto.requisiti.items():
            
            persone_trovate = 0
            
            candidati = [r for r in risorse if r.skill == skill_richiesta]
            candidati.sort(key=lambda r: r.ore_residue, reverse=True)

            print(f"   🔎 Cerco {quantita_necessaria} x {skill_richiesta}...")

            for risorsa in candidati:
                # Se abbiamo trovato tutti per questa skill, stop.
                if persone_trovate >= quantita_necessaria: break
                
                # Se le ore sono finite, stop.
                if progetto.ore_ancora_da_coprire <= 0: break

                # --- NOVITÀ: CALCOLO DISTRIBUITO ---
                # Quante persone mancano ancora da trovare (inclusa questa)?
                persone_mancanti = quantita_necessaria - persone_trovate
                
                # Calcoliamo il fabbisogno totale SCONTATO
                fabbisogno_reale = progetto.ore_ancora_da_coprire
                fabbisogno_scontato_totale = fabbisogno_reale * fattore_pianificazione
                
                # Dividiamo la torta: Ognuno prende una fetta uguale in base a quanti mancano
                # Es. 40 ore, 2 persone -> Tetto max 20 ore a testa.
                quota_massima_per_persona = fabbisogno_scontato_totale / persone_mancanti
                
                # Verifica: La risorsa ha spazio almeno per un po' di lavoro?
                # Nota: qui siamo più flessibili, se ha spazio lo usiamo fino alla quota.
                if risorsa.ore_residue <= 0:
                    continue 

                # ASSEGNAZIONE
                # Prendiamo il MINIMO tra:
                # 1. La quota che spetta a questa persona (per non rubare lavoro agli altri)
                # 2. Le ore libere della risorsa
                ore_da_impegnare = min(quota_massima_per_persona, risorsa.ore_residue)
                
                # Arrotondiamo per pulizia (evita 19.9999999)
                ore_da_impegnare = round(ore_da_impegnare, 2)
                
                if ore_da_impegnare <= 0: continue

                # Calcoliamo quanto "valgono" queste ore sul progetto reale
                if fattore_pianificazione > 0:
                    progresso_reale = ore_da_impegnare / fattore_pianificazione
                else:
                    progresso_reale = ore_da_impegnare
                
                # Eseguiamo
                risorsa.assegna_ore(ore_da_impegnare)
                progetto.ore_ancora_da_coprire -= progresso_reale
                progetto.risorse_assegnate.append(risorsa)
                persone_trovate += 1
                
                print(f"      ✅ Preso {risorsa.nome}: {ore_da_impegnare}h (Quota max era {round(quota_massima_per_persona,1)}h)")

            if persone_trovate < quantita_necessaria:
                print(f"      ⚠️  Mancano risorse per {skill_richiesta} (Trovati {persone_trovate}/{quantita_necessaria})")
                progetto_completamente_coperto = False
        
        # Tolleranza minima per i float
        if progetto.ore_ancora_da_coprire > 0.1 or not progetto_completamente_coperto:
            progetto.fattibile = False
            print(f"   ⛔ NON FATTIBILE. Ore mancanti: {round(progetto.ore_ancora_da_coprire, 1)}")
        else:
            progetto.fattibile = True
            print("   ✨ Progetto coperto!")