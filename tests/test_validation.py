import sys
import importlib.util
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Load simulator.py directly to avoid triggering agents/__init__.py and heavy dependencies
spec = importlib.util.spec_from_file_location("simulator", PROJECT_ROOT / "agents" / "simulator.py")
simulator_module = importlib.util.module_from_spec(spec)
sys.modules["simulator"] = simulator_module
spec.loader.exec_module(simulator_module)

validate_code_before_execution = simulator_module.validate_code_before_execution

def test_validation():
    print("Testing Robust Syntax Validation...")
    
    # Case 1: Valid Code
    valid_code = """
import ns.core
import ns.network

def main():
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()

if __name__ == "__main__":
    main()
"""
    is_valid, msg = validate_code_before_execution(valid_code)
    if is_valid:
        print("✅ Valid code passed")
    else:
        print(f"❌ Valid code failed: {msg}")

    # Case 2: Syntax Error
    syntax_error_code = """
import ns.core
def main()  # Missing colon
    pass
"""
    is_valid, msg = validate_code_before_execution(syntax_error_code)
    if not is_valid and "Error de sintaxis" in msg:
        print(f"✅ Syntax error caught: {msg}")
    else:
        print(f"❌ Syntax error NOT caught correctly: {is_valid}, {msg}")

    # Case 3: Missing Imports
    missing_import_code = """
def main():
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()
"""
    is_valid, msg = validate_code_before_execution(missing_import_code)
    if not is_valid and "Faltan imports" in msg:
        print(f"✅ Missing imports caught: {msg}")
    else:
        print(f"❌ Missing imports NOT caught: {is_valid}, {msg}")

    # Case 4: Missing Simulator.Run
    missing_run_code = """
import ns.core
import ns.network
def main():
    ns.core.Simulator.Destroy()
"""
    is_valid, msg = validate_code_before_execution(missing_run_code)
    if not is_valid and "Falta llamada a Simulator.Run" in msg:
        print(f"✅ Missing Simulator.Run caught: {msg}")
    else:
        print(f"❌ Missing Simulator.Run NOT caught: {is_valid}, {msg}")

if __name__ == "__main__":
    test_validation()
