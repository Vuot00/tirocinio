from datetime import date, timedelta

def test_home_page_redirect(client):
    """Verifica che la home reindirizzi ai progetti."""
    response = client.get('/')
    assert response.status_code == 302 # 302 = Redirect
    assert '/progetti' in response.headers['Location']

def test_progetti_page(client):
    """Verifica che la pagina progetti carichi correttamente."""
    response = client.get('/progetti', follow_redirects=True)
    assert response.status_code == 200
    # Controlla se nel HTML c'è il titolo della pagina
    assert b"Dashboard Progetti" in response.data

def test_creazione_progetto_via_post(client):
    """Simula l'invio del form per creare un progetto."""
    
    # Calcoliamo date future per essere sicuri che la validazione passi
    oggi = date.today()
    inizio = oggi + timedelta(days=10)
    fine = oggi + timedelta(days=40)
    
    dati_form = {
        'nome': 'Progetto Web Test',
        'priorita': '1',
        'margine': '5',
        'data_inizio': inizio.strftime('%Y-%m-%d'),
        'data': fine.strftime('%Y-%m-%d'), # 'data' è il nome del campo consegna nel form
        'ore': '100',
        'qty_dev': '1', 'pct_dev': '100',
        'qty_tester': '0', 'pct_tester': '0',
        'qty_pm': '0', 'pct_pm': '0'
    }
    
    # Facciamo la POST
    response = client.post('/aggiungi_progetto', data=dati_form, follow_redirects=True)
    
    # Debug: Se fallisce, stampa cosa c'è nella pagina per capire l'errore
    if b"Progetto Web Test" not in response.data:
        print("\n--- HTML RICEVUTO ---")
        # Cerchiamo messaggi di errore flash
        if b"Errore:" in response.data:
            print("TROVATO ERRORE FLASH NELLA PAGINA!")
    
    assert response.status_code == 200
    # Controlliamo se il nuovo progetto appare nella pagina
    assert b"Progetto Web Test" in response.data