from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, time
from sqlalchemy import func, and_, or_
from models import db, Ponto, User
from utils import admin_required, manager_required

bp_ponto = Blueprint('ponto', __name__, url_prefix='/ponto')

@bp_ponto.route('/')
@login_required
def index():
    """Página principal do controle de ponto"""
    # Buscar registros do usuário atual
    registros = Ponto.query.filter_by(user_id=current_user.id).order_by(
        Ponto.data.desc(), 
        Ponto.hora_entrada.desc()
    ).limit(30).all()
    
    # Verificar se já bateu ponto hoje
    hoje = date.today()
    ponto_hoje = Ponto.query.filter_by(
        user_id=current_user.id,
        data=hoje
    ).first()
    
    return render_template('employees/ponto.html', 
                         registros=registros, 
                         ponto_hoje=ponto_hoje,
                         hoje=hoje)

@bp_ponto.route('/bater', methods=['GET', 'POST'])
@login_required
def bater_ponto():
    """Registrar entrada ou saída de ponto"""
    if request.method == 'GET':
        return render_template('ponto/registrar.html')
    
    try:
        # Obter dados da requisição
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)
        observacao = request.form.get('observacao', '').strip()
        
        hoje = date.today()
        agora = datetime.now()
        
        # Verificar se já existe registro para hoje
        ponto_existente = Ponto.query.filter_by(
            user_id=current_user.id,
            data=hoje
        ).first()
        
        if ponto_existente:
            # Se já existe e não tem hora de saída, registrar saída
            if not ponto_existente.hora_saida:
                ponto_existente.hora_saida = agora
                if observacao:
                    ponto_existente.observacao = f"{ponto_existente.observacao or ''}\nSaída: {observacao}".strip()
                ponto_existente.updated_at = agora
                
                db.session.commit()
                flash('Saída registrada com sucesso!', 'success')
            else:
                flash('Você já registrou entrada e saída hoje.', 'warning')
        else:
            # Criar novo registro de entrada
            novo_ponto = Ponto(
                user_id=current_user.id,
                data=hoje,
                hora_entrada=agora,
                observacao=f"Entrada: {observacao}" if observacao else None,
                latitude=latitude,
                longitude=longitude
            )
            
            db.session.add(novo_ponto)
            db.session.commit()
            flash('Entrada registrada com sucesso!', 'success')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao registrar ponto: {str(e)}', 'error')
    
    return redirect(url_for('ponto.index'))

@bp_ponto.route('/admin')
@admin_required
def admin_view():
    """Visão administrativa do controle de ponto"""
    # Buscar todos os registros do mês atual
    hoje = date.today()
    inicio_mes = hoje.replace(day=1)
    
    registros = db.session.query(Ponto, User).join(User).filter(
        Ponto.data >= inicio_mes
    ).order_by(Ponto.data.desc(), User.name).all()
    
    return render_template('ponto/admin.html', registros=registros, mes_atual=hoje)

@bp_ponto.route('/relatorio')
@manager_required  
def relatorio():
    """Relatório de ponto por período"""
    data_inicio = request.args.get('inicio')
    data_fim = request.args.get('fim')
    user_id = request.args.get('usuario', type=int)
    
    # Filtros padrão (últimos 30 dias)
    if not data_inicio:
        data_inicio = (date.today().replace(day=1)).strftime('%Y-%m-%d')
    if not data_fim:
        data_fim = date.today().strftime('%Y-%m-%d')
    
    # Query base
    query = db.session.query(Ponto, User).join(User)
    
    # Aplicar filtros
    if data_inicio:
        query = query.filter(Ponto.data >= data_inicio)
    if data_fim:
        query = query.filter(Ponto.data <= data_fim)
    if user_id:
        query = query.filter(Ponto.user_id == user_id)
    
    registros = query.order_by(Ponto.data.desc(), User.name).all()
    usuarios = User.query.filter_by(active=True).order_by(User.name).all()
    
    return render_template('ponto/relatorio.html', 
                         registros=registros,
                         usuarios=usuarios,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         user_id=user_id)

@bp_ponto.route('/api/status')
@login_required
def api_status():
    """API para verificar status do ponto do usuário"""
    hoje = date.today()
    ponto = Ponto.query.filter_by(
        user_id=current_user.id,
        data=hoje
    ).first()
    
    status = {
        'tem_entrada': bool(ponto and ponto.hora_entrada),
        'tem_saida': bool(ponto and ponto.hora_saida),
        'pode_bater': True
    }
    
    if ponto:
        status['hora_entrada'] = ponto.hora_entrada.strftime('%H:%M') if ponto.hora_entrada else None
        status['hora_saida'] = ponto.hora_saida.strftime('%H:%M') if ponto.hora_saida else None
    
    return jsonify(status)
