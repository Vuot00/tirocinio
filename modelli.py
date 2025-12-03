from datetime import datetime, date

class Risorsa:
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
    # NOTA: Qui abbiamo tolto 'skill_richiesta' e 'max_risorse' 
    # e messo 'requisiti'
    def __init__(self, nome, priorita, data_consegna, ore_stimate, margine_percentuale, requisiti):
        self.nome = nome
        self.priorita = priorita
        
        # Gestione Data (Stringa o Oggetto)
        if isinstance(data_consegna, str):
            try:
                self.data_consegna = datetime.strptime(data_consegna, "%Y-%m-%d")
            except ValueError:
                self.data_consegna = datetime.max
        elif isinstance(data_consegna, (date, datetime)):
            self.data_consegna = data_consegna
        else:
            self.data_consegna = datetime.max

        # NUOVO: Requisiti è un dizionario {'Skill': quantita}
        # Es: {'Developer': 2, 'Tester': 1}
        self.requisiti = requisiti
        
        self.ore_totali_richieste = ore_stimate
        self.margine_percentuale = margine_percentuale
        
        self.ore_ancora_da_coprire = self.ore_totali_richieste
        self.risorse_assegnate = []
        self.fattibile = True
        
    def __repr__(self):
        return f"Progetto: {self.nome}"