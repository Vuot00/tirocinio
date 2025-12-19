from app.models import Risorsa, Progetto
from app.logic import engine
from datetime import date

def test_assegnazione_semplice():
    """Testa se il motore assegna le risorse quando c'è disponibilità."""
    # Dati Finti (Logici)
    mario = Risorsa("Mario", "Developer", 100)
    team = [mario]
    
    reqs = {'Developer': {'qty': 1, 'perc': 100}}
    
    # Progetto di 40 ore su 5 giorni lavorativi (8h/giorno)
    # È fattibile.
    p = Progetto(
        nome="Test Motore", 
        priorita=1, 
        data_inizio=date(2025,1,1), 
        data_consegna=date(2025,1,10), 
        ore_stimate=40, 
        margine_percentuale=0, 
        requisiti=reqs
    )
    
    # Lancia il motore
    engine.assegna_risorse([p], team)
    
    # Verifiche
    assert p.fattibile == True
    assert mario.ore_impegnate == 40
    assert mario.ore_residue == 60

def test_risorse_insufficienti():
    """Testa che il motore segni NON fattibile se mancano ore."""
    mario = Risorsa("Mario", "Developer", 10) # Ha solo 10 ore
    team = [mario]
    
    reqs = {'Developer': {'qty': 1, 'perc': 100}}
    p = Progetto(
        nome="Progetto Pesante", 
        priorita=1, 
        data_inizio=date(2025,1,1), 
        data_consegna=date(2025,1,10), 
        ore_stimate=100, # Ne servono 100
        margine_percentuale=0, 
        requisiti=reqs
    )
    
    engine.assegna_risorse([p], team)
    
    assert p.fattibile == False