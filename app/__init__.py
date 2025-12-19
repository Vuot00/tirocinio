# File: app/__init__.py
from flask import Flask
from config import Config
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Registra i Blueprint (i nuovi controller)
    from app.routes.main import bp as main_bp
    from app.routes.risorse import bp as risorse_bp
    from app.routes.progetti import bp as progetti_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(risorse_bp)
    app.register_blueprint(progetti_bp)

    with app.app_context():
        db.create_all()

    return app