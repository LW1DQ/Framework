import unittest
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock dependencies
sys.modules["langgraph"] = MagicMock()
sys.modules["langgraph.graph"] = MagicMock()
sys.modules["langgraph.checkpoint"] = MagicMock()
sys.modules["langgraph.checkpoint.sqlite"] = MagicMock()
sys.modules["langchain_ollama"] = MagicMock()
sys.modules["utils.logging_utils"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["semanticscholar"] = MagicMock()
sys.modules["arxiv"] = MagicMock()
sys.modules["agents.ns3_ai_integration"] = MagicMock()

# Import supervisor using importlib
import importlib.util
spec = importlib.util.spec_from_file_location("supervisor", PROJECT_ROOT / "supervisor.py")
supervisor_module = importlib.util.module_from_spec(spec)
sys.modules["supervisor"] = supervisor_module
spec.loader.exec_module(supervisor_module)

class TestSupervisorLogic(unittest.TestCase):
    
    def setUp(self):
        self.supervisor = supervisor_module.SupervisorOrchestrator()

    def test_should_retry_code_success(self):
        """Test routing when code is valid"""
        state = {
            "simulation_status": "completed",
            "iteration_count": 1,
            "max_iterations": 5,
            "code_validated": True
        }
        
        # Should go to simulator if code is validated
        next_step = self.supervisor._should_retry_code(state)
        self.assertEqual(next_step, "simulator")

    def test_should_retry_code_failure_retry(self):
        """Test routing when validation fails and should retry"""
        state = {
            "simulation_status": "failed",
            "iteration_count": 1,
            "max_iterations": 5,
            "errors": ["Syntax Error"]
        }
        
        # Should go back to coder (retry)
        next_step = self.supervisor._should_retry_code(state)
        self.assertEqual(next_step, "retry")

    def test_should_retry_code_failure_max_retries(self):
        """Test routing when validation fails and max retries reached"""
        state = {
            "simulation_status": "failed",
            "iteration_count": 5,
            "max_iterations": 5,
            "errors": ["Syntax Error"]
        }
        
        # Should end
        next_step = self.supervisor._should_retry_code(state)
        self.assertEqual(next_step, "end")

    def test_should_optimize_continue(self):
        """Test routing when optimization loop should continue"""
        state = {
            "optimization_count": 1,
            "max_iterations": 5,
            "simulation_status": "completed",
            "metrics": {"avg_pdr": 50.0} # Low PDR triggers optimization
        }
        
        # Logic is hardcoded to < 2 optimizations in supervisor.py
        next_step = self.supervisor._should_optimize(state)
        self.assertEqual(next_step, "optimizer")

    def test_should_optimize_stop(self):
        """Test routing when optimization limit reached"""
        state = {
            "optimization_count": 2, # Limit is 2
            "metrics": {"avg_pdr": 50.0}
        }
        
        next_step = self.supervisor._should_optimize(state)
        self.assertEqual(next_step, "visualizer")

if __name__ == '__main__':
    unittest.main()
