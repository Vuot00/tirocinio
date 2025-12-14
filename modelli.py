from datetime import datetime, date
from typing import Dict, Union, Any

class Risorsa:
    def __init__(self, nome: str, skill: str, ore_totali_disponibili: int, ore_assenze: int = 0):
        self.nome = nome
        self.skill = skill
        self.ore_totali_disponibili = ore_totali_disponibili
        self.ore_assenze = ore_assenze
        self.ore_impegnate = 0

    @property
    def ore_residue(self) -> float:
        return self.ore_totali_disponibili - self.ore_impegnate - self.ore_assenze

    def assegna_ore(self, ore: float):
        self.ore_impegnate += ore

    def __repr__(self):
        return f"[{self.skill}] {self.nome}"


class Progetto:
    def __init__(
        self, 
        nome: str, 
        priorita: int, 
        data_inizio: Union[str, date, datetime],    
        data_consegna: Union[str, date, datetime], 
        ore_stimate: int, 
        margine_percentuale: int, 
        requisiti: Dict[str, Any], 
        id: int = None, 
        stato_db: str = 'In svolgimento'
    ):
        self.id = id
        self.nome = nome
        self.priorita = priorita
        
        # Normalizziamo entrambe le date
        self.data_inizio = self._normalizza_data(data_inizio)      
        self.data_consegna = self._normalizza_data(data_consegna)
        
        self.requisiti = requisiti
        self.ore_totali_richieste = ore_stimate
        self.margine_percentuale = margine_percentuale
        self.stato_db = stato_db
        
        self.ore_ancora_da_coprire = self.ore_totali_richieste
        self.assegnazioni_dettagliate = [] 
        self.fattibile = True

    @staticmethod
    def _normalizza_data(valore_data) -> datetime:
        if isinstance(valore_data, str):
            try:
                return datetime.strptime(valore_data, "%Y-%m-%d")
            except ValueError:
                return datetime.max
        elif isinstance(valore_data, (date, datetime)):
            return valore_data
        else:
            return datetime.max

    def __repr__(self):
        return f"Progetto: {self.nome}"