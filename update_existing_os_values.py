"""
Script para atualizar Ordens de Serviço existentes com valores NULL nos novos campos
"""
import psycopg2

# Configuração do banco de dados
DB_CONFIG = {
    'host': 'trolley.proxy.rlwy.net',
    'port': 22285,
    'database': 'railway',
    'user': 'postgres',
    'password': 'qUngJAyBvLWQdkmSkZEjjEoMoDVzOBnx'
}

def update_existing_orders():
    """Atualiza todas as OSs existentes para garantir valores válidos nos novos campos"""
    
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("Conectado ao banco de dados com sucesso!")
        
        # Atualizar valores NULL para 0 nos novos campos
        update_query = """
        UPDATE service_order 
        SET 
            km_rate = COALESCE(km_rate, 0),
            km_value = COALESCE(km_value, 0),
            labor_value = COALESCE(labor_value, 0),
            parts_value = COALESCE(parts_value, 0),
            total_value = COALESCE(total_value, 0)
        WHERE 
            km_rate IS NULL OR
            km_value IS NULL OR
            labor_value IS NULL OR
            parts_value IS NULL OR
            total_value IS NULL;
        """
        
        cursor.execute(update_query)
        affected_rows = cursor.rowcount
        
        print(f"✓ {affected_rows} ordem(ns) de serviço atualizada(s)")
        
        # Verificar quantas OSs existem no total
        cursor.execute("SELECT COUNT(*) FROM service_order;")
        total_orders = cursor.fetchone()[0]
        print(f"Total de OSs no banco: {total_orders}")
        
        # Mostrar algumas OSs para verificação
        cursor.execute("""
            SELECT id, client_id, km_inicial, km_final, km_total, km_rate, km_value, 
                   labor_value, parts_value, total_value, estimated_value
            FROM service_order 
            ORDER BY id DESC 
            LIMIT 5;
        """)
        
        print("\nÚltimas 5 OSs (verificação):")
        print("-" * 120)
        print(f"{'ID':<5} {'Cliente':<10} {'KM Ini':<10} {'KM Fin':<10} {'KM Tot':<10} {'KM Rate':<10} {'KM Val':<10} {'Mão Obra':<12} {'Peças':<10} {'Total':<10} {'Estimado':<10}")
        print("-" * 120)
        
        for row in cursor.fetchall():
            print(f"{row[0]:<5} {row[1]:<10} {row[2] or 0:<10.2f} {row[3] or 0:<10.2f} {row[4] or 0:<10.2f} "
                  f"{row[5] or 0:<10.2f} {row[6] or 0:<10.2f} {row[7] or 0:<12.2f} {row[8] or 0:<10.2f} "
                  f"{row[9] or 0:<10.2f} {row[10] or 0:<10.2f}")
        
        # Commit das alterações
        conn.commit()
        print("\n✓ Todas as alterações foram salvas no banco de dados!")
        
        cursor.close()
        conn.close()
        
        print("\n✓ Script executado com sucesso!")
        print("\nAgora as OSs existentes devem exibir os campos corretamente nos templates.")
        
    except Exception as e:
        print(f"\n✗ Erro ao atualizar OSs: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == '__main__':
    print("=" * 120)
    print("ATUALIZAÇÃO DE ORDENS DE SERVIÇO EXISTENTES")
    print("=" * 120)
    print("\nEste script irá atualizar todas as OSs existentes para garantir que os novos campos")
    print("tenham valores válidos (0 em vez de NULL).\n")
    
    update_existing_orders()
