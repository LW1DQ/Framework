"""
Tests de Integración para el Sistema Multi-Agente A2A
"""

import pytest
import time
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

# Importar componentes del sistema
from utils.state import AgentState, create_initial_state
from agents.researcher import research_node
from agents.coder import coder_node
from agents.simulator import simulator_node
from agents.optimizer_refactored import optimizer_node
from agents.analyst import analyst_node
from utils.dependency_injection import get_di_container, Environment, initialize_di


@pytest.fixture(scope="module")
def test_container():
    """Fixture que proporciona un contenedor de DI para testing"""
    # Inicializar container para testing
    container = initialize_di(Environment.TESTING)
    
    # Mock de servicios externos
    with patch('utils.dependency_injection.requests.Session') as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"models": [{"name": "llama3.1:8b"}]}
        mock_session.return_value.get.return_value = mock_response
        
        yield container


@pytest.fixture
def sample_state():
    """Estado de prueba para los tests"""
    return create_initial_state("Test task", max_iterations=2)


class TestIntegrationWorkflow:
    """Tests de integración del flujo de trabajo completo"""
    
    @pytest.mark.integration
    @pytest.mark.slow
    def test_basic_workflow_integration(self, test_container, sample_state):
        """Test básico del flujo de trabajo completo"""
        print("\n=== Test de Integración Básico ===")
        
        # Simular flujo researcher -> coder
        with patch('agents.researcher.get_reasoning_llm') as mock_llm, \
             patch('agents.coder.get_coding_llm') as mock_coder_llm:
            
            # Mock responses
            mock_llm.return_value.invoke.return_value.content = """
            Investigación sobre protocolos AODV.
            Papers relevantes encontrados sobre optimización de rutas.
            """
            
            mock_coder_llm.return_value.invoke.return_value.content = """
            #!/usr/bin/env python3
            # Código NS-3 para simulación AODV
            import ns3
            
            # Configuración básica
            def main():
                pass
            """
            
            # 1. Researcher
            result = research_node(sample_state.copy())
            assert 'research_notes' in result
            assert len(result['research_notes']) > 0
            
            # 2. Coder
            result = coder_node(result.copy())
            assert 'code_snippet' in result
            assert len(result['code_snippet']) > 0
            assert result.get('code_validated', False) is True
            
            print("✅ Flujo básico researcher -> coder funciona correctamente")
    
    @pytest.mark.integration
    @pytest.mark.requires_ns3
    def test_simulation_workflow(self, test_container, sample_state):
        """Test del flujo de simulación"""
        print("\n=== Test de Flujo de Simulación ===")
        
        # Preparar estado con código
        sample_state['code_snippet'] = '''
        #!/usr/bin/env python3
        import sys
        sys.path.insert(0, "/home/diego/ns3/build/bindings/python")
        
        def main():
            print("Simulación de prueba")
            return 0
        
        if __name__ == "__main__":
            main()
        '''
        
        with patch('agents.simulator.get_coding_llm') as mock_llm:
            # Mock response con código mejorado
            mock_llm.return_value.invoke.return_value.content = '''
            #!/usr/bin/env python3
            import sys
            sys.path.insert(0, "/home/diego/ns3/build/bindings/python")
            import ns.core
            import ns.network
            
            def main():
                print("Simulación NS-3 mejorada")
                return 0
            
            if __name__ == "__main__":
                main()
            '''
            
            result = simulator_node(sample_state.copy())
            
            assert 'simulation_status' in result
            assert result['simulation_status'] in ['pending', 'running', 'completed', 'failed']
            
            print(f"✅ Estado de simulación: {result['simulation_status']}")
    
    @pytest.mark.integration
    def test_optimization_workflow(self, test_container, sample_state):
        """Test del flujo de optimización"""
        print("\n=== Test de Flujo de Optimización ===")
        
        # Preparar estado con métricas pobres
        sample_state['metrics'] = {
            'avg_pdr': 65.5,
            'avg_delay': 150.3,
            'avg_throughput': 0.45,
            'success_rate': 70.0
        }
        
        sample_state['code_snippet'] = "# Código AODV de prueba"
        
        with patch('agents.optimizer_refactored.get_reasoning_llm') as mock_llm:
            mock_llm.return_value.invoke.return_value.content = """
            Resumen ejecutivo de optimización:
            - Problemas principales: PDR bajo, delay alto
            - Soluciones: Control de congestión, optimización de rutas
            - Impacto esperado: 25-35% mejora en rendimiento
            """
            
            result = optimizer_node(sample_state.copy())
            
            assert 'optimization_proposal' in result
            assert len(result['optimization_proposal']) > 0
            assert 'bottlenecks' in result
            assert 'performance_grade' in result
            
            print(f"✅ Optimización generada - Grado: {result['performance_grade']}")
    
    @pytest.mark.integration
    def test_analysis_workflow(self, test_container, sample_state):
        """Test del flujo de análisis"""
        print("\n=== Test de Flujo de Análisis ===")
        
        # Preparar estado con resultados de simulación
        sample_state['simulation_logs'] = "/tmp/test_simulation.xml"
        sample_state['pcap_files'] = ["/tmp/test.pcap"]
        
        with patch('agents.analyst.get_reasoning_llm') as mock_llm, \
             patch('agents.analyst.analyze_pcap_traces') as mock_analyze:
            
            mock_analyze.return_value = {
                'packet_loss': 15.2,
                'throughput': 1.2,
                'delay': 45.6
            }
            
            mock_llm.return_value.invoke.return_value.content = """
            {
                "kpis": {
                    "avg_pdr": 84.8,
                    "avg_delay": 45.6,
                    "avg_throughput": 1.2
                },
                "analysis": "Rendimiento aceptable con oportunidades de mejora"
            }
            """
            
            result = analyst_node(sample_state.copy())
            
            assert 'analysis_results' in result
            assert 'metrics' in result
            assert len(result['metrics']) > 0
            
            print(f"✅ Análisis completado - Métricas: {len(result['metrics'])}")


class TestPerformanceBenchmarks:
    """Tests de rendimiento del sistema"""
    
    @pytest.mark.performance
    def test_state_management_performance(self):
        """Benchmark de operaciones de estado"""
        print("\n=== Benchmark de Gestión de Estado ===")
        
        iterations = 1000
        
        # Test creación de estado
        start_time = time.time()
        for i in range(iterations):
            state = create_initial_state(f"Task {i}")
        creation_time = time.time() - start_time
        
        print(f"Creación de {iterations} estados: {creation_time:.3f}s")
        print(f"Promedio por estado: {creation_time/iterations*1000:.3f}ms")
        
        # Test modificación de estado
        state = create_initial_state("Performance test")
        start_time = time.time()
        
        for i in range(iterations):
            state['messages'].append(f"Message {i}")
            state['iteration_count'] += 1
        
        modification_time = time.time() - start_time
        
        print(f"Modificación de {iterations} mensajes: {modification_time:.3f}s")
        
        # Aserciones de rendimiento
        assert creation_time < 1.0, f"Creación muy lenta: {creation_time:.3f}s"
        assert modification_time < 0.5, f"Modificación muy lenta: {modification_time:.3f}s"
    
    @pytest.mark.performance
    def test_di_container_performance(self):
        """Benchmark del contenedor de inyección de dependencias"""
        print("\n=== Benchmark de Contenedor DI ===")
        
        iterations = 100
        
        # Test inicialización
        start_time = time.time()
        for i in range(iterations):
            container = initialize_di(Environment.TESTING)
        initialization_time = time.time() - start_time
        
        print(f"Inicialización de {iterations} contenedores: {initialization_time:.3f}s")
        
        # Test obtención de servicios
        container = initialize_di(Environment.TESTING)
        start_time = time.time()
        
        for i in range(iterations):
            try:
                container.get_reasoning_llm()
            except:
                pass  # Ignorar errores de conexión en testing
        
        service_time = time.time() - start_time
        print(f"Obtención de {iterations} servicios: {service_time:.3f}s")
        
        # Aserciones de rendimiento
        assert initialization_time < 5.0, f"Inicialización muy lenta: {initialization_time:.3f}s"
    
    @pytest.mark.performance
    def test_agent_function_performance(self):
        """Benchmark de funciones de agentes"""
        print("\n=== Benchmark de Funciones de Agentes ===")
        
        # Preparar estado de prueba
        state = create_initial_state("Performance test", max_iterations=1)
        
        # Test performance analyzer
        with patch('agents.optimizer_refactored.get_reasoning_llm'):
            from agents.optimization.performance_analyzer import PerformanceAnalyzer
            
            metrics = {
                'avg_pdr': 85.0,
                'avg_delay': 100.0,
                'avg_throughput': 1.0
            }
            
            iterations = 100
            start_time = time.time()
            
            for i in range(iterations):
                bottlenecks = PerformanceAnalyzer.analyze_bottlenecks(metrics)
                grade, score = PerformanceAnalyzer.get_performance_grade(bottlenecks)
            
            analysis_time = time.time() - start_time
            print(f"Análisis de rendimiento {iterations} veces: {analysis_time:.3f}s")
            print(f"Promedio por análisis: {analysis_time/iterations*1000:.3f}ms")
            
            assert analysis_time < 1.0, f"Análisis muy lento: {analysis_time:.3f}s"


class TestErrorHandling:
    """Tests de manejo de errores y resiliencia"""
    
    @pytest.mark.integration
    def test_workflow_error_recovery(self, sample_state):
        """Test de recuperación de errores en el flujo"""
        print("\n=== Test de Recuperación de Errores ===")
        
        # Simular error en researcher
        with patch('agents.researcher.get_reasoning_llm') as mock_llm:
            mock_llm.side_effect = Exception("LLM connection error")
            
            result = research_node(sample_state.copy())
            
            assert 'errors' in result
            assert len(result['errors']) > 0
            assert 'LLM connection error' in str(result['errors'][0])
            
            print("✅ Error detectado y registrado correctamente")
    
    @pytest.mark.integration
    def test_iteration_limit_enforcement(self, sample_state):
        """Test de límite de iteraciones"""
        print("\n=== Test de Límite de Iteraciones ===")
        
        # Establecer límite bajo
        sample_state['max_iterations'] = 1
        sample_state['iteration_count'] = 1
        
        with patch('agents.coder.get_coding_llm') as mock_llm:
            mock_llm.return_value.invoke.return_value.content = "Código inválido"
            
            result = coder_node(sample_state.copy())
            
            # Verificar que se respeta el límite
            assert result['iteration_count'] <= sample_state['max_iterations']
            
            print(f"✅ Límite de iteraciones respetado: {result['iteration_count']}/{sample_state['max_iterations']}")


class TestSystemScalability:
    """Tests de escalabilidad del sistema"""
    
    @pytest.mark.performance
    @pytest.mark.slow
    def test_concurrent_state_operations(self):
        """Test de operaciones concurrentes con estado"""
        print("\n=== Test de Operaciones Concurrentes ===")
        
        import threading
        import concurrent.futures
        
        def worker_task(task_id):
            """Tarea worker que manipula estado"""
            state = create_initial_state(f"Task {task_id}")
            
            # Simular procesamiento
            for i in range(10):
                state['messages'].append(f"Message {i}")
                state['iteration_count'] += 1
            
            return len(state['messages']), state['iteration_count']
        
        # Ejecutar tareas concurrentes
        num_threads = 10
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker_task, i) for i in range(num_threads)]
            
            results = [future.result() for future in futures]
        
        # Verificar resultados
        for messages, iterations in results:
            assert messages == 10, f"Messages incorrect: {messages}"
            assert iterations == 10, f"Iterations incorrect: {iterations}"
        
        print(f"✅ {num_threads} tareas concurrentes completadas exitosamente")
    
    @pytest.mark.performance
    def test_memory_usage_scaling(self):
        """Test de uso de memoria con estados grandes"""
        print("\n=== Test de Escalabilidad de Memoria ===")
        
        import psutil
        import os
        
        # Medir memoria inicial
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Crear múltiples estados grandes
        states = []
        for i in range(100):
            state = create_initial_state(f"Large task {i}")
            
            # Añadir datos grandes
            state['research_notes'] = [f"Note {j}" * 1000 for j in range(100)]
            state['papers_found'] = [{'title': f"Paper {j}", 'content': 'x' * 1000} for j in range(50)]
            state['messages'] = [f"Message {j}" * 500 for j in range(200)]
            
            states.append(state)
        
        # Medir memoria final
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memoria inicial: {initial_memory:.1f} MB")
        print(f"Memoria final: {final_memory:.1f} MB")
        print(f"Aumento: {memory_increase:.1f} MB")
        print(f"Promedio por estado: {memory_increase/100:.2f} MB")
        
        # Verificar que el aumento sea razonable (< 50MB por estado)
        assert memory_increase/100 < 50, f"Uso de memoria excesivo: {memory_increase/100:.2f} MB/estado"
        
        print("✅ Uso de memoria dentro de límites aceptables")


if __name__ == "__main__":
    # Ejecutar tests específicos para desarrollo
    pytest.main([__file__, "-v", "-m", "integration", "--tb=short"])