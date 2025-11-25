import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
import subprocess

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock dependencies
sys.path.insert(0, str(PROJECT_ROOT))
sys.modules["utils.logging_utils"] = MagicMock()
sys.modules["config.settings"] = MagicMock()
sys.modules["config.settings"].NS3_ROOT = Path("/tmp/ns3")
sys.modules["config.settings"].SIMULATION_TIMEOUT = 60
sys.modules["config.settings"].SIMULATIONS_DIR = Path("/tmp/sims")
sys.modules["langchain_ollama"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["semanticscholar"] = MagicMock()
sys.modules["arxiv"] = MagicMock()

# Mock agents package to avoid importing real agents
sys.modules["agents.researcher"] = MagicMock()
sys.modules["agents.coder"] = MagicMock()
sys.modules["agents.trace_analyzer"] = MagicMock()
sys.modules["agents.analyst"] = MagicMock()
sys.modules["agents.visualizer"] = MagicMock()
sys.modules["agents.github_manager"] = MagicMock()
sys.modules["agents.optimizer"] = MagicMock()
sys.modules["agents.critic"] = MagicMock()

from agents.simulator import simulator_node
from utils.state import create_initial_state

class TestErrorHandling(unittest.TestCase):
    
    @patch('agents.simulator.subprocess.run')
    @patch('agents.simulator.validate_code_before_execution')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('agents.simulator.Path.mkdir')
    @patch('agents.simulator.shutil.copy')
    def test_simulation_crash(self, mock_copy, mock_mkdir, mock_open, mock_validate, mock_run):
        """Test that simulator catches runtime errors"""
        # Setup
        mock_validate.return_value = (True, "Valid")
        
        # Simulate NS-3 crash
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = "Simulation started..."
        mock_process.stderr = "FATAL ERROR: Segmentation fault"
        mock_run.return_value = mock_process
        
        state = create_initial_state("Test Task")
        state['code_snippet'] = "print('hello')"
        
        # Execute
        result = simulator_node(state)
        
        # Verify
        self.assertEqual(result['simulation_status'], 'failed')
        self.assertEqual(result['error_type'], 'SimulationError')
        self.assertIn("Segmentation fault", result['errors'][0])

    @patch('agents.simulator.subprocess.run')
    @patch('agents.simulator.validate_code_before_execution')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('agents.simulator.Path.mkdir')
    @patch('agents.simulator.shutil.copy')
    def test_simulation_timeout(self, mock_copy, mock_mkdir, mock_open, mock_validate, mock_run):
        """Test that simulator catches timeouts"""
        # Setup
        mock_validate.return_value = (True, "Valid")
        
        # Simulate Timeout
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="run", timeout=60)
        
        state = create_initial_state("Test Task")
        state['code_snippet'] = "while True: pass"
        
        # Execute
        result = simulator_node(state)
        
        # Verify
        self.assertEqual(result['simulation_status'], 'failed')
        self.assertEqual(result['error_type'], 'TimeoutError')
        self.assertIn("Timeout", result['errors'][0])

    @patch('agents.simulator.validate_code_before_execution')
    def test_compilation_error(self, mock_validate):
        """Test that simulator catches pre-validation errors"""
        # Setup
        mock_validate.return_value = (False, "SyntaxError: invalid syntax")
        
        state = create_initial_state("Test Task")
        state['code_snippet'] = "invalid python code"
        
        # Execute
        result = simulator_node(state)
        
        # Verify
        self.assertEqual(result['simulation_status'], 'failed')
        self.assertEqual(result['error_type'], 'CompilationError')
        self.assertIn("SyntaxError", result['errors'][0])

if __name__ == '__main__':
    unittest.main()
