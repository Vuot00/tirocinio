from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from db_manager import db, RisorsaDB, ProgettoDB
import motore

# Importiamo il gestore DB e le tabelle
from db_manager import db, RisorsaDB, ProgettoDB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pianificatore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Mostriamo i dati salvati nel DB
    risorse = RisorsaDB.query.all()
    progetti = ProgettoDB.query.all()
    return render_template('index.html', risorse=risorse, progetti=progetti)

@app.route('/aggiungi_risorsa', methods=['POST'])
def aggiungi_risorsa():
    # Salviamo nel DB usando la classe DB
    nuova = RisorsaDB(
        nome=request.form['nome'],
        skill=request.form['skill'],
        ore_totali=int(request.form['ore'])
    )
    db.session.add(nuova)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/aggiungi_progetto', methods=['POST'])
def aggiungi_progetto():
    data_obj = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    
    # Costruiamo la stringa dei requisiti
    # Leggiamo i campi input HTML (qty_dev, qty_tester, qty_pm)
    req_list = []
    
    qty_dev = int(request.form.get('qty_dev', 0))
    if qty_dev > 0: req_list.append(f"Developer:{qty_dev}")
    
    qty_tester = int(request.form.get('qty_tester', 0))
    if qty_tester > 0: req_list.append(f"Tester:{qty_tester}")
    
    qty_pm = int(request.form.get('qty_pm', 0))
    if qty_pm > 0: req_list.append(f"PM:{qty_pm}")
    
    # Risultato es: "Developer:2;Tester:1"
    requisiti_finali = ";".join(req_list)

    nuovo = ProgettoDB(
        nome=request.form['nome'],
        priorita=int(request.form['priorita']),
        data_consegna=data_obj,
        ore_stimate=int(request.form['ore']),
        margine=int(request.form['margine']),
        requisiti_str=requisiti_finali # Salviamo la stringa
    )
    db.session.add(nuovo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/calcola_piano')
def calcola_piano():
    # 1. Recupera i dati DAL DATABASE
    risorse_db = RisorsaDB.query.all()
    progetti_db = ProgettoDB.query.all()
    
    # 2. CONVERSIONE: Da Database -> A Oggetti Puri (Logica)
    # Qui avviene il distacco: il motore riceve oggetti puliti, non sa che arrivano dal DB.
    risorse_logica = [r.to_logic_object() for r in risorse_db]
    progetti_logica = [p.to_logic_object() for p in progetti_db]
    
    # 3. Lancia il MOTORE (lavora sugli oggetti puri)
    motore.assegna_risorse(progetti_logica, risorse_logica)
    
    # 4. Mostra i risultati
    # Passiamo al template gli oggetti LOGICI (che ora contengono i risultati del calcolo)
    return render_template('risultato.html', progetti=progetti_logica, risorse=risorse_logica)


# --- NUOVE ROTTE PER LA MODIFICA ---

@app.route('/modifica_progetto/<int:id>', methods=['GET'])
def modifica_progetto_view(id):
    # 1. Cerca il progetto nel DB (se non c'è, da errore 404)
    progetto = ProgettoDB.query.get_or_404(id)
    
    # 2. Dobbiamo "smontare" la stringa dei requisiti (es. "Developer:2;Tester:1")
    # per rimettere i numeri nelle caselline giuste del form.
    req_dict = {'Developer': 0, 'Tester': 0, 'PM': 0}
    
    if progetto.requisiti_str:
        pairs = progetto.requisiti_str.split(';')
        for p in pairs:
            if ':' in p:
                skill, qty = p.split(':')
                if skill in req_dict:
                    req_dict[skill] = int(qty)
    
    # 3. Mostra la pagina di modifica passando i dati attuali
    return render_template('modifica_progetto.html', p=progetto, reqs=req_dict)

@app.route('/aggiorna_progetto/<int:id>', methods=['POST'])
def aggiorna_progetto(id):
    # 1. Recupera il progetto dal DB
    progetto = ProgettoDB.query.get_or_404(id)
    
    # 2. Aggiorna i campi semplici
    progetto.nome = request.form['nome']
    progetto.priorita = int(request.form['priorita'])
    progetto.data_consegna = datetime.strptime(request.form['data'], '%Y-%m-%d').date()
    progetto.ore_stimate = int(request.form['ore'])
    progetto.margine = int(request.form['margine'])
    
    # 3. Ricostruisci la stringa requisiti (esattamente come in aggiungi_progetto)
    req_list = []
    qty_dev = int(request.form.get('qty_dev', 0))
    if qty_dev > 0: req_list.append(f"Developer:{qty_dev}")
    
    qty_tester = int(request.form.get('qty_tester', 0))
    if qty_tester > 0: req_list.append(f"Tester:{qty_tester}")
    
    qty_pm = int(request.form.get('qty_pm', 0))
    if qty_pm > 0: req_list.append(f"PM:{qty_pm}")
    
    progetto.requisiti_str = ";".join(req_list)
    
    # 4. Salva le modifiche
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/elimina_progetto/<int:id>')
def elimina_progetto(id):
    # Già che ci siamo, aggiungiamo anche la cancellazione!
    progetto = ProgettoDB.query.get_or_404(id)
    db.session.delete(progetto)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)