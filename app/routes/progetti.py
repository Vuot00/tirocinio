# app/routes/progetti.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, date
from app.models import db, ProgettoDB
from app.logic.services import ServiceProgetti
from app.config_modelli import BEST_PRACTICE

# Creiamo il "pezzo" di applicazione
bp = Blueprint('progetti', __name__)

@bp.route('/progetti')
def pagina_progetti():
    # Usiamo il service per ottenere i dati calcolati
    _, progetti_misti = ServiceProgetti.ottieni_dati_calcolati()
    
    sort_by = request.args.get('sort', 'recenti')
    
    # Logica di ordinamento (Presa dal tuo app.py)
    if sort_by == 'priorita':
        progetti_misti.sort(key=lambda p: (
            0 if p.stato_db == 'In svolgimento' else (1 if p.stato_db == 'Pianificato' else 2),
            0 if p.fattibile else 1,
            p.priorita
        ))
    elif sort_by == 'scadenza':
        progetti_misti.sort(key=lambda p: p.data_consegna)
    else:
        progetti_misti.sort(key=lambda p: (p.id or 0), reverse=True)

    return render_template('progetti.html', progetti=progetti_misti, 
                           best_practices=BEST_PRACTICE, current_sort=sort_by, today=date.today())

@bp.route('/aggiungi_progetto', methods=['POST'])
def aggiungi_progetto():
    d_in = datetime.strptime(request.form['data_inizio'], '%Y-%m-%d').date()
    
    # Validazione Data
    if d_in < date.today():
        flash("Errore: Non puoi inserire un progetto che inizia nel passato!", "error")
        return redirect(url_for('progetti.pagina_progetti')) # Nota il prefisso 'progetti.'

    d_out = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    
    if d_out < d_in:
        flash("Errore: La scadenza deve essere successiva all'inizio.", "error")
        return redirect(url_for('progetti.pagina_progetti'))

    # Parsing Requisiti
    req_list = []
    # Helper interno per evitare ripetizioni
    def add_req(skill, form_qty, form_perc):
        q = int(request.form.get(form_qty, 0))
        pct = int(request.form.get(form_perc, 0))
        if q > 0: req_list.append(f"{skill}:{q}:{pct}")
        
    add_req("Developer", "qty_dev", "pct_dev")
    add_req("Tester", "qty_tester", "pct_tester")
    add_req("PM", "qty_pm", "pct_pm")
    
    stato_iniziale = 'Pianificato' if d_in > date.today() else 'In svolgimento'

    nuovo = ProgettoDB(
        nome=request.form['nome'], priorita=int(request.form['priorita']),
        data_inizio=d_in, data_consegna=d_out, ore_stimate=int(request.form['ore']),
        margine=int(request.form['margine']), requisiti_str=";".join(req_list),
        stato=stato_iniziale
    )
    db.session.add(nuovo)
    db.session.commit()
    return redirect(url_for('progetti.pagina_progetti'))

@bp.route('/modifica_progetto/<int:id>', methods=['GET'])
def modifica_progetto_view(id):
    p = ProgettoDB.query.get_or_404(id)
    # Parsing per popolare il form
    reqs = {'Developer': {'qty':0,'perc':0}, 'Tester': {'qty':0,'perc':0}, 'PM': {'qty':0,'perc':0}}
    if p.requisiti_str:
        for pair in p.requisiti_str.split(';'):
            parts = pair.split(':')
            if len(parts)==3: reqs[parts[0]] = {'qty':int(parts[1]), 'perc':int(parts[2])}
            
    return render_template('modifica_progetto.html', p=p, reqs=reqs, today=date.today())

@bp.route('/aggiorna_progetto/<int:id>', methods=['POST'])
def aggiorna_progetto(id):
    p = ProgettoDB.query.get_or_404(id)
    
    d_in = datetime.strptime(request.form['data_inizio'], '%Y-%m-%d').date()
    
    # Validazione Modifica
    if d_in < date.today() and p.data_inizio >= date.today(): 
       flash("Errore: Non puoi spostare l'inizio nel passato!", "error")
       return redirect(url_for('progetti.modifica_progetto_view', id=id))

    p.nome = request.form['nome']
    p.priorita = int(request.form['priorita'])
    p.data_inizio = d_in
    p.data_consegna = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    p.ore_stimate = int(request.form['ore'])
    p.margine = int(request.form['margine'])
    
    # Aggiorna stato locale
    if p.stato != 'Sospeso':
        if p.data_consegna < date.today(): p.stato = 'Concluso'
        elif p.data_inizio > date.today(): p.stato = 'Pianificato'
        else: p.stato = 'In svolgimento'

    # Ricostruzione Requisiti
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
    return redirect(url_for('progetti.pagina_progetti'))

@bp.route('/elimina_progetto/<int:id>')
def elimina_progetto(id):
    p = ProgettoDB.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('progetti.pagina_progetti'))

@bp.route('/cambia_stato/<int:id>/<nuovo_stato>')
def cambia_stato(id, nuovo_stato):
    p = ProgettoDB.query.get_or_404(id)
    p.stato = nuovo_stato
    db.session.commit()
    return redirect(url_for('progetti.pagina_progetti'))