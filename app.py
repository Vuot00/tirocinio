from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import motore
from db_manager import db, RisorsaDB, ProgettoDB, AssenzaDB

# ==============================================================================
# CONFIGURAZIONE APP E DATABASE
# ==============================================================================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pianificatore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ==============================================================================
# 🏠 HOME PAGE (DASHBOARD)
# ==============================================================================
@app.route('/')
def index():
    risorse = RisorsaDB.query.all()
    progetti = ProgettoDB.query.all()
    return render_template('index.html', risorse=risorse, progetti=progetti)

# ==============================================================================
# 👤 GESTIONE RISORSE (CRUD)
# ==============================================================================
@app.route('/aggiungi_risorsa', methods=['POST'])
def aggiungi_risorsa():
    nuova = RisorsaDB(
        nome=request.form['nome'],
        skill=request.form['skill'],
        ore_totali=int(request.form['ore'])
    )
    db.session.add(nuova)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modifica_risorsa/<int:id>', methods=['GET'])
def modifica_risorsa_view(id):
    risorsa = RisorsaDB.query.get_or_404(id)
    return render_template('modifica_risorsa.html', r=risorsa)

@app.route('/aggiorna_risorsa/<int:id>', methods=['POST'])
def aggiorna_risorsa(id):
    risorsa = RisorsaDB.query.get_or_404(id)
    
    risorsa.nome = request.form['nome']
    risorsa.skill = request.form['skill']
    risorsa.ore_totali = int(request.form['ore'])
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/elimina_risorsa/<int:id>')
def elimina_risorsa(id):
    risorsa = RisorsaDB.query.get_or_404(id)
    # Nota: SQLAlchemy gestirà le assenze collegate in base alla configurazione cascade,
    # ma per ora cancelliamo l'oggetto principale.
    db.session.delete(risorsa)
    db.session.commit()
    return redirect(url_for('index'))

# ==============================================================================
# 🏖️ GESTIONE ASSENZE
# ==============================================================================
@app.route('/aggiungi_assenza', methods=['POST'])
def aggiungi_assenza():
    nuova = AssenzaDB(
        risorsa_id=int(request.form['risorsa_id']),
        data_inizio=datetime.strptime(request.form['inizio'], '%Y-%m-%d').date(),
        data_fine=datetime.strptime(request.form['fine'], '%Y-%m-%d').date(),
        motivo=request.form['motivo']
    )
    db.session.add(nuova)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/elimina_assenza/<int:id>')
def elimina_assenza(id):
    # 1. Trova l'assenza
    assenza = AssenzaDB.query.get_or_404(id)
    
    # 2. Salviamo l'ID della risorsa per tornarci dopo
    risorsa_id = assenza.risorsa_id
    
    # 3. Cancelliamo
    db.session.delete(assenza)
    db.session.commit()
    
    # 4. Ricarichiamo la pagina di modifica di QUELLA risorsa
    return redirect(url_for('modifica_risorsa_view', id=risorsa_id))

# ==============================================================================
# 🚀 GESTIONE PROGETTI (CRUD)
# ==============================================================================
@app.route('/aggiungi_progetto', methods=['POST'])
def aggiungi_progetto():
    data_obj = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    
    # Helper function locale per leggere i dati
    req_list = []
    def add_req(skill, form_qty, form_perc):
        q = int(request.form.get(form_qty, 0))
        p = int(request.form.get(form_perc, 0))
        if q > 0:
            req_list.append(f"{skill}:{q}:{p}")

    add_req("Developer", "qty_dev", "pct_dev")
    add_req("Tester", "qty_tester", "pct_tester")
    add_req("PM", "qty_pm", "pct_pm")
    
    requisiti_finali = ";".join(req_list)

    nuovo = ProgettoDB(
        nome=request.form['nome'],
        priorita=int(request.form['priorita']),
        data_consegna=data_obj,
        ore_stimate=int(request.form['ore']),
        margine=int(request.form['margine']),
        requisiti_str=requisiti_finali
    )
    db.session.add(nuovo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/modifica_progetto/<int:id>', methods=['GET'])
def modifica_progetto_view(id):
    progetto = ProgettoDB.query.get_or_404(id)
    # Dizionario con struttura base
    req_dict = {
        'Developer': {'qty': 0, 'perc': 0}, 
        'Tester': {'qty': 0, 'perc': 0}, 
        'PM': {'qty': 0, 'perc': 0}
    }
    
    # Parsing della stringa requisiti
    if progetto.requisiti_str:
        pairs = progetto.requisiti_str.split(';')
        for p in pairs:
            parts = p.split(':')
            if len(parts) == 3:
                skill, qty, perc = parts
                if skill in req_dict:
                    req_dict[skill] = {'qty': int(qty), 'perc': int(perc)}
                    
    return render_template('modifica_progetto.html', p=progetto, reqs=req_dict)

@app.route('/aggiorna_progetto/<int:id>', methods=['POST'])
def aggiorna_progetto(id):
    progetto = ProgettoDB.query.get_or_404(id)
    
    # Aggiornamento campi base
    progetto.nome = request.form['nome']
    progetto.priorita = int(request.form['priorita'])
    progetto.data_consegna = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    progetto.ore_stimate = int(request.form['ore'])
    progetto.margine = int(request.form['margine'])
    
    # Ricostruzione stringa requisiti
    req_list = []
    def add_req(skill, form_qty, form_perc):
        q = int(request.form.get(form_qty, 0))
        p = int(request.form.get(form_perc, 0))
        if q > 0:
            req_list.append(f"{skill}:{q}:{p}")

    add_req("Developer", "qty_dev", "pct_dev")
    add_req("Tester", "qty_tester", "pct_tester")
    add_req("PM", "qty_pm", "pct_pm")
    
    progetto.requisiti_str = ";".join(req_list)
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/elimina_progetto/<int:id>')
def elimina_progetto(id):
    progetto = ProgettoDB.query.get_or_404(id)
    db.session.delete(progetto)
    db.session.commit()
    return redirect(url_for('index'))

# ==============================================================================
# 🧠 MOTORE DI CALCOLO
# ==============================================================================
@app.route('/calcola_piano')
def calcola_piano():
    risorse_db = RisorsaDB.query.all()
    progetti_db = ProgettoDB.query.all()
    
    risorse_logica = [r.to_logic_object() for r in risorse_db]
    progetti_logica = [p.to_logic_object() for p in progetti_db]
    
    motore.assegna_risorse(progetti_logica, risorse_logica)
    
    return render_template('risultato.html', progetti=progetti_logica, risorse=risorse_logica)

# ==============================================================================
# AVVIO APP
# ==============================================================================
if __name__ == '__main__':
    app.run(debug=True)