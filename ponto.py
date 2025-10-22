from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, time, timedelta
from sqlalchemy import func, and_, or_
from models import db, Ponto, User, UserRole
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
    # Parâmetros de filtro
    mes_param = request.args.get('mes')
    ano_param = request.args.get('ano', type=int)
    
    # Data atual como padrão
    hoje = date.today()
    
    if mes_param and ano_param:
        try:
            mes_filtro = int(mes_param)
            ano_filtro = ano_param
            inicio_mes = date(ano_filtro, mes_filtro, 1)
        except (ValueError, TypeError):
            inicio_mes = hoje.replace(day=1)
    else:
        inicio_mes = hoje.replace(day=1)
    
    # Calcular o fim do mês
    if inicio_mes.month == 12:
        fim_mes = inicio_mes.replace(year=inicio_mes.year + 1, month=1, day=1)
    else:
        fim_mes = inicio_mes.replace(month=inicio_mes.month + 1, day=1)
    
    # Último dia do mês para exibição
    ultimo_dia_mes = (fim_mes - timedelta(days=1)).date()
    
    # Buscar todos os registros do período filtrado de todos os funcionários ativos
    registros = db.session.query(Ponto, User).join(User).filter(
        Ponto.data >= inicio_mes,
        Ponto.data < fim_mes,
        User.active == True
    ).order_by(Ponto.data.desc(), User.name).all()
    
    # Estatísticas do período
    total_registros = len(registros)
    funcionarios_com_ponto = len(set([user.id for ponto, user in registros]))
    funcionarios_ativos = User.query.filter_by(active=True, role=UserRole.funcionario).count()
    
    stats = {
        'total_registros': total_registros,
        'funcionarios_com_ponto': funcionarios_com_ponto,
        'funcionarios_ativos': funcionarios_ativos,
        'inicio_mes': inicio_mes,
        'fim_mes': fim_mes,
        'ultimo_dia_mes': ultimo_dia_mes,
        'mes_atual': inicio_mes
    }
    
    return render_template('ponto/admin.html', registros=registros, stats=stats)

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

@bp_ponto.route('/editar/<int:ponto_id>', methods=['GET', 'POST'])
@admin_required
def editar_ponto(ponto_id):
    """Editar registro de ponto (apenas administradores)"""
    ponto = Ponto.query.get_or_404(ponto_id)
    usuario = User.query.get(ponto.user_id)
    
    if request.method == 'POST':
        # Verificar senha do administrador
        senha_admin = request.form.get('senha_admin')
        if not senha_admin or not current_user.check_password(senha_admin):
            flash('Senha de administrador incorreta!', 'error')
            return render_template('ponto/editar.html', ponto=ponto, usuario=usuario)
        
        try:
            # Atualizar dados do ponto
            data_str = request.form.get('data')
            hora_entrada_str = request.form.get('hora_entrada')
            hora_saida_str = request.form.get('hora_saida')
            observacao = request.form.get('observacao', '').strip()
            
            # Converter data
            if data_str:
                ponto.data = datetime.strptime(data_str, '%Y-%m-%d').date()
            
            # Converter hora de entrada
            if hora_entrada_str:
                hora_entrada = datetime.strptime(hora_entrada_str, '%H:%M').time()
                ponto.hora_entrada = datetime.combine(ponto.data, hora_entrada)
            
            # Converter hora de saída
            if hora_saida_str:
                hora_saida = datetime.strptime(hora_saida_str, '%H:%M').time()
                ponto.hora_saida = datetime.combine(ponto.data, hora_saida)
            elif request.form.get('limpar_saida'):
                ponto.hora_saida = None
            
            # Atualizar observação
            ponto.observacao = observacao if observacao else None
            ponto.updated_at = datetime.now()
            
            # Adicionar log da alteração
            log_msg = f"Ponto editado pelo admin {current_user.name}"
            if ponto.observacao:
                ponto.observacao = f"{ponto.observacao}\n[ADMIN] {log_msg}"
            else:
                ponto.observacao = f"[ADMIN] {log_msg}"
            
            db.session.commit()
            flash(f'Ponto de {usuario.name} editado com sucesso!', 'success')
            return redirect(url_for('ponto.admin_view'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao editar ponto: {str(e)}', 'error')
    
    return render_template('ponto/editar.html', ponto=ponto, usuario=usuario)

@bp_ponto.route('/excluir/<int:ponto_id>', methods=['POST'])
@admin_required
def excluir_ponto(ponto_id):
    """Excluir registro de ponto (apenas administradores)"""
    ponto = Ponto.query.get_or_404(ponto_id)
    usuario = User.query.get(ponto.user_id)
    
    # Verificar senha do administrador
    senha_admin = request.form.get('senha_admin')
    if not senha_admin or not current_user.check_password(senha_admin):
        flash('Senha de administrador incorreta!', 'error')
        return redirect(url_for('ponto.admin_view'))
    
    try:
        db.session.delete(ponto)
        db.session.commit()
        flash(f'Ponto de {usuario.name} excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir ponto: {str(e)}', 'error')
    
    return redirect(url_for('ponto.admin_view'))

@bp_ponto.route('/criar', methods=['GET', 'POST'])
@admin_required
def criar_ponto():
    """Criar novo registro de ponto para funcionário (apenas administradores)"""
    usuarios = User.query.filter_by(active=True).order_by(User.name).all()
    
    if request.method == 'POST':
        # Verificar senha do administrador
        senha_admin = request.form.get('senha_admin')
        if not senha_admin or not current_user.check_password(senha_admin):
            flash('Senha de administrador incorreta!', 'error')
            return render_template('ponto/criar.html', usuarios=usuarios)
        
        try:
            user_id = request.form.get('user_id', type=int)
            data_str = request.form.get('data')
            hora_entrada_str = request.form.get('hora_entrada')
            hora_saida_str = request.form.get('hora_saida')
            observacao = request.form.get('observacao', '').strip()
            
            if not user_id or not data_str or not hora_entrada_str:
                flash('Usuário, data e hora de entrada são obrigatórios!', 'error')
                return render_template('ponto/criar.html', usuarios=usuarios)
            
            # Verificar se já existe ponto para este usuário nesta data
            data_ponto = datetime.strptime(data_str, '%Y-%m-%d').date()
            ponto_existente = Ponto.query.filter_by(user_id=user_id, data=data_ponto).first()
            if ponto_existente:
                flash('Já existe um registro de ponto para este funcionário nesta data!', 'error')
                return render_template('ponto/criar.html', usuarios=usuarios)
            
            # Criar novo ponto
            hora_entrada = datetime.strptime(hora_entrada_str, '%H:%M').time()
            hora_entrada_dt = datetime.combine(data_ponto, hora_entrada)
            
            hora_saida_dt = None
            if hora_saida_str:
                hora_saida = datetime.strptime(hora_saida_str, '%H:%M').time()
                hora_saida_dt = datetime.combine(data_ponto, hora_saida)
            
            # Adicionar log da criação na observação
            log_msg = f"Ponto criado pelo admin {current_user.name}"
            if observacao:
                observacao = f"{observacao}\n[ADMIN] {log_msg}"
            else:
                observacao = f"[ADMIN] {log_msg}"
            
            novo_ponto = Ponto(
                user_id=user_id,
                data=data_ponto,
                hora_entrada=hora_entrada_dt,
                hora_saida=hora_saida_dt,
                observacao=observacao
            )
            
            db.session.add(novo_ponto)
            db.session.commit()
            
            usuario = User.query.get(user_id)
            flash(f'Ponto criado com sucesso para {usuario.name}!', 'success')
            return redirect(url_for('ponto.admin_view'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar ponto: {str(e)}', 'error')
    
    return render_template('ponto/criar.html', usuarios=usuarios)
