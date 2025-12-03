from flask_sqlalchemy import SQLAlchemy
from modelli import Risorsa, Progetto
from datetime import date

db = SQLAlchemy()

class AssenzaDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    risorsa_id = db.Column(db.Integer, db.ForeignKey('risorsa_db.id'), nullable=False)
    data_inizio = db.Column(db.Date, nullable=False)
    data_fine = db.Column(db.Date, nullable=False)
    motivo = db.Column(db.String(50))

class RisorsaDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(50), nullable=False)
    ore_totali = db.Column(db.Integer, nullable=False)
    assenze = db.relationship('AssenzaDB', backref='risorsa', lazy=True)

    def to_logic_object(self):
        ore_perse = 0
        for a in self.assenze:
            d = (a.data_fine - a.data_inizio).days + 1
            ore_perse += (d * 8)
        return Risorsa(self.nome, self.skill, self.ore_totali, ore_assenze=ore_perse)

class ProgettoDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    priorita = db.Column(db.Integer, nullable=False)
    data_consegna = db.Column(db.Date, nullable=False)
    ore_stimate = db.Column(db.Integer, nullable=False)
    margine = db.Column(db.Integer, default=10)
    
    # FORMATO STRINGA: "Skill:Qty:Perc;Skill:Qty:Perc"
    requisiti_str = db.Column(db.String(200), nullable=False, default="") 

    def to_logic_object(self):
        # Parsing: Da "Dev:2:20" a {'Dev': {'qty':2, 'perc':20}}
        requisiti_dict = {}
        if self.requisiti_str:
            gruppi = self.requisiti_str.split(";")
            for g in gruppi:
                parti = g.split(":")
                if len(parti) == 3: # Skill, Qty, Perc
                    skill = parti[0]
                    qty = int(parti[1])
                    perc = int(parti[2])
                    requisiti_dict[skill] = {'qty': qty, 'perc': perc}

        return Progetto(
            nome=self.nome,
            priorita=self.priorita,
            data_consegna=self.data_consegna,
            ore_stimate=self.ore_stimate,
            margine_percentuale=self.margine,
            requisiti=requisiti_dict
        )