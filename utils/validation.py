
import ast
import subprocess
import logging
import sys
from typing import Tuple, List

logger = logging.getLogger(__name__)

def validate_code(code: str) -> Tuple[bool, str]:
    """
    Validates Python code for syntax errors, compilation issues, and required NS-3 imports.
    
    Args:
        code: The Python code string to validate.
        
    Returns:
        A tuple (is_valid, message).
    """
    # 1. Syntax Validation with AST
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error inesperado durante análisis AST: {str(e)}"

    import tempfile
    import os
    
    # 2. Compilation Validation
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
            
        try:
            # We use subprocess to run python -m py_compile <file>
            process = subprocess.run(
                [sys.executable, '-m', 'py_compile', tmp_path],
                capture_output=True,
                timeout=5
            )
            if process.returncode != 0:
                error_msg = process.stderr.decode('utf-8').strip()
                # Try to extract the last line which usually contains the error
                if error_msg:
                    lines = error_msg.splitlines()
                    error_msg = lines[-1] if lines else error_msg
                return False, f"Error de compilación: {error_msg}"
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    except subprocess.TimeoutExpired:
        return False, "Timeout durante la validación de compilación"
    except Exception as e:
        return False, f"Error inesperado durante compilación: {str(e)}"

    # 3. NS-3 Specific Verification
    required_imports = ['ns.core', 'ns.network']
    missing_imports = [imp for imp in required_imports if f"import {imp}" not in code and f"from {imp}" not in code]
    
    if missing_imports:
        return False, f"Faltan imports críticos de NS-3: {', '.join(missing_imports)}"

    # Check for main function or if __name__ == "__main__"
    if 'def main()' not in code and 'if __name__' not in code:
         return False, "Falta función main() o bloque if __name__"

    return True, "Código válido"
