
import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.errors import (
    A2AError, SimulationError, TimeoutError, CompilationError, CodeGenerationError
)
from agents.simulator import run_ns3_simulation
from agents.coder import generate_code

class TestExceptions(unittest.TestCase):
    def test_exception_hierarchy(self):
        """Verify exception inheritance"""
        self.assertTrue(issubclass(SimulationError, A2AError))
        self.assertTrue(issubclass(TimeoutError, SimulationError))
        self.assertTrue(issubclass(CompilationError, A2AError)) # Actually AgentError -> A2AError
        self.assertTrue(issubclass(CodeGenerationError, A2AError))

    @patch('subprocess.run')
    def test_simulator_timeout(self, mock_run):
        """Verify run_ns3_simulation raises TimeoutError"""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd='ns3', timeout=10)
        
        with self.assertRaises(TimeoutError):
            run_ns3_simulation(Path('scratch/test.py'), 10)

    @patch('subprocess.run')
    def test_simulator_compilation_error(self, mock_run):
        """Verify run_ns3_simulation raises CompilationError on syntax error"""
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "SyntaxError: invalid syntax"
        mock_run.return_value = mock_result
        
        with self.assertRaises(CompilationError):
            run_ns3_simulation(Path('scratch/test.py'), 10)

    @patch('agents.coder.ChatOllama')
    def test_coder_generation_error(self, mock_ollama_cls):
        """Verify generate_code raises CodeGenerationError on LLM failure"""
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("LLM connection failed")
        mock_ollama_cls.return_value = mock_llm
        
        # We need to mock memory to avoid other errors
        with patch('agents.coder.memory') as mock_memory:
            with self.assertRaises(CodeGenerationError):
                generate_code("Task", "Notes")

if __name__ == '__main__':
    unittest.main()
