#!/usr/bin/env python3
"""
Dependency Checker Utility for A2A Framework
Validates the environment, including NS-3, ns3-ai, and Python dependencies.
"""

import sys
import shutil
import importlib
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DependencyChecker")

class DependencyChecker:
    def __init__(self):
        self.results = {
            'ns3': False,
            'ns3_ai': False,
            'python_packages': {},
            'ollama': False
        }
        
    def check_ns3_bindings(self):
        """Check if NS-3 Python bindings are available"""
        try:
            # Attempt to import ns.core
            import ns.core
            version = ns.core.Version()
            logger.info(f"✅ NS-3 found. Version info available.")
            self.results['ns3'] = True
            return True
        except ImportError:
            logger.error("❌ NS-3 Python bindings not found.")
            logger.error("   Please ensure PYTHONPATH includes 'build/lib/python3' and 'ns3/build/bindings/python'")
            return False
            
    def check_ns3_ai(self):
        """Check if ns3-ai module is available and compiled"""
        try:
            # This is a bit tricky as ns3-ai might be part of ns module or separate
            # Inspecting via ns.core to see if we can find AI related attributes
            # Or try importing if it's a separate binding
            import ns.core
            
            # Try to see if there is any 'ai' or 'Ai' string in the bindings
            # This is a heuristic check if we don't have a direct import
            # For now, we assume if ns3-ai is installed, it might be under ns.ai or similar
            
            try:
                import ns.ai
                logger.info("✅ ns3-ai binding found (ns.ai)")
                self.results['ns3_ai'] = True
                return True
            except ImportError:
                pass
                
            # If not found directly, check if we can find the shared library
            # This is a fallback check
            logger.warning("⚠️  ns3-ai binding not directly importable as 'ns.ai'.")
            return False
            
        except ImportError:
            return False

    def check_python_packages(self, requirements_path='requirements.txt'):
        """Check if Python packages from requirements.txt are installed"""
        if not Path(requirements_path).exists():
            logger.warning(f"⚠️  {requirements_path} not found. Skipping package check.")
            return

        with open(requirements_path, 'r') as f:
            requirements = [line.strip().split('==')[0] for line in f if line.strip() and not line.startswith('#')]

        for package in requirements:
            try:
                importlib.import_module(package)
                self.results['python_packages'][package] = True
            except ImportError:
                # Handle package name differences (e.g., PyYAML -> yaml)
                pkg_map = {
                    'PyYAML': 'yaml',
                    'scikit-learn': 'sklearn',
                    'langchain-ollama': 'langchain_ollama'
                }
                mapped_pkg = pkg_map.get(package, package)
                try:
                    importlib.import_module(mapped_pkg)
                    self.results['python_packages'][package] = True
                except ImportError:
                    logger.error(f"❌ Missing Python package: {package}")
                    self.results['python_packages'][package] = False
        
        all_installed = all(self.results['python_packages'].values())
        if all_installed:
            logger.info("✅ All Python requirements installed.")
        else:
            logger.warning("⚠️  Some Python requirements are missing.")

    def check_ollama(self):
        """Check if Ollama is reachable"""
        try:
            result = subprocess.run(['curl', '-s', 'http://localhost:11434/api/tags'], capture_output=True)
            if result.returncode == 0:
                logger.info("✅ Ollama is running and reachable.")
                self.results['ollama'] = True
            else:
                logger.error("❌ Ollama is not reachable on localhost:11434")
        except FileNotFoundError:
            # curl might not be installed, try python requests
            try:
                import requests
                response = requests.get('http://localhost:11434/api/tags', timeout=2)
                if response.status_code == 200:
                    logger.info("✅ Ollama is running and reachable.")
                    self.results['ollama'] = True
                else:
                    logger.error(f"❌ Ollama returned status code: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ Error checking Ollama: {e}")

    def run_all_checks(self):
        print("\n" + "="*40)
        print("🔍 RUNNING DEPENDENCY CHECKS")
        print("="*40)
        
        self.check_python_packages()
        
        # Check NS-3 environment variables first
        import os
        ppath = os.environ.get('PYTHONPATH', '')
        if 'ns3' not in ppath:
             logger.warning("⚠️  'ns3' not found in PYTHONPATH. Bindings check might fail.")
             print(f"    Current PYTHONPATH: {ppath}")

        # Try to insert paths if we know them (dev environment heuristic)
        # This mirrors what we do in agents/coder.py
        sys.path.insert(0, 'build/lib/python3')
        sys.path.insert(0, str(Path.home() / 'ns3/build/bindings/python'))

        self.check_ns3_bindings()
        self.check_ns3_ai()
        self.check_ollama()
        
        print("\n" + "="*40)
        print("📊 SUMMARY")
        print("="*40)
        print(f"NS-3 Bindings: {'✅ OK' if self.results['ns3'] else '❌ MISSING'}")
        print(f"ns3-ai Module: {'✅ OK' if self.results['ns3_ai'] else '❌ MISSING'}")
        print(f"Ollama Service: {'✅ OK' if self.results['ollama'] else '❌ NOT REACHABLE'}")
        
        missing_pkgs = [p for p, installed in self.results['python_packages'].items() if not installed]
        if missing_pkgs:
            print(f"Missing Packages: {', '.join(missing_pkgs)}")
        else:
            print("Python Packages: ✅ ALL OK")
        
        return all(self.results.values()) and not missing_pkgs

if __name__ == "__main__":
    checker = DependencyChecker()
    checker.run_all_checks()
