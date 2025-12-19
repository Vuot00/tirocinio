from app.models import Risorsa, Progetto
from datetime import date, datetime

def test_creazione_progetto_logico():
    """Testa l'inizializzazione della classe Progetto."""
    p = Progetto(
        nome="Unit Test", 
        priorita=1,
        data_inizio="2025-01-01", # Passiamo stringa, deve convertirla
        data_consegna="2025-01-10",
        ore_stimate=100, 
        margine_percentuale=10, 
        requisiti={}
    )
    assert p.nome == "Unit Test"
    # Verifica che la conversione data abbia funzionato
    assert isinstance(p.data_inizio, (date, datetime))

def test_calcolo_ore_residue_risorsa():
    """Testa matematica semplice della risorsa."""
    r = Risorsa("TestUser", "Dev", 100)
    assert r.ore_residue == 100
    
    r.assegna_ore(25.5)
    assert r.ore_residue == 74.5
    assert r.ore_impegnate == 25.5