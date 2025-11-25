import unittest
import sys
from unittest.mock import MagicMock, patch
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock dependencies
sys.modules["langchain_ollama"] = MagicMock()
sys.modules["langchain_core.messages"] = MagicMock()
sys.modules["langchain_core.prompts"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["semanticscholar"] = MagicMock()
sys.modules["arxiv"] = MagicMock()
sys.modules["utils.logging_utils"] = MagicMock()

# Import agents using importlib to avoid side effects
import importlib.util

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[f"agents.{name}"] = module
    spec.loader.exec_module(module)
    return module

researcher = load_module("researcher", PROJECT_ROOT / "agents" / "researcher.py")
coder = load_module("coder", PROJECT_ROOT / "agents" / "coder.py")
simulator = load_module("simulator", PROJECT_ROOT / "agents" / "simulator.py")

class TestAgents(unittest.TestCase):

    @patch('agents.researcher.search_semantic_scholar')
    @patch('agents.researcher.ChatOllama')
    def test_researcher_node(self, mock_llm, mock_search):
        """Test researcher agent logic"""
        # Setup mock LLM
        mock_instance = mock_llm.return_value
        mock_instance.invoke.return_value.content = "Research summary"
        
        # Setup mock search to return papers
        mock_search.return_value = [{
            'title': 'Test Paper',
            'abstract': 'Abstract',
            'year': 2024,
            'citations': 10,
            'url': 'http://test.com',
            'relevance_score': 90
        }]
        
        state = {
            "task": "Test Task",
            "iterations": 0,
            "max_iterations": 5,
            "research_notes": [],
            "papers_found": [],
            "code_snippet": "",
            "simulation_results": {},
            "logs": [],
            "audit_trail": []
        }
        
        result = researcher.research_node(state)
        
        self.assertIn("research_notes", result)
        self.assertIn("Research summary", result["research_notes"][0])

    @patch('agents.coder.ChatOllama')
    def test_coder_node(self, mock_llm):
        """Test coder agent logic"""
        mock_instance = mock_llm.return_value
        mock_instance.invoke.return_value.content = "```python\nprint('Hello')\n```"
        
        state = {
            "task": "Test Task",
            "research_notes": ["Some info"],
            "code_snippet": "",
            "logs": [],
            "iteration_count": 0,
            "audit_trail": []
        }
        
        result = coder.coder_node(state)
        
        self.assertIn("code_snippet", result)
        self.assertIn("print('Hello')", result["code_snippet"])

    @patch('agents.simulator.subprocess.run')
    def test_simulator_node_success(self, mock_run):
        """Test simulator agent success path"""
        # Mock successful execution
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Simulation finished nodes: 20 time: 100.0 seconds"
        mock_run.return_value.stderr = ""
        
        # Mock file reading for results
        with patch('builtins.open', unittest.mock.mock_open(read_data='<results><pdr>95.5</pdr></results>')):
            with patch('os.path.exists', return_value=True):
                # Mock stat().st_size
                with patch('pathlib.Path.stat') as mock_stat:
                    mock_stat.return_value.st_size = 1024
                    
                    # Mock mkdir to avoid filesystem errors
                    with patch('pathlib.Path.mkdir'):
                        
                        state = {
                            "code_snippet": "import ns.core\n...",
                            "task": "Test Task",
                            "logs": [],
                            "iteration_count": 0,
                            "audit_trail": []
                        }
                        
                        # We need to mock validate_code_before_execution to pass
                        with patch('agents.simulator.validate_code_before_execution', return_value=(True, "Valid")):
                            # Mock shutil.copy to avoid actual file operations
                            with patch('shutil.copy'):
                                 result = simulator.simulator_node(state)
                            
                            self.assertEqual(result["simulation_status"], "completed")

    def test_simulator_node_validation_fail(self):
        """Test simulator agent validation failure"""
        state = {
            "code_snippet": "bad code",
            "task": "Test Task",
            "logs": [],
            "iteration_count": 0,
            "audit_trail": []
        }
        
        with patch('agents.simulator.validate_code_before_execution', return_value=(False, "Syntax Error")):
            result = simulator.simulator_node(state)
            
            self.assertIn("errors", result)
            self.assertIn("Syntax Error", result["errors"][0])

if __name__ == '__main__':
    unittest.main()
