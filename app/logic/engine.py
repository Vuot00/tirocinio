from datetime import timedelta
import holidays

TOLLERANZA_ERRORE_FLOAT = 0.5
MIN_ORE_ASSEGNABILI = 0.1
it_holidays = holidays.IT()

# --- NUOVE FUNZIONI PER GESTIONE DATE E FESTIVITÀ ---

def is_giorno_lavorativo(data_check):
    """
    Restituisce True se è un giorno lavorativo (Lun-Ven e NON festivo).
    """
    # 1. Controllo Weekend (0=Lun, 5=Sab, 6=Dom)
    if data_check.weekday() >= 5: 
        return False
    
    # 2. Controllo Festività Nazionale (libreria holidays)
    if data_check in it_holidays:
        return False
        
    return True

def calcola_ore_lavorative_tra_date(inizio, fine, ore_giornaliere=8):
    """
    Conta le ore lavorative effettive tra due date, saltando feste e weekend.
    """
    ore_totali = 0
    giorno_corrente = inizio
    
    while giorno_corrente <= fine:
        if is_giorno_lavorativo(giorno_corrente):
            ore_totali += ore_giornaliere
        giorno_corrente += timedelta(days=1)
        
    return ore_totali

# --- FINE NUOVE FUNZIONI ---

def ordina_progetti(lista_progetti):
    """
    1. Priorità (1 vince su 5)
    2. ID (A parità di priorità, il vecchio vince sul nuovo)
    """
    return sorted(lista_progetti, key=lambda p: (p.priorita, p.id or 999999))

def calcola_fattore_pianificazione(margine_percentuale):
    return 1 - (margine_percentuale / 100)

def assegna_risorse(progetti, risorse):
    # Nota: Lavoriamo solo sui progetti che l'utente ha segnato come attivi
    progetti_attivi = [p for p in progetti if p.stato_db in ['In svolgimento', 'Pianificato']]    
    progetti_ordinati = ordina_progetti(progetti_attivi)
    
    print(f"--- 🚀 Calcolo Live su {len(progetti_ordinati)} progetti attivi ---")

    for progetto in progetti_ordinati:
        fattore_pianificazione = calcola_fattore_pianificazione(progetto.margine_percentuale)
        progetto_completamente_coperto = True
        
        # 1. Calcolo ore lavorative del calendario (escluso feste/weekend)
        max_ore_lavorabili_periodo = calcola_ore_lavorative_tra_date(progetto.data_inizio, progetto.data_consegna)

        # --- BLOCCO ROSSO: IMPOSSIBILITÀ CALENDARIO (⛔) ---
        # Scatta se il periodo selezionato è vuoto 
        if max_ore_lavorabili_periodo <= 0:
            progetto.fattibile = False
            progetto.note_errore = "⛔ PERIODO VUOTO: Nessun giorno lavorativo utile tra le date scelte."
            print(f"   -> {progetto.note_errore}")
            continue 

        # --- BLOCCO GIALLO: EROSIONE MARGINE / ALTA DENSITÀ (⚠️) ---
        # Verifichiamo se il totale ore richieste "ci sta" comodamente nel periodo,
        # rispettando il cuscinetto (buffer) imposto dal margine.
        
        # Es: Se il periodo offre 100h e il margine è 20%, la "Soglia Sicura" è 80h.
        fattore_pianificazione = calcola_fattore_pianificazione(progetto.margine_percentuale)
        soglia_sicura_periodo = max_ore_lavorabili_periodo * fattore_pianificazione
        
        if progetto.ore_totali_richieste > soglia_sicura_periodo:
             progetto.warning_messaggio = (
                 f"⚠️ RISCHIO TEMPI: Richieste {progetto.ore_totali_richieste}h su {int(max_ore_lavorabili_periodo)}h disponibili. "
                 f"Stai erodendo il buffer di sicurezza del {progetto.margine_percentuale}% "
                 f"(Soglia sicura: {int(soglia_sicura_periodo)}h)."
             )
             print(f"   -> {progetto.warning_messaggio}")
        
        
        for skill_richiesta, skill_data in progetto.requisiti.items():
            qty_necessaria = skill_data['qty']
            percentuale_carico = skill_data['perc']
            ore_target_ruolo = progetto.ore_totali_richieste * (percentuale_carico / 100)
            ore_ancora_da_coprire = ore_target_ruolo
            
            candidati = [r for r in risorse if r.skill == skill_richiesta]
            # Ordiniamo per chi ha più ore, per non frammentare troppo
            candidati.sort(key=lambda r: r.ore_residue, reverse=True)
            
            persone_trovate = 0

            for risorsa in candidati:
                if ore_ancora_da_coprire <= 0: break
                
                persone_mancanti = qty_necessaria - persone_trovate
                if persone_mancanti < 1: persone_mancanti = 1 
                
                fabbisogno_scontato_rimanente = ore_ancora_da_coprire * fattore_pianificazione
                quota_massima_per_persona = fabbisogno_scontato_rimanente / persone_mancanti
                
                if risorsa.ore_residue <= 0: continue

                ore_da_impegnare = min(quota_massima_per_persona, risorsa.ore_residue)
                ore_da_impegnare = round(ore_da_impegnare, 2)
                
                if ore_da_impegnare <= MIN_ORE_ASSEGNABILI: continue

                risorsa.assegna_ore(ore_da_impegnare)
                
                if fattore_pianificazione > 0:
                    progresso_reale = ore_da_impegnare / fattore_pianificazione
                else:
                    progresso_reale = ore_da_impegnare

                ore_ancora_da_coprire -= progresso_reale
                
                # Salviamo i dettagli per disegnare la barra specifica di questo progetto
                progetto.assegnazioni_dettagliate.append({
                    'nome_risorsa': risorsa.nome,
                    'skill': risorsa.skill,
                    'ore_su_questo_progetto': ore_da_impegnare,
                    'ore_totali_risorsa': risorsa.ore_totali_disponibili, 
                    'ore_nette_risorsa': (risorsa.ore_totali_disponibili - risorsa.ore_assenze)
                })
                
                persone_trovate += 1

            if ore_ancora_da_coprire > TOLLERANZA_ERRORE_FLOAT:
                progetto_completamente_coperto = False
            elif persone_trovate < qty_necessaria:
                progetto_completamente_coperto = False
        
        if not progetto_completamente_coperto:
            progetto.fattibile = False
        else:
            progetto.fattibile = True