"""
Tests Unitarios para Agentes del Sistema A2A

Ejecutar con: pytest tests/test_agents.py -v
"""

import pytest
import sys
from pathlib import Path

# Añadir directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.state import create_initial_state, add_audit_entry, increment_iteration
from agents.analyst import calculate_kpis, classify_performance
import pandas as pd


class TestState:
    """Tests para gestión de estado"""
    
    def test_create_initial_state(self):
        """Test creación de estado inicial"""
        state = create_initial_state("Simular AODV con 10 nodos")
        
        assert state['task'] == "Simular AODV con 10 nodos"
        assert state['iteration_count'] == 0
        assert state['max_iterations'] == 5
        assert state['simulation_status'] == "pending"
        assert len(state['errors']) == 0
        assert state['simulation_seed'] is not None
    
    def test_create_initial_state_with_seed(self):
        """Test creación con semilla específica"""
        state = create_initial_state("Test", seed=12345)
        
        assert state['simulation_seed'] == 12345
    
    def test_add_audit_entry(self):
        """Test añadir entrada de auditoría"""
        state = create_initial_state("Test")
        
        update = add_audit_entry(state, "test_agent", "test_action", {'key': 'value'})
        
        assert 'audit_trail' in update
        assert len(update['audit_trail']) == 1
        assert update['audit_trail'][0]['agent'] == "test_agent"
        assert update['audit_trail'][0]['action'] == "test_action"
    
    def test_increment_iteration(self):
        """Test incremento de iteración"""
        state = create_initial_state("Test")
        state['iteration_count'] = 2
        
        update = increment_iteration(state)
        
        assert update['iteration_count'] == 3


class TestAnalyst:
    """Tests para agente Analyst"""
    
    def test_calculate_kpis_basic(self):
        """Test cálculo básico de KPIs"""
        df = pd.DataFrame({
            'pdr': [95.5, 94.2, 96.1],
            'throughput_mbps': [1.2, 1.5, 1.3],
            'avg_delay_ms': [45.2, 50.1, 42.3],
            'tx_packets': [1000, 1000, 1000],
            'rx_packets': [955, 942, 961]
        })
        
        kpis = calculate_kpis(df)
        
        assert 'avg_pdr' in kpis
        assert 90 < kpis['avg_pdr'] < 100
        assert 'avg_delay' in kpis
        assert 'avg_throughput' in kpis
        assert 'performance_grade' in kpis
        assert 'jitter_ms' in kpis
    
    def test_calculate_kpis_empty_dataframe(self):
        """Test con DataFrame vacío"""
        df = pd.DataFrame()
        
        kpis = calculate_kpis(df)
        
        assert kpis == {}
    
    def test_classify_performance_excellent(self):
        """Test clasificación de rendimiento excelente"""
        kpis = {
            'avg_pdr': 96.0,
            'avg_delay': 40.0,
            'success_rate': 98.0
        }
        
        grade = classify_performance(kpis)
        
        assert grade == "Excelente"
    
    def test_classify_performance_poor(self):
        """Test clasificación de rendimiento pobre"""
        kpis = {
            'avg_pdr': 60.0,
            'avg_delay': 250.0,
            'success_rate': 55.0
        }
        
        grade = classify_performance(kpis)
        
        assert grade == "Pobre"


class TestMemory:
    """Tests para memoria episódica"""
    
    def test_memory_add_and_retrieve(self):
        """Test añadir y recuperar experiencias"""
        from utils.memory import EpisodicMemory
        import tempfile
        
        # Crear memoria temporal
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        memory = EpisodicMemory(memory_file=temp_file)
        
        # Añadir experiencia
        memory.add_experience(
            task="Simular AODV",
            code="import ns.core",
            error="AttributeError: no attribute 'core'",
            solution="import ns.core\nimport ns.network"
        )
        
        assert len(memory.experiences) == 1
        
        # Recuperar experiencia similar
        results = memory.retrieve_experience(
            task="Simular AODV",
            error="AttributeError"
        )
        
        assert len(results) > 0
        assert 'relevance' in results[0]
        
        # Limpiar
        import os
        os.unlink(temp_file)
    
    def test_memory_stats(self):
        """Test estadísticas de memoria"""
        from utils.memory import EpisodicMemory
        import tempfile
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        
        memory = EpisodicMemory(memory_file=temp_file)
        
        stats = memory.get_stats()
        
        assert 'total_experiences' in stats
        assert 'memory_file' in stats
        assert 'has_sklearn' in stats
        
        # Limpiar
        import os
        os.unlink(temp_file)


class TestErrors:
    """Tests para excepciones personalizadas"""
    
    def test_custom_exceptions(self):
        """Test jerarquía de excepciones"""
        from utils.errors import (
            A2AError, CompilationError, SimulationError,
            TimeoutError, get_error_class
        )
        
        # Test jerarquía
        assert issubclass(CompilationError, A2AError)
        assert issubclass(SimulationError, A2AError)
        assert issubclass(TimeoutError, SimulationError)
        
        # Test get_error_class
        ErrorClass = get_error_class('CompilationError')
        assert ErrorClass == CompilationError
        
        # Test lanzar y capturar
        with pytest.raises(CompilationError):
            raise CompilationError("Test error")


if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, '-v', '--tb=short'])
