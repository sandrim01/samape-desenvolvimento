"""
Script de monitoramento de performance em tempo real
Execute para identificar gargalos no sistema
"""

import time
import psutil
import threading
from datetime import datetime
import logging
import requests
import os
import json

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('performance_monitor.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self, app_url="http://localhost:5000"):
        self.app_url = app_url
        self.monitoring = False
        self.stats = []
        
    def get_system_stats(self):
        """Coleta estatísticas do sistema"""
        return {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent,
            'network_connections': len(psutil.net_connections()),
            'processes': len(psutil.pids())
        }
    
    def test_endpoint_performance(self, endpoint, expected_time=2.0):
        """Testa performance de um endpoint específico"""
        url = f"{self.app_url}{endpoint}"
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            end_time = time.time()
            
            response_time = end_time - start_time
            status = "OK" if response_time <= expected_time else "SLOW"
            
            result = {
                'endpoint': endpoint,
                'response_time': round(response_time, 3),
                'status_code': response.status_code,
                'status': status,
                'expected_time': expected_time,
                'timestamp': datetime.now().isoformat()
            }
            
            if status == "SLOW":
                logger.warning(f"SLOW ENDPOINT: {endpoint} took {response_time:.3f}s (expected <= {expected_time}s)")
            else:
                logger.info(f"OK: {endpoint} - {response_time:.3f}s")
                
            return result
            
        except requests.RequestException as e:
            logger.error(f"Error testing {endpoint}: {e}")
            return {
                'endpoint': endpoint,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_performance_tests(self):
        """Executa testes de performance em endpoints críticos"""
        critical_endpoints = [
            ('/dashboard', 3.0),
            ('/dashboard/fast', 1.0),
            ('/os', 5.0),
            ('/clients', 3.0),
            ('/equipment', 3.0),
        ]
        
        logger.info("🚀 Iniciando testes de performance...")
        
        results = []
        system_stats = self.get_system_stats()
        
        logger.info(f"Sistema - CPU: {system_stats['cpu_percent']}%, "
                   f"RAM: {system_stats['memory_percent']}%, "
                   f"Conexões: {system_stats['network_connections']}")
        
        for endpoint, expected_time in critical_endpoints:
            result = self.test_endpoint_performance(endpoint, expected_time)
            results.append(result)
            time.sleep(0.5)  # Pequena pausa entre testes
        
        # Salvar resultados
        report = {
            'system_stats': system_stats,
            'endpoint_tests': results,
            'summary': self.generate_summary(results)
        }
        
        self.save_report(report)
        return report
    
    def generate_summary(self, results):
        """Gera resumo dos testes"""
        total_tests = len(results)
        slow_tests = len([r for r in results if r.get('status') == 'SLOW'])
        error_tests = len([r for r in results if 'error' in r])
        
        avg_time = sum([r.get('response_time', 0) for r in results if 'response_time' in r])
        avg_time = avg_time / max(1, total_tests - error_tests)
        
        return {
            'total_tests': total_tests,
            'slow_endpoints': slow_tests,
            'error_endpoints': error_tests,
            'average_response_time': round(avg_time, 3),
            'health_score': round((total_tests - slow_tests - error_tests) / total_tests * 100, 1)
        }
    
    def save_report(self, report):
        """Salva relatório em arquivo"""
        filename = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📊 Relatório salvo em: {filename}")
        
        # Log do resumo
        summary = report['summary']
        logger.info(f"📈 RESUMO - Health Score: {summary['health_score']}%, "
                   f"Tempo médio: {summary['average_response_time']}s, "
                   f"Endpoints lentos: {summary['slow_endpoints']}/{summary['total_tests']}")
    
    def continuous_monitoring(self, interval=60):
        """Monitoramento contínuo a cada X segundos"""
        logger.info(f"🔄 Iniciando monitoramento contínuo (a cada {interval}s)")
        self.monitoring = True
        
        while self.monitoring:
            try:
                self.run_performance_tests()
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("⏹️  Monitoramento interrompido pelo usuário")
                self.monitoring = False
                break
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(10)  # Pausa maior em caso de erro

def main():
    monitor = PerformanceMonitor()
    
    print("=" * 60)
    print("🔧 MONITOR DE PERFORMANCE DO SISTEMA SAMAPE")
    print("=" * 60)
    print("1. Teste único de performance")
    print("2. Monitoramento contínuo (Ctrl+C para parar)")
    print("3. Sair")
    
    choice = input("\nEscolha uma opção: ").strip()
    
    if choice == "1":
        print("\n🚀 Executando teste único...")
        report = monitor.run_performance_tests()
        print(f"\n✅ Teste concluído! Health Score: {report['summary']['health_score']}%")
        
    elif choice == "2":
        interval = input("Intervalo entre testes (segundos, padrão=60): ").strip()
        interval = int(interval) if interval.isdigit() else 60
        monitor.continuous_monitoring(interval)
        
    else:
        print("👋 Saindo...")

if __name__ == "__main__":
    main()