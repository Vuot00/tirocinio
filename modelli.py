from datetime import datetime, date
from typing import Dict, Union, Any

class Risorsa:
    """
    Rappresenta una persona o un asset disponibile a lavorare.
    Gestisce il monte ore totale, le assenze e il calcolo del residuo.
    """
    def __init__(self, nome: str, skill: str, ore_totali_disponibili: int, ore_assenze: int = 0):
        self.nome = nome
        self.skill = skill
        self.ore_totali_disponibili = ore_totali_disponibili
        self.ore_assenze = ore_assenze
        self.ore_impegnate = 0  # Contatore che avanza durante la pianificazione

    @property
    def ore_residue(self) -> float:
        """
        Calcola dinamicamente le ore ancora disponibili.
        Formula: Totale - Impegnate - Assenze.
        """
        return self.ore_totali_disponibili - self.ore_impegnate - self.ore_assenze

    def assegna_ore(self, ore: float):
        """Aggiunge ore al carico di lavoro della risorsa."""
        self.ore_impegnate += ore

    def __repr__(self):
        return f"[{self.skill}] {self.nome} (Residuo: {self.ore_residue}h)"


class Progetto:
    """
    Rappresenta un progetto da pianificare.
    Gestisce i requisiti del team e lo stato di avanzamento della copertura.
    """
    def __init__(
        self, 
        nome: str, 
        priorita: int, 
        data_consegna: Union[str, date, datetime], 
        ore_stimate: int, 
        margine_percentuale: int, 
        requisiti: Dict[str, Any]
    ):
        self.nome = nome
        self.priorita = priorita
        
        # Normalizzazione della data (delegata a metodo statico per pulizia)
        self.data_consegna = self._normalizza_data(data_consegna)

        # Requisiti del team
        # Formato atteso: {'Developer': {'qty': 2, 'perc': 20}, ...}
        self.requisiti = requisiti
        
        # Dati economici/temporali
        self.ore_totali_richieste = ore_stimate
        self.margine_percentuale = margine_percentuale
        
        # Variabili di Stato (mutabili durante il calcolo)
        self.ore_ancora_da_coprire = self.ore_totali_richieste
        self.risorse_assegnate = []
        self.fattibile = True

    @staticmethod
    def _normalizza_data(valore_data) -> datetime:
        """
        Converte l'input in un oggetto datetime valido.
        Accetta stringhe ("YYYY-MM-DD") o oggetti date/datetime.
        Restituisce datetime.max in caso di errore per evitare crash nel sorting.
        """
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
        return f"Progetto: {self.nome} (P{self.priorita})"