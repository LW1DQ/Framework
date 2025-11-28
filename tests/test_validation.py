
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.validation import validate_code

class TestValidation(unittest.TestCase):
    def test_valid_code(self):
        code = """
import ns.core
import ns.network

def main():
    print("Hello")
    return 0

if __name__ == "__main__":
    main()
"""
        is_valid, msg = validate_code(code)
        self.assertTrue(is_valid, msg)

    def test_syntax_error(self):
        code = """
import ns.core
def main() # Missing colon
    pass
"""
        is_valid, msg = validate_code(code)
        self.assertFalse(is_valid)
        self.assertIn("sintaxis", msg.lower())

    def test_missing_imports(self):
        code = """
def main():
    pass
"""
        is_valid, msg = validate_code(code)
        self.assertFalse(is_valid)
        self.assertIn("faltan imports", msg.lower())

    def test_compilation_error(self):
        # Valid syntax but invalid logic that might be caught by some linters, 
        # but py_compile mainly checks syntax. 
        # However, let's try something that is syntactically correct but might fail if we were doing more.
        # Actually py_compile is just syntax check + bytecode generation.
        # Let's test a case where indentation is wrong which is a syntax error but good to check.
        code = """
def main():
print("Bad indentation")
"""
        is_valid, msg = validate_code(code)
        self.assertFalse(is_valid)
        self.assertIn("sintaxis", msg.lower())

if __name__ == '__main__':
    unittest.main()
