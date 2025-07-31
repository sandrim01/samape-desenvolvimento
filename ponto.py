from flask import Blueprint, render_template

bp_ponto = Blueprint('ponto', __name__, url_prefix='/ponto')

from flask import request, redirect, url_for, flash
from models import Ponto, db
from flask_login import login_required, current_user
import datetime

@bp_ponto.route('/', methods=['GET'])
@login_required
def ponto_index():
    registros = Ponto.query.filter_by(user_id=current_user.id).order_by(Ponto.data.desc(), Ponto.hora_entrada.desc()).all()
    return render_template('employees/ponto.html', registros=registros)

@bp_ponto.route('/bater', methods=['POST'])
@login_required
def bater_ponto():
    foto_base64 = request.form.get('foto')
    agora = datetime.datetime.now()
    novo_ponto = Ponto(user_id=current_user.id, data=agora.date(), hora_entrada=agora, observacao=None)
    if hasattr(novo_ponto, 'foto_base64'):
        novo_ponto.foto_base64 = foto_base64
    db.session.add(novo_ponto)
    db.session.commit()
    flash('Ponto registrado com sucesso!', 'success')
    return redirect(url_for('dashboard'))
