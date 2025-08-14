#!/usr/bin/env python3
"""
Verificação rápida de problemas no sistema SAMAPE
"""

def check_import_issues():
    """Verifica se há problemas de importação"""
    print("🔍 Verificando importações principais...")
    
    try:
        import app
        print("✅ app.py - OK")
    except Exception as e:
        print(f"❌ app.py - ERRO: {e}")
        return False
    
    try:
        import routes
        print("✅ routes.py - OK")
    except Exception as e:
        print(f"❌ routes.py - ERRO: {e}")
        return False
        
    try:
        import models
        print("✅ models.py - OK")
    except Exception as e:
        print(f"❌ models.py - ERRO: {e}")
        return False
        
    return True

def check_database_tables():
    """Verifica estrutura das tabelas"""
    print("\n🗄️ Verificando estrutura do banco de dados...")
    
    try:
        from app import app, db
        from models import StockItem, StockMovement, User
        from sqlalchemy import inspect
        
        with app.app_context():
            # Usar inspector para verificar tabelas
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # Verificar se as tabelas existem
            if 'stock_items' in existing_tables:
                print("✅ Tabela stock_items - OK")
            else:
                print("❌ Tabela stock_items - NÃO ENCONTRADA")
                
            if 'stock_movements' in existing_tables:
                print("✅ Tabela stock_movements - OK")
            else:
                print("❌ Tabela stock_movements - NÃO ENCONTRADA")
                
            if 'users' in existing_tables:
                print("✅ Tabela users - OK")
            else:
                print("❌ Tabela users - NÃO ENCONTRADA")
                
            # Contar registros
            try:
                stock_count = StockItem.query.count()
                print(f"📊 Itens de estoque: {stock_count}")
                
                user_count = User.query.count()
                print(f"👥 Usuários: {user_count}")
                
            except Exception as e:
                print(f"⚠️ Erro ao consultar dados: {e}")
                
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação do banco: {e}")
        return False

def check_routes_registration():
    """Verifica se as rotas estão registradas corretamente"""
    print("\n🛣️ Verificando rotas registradas...")
    
    try:
        from app import app
        
        # Rotas importantes para verificar
        important_routes = [
            '/stock',
            '/estoque/<int:id>/excluir',
            '/stock/item/<int:id>/delete',
            '/stock/new',
            '/stock/<int:id>/view',
            '/stock/<int:id>/edit'
        ]
        
        registered_routes = []
        for rule in app.url_map.iter_rules():
            registered_routes.append(str(rule))
        
        missing_routes = []
        for route in important_routes:
            # Verificar se a rota ou uma similar existe
            route_found = any(route in reg_route or reg_route.startswith(route.split('<')[0]) 
                            for reg_route in registered_routes)
            
            if route_found:
                print(f"✅ Rota {route} - OK")
            else:
                print(f"❌ Rota {route} - NÃO ENCONTRADA")
                missing_routes.append(route)
        
        if missing_routes:
            print(f"\n⚠️ Rotas em falta: {len(missing_routes)}")
            return False
        else:
            print("✅ Todas as rotas principais registradas")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao verificar rotas: {e}")
        return False

def check_csrf_configuration():
    """Verifica configuração CSRF"""
    print("\n🔒 Verificando configuração CSRF...")
    
    try:
        from app import app
        
        csrf_enabled = app.config.get('WTF_CSRF_ENABLED', True)
        print(f"🔐 CSRF Habilitado: {csrf_enabled}")
        
        if not csrf_enabled:
            print("⚠️ AVISO: CSRF está desabilitado - pode causar problemas de segurança")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar CSRF: {e}")
        return False

def main():
    print("🚀 VERIFICAÇÃO RÁPIDA DO SISTEMA SAMAPE")
    print("=" * 50)
    
    issues = []
    
    # Verificações
    if not check_import_issues():
        issues.append("Problemas de importação")
    
    if not check_database_tables():
        issues.append("Problemas no banco de dados")
        
    if not check_routes_registration():
        issues.append("Problemas no registro de rotas")
        
    if not check_csrf_configuration():
        issues.append("Problemas na configuração CSRF")
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)
    
    if not issues:
        print("✅ SISTEMA OK - Nenhum problema detectado")
        print("🌐 Servidor disponível em: http://127.0.0.1:5000")
        print("📦 Estoque disponível em: http://127.0.0.1:5000/stock")
    else:
        print("⚠️ PROBLEMAS ENCONTRADOS:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
            
        print("\n💡 SOLUÇÕES RECOMENDADAS:")
        print("   • Verificar logs do servidor para mais detalhes")
        print("   • Confirmar se todas as migrações foram executadas")
        print("   • Testar funcionalidades manualmente no navegador")

if __name__ == "__main__":
    main()
