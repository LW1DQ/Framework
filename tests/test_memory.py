import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock dependencies before importing utils.memory
sys.modules["chromadb"] = MagicMock()
sys.modules["chromadb.config"] = MagicMock()
sys.modules["config.settings"] = MagicMock()

# Import memory module
import importlib.util
spec = importlib.util.spec_from_file_location("utils.memory", PROJECT_ROOT / "utils/memory.py")
memory_module = importlib.util.module_from_spec(spec)
sys.modules["utils.memory"] = memory_module
spec.loader.exec_module(memory_module)

class TestEpisodicMemory(unittest.TestCase):
    
    def setUp(self):
        self.mock_client = MagicMock()
        self.mock_collection = MagicMock()
        self.mock_client.get_or_create_collection.return_value = self.mock_collection
        
        with patch('chromadb.PersistentClient', return_value=self.mock_client):
            self.memory = memory_module.EpisodicMemory()

    def test_add_experience(self):
        """Test adding an experience to memory"""
        task = "Test Task"
        code = "print('hello')"
        error = "SyntaxError"
        solution = "print('hello world')"
        
        self.memory.add_experience(task, code, error, solution)
        
        # Verify collection.add was called
        self.mock_collection.add.assert_called_once()
        call_args = self.mock_collection.add.call_args[1]
        self.assertIn("documents", call_args)
        self.assertIn("metadatas", call_args)
        self.assertEqual(call_args["metadatas"][0]["task"], task)
        self.assertEqual(call_args["metadatas"][0]["error"], error)

    def test_retrieve_experience_found(self):
        """Test retrieving an existing experience"""
        # Mock query results
        self.mock_collection.query.return_value = {
            'documents': [['Task: Test Task\nError: SyntaxError']],
            'metadatas': [[{
                'task': 'Test Task',
                'error': 'SyntaxError',
                'solution': 'Fixed Code',
                'type': 'error_resolution'
            }]],
            'distances': [[0.1]]
        }
        
        results = self.memory.retrieve_experience("Test Task", "SyntaxError")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['solution'], 'Fixed Code')
        self.assertGreater(results[0]['relevance'], 0.8)

    def test_retrieve_experience_empty(self):
        """Test retrieving when no match found"""
        self.mock_collection.query.return_value = {
            'documents': [],
            'metadatas': [],
            'distances': []
        }
        
        results = self.memory.retrieve_experience("New Task", "New Error")
        
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main()
