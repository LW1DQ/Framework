import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock ns3_ai module BEFORE importing agents.ns3_ai_integration
mock_ns3_ai = MagicMock()
sys.modules["ns3_ai"] = mock_ns3_ai

# Mock other dependencies to avoid ImportErrors from agents/__init__.py
sys.modules["langchain_ollama"] = MagicMock()
sys.modules["chromadb"] = MagicMock()
sys.modules["chromadb.config"] = MagicMock()
sys.modules["sentence_transformers"] = MagicMock()
sys.modules["semanticscholar"] = MagicMock()
sys.modules["arxiv"] = MagicMock()
sys.modules["utils.logging_utils"] = MagicMock()

# Import module under test
import agents.ns3_ai_integration as ns3_ai_module

class MockRingBuffer:
    """Simulates ns3_ai.RingBuffer behavior"""
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.data = []

    def is_empty(self):
        return len(self.data) == 0

    def get(self):
        if self.data:
            return self.data.pop(0)
        return None

    def put(self, item):
        self.data.append(item)

class TestNS3AIIntegration(unittest.TestCase):
    
    def setUp(self):
        # Reset mock
        ns3_ai_module.HAS_NS3_AI = True
        ns3_ai_module.HAS_TORCH = True 
        
        # Inject mock torch
        self.mock_torch = MagicMock()
        ns3_ai_module.torch = self.mock_torch
        
        # Patch RingBuffer with our Mock
        self.mock_rb_patcher = patch('agents.ns3_ai_integration.RingBuffer', side_effect=MockRingBuffer)
        self.mock_rb = self.mock_rb_patcher.start()

    def tearDown(self):
        self.mock_rb_patcher.stop()

    def test_agent_initialization(self):
        """Test that NS3AIAgent initializes correctly with RingBuffer"""
        agent = ns3_ai_module.NS3AIAgent(shm_name="test_shm")
        self.assertIsNotNone(agent.rb)
        self.assertEqual(agent.rb.name, "test_shm")
        self.assertIsNotNone(agent.policy)

    def test_interaction_loop_logic(self):
        """Test the read-inference-write loop"""
        agent = ns3_ai_module.NS3AIAgent(shm_name="test_shm")
        
        # Inject mock data into RingBuffer (simulating NS-3 writing state)
        # In the real code, get() returns bytes, but our mock agent logic 
        # currently generates random state for demo. 
        # We verify that the loop runs and calls is_empty.
        
        # Mock is_empty to return False once (data available), then True (empty, wait), then raise StopIteration to break loop
        # But run_interaction_loop has a max_steps counter, so we just need it to run a few steps.
        
        # Let's mock the internal logic of run_interaction_loop slightly to verify flow
        # The current implementation of run_interaction_loop uses a while loop with time.sleep
        # We don't want to sleep in tests.
        
        with patch('time.sleep', return_value=None):
            # Pre-fill buffer so is_empty returns False initially
            agent.rb.put(b'dummy_data') 
            agent.rb.put(b'dummy_data')
            
            # Run for 2 steps
            agent.run_interaction_loop(max_steps=2)
            
            # Verify that we processed 2 steps
            # Since we didn't mock the internal state generation (it uses np.random), 
            # we just ensure no exceptions were raised and flow completed.
            pass

    def test_code_generation(self):
        """Test that NS-3 script generation includes ns3-ai imports"""
        code = ns3_ai_module.generate_ns3_ai_code("AODV", 10, 500)
        self.assertIn("from ns3_ai import RingBuffer", code)
        self.assertIn("RingBuffer(\"ns3_ai_shm\"", code)

if __name__ == '__main__':
    unittest.main()
