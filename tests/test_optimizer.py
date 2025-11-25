import unittest
import sys
from unittest.mock import MagicMock
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Mock dependencies BEFORE importing the module under test
sys.modules["langchain_ollama"] = MagicMock()
sys.modules["agents.ns3_ai_integration"] = MagicMock()
sys.modules["config.settings"] = MagicMock()
sys.modules["utils.state"] = MagicMock()
sys.modules["utils.logging_utils"] = MagicMock()

# Now we can safely import the optimizer functions
# We use importlib to load it directly to avoid issues with other agent imports if we were to import 'agents.optimizer'
import importlib.util
spec = importlib.util.spec_from_file_location("optimizer", PROJECT_ROOT / "agents" / "optimizer.py")
optimizer_module = importlib.util.module_from_spec(spec)
sys.modules["agents.optimizer"] = optimizer_module
spec.loader.exec_module(optimizer_module)

analyze_performance_bottlenecks = optimizer_module.analyze_performance_bottlenecks
extract_drl_parameters = optimizer_module.extract_drl_parameters

class TestOptimizer(unittest.TestCase):

    def test_analyze_bottlenecks_critical(self):
        """Test detection of critical bottlenecks"""
        kpis = {
            'avg_pdr': 65.0,  # < 70 is critical
            'avg_delay': 250.0, # > 200 is critical
            'avg_throughput': 0.3, # < 0.5 is critical
            'success_rate': 75.0 # < 80 is critical
        }
        
        bottlenecks = analyze_performance_bottlenecks(kpis)
        
        self.assertTrue(len(bottlenecks['critical']) > 0)
        
        metrics = [b['metric'] for b in bottlenecks['critical']]
        self.assertIn('PDR', metrics)
        self.assertIn('Delay', metrics)
        self.assertIn('Throughput', metrics)
        self.assertIn('Success Rate', metrics)

    def test_analyze_bottlenecks_moderate(self):
        """Test detection of moderate bottlenecks"""
        kpis = {
            'avg_pdr': 80.0,  # 70-85 is moderate
            'avg_delay': 150.0, # 100-200 is moderate
            'avg_throughput': 0.8, # 0.5-1.0 is moderate
            'std_pdr': 25.0, # > 20 is moderate
            'success_rate': 90.0
        }
        
        bottlenecks = analyze_performance_bottlenecks(kpis)
        
        self.assertEqual(len(bottlenecks['critical']), 0)
        self.assertTrue(len(bottlenecks['moderate']) > 0)
        
        metrics = [b['metric'] for b in bottlenecks['moderate']]
        self.assertIn('PDR', metrics)
        self.assertIn('Delay', metrics)
        self.assertIn('Throughput', metrics)
        self.assertIn('Variabilidad PDR', metrics)

    def test_analyze_bottlenecks_optimal(self):
        """Test optimal performance (no bottlenecks)"""
        kpis = {
            'avg_pdr': 95.0,
            'avg_delay': 50.0,
            'avg_throughput': 2.5,
            'std_pdr': 5.0,
            'success_rate': 100.0
        }
        
        bottlenecks = analyze_performance_bottlenecks(kpis)
        
        self.assertEqual(len(bottlenecks['critical']), 0)
        self.assertEqual(len(bottlenecks['moderate']), 0)

    def test_extract_drl_parameters(self):
        """Test extraction of DRL parameters"""
        proposal = "Some proposal text"
        params = extract_drl_parameters(proposal)
        
        self.assertEqual(params['algorithm'], 'PPO')
        self.assertEqual(params['learning_rate'], 0.0003)
        self.assertEqual(params['gamma'], 0.99)
        self.assertIn('eps_clip', params)

if __name__ == '__main__':
    unittest.main()
