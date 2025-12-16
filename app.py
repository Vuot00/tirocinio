from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from datetime import datetime, date, timedelta
import motore
import holidays
from db_manager import db, RisorsaDB, ProgettoDB, AssenzaDB
from config_modelli import BEST_PRACTICE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pianificatore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chiave_segreta_super_sicura'

db.init_app(app)

with app.app_context():
    db.create_all()

# --- HELPER: GESTIONE AUTOMATICA STATI ---
def aggiorna_stati_automatici():
    """
    Controlla le date di tutti i progetti e aggiorna lo stato.
    Regola: Sospeso vince su tutto (manuale). Altrimenti decide il calendario.
    """
    oggi = date.today()
    progetti = ProgettoDB.query.all()
    
    for p in progetti:
        # Se è stato sospeso manualmente, non lo tocchiamo automaticamente
        if p.stato == 'Sospeso':
            continue
            
        # Logica temporale
        if p.data_consegna < oggi:
            p.stato = 'Concluso'
        elif p.data_inizio > oggi:
            p.stato = 'Pianificato' # Nuovo stato per il futuro
        else:
            # Se oggi è compreso tra inizio e fine
            p.stato = 'In svolgimento'
            
    db.session.commit()

def ottieni_dati_calcolati():
    # 1. Aggiorna gli stati in base alla data odierna
    aggiorna_stati_automatici()
    
    risorse_db = RisorsaDB.query.all()
    progetti_db = ProgettoDB.query.all()
    
    # 2. Filtriamo per il motore:
    # Il motore deve considerare sia quelli ATTIVI che quelli FUTURI (Pianificati)
    # per vedere se sono fattibili. Quelli conclusi o sospesi liberano risorse.
    progetti_da_calcolare = [p for p in progetti_db if p.stato in ['In svolgimento', 'Pianificato']]
    
    risorse_logica = [r.to_logic_object() for r in risorse_db]
    progetti_da_calcolare_logica = [p.to_logic_object() for p in progetti_da_calcolare]
    
    # Eseguiamo il calcolo solo su questo sottoinsieme
    motore.assegna_risorse(progetti_da_calcolare_logica, risorse_logica)
    
    # Ora dobbiamo "unire" i risultati logici con la lista completa DB per visualizzarli tutti
    # Creiamo un dizionario per accesso rapido ai risultati calcolati
    map_risultati = {p.id: p for p in progetti_da_calcolare_logica}
    
    lista_finale_progetti = []
    for p_db in progetti_db:
        # Se il progetto era nel calcolo, usiamo la versione calcolata (con fattibilità e dettagli)
        if p_db.id in map_risultati:
            lista_finale_progetti.append(map_risultati[p_db.id])
        else:
            # Altrimenti usiamo l'oggetto base (per visualizzare sospesi/conclusi)
            lista_finale_progetti.append(p_db.to_logic_object())
            
    return risorse_logica, lista_finale_progetti

# --- NAVIGAZIONE ---

@app.route('/')
def home():
    return redirect(url_for('pagina_progetti'))

@app.route('/risorse')
def pagina_risorse():
    risorse_calcolate, _ = ottieni_dati_calcolati()
    
    # Unione dati per visualizzazione live
    risorse_db = RisorsaDB.query.all()
    for r_db in risorse_db:
        r_log = next((x for x in risorse_calcolate if x.nome == r_db.nome), None)
        if r_log:
            r_db.dati_live = r_log
            
    return render_template('risorse.html', risorse=risorse_db)

@app.route('/progetti')
def pagina_progetti():
    _, progetti_misti = ottieni_dati_calcolati()
    
    sort_by = request.args.get('sort', 'recenti')
    
    if sort_by == 'priorita':
        # Ordine: Attivi > Pianificati > Sospesi/Chiusi
        progetti_misti.sort(key=lambda p: (
            0 if p.stato_db == 'In svolgimento' else (1 if p.stato_db == 'Pianificato' else 2),
            0 if p.fattibile else 1,
            p.priorita
        ))
    elif sort_by == 'scadenza':
        progetti_misti.sort(key=lambda p: p.data_consegna)
    else:
        progetti_misti.sort(key=lambda p: (p.id or 0), reverse=True)

    # Passiamo la data di oggi per il vincolo 'min' nei form HTML
    return render_template('progetti.html', progetti=progetti_misti, best_practices=BEST_PRACTICE, current_sort=sort_by, today=date.today())

@app.route('/calendario')
def pagina_calendario():
    return render_template('calendario.html')

# --- API ---

@app.route('/api/eventi_calendario')
def api_eventi():
    aggiorna_stati_automatici() # Assicuriamoci che i dati siano freschi
    progetti = ProgettoDB.query.filter(ProgettoDB.stato != 'Concluso').all()
    eventi = []
    for p in progetti:
        colore = '#3498db' # In svolgimento
        if p.stato == 'Sospeso': colore = '#95a5a6'
        elif p.stato == 'Pianificato': colore = '#9b59b6' # Viola per futuri
        
        if p.priorita == 1 and p.stato != 'Sospeso': colore = '#e74c3c'
        
        data_fine_vis = p.data_consegna + timedelta(days=1)
        eventi.append({
            'title': f"[{p.stato[0].upper()}] {p.nome}",
            'start': p.data_inizio.strftime('%Y-%m-%d'),
            'end': data_fine_vis.strftime('%Y-%m-%d'),
            'color': colore,
            'url': url_for('modifica_progetto_view', id=p.id),
            'allDay': True
        })
    return jsonify(eventi)

@app.route('/api/festivita')
def api_festivita():
    anno_corrente = date.today().year
    feste_it = holidays.IT(years=[anno_corrente, anno_corrente + 1])

    traduzioni = {
        "New Year's Day": "Capodanno",
        "Epiphany": "Epifania",
        "Easter Monday": "Pasquetta",
        "Liberation Day": "Festa della Liberazione",
        "Labor Day": "Festa dei Lavoratori",
        "Republic Day": "Festa della Repubblica",
        "Assumption Of Mary Day": "Ferragosto",
        "All Saints' Day": "Ognissanti",
        "Immaculate Conception": "Immacolata Concezione",
        "Christmas Day": "Natale",
        "Saint Stephen's Day": "Santo Stefano",
        "National Unity Day": "Giornata dell'Unità Nazionale",
        "Saint Francis of Assisi, Patron Saint of Italy": "San Francesco (Patrono d'Italia)"
    }
    
    eventi_festivi = []
    
    for data, nome_inglese in feste_it.items():
        nome_italiano = traduzioni.get(nome_inglese, nome_inglese)
        eventi_festivi.append({
            'title': f"{nome_italiano}",  
            'start': data.isoformat(),
            'allDay': True,
            'textColor': "#000000",
            'backgroundColor': '#ffcccc', 
            'className': 'giorno-festivo', 
            'editable': False  
        })
        
    return jsonify(eventi_festivi)

@app.route('/cambia_stato/<int:id>/<nuovo_stato>')
def cambia_stato(id, nuovo_stato):
    p = ProgettoDB.query.get_or_404(id)
    # Permettiamo cambio manuale solo verso Sospeso o per forzare altri stati
    p.stato = nuovo_stato
    db.session.commit()
    return redirect(url_for('pagina_progetti'))

# --- CRUD RISORSE --- (Invariato)
@app.route('/aggiungi_risorsa', methods=['POST'])
def aggiungi_risorsa():
    nuova = RisorsaDB(nome=request.form['nome'], skill=request.form['skill'], ore_totali=int(request.form['ore']))
    db.session.add(nuova); db.session.commit()
    return redirect(url_for('pagina_risorse'))

@app.route('/aggiungi_assenza', methods=['POST'])
def aggiungi_assenza():
    r_id = int(request.form['risorsa_id'])
    inizio = datetime.strptime(request.form['inizio'], '%Y-%m-%d').date()
    fine = datetime.strptime(request.form['fine'], '%Y-%m-%d').date()
    giorni = (fine - inizio).days + 1
    ore_richieste = giorni * 8
    
    risorse_calcolate, _ = ottieni_dati_calcolati()
    target = next((r for r in risorse_calcolate if r.nome == RisorsaDB.query.get(r_id).nome), None)
    
    if target and target.ore_residue < ore_richieste:
        flash(f"Impossibile: {target.nome} ha solo {target.ore_residue:.1f}h libere.", "error")
        return redirect(url_for('pagina_risorse'))

    nuova = AssenzaDB(risorsa_id=r_id, data_inizio=inizio, data_fine=fine, motivo=request.form['motivo'])
    db.session.add(nuova); db.session.commit()
    return redirect(url_for('pagina_risorse'))

@app.route('/elimina_assenza/<int:id>')
def elimina_assenza(id):
    assenza = AssenzaDB.query.get_or_404(id)
    r_id = assenza.risorsa_id
    db.session.delete(assenza); db.session.commit()
    return redirect(request.referrer or url_for('pagina_risorse'))

# --- CRUD PROGETTI ---

@app.route('/aggiungi_progetto', methods=['POST'])
def aggiungi_progetto():
    d_in = datetime.strptime(request.form['data_inizio'], '%Y-%m-%d').date()
    
    # VALIDAZIONE DATA NEL PASSATO
    if d_in < date.today():
        flash("Errore: Non puoi inserire un progetto che inizia nel passato!", "error")
        return redirect(url_for('pagina_progetti'))

    d_out = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    
    if d_out < d_in:
        flash("Errore: La scadenza deve essere successiva all'inizio.", "error")
        return redirect(url_for('pagina_progetti'))

    req_list = []
    def add_req(skill, form_qty, form_perc):
        q = int(request.form.get(form_qty, 0))
        p = int(request.form.get(form_perc, 0))
        if q > 0: req_list.append(f"{skill}:{q}:{p}")
    add_req("Developer", "qty_dev", "pct_dev")
    add_req("Tester", "qty_tester", "pct_tester")
    add_req("PM", "qty_pm", "pct_pm")
    
    # Lo stato iniziale sarà deciso automaticamente al prossimo refresh
    # ma lo settiamo coerente subito
    stato_iniziale = 'Pianificato' if d_in > date.today() else 'In svolgimento'

    nuovo = ProgettoDB(
        nome=request.form['nome'], priorita=int(request.form['priorita']),
        data_inizio=d_in, data_consegna=d_out, ore_stimate=int(request.form['ore']),
        margine=int(request.form['margine']), requisiti_str=";".join(req_list),
        stato=stato_iniziale
    )
    db.session.add(nuovo); db.session.commit()
    return redirect(url_for('pagina_progetti'))

@app.route('/modifica_progetto/<int:id>', methods=['GET'])
def modifica_progetto_view(id):
    p = ProgettoDB.query.get_or_404(id)
    reqs = {'Developer': {'qty':0,'perc':0}, 'Tester': {'qty':0,'perc':0}, 'PM': {'qty':0,'perc':0}}
    if p.requisiti_str:
        for pair in p.requisiti_str.split(';'):
            parts = pair.split(':')
            if len(parts)==3: reqs[parts[0]] = {'qty':int(parts[1]), 'perc':int(parts[2])}
    # Passiamo 'today' anche qui
    return render_template('modifica_progetto.html', p=p, reqs=reqs, today=date.today())

@app.route('/aggiorna_progetto/<int:id>', methods=['POST'])
def aggiorna_progetto(id):
    p = ProgettoDB.query.get_or_404(id)
    
    d_in = datetime.strptime(request.form['data_inizio'], '%Y-%m-%d').date()
    
    # VALIDAZIONE MODIFICA
    # Nota: se il progetto era GIA' nel passato, permettiamo la modifica? 
    # Mettiamo il vincolo rigido come richiesto.
    if d_in < date.today() and p.data_inizio >= date.today(): 
       # Se stiamo provando a spostarlo nel passato (ma non lo era già)
       flash("Errore: Non puoi spostare l'inizio nel passato!", "error")
       return redirect(url_for('modifica_progetto_view', id=id))

    p.nome = request.form['nome']
    p.priorita = int(request.form['priorita'])
    p.data_inizio = d_in
    p.data_consegna = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    p.ore_stimate = int(request.form['ore'])
    p.margine = int(request.form['margine'])
    
    # Aggiorna stato automatico immediato
    if p.stato != 'Sospeso':
        if p.data_consegna < date.today(): p.stato = 'Concluso'
        elif p.data_inizio > date.today(): p.stato = 'Pianificato'
        else: p.stato = 'In svolgimento'

    req_list = []
    def add_req(skill, form_qty, form_perc):
        q = int(request.form.get(form_qty, 0))
        pct = int(request.form.get(form_perc, 0))
        if q > 0: req_list.append(f"{skill}:{q}:{pct}")
    add_req("Developer", "qty_dev", "pct_dev")
    add_req("Tester", "qty_tester", "pct_tester")
    add_req("PM", "qty_pm", "pct_pm")
    p.requisiti_str = ";".join(req_list)
    db.session.commit()
    return redirect(url_for('pagina_progetti'))

@app.route('/elimina_progetto/<int:id>')
def elimina_progetto(id):
    p = ProgettoDB.query.get_or_404(id)
    db.session.delete(p); db.session.commit()
    return redirect(url_for('pagina_progetti'))

# --- CRUD RISORSE EDIT ---
@app.route('/modifica_risorsa/<int:id>', methods=['GET'])
def modifica_risorsa_view(id):
    return render_template('modifica_risorsa.html', r=RisorsaDB.query.get_or_404(id))

@app.route('/aggiorna_risorsa/<int:id>', methods=['POST'])
def aggiorna_risorsa(id):
    r = RisorsaDB.query.get_or_404(id)
    r.nome = request.form['nome']
    r.skill = request.form['skill']
    r.ore_totali = int(request.form['ore'])
    db.session.commit()
    return redirect(url_for('pagina_risorse'))

@app.route('/elimina_risorsa/<int:id>')
def elimina_risorsa(id):
    db.session.delete(RisorsaDB.query.get_or_404(id)); db.session.commit()
    return redirect(url_for('pagina_risorse'))

if __name__ == '__main__':
    app.run(debug=True)