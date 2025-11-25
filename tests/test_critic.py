import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock dependencies
sys.modules["langchain_ollama"] = MagicMock()
sys.modules["utils.logging_utils"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["chromadb.config"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["semanticscholar"] = MagicMock()
sys.modules["arxiv"] = MagicMock()
sys.modules["agents.ns3_ai_integration"] = MagicMock()

# Import critic module
import importlib.util
spec = importlib.util.spec_from_file_location("agents.critic", PROJECT_ROOT / "agents/critic.py")
critic_module = importlib.util.module_from_spec(spec)
sys.modules["agents.critic"] = critic_module
spec.loader.exec_module(critic_module)

class TestCriticAgent(unittest.TestCase):
    
    @patch('agents.critic.ChatOllama')
    def test_critic_approval(self, mock_llm):
        """Test critic approving valid code"""
        # Mock LLM response
        mock_instance = mock_llm.return_value
        mock_instance.invoke.return_value.content = '{"approved": true, "critique": "Code looks good"}'
        
        state = {
            "task": "Test Task",
            "code_snippet": "print('valid code')",
            "iteration": 0,
            "audit_trail": []
        }
        
        result = critic_module.critic_node(state)
        
        self.assertTrue(result['critic_approved'])
        self.assertEqual(result['critique'], "Code looks good")
        self.assertIn('approved', result['audit_trail'][-1]['action'])

    @patch('agents.critic.ChatOllama')
    def test_critic_rejection(self, mock_llm):
        """Test critic rejecting invalid logic"""
        # Mock LLM response
        mock_instance = mock_llm.return_value
        mock_instance.invoke.return_value.content = '{"approved": false, "critique": "Logic error: wrong protocol"}'
        
        state = {
            "task": "Test Task",
            "code_snippet": "print('wrong protocol')",
            "iteration": 0,
            "audit_trail": []
        }
        
        result = critic_module.critic_node(state)
        
        self.assertFalse(result['critic_approved'])
        self.assertEqual(result['critique'], "Logic error: wrong protocol")
        self.assertIn('rejected', result['audit_trail'][-1]['action'])

    @patch('agents.critic.ChatOllama')
    def test_critic_fallback_parsing(self, mock_llm):
        """Test critic parsing non-JSON response"""
        # Mock LLM response (plain text)
        mock_instance = mock_llm.return_value
        mock_instance.invoke.return_value.content = "The code is Approved. It looks correct."
        
        state = {
            "task": "Test Task",
            "code_snippet": "print('valid code')",
            "iteration": 0,
            "audit_trail": []
        }
        
        result = critic_module.critic_node(state)
        
        self.assertTrue(result['critic_approved'])
        self.assertIn("Aprobado", result['critique'])

if __name__ == '__main__':
    unittest.main()
