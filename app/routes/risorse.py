from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import db, RisorsaDB, AssenzaDB
from app.logic.services import ServiceProgetti

bp = Blueprint('risorse', __name__)

@bp.route('/risorse')
def pagina_risorse():
    risorse_calcolate, _ = ServiceProgetti.ottieni_dati_calcolati()
    
    risorse_db = RisorsaDB.query.all()
    for r_db in risorse_db:
        r_log = next((x for x in risorse_calcolate if x.nome == r_db.nome), None)
        if r_log:
            r_db.dati_live = r_log
            
    return render_template('risorse.html', risorse=risorse_db)

@bp.route('/aggiungi_risorsa', methods=['POST'])
def aggiungi_risorsa():
    nuova = RisorsaDB(nome=request.form['nome'], skill=request.form['skill'], ore_totali=int(request.form['ore']))
    db.session.add(nuova)
    db.session.commit()
    return redirect(url_for('risorse.pagina_risorse'))

@bp.route('/aggiungi_assenza', methods=['POST'])
def aggiungi_assenza():
    r_id = int(request.form['risorsa_id'])
    inizio = datetime.strptime(request.form['inizio'], '%Y-%m-%d').date()
    fine = datetime.strptime(request.form['fine'], '%Y-%m-%d').date()
    
    risorse_calcolate, _ = ServiceProgetti.ottieni_dati_calcolati()
    nome_target = RisorsaDB.query.get(r_id).nome
    target = next((r for r in risorse_calcolate if r.nome == nome_target), None)
    
    giorni = (fine - inizio).days + 1
    ore_richieste = giorni * 8
    
    if target and target.ore_residue < ore_richieste:
        flash(f"Impossibile: {target.nome} ha solo {target.ore_residue:.1f}h libere.", "error")
        return redirect(url_for('risorse.pagina_risorse'))

    nuova = AssenzaDB(risorsa_id=r_id, data_inizio=inizio, data_fine=fine, motivo=request.form['motivo'])
    db.session.add(nuova)
    db.session.commit()
    return redirect(url_for('risorse.pagina_risorse'))

@bp.route('/elimina_assenza/<int:id>')
def elimina_assenza(id):
    assenza = AssenzaDB.query.get_or_404(id)
    db.session.delete(assenza)
    db.session.commit()
    # request.referrer ci riporta alla pagina da cui siamo venuti
    return redirect(request.referrer or url_for('risorse.pagina_risorse'))

@bp.route('/modifica_risorsa/<int:id>', methods=['GET'])
def modifica_risorsa_view(id):
    return render_template('modifica_risorsa.html', r=RisorsaDB.query.get_or_404(id))

@bp.route('/aggiorna_risorsa/<int:id>', methods=['POST'])
def aggiorna_risorsa(id):
    r = RisorsaDB.query.get_or_404(id)
    r.nome = request.form['nome']
    r.skill = request.form['skill']
    r.ore_totali = int(request.form['ore'])
    db.session.commit()
    return redirect(url_for('risorse.pagina_risorse'))

@bp.route('/elimina_risorsa/<int:id>')
def elimina_risorsa(id):
    db.session.delete(RisorsaDB.query.get_or_404(id))
    db.session.commit()
    return redirect(url_for('risorse.pagina_risorse'))