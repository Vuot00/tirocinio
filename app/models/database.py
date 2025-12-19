from flask_sqlalchemy import SQLAlchemy
from .entities import Risorsa, Progetto
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

    @property
    def ore_perse_totali(self):
        ore = 0
        for a in self.assenze:
            giorni = (a.data_fine - a.data_inizio).days + 1
            ore += (giorni * 8)
        return ore

    @property
    def ore_nette(self):
        return self.ore_totali - self.ore_perse_totali

    def to_logic_object(self):
        return Risorsa(self.nome, self.skill, self.ore_totali, ore_assenze=self.ore_perse_totali)

class ProgettoDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    stato = db.Column(db.String(50), default='In svolgimento', nullable=False)
    priorita = db.Column(db.Integer, nullable=False)
    
    # Campo Data Inizio presente nel DB
    data_inizio = db.Column(db.Date, nullable=False)
    
    data_consegna = db.Column(db.Date, nullable=False)
    ore_stimate = db.Column(db.Integer, nullable=False)
    margine = db.Column(db.Integer, default=10)
    requisiti_str = db.Column(db.String(200), nullable=False, default="") 

    def to_logic_object(self):
        requisiti_dict = {}
        if self.requisiti_str:
            gruppi = self.requisiti_str.split(";")
            for g in gruppi:
                parti = g.split(":")
                if len(parti) == 3:
                    skill = parti[0]
                    qty = int(parti[1])
                    perc = int(parti[2])
                    requisiti_dict[skill] = {'qty': qty, 'perc': perc}

        return Progetto(
            id=self.id,
            nome=self.nome,
            priorita=self.priorita,
            
            data_inizio=self.data_inizio,      
            data_consegna=self.data_consegna,            
            ore_stimate=self.ore_stimate,
            margine_percentuale=self.margine,
            requisiti=requisiti_dict,
            stato_db=self.stato
        )