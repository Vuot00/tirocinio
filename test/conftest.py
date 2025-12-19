import pytest
import sys
import os

# Aggiungiamo la cartella principale al percorso di Python
# così possiamo importare 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models import db

@pytest.fixture
def app():
    """Crea e configura una nuova istanza dell'app per ogni test."""
    app = create_app()
    
    # Configurazione di test: Database in memoria (veloce e pulito)
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False # Disabilita protezione CSRF nei form
    })

    with app.app_context():
        db.create_all() # Crea le tabelle
        yield app       # Esegue il test
        db.session.remove()
        db.drop_all()   # Distrugge tutto alla fine

@pytest.fixture
def client(app):
    """Client simulato per fare richieste HTTP."""
    return app.test_client()