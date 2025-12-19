from flask import Blueprint, render_template, redirect, url_for, jsonify
from app.logic.services import ServiceCalendario

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    # Reindirizza alla dashboard progetti
    return redirect(url_for('progetti.pagina_progetti'))

@bp.route('/calendario')
def pagina_calendario():
    return render_template('calendario.html')

@bp.route('/api/eventi_calendario')
def api_eventi():
    return jsonify(ServiceCalendario.get_eventi_json())

@bp.route('/api/festivita')
def api_festivita():
    return jsonify(ServiceCalendario.get_festivita_json())