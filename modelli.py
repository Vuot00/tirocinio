from datetime import datetime

class Risorsa:
    """
    Rappresenta una persona o un team.
    """
    def __init__(self, nome, skill, ore_totali_disponibili):
        self.nome = nome
        self.skill = skill  
        self.ore_totali_disponibili = ore_totali_disponibili
        self.ore_impegnate = 0 

    @property
    def ore_residue(self):
        return self.ore_totali_disponibili - self.ore_impegnate

    def assegna_ore(self, ore):
        self.ore_impegnate += ore

    def __repr__(self):
        return f"[{self.skill}] {self.nome} (Libere: {self.ore_residue}h)"


class Progetto:
    """
    Rappresenta un progetto da pianificare.
    """
    def __init__(self, nome, data_consegna, ore_stimate, margine_percentuale, skill_richiesta, max_risorse):
        self.nome = nome
        
        try:
            self.data_consegna = datetime.strptime(data_consegna, "%Y-%m-%d")
        except ValueError:
            self.data_consegna = datetime.max 

        self.skill_richiesta = skill_richiesta
        self.max_risorse = max_risorse
        
        # --- CORREZIONE: MANTENIAMO I DATI PULITI ---
        # Non gonfiamo più le ore qui.
        self.ore_totali_richieste = ore_stimate 
        
        # Salviamo il margine. Lo userà il MOTORE per calcolare la velocità giornaliera.
        # Es. Se margine è 20%, nel motore useremo solo l'80% della giornata lavorativa.
        self.margine_percentuale = margine_percentuale
        
        self.ore_ancora_da_coprire = self.ore_totali_richieste
        self.risorse_assegnate = [] 
        self.fattibile = True 

    def __repr__(self):
        # Stampa pulita: mostra le ore reali del preventivo
        return (f"Progetto: {self.nome} | Scadenza: {self.data_consegna.date()} | "
                f"Budget Ore: {self.ore_totali_richieste} (Margine Sicurezza: {self.margine_percentuale}%)")

if __name__ == "__main__":
    print("--- TEST VERSIONE CORRETTA (Buffer Temporale) ---")
    p = Progetto("Test App", "2025-10-10", 120, 5, "Dev", 1)
    print(p)
    
    ore_progetto = input("di quante ore necessita il progetto?")
    if p.ore_totali_richieste == ore_progetto: #da modificare se si cambiano nel costruttore
        print("✅ Ottimo. Il progetto richiede", p.ore_totali_richieste, "ore, con un margine del", p.margine_percentuale, "%")
    else:
        print("❌ Errore: Le ore sono state modificate.")