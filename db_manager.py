from flask_sqlalchemy import SQLAlchemy
from modelli import Risorsa, Progetto

db = SQLAlchemy()

# --- TABELLE DB ---
class RisorsaDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(50), nullable=False)
    ore_totali = db.Column(db.Integer, nullable=False)

    def to_logic_object(self):
        return Risorsa(self.nome, self.skill, self.ore_totali)

class ProgettoDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    priorita = db.Column(db.Integer, nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    ore_stimate = db.Column(db.Integer, nullable=False)
    margine = db.Column(db.Integer, default=10)
    
    # NUOVO: Salviamo la ricetta come stringa "Developer:2;Tester:1"
    requisiti_str = db.Column(db.String(200), nullable=False, default="") 

    def to_logic_object(self):
        # Conversione da Stringa DB "Dev:2;Tester:1" -> Dizionario Python {'Dev':2, 'Tester':1}
        requisiti_dict = {}
        if self.requisiti_str:
            coppie = self.requisiti_str.split(";") # Separa i ruoli
            for c in coppie:
                if ":" in c:
                    skill, qty = c.split(":")
                    requisiti_dict[skill] = int(qty)

        # Qui chiamiamo il nuovo __init__ di modelli.py
        return Progetto(
            nome=self.nome,
            priorita=self.priorita,
            data_consegna=self.data_consegna,
            ore_stimate=self.ore_stimate,
            margine_percentuale=self.margine,
            requisiti=requisiti_dict # Passiamo il dizionario
        )