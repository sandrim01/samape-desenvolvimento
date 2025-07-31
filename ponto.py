from flask import Blueprint, render_template

bp_ponto = Blueprint('ponto', __name__, url_prefix='/ponto')

@bp_ponto.route('/')
def ponto_index():
    return render_template('employees/ponto.html')
