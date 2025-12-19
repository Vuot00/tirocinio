from app.models import db, ProgettoDB, RisorsaDB
from datetime import date

def test_salvataggio_lettura_progetto(app):
    """Testa che si possa salvare e rileggere un progetto."""
    with app.app_context():
        # Creiamo un progetto finto
        p = ProgettoDB(
            nome="Progetto Test DB",
            priorita=1,
            data_inizio=date(2025, 1, 1),
            data_consegna=date(2025, 1, 31),
            ore_stimate=100,
            margine=10,
            requisiti_str="Developer:1:100",
            stato="Pianificato"
        )
        db.session.add(p)
        db.session.commit()

        # Proviamo a rileggerlo
        letto = ProgettoDB.query.filter_by(nome="Progetto Test DB").first()
        assert letto is not None
        assert letto.priorita == 1
        assert letto.ore_stimate == 100

def test_salvataggio_risorsa(app):
    """Testa salvataggio risorse."""
    with app.app_context():
        # Nota: usa 'ore_totali' come definito nel tuo modello
        r = RisorsaDB(nome="Mario Rossi", skill="Developer", ore_totali=160)
        
        db.session.add(r)
        db.session.commit()
        
        letto = RisorsaDB.query.filter_by(nome="Mario Rossi").first()
        
        assert letto is not None
        assert letto.skill == "Developer"
        assert letto.ore_totali == 160