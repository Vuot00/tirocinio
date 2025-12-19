# app/logic/services.py
from datetime import date, timedelta
from flask import url_for
import holidays
from app.models import db, RisorsaDB, ProgettoDB, AssenzaDB
from app.logic import engine # Importiamo il motore appena spostato

class ServiceProgetti:
    @staticmethod
    def aggiorna_stati_automatici():
        """Controlla le date di tutti i progetti e aggiorna lo stato."""
        oggi = date.today()
        progetti = ProgettoDB.query.all()
        
        for p in progetti:
            if p.stato == 'Sospeso':
                continue
            
            if p.data_consegna < oggi:
                p.stato = 'Concluso'
            elif p.data_inizio > oggi:
                p.stato = 'Pianificato'
            else:
                p.stato = 'In svolgimento'
        db.session.commit()

    @staticmethod
    def ottieni_dati_calcolati():
        """Prepara i dati, lancia il motore e unisce i risultati."""
        # 1. Aggiorna stati
        ServiceProgetti.aggiorna_stati_automatici()
        
        risorse_db = RisorsaDB.query.all()
        progetti_db = ProgettoDB.query.all()
        
        # 2. Filtro per motore
        progetti_da_calcolare = [p for p in progetti_db if p.stato in ['In svolgimento', 'Pianificato']]
        
        # 3. Conversione in oggetti logici
        risorse_logica = [r.to_logic_object() for r in risorse_db]
        progetti_da_calcolare_logica = [p.to_logic_object() for p in progetti_da_calcolare]
        
        # 4. Esecuzione Motore
        engine.assegna_risorse(progetti_da_calcolare_logica, risorse_logica)
        
        # 5. Unione Risultati
        map_risultati = {p.id: p for p in progetti_da_calcolare_logica}
        
        lista_finale_progetti = []
        for p_db in progetti_db:
            if p_db.id in map_risultati:
                lista_finale_progetti.append(map_risultati[p_db.id])
            else:
                lista_finale_progetti.append(p_db.to_logic_object())
                
        return risorse_logica, lista_finale_progetti

class ServiceCalendario:
    @staticmethod
    def get_eventi_json():
        """Logica per generare il JSON del calendario"""
        ServiceProgetti.aggiorna_stati_automatici()
        progetti = ProgettoDB.query.filter(ProgettoDB.stato != 'Concluso').all()
        eventi = []
        for p in progetti:
            colore = '#3788d8'
            if p.stato == 'Pianificato': colore = '#9b59b6'  
            elif p.stato == 'In svolgimento': colore = '#27ae60'  
            elif p.stato == 'Sospeso': colore = '#f39c12'  
            elif p.stato == 'Concluso': colore = '#7f8c8d'  
            
            data_fine_vis = p.data_consegna + timedelta(days=1)
            eventi.append({
                'title': f"[{p.stato.upper()}] {p.nome}",
                'start': p.data_inizio.strftime('%Y-%m-%d'),
                'end': data_fine_vis.strftime('%Y-%m-%d'),
                'color': colore,
                # Nota: url_for richiede il contesto dell'app, lo gestiamo nel controller o qui se siamo nel contesto
                'url': f"/modifica_progetto/{p.id}", 
                'allDay': True
            })
        return eventi
    
    @staticmethod
    def get_festivita_json():
        anno = date.today().year
        feste_it = holidays.IT(years=[anno, anno + 1])
        traduzioni = {
            "New Year's Day": "Capodanno", "Epiphany": "Epifania",
            "Easter Monday": "Pasquetta", "Liberation Day": "Liberazione",
            "Labor Day": "Festa Lavoratori", "Republic Day": "Festa Repubblica",
            "Assumption Of Mary Day": "Ferragosto", "All Saints' Day": "Ognissanti",
            "Immaculate Conception": "Immacolata", "Christmas Day": "Natale",
            "Saint Stephen's Day": "Santo Stefano"
        }
        eventi = []
        for data_festa, nome_en in feste_it.items():
            nome_it = traduzioni.get(nome_en, nome_en)
            eventi.append({
                'title': nome_it, 'start': data_festa.isoformat(),
                'allDay': True, 'textColor': "#000000",
                'backgroundColor': '#ffcccc', 'className': 'giorno-festivo', 'editable': False
            })
        return eventi