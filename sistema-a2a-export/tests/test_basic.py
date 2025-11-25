#!/usr/bin/env python3
"""
Tests Básicos del Sistema A2A

Ejecutar con: pytest tests/test_basic.py -v
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from utils.state import create_initial_state, add_audit_entry, increment_iteration


class TestState:
    """Tests para el estado global"""
    
    def test_create_initial_state(self):
        """Test creación de estado inicial"""
        state = create_initial_state("Tarea de prueba")
        
        assert state['task'] == "Tarea de prueba"
        assert state['iteration_count'] == 0
        assert state['max_iterations'] == 5
        assert len(state['errors']) == 0
        assert len(state['research_notes']) == 0
    
    def test_add_audit_entry(self):
        """Test añadir entrada de auditoría"""
        state = create_initial_state("Test")
        
        entry = add_audit_entry(state, "test_agent", "test_action", {'key': 'value'})
        
        assert 'audit_trail' in entry
        assert len(entry['audit_trail']) == 1
        assert entry['audit_trail'][0]['agent'] == "test_agent"
    
    def test_increment_iteration(self):
        """Test incrementar iteración"""
        state = create_initial_state("Test")
        state['iteration_count'] = 2
        
        result = increment_iteration(state)
        
        assert result['iteration_count'] == 3


class TestConfiguration:
    """Tests para configuración"""
    
    def test_import_settings(self):
        """Test importar configuración"""
        from config import settings
        
        assert hasattr(settings, 'NS3_ROOT')
        assert hasattr(settings, 'OLLAMA_BASE_URL')
        assert hasattr(settings, 'MODEL_REASONING')
    
    def test_paths_exist(self):
        """Test que los directorios existen"""
        from config.settings import SIMULATIONS_DIR, DATA_DIR, LOGS_DIR
        
        assert SIMULATIONS_DIR.exists()
        assert DATA_DIR.exists()
        assert LOGS_DIR.exists()


class TestAgents:
    """Tests para agentes"""
    
    def test_researcher_import(self):
        """Test importar agente investigador"""
        from agents.researcher import research_node
        
        assert callable(research_node)
    
    def test_coder_import(self):
        """Test importar agente programador"""
        from agents.coder import coder_node
        
        assert callable(coder_node)
    
    def test_simulator_import(self):
        """Test importar agente simulador"""
        from agents.simulator import simulator_node
        
        assert callable(simulator_node)
    
    def test_analyst_import(self):
        """Test importar agente analista"""
        from agents.analyst import analyst_node
        
        assert callable(analyst_node)
    
    def test_visualizer_import(self):
        """Test importar agente visualizador"""
        from agents.visualizer import visualizer_node
        
        assert callable(visualizer_node)


class TestSupervisor:
    """Tests para el supervisor"""
    
    def test_supervisor_import(self):
        """Test importar supervisor"""
        from supervisor import SupervisorOrchestrator
        
        assert SupervisorOrchestrator is not None
    
    def test_supervisor_creation(self):
        """Test crear instancia del supervisor"""
        from supervisor import SupervisorOrchestrator
        
        supervisor = SupervisorOrchestrator()
        
        assert supervisor is not None
        assert hasattr(supervisor, 'workflow')
        assert hasattr(supervisor, 'app')


class TestIntegration:
    """Tests de integración básicos"""
    
    @pytest.mark.slow
    def test_researcher_execution(self):
        """Test ejecutar agente investigador"""
        from agents.researcher import research_node
        from utils.state import create_initial_state
        
        state = create_initial_state("Test de búsqueda de papers")
        result = research_node(state)
        
        assert 'research_notes' in result
        assert isinstance(result['research_notes'], list)
    
    @pytest.mark.slow
    def test_coder_execution(self):
        """Test ejecutar agente programador"""
        from agents.coder import coder_node
        from utils.state import create_initial_state
        
        state = create_initial_state("Simular AODV con 10 nodos")
        state['research_notes'] = ["AODV es un protocolo reactivo"]
        
        result = coder_node(state)
        
        assert 'code_snippet' in result
        assert len(result['code_snippet']) > 0


class TestUtilities:
    """Tests para utilidades"""
    
    def test_state_import(self):
        """Test importar módulo de estado"""
        from utils import state
        
        assert hasattr(state, 'AgentState')
        assert hasattr(state, 'create_initial_state')
    
    def test_state_structure(self):
        """Test estructura del estado"""
        from utils.state import AgentState
        
        # Verificar que tiene los campos necesarios
        required_fields = [
            'task', 'research_notes', 'code_snippet',
            'simulation_logs', 'errors', 'iteration_count'
        ]
        
        # AgentState es un TypedDict, verificar anotaciones
        annotations = AgentState.__annotations__
        
        for field in required_fields:
            assert field in annotations


class TestExamples:
    """Tests para ejemplos"""
    
    def test_ejemplo_basico_import(self):
        """Test importar ejemplo básico"""
        sys.path.insert(0, str(Path(__file__).parent.parent / "examples"))
        
        import ejemplo_basico
        
        assert hasattr(ejemplo_basico, 'ejemplo_simple')


class TestScripts:
    """Tests para scripts"""
    
    def test_check_system_import(self):
        """Test importar script de verificación"""
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        
        # Verificar que el archivo existe
        check_system_path = Path(__file__).parent.parent / "scripts" / "check_system.py"
        assert check_system_path.exists()


# Configuración de pytest
def pytest_configure(config):
    """Configuración de pytest"""
    config.addinivalue_line(
        "markers", "slow: marca tests que tardan mucho tiempo"
    )


if __name__ == "__main__":
    # Ejecutar tests
    pytest.main([__file__, "-v"])
