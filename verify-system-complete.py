#!/usr/bin/env python3
"""
Script de Verificación Completa del Sistema A2A
Verifica que todos los componentes estén instalados y funcionando correctamente

Ejecutar con: python verify-system-complete.py
"""

import sys
import os
from pathlib import Path
import subprocess
import importlib
from datetime import datetime

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.END}")

def print_section(text):
    print(f"\n{Colors.PURPLE}{Colors.BOLD}📋 {text}{Colors.END}")
    print(f"{Colors.PURPLE}{'-' * (len(text) + 4)}{Colors.END}")

def check_python_version():
    """Verifica versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (se requiere 3.8+)")
        return False

def check_required_packages():
    """Verifica paquetes Python requeridos"""
    required_packages = {
        'langchain': 'LangChain',
        'langchain_ollama': 'LangChain Ollama',
        'langgraph': 'LangGraph',
        'chromadb': 'ChromaDB',
        'requests': 'Requests',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'plotly': 'Plotly',
        'streamlit': 'Streamlit',
        'tqdm': 'TQDM',
        'yaml': 'PyYAML',
        'pytest': 'Pytest',
        'sklearn': 'Scikit-learn',
        'scipy': 'SciPy',
        'seaborn': 'Seaborn'
    }
    
    all_installed = True
    
    for package, name in required_packages.items():
        try:
            importlib.import_module(package)
            print_success(f"{name}")
        except ImportError:
            print_error(f"{name} NO instalado")
            all_installed = False
    
    return all_installed

def check_optional_packages():
    """Verifica paquetes opcionales"""
    optional_packages = {
        'torch': 'PyTorch (para DRL)',
        'torchvision': 'TorchVision (para DRL)',
        'ns3_ai': 'ns3-ai (para integración NS-3)'
    }
    
    for package, name in optional_packages.items():
        try:
            importlib.import_module(package)
            print_success(f"{name}")
        except ImportError:
            print_warning(f"{name} no instalado (opcional)")

def check_file_structure():
    """Verifica estructura de archivos"""
    required_files = [
        'main.py',
        'supervisor.py',
        'dashboard.py',
        'requirements.txt',
        'config/settings.py',
        'agents/researcher.py',
        'agents/coder.py',
        'agents/simulator.py',
        'agents/analyst.py',
        'utils/memory.py',
        'utils/errors.py',
        'utils/logging_utils.py',
        'tests/test_agents.py',
        'pytest.ini'
    ]
    
    required_dirs = [
        'agents',
        'config',
        'utils',
        'tests',
        'docs',
        'experiments',
        'ns3-integration'
    ]
    
    all_present = True
    
    # Verificar archivos
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"Archivo: {file_path}")
        else:
            print_error(f"Archivo faltante: {file_path}")
            all_present = False
    
    # Verificar directorios
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print_success(f"Directorio: {dir_path}/")
        else:
            print_error(f"Directorio faltante: {dir_path}/")
            all_present = False
    
    return all_present

def check_documentation():
    """Verifica documentación clave"""
    key_docs = [
        'TESIS-DOCTORAL-GUIA-COMPLETA.md',
        'RESUMEN-FINAL-COMPLETO.md',
        'INDICE-MAESTRO-DOCUMENTACION.md',
        'docs/TROUBLESHOOTING.md',
        'experiments/README.md',
        'ns3-integration/INSTALL-NS3-AI.md'
    ]
    
    all_present = True
    
    for doc in key_docs:
        if Path(doc).exists():
            size = Path(doc).stat().st_size
            print_success(f"{doc} ({size:,} bytes)")
        else:
            print_error(f"Documentación faltante: {doc}")
            all_present = False
    
    return all_present

def check_system_functionality():
    """Verifica funcionalidad básica del sistema"""
    tests = []
    
    # Test 1: Importar memoria episódica
    try:
        from utils.memory import memory
        stats = memory.get_stats()
        print_success(f"Memoria episódica: {stats['total_experiences']} experiencias")
        tests.append(True)
    except Exception as e:
        print_error(f"Memoria episódica: {e}")
        tests.append(False)
    
    # Test 2: Importar excepciones personalizadas
    try:
        from utils.errors import CompilationError, SimulationError
        print_success("Excepciones personalizadas")
        tests.append(True)
    except Exception as e:
        print_error(f"Excepciones personalizadas: {e}")
        tests.append(False)
    
    # Test 3: Importar agentes
    try:
        from agents.researcher import research_node
        from agents.coder import coder_node
        from agents.analyst import calculate_kpis
        print_success("Agentes principales")
        tests.append(True)
    except Exception as e:
        print_error(f"Agentes principales: {e}")
        tests.append(False)
    
    # Test 4: Configuración
    try:
        from config.settings import OLLAMA_BASE_URL, MODEL_REASONING
        print_success(f"Configuración (Modelo: {MODEL_REASONING})")
        tests.append(True)
    except Exception as e:
        print_error(f"Configuración: {e}")
        tests.append(False)
    
    return all(tests)

def run_unit_tests():
    """Ejecuta tests unitarios"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pytest', 'tests/test_agents.py', '-v', '--tb=short'],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            output_lines = result.stdout.split('\n')
            passed_line = [line for line in output_lines if 'passed' in line and '::' not in line]
            if passed_line:
                print_success(f"Tests unitarios: {passed_line[-1].strip()}")
            else:
                print_success("Tests unitarios: Ejecutados correctamente")
            return True
        else:
            print_error(f"Tests unitarios fallaron")
            return False
    except subprocess.TimeoutExpired:
        print_error("Tests unitarios: Timeout")
        return False
    except Exception as e:
        print_error(f"Tests unitarios: {e}")
        return False

def check_external_tools():
    """Verifica herramientas externas"""
    tools = {
        'git': 'Git (control de versiones)',
        'python': 'Python (intérprete)',
        'pip': 'Pip (gestor de paquetes)'
    }
    
    all_present = True
    
    for tool, description in tools.items():
        try:
            result = subprocess.run([tool, '--version'], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print_success(f"{description}")
            else:
                print_error(f"{description} no funciona")
                all_present = False
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print_error(f"{description} no encontrado")
            all_present = False
    
    return all_present

def generate_report(results):
    """Genera reporte de verificación"""
    print_header("REPORTE DE VERIFICACIÓN")
    
    total_checks = len(results)
    passed_checks = sum(1 for result in results.values() if result)
    
    print(f"📊 Resumen de Verificación")
    print(f"   Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Checks realizados: {total_checks}")
    print(f"   Checks pasados: {passed_checks}")
    print(f"   Porcentaje de éxito: {(passed_checks/total_checks)*100:.1f}%")
    print()
    
    print("📋 Detalle por Categoría:")
    for category, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status}  {category}")
    
    print()
    
    if all(results.values()):
        print_success("🎉 ¡SISTEMA COMPLETAMENTE VERIFICADO!")
        print_info("\n🚀 Próximos pasos:")
        print_info("   1. Leer: TESIS-DOCTORAL-GUIA-COMPLETA.md")
        print_info("   2. Instalar NS-3: ns3-integration/INSTALL-NS3-AI.md")
        print_info("   3. Ejecutar experimento: experiments/README.md")
    else:
        print_error("⚠️  SISTEMA PARCIALMENTE VERIFICADO")
        print_info("\n🔧 Acciones recomendadas:")
        
        if not results.get('Paquetes Python', True):
            print_info("   - Instalar dependencias: pip install -r requirements.txt")
        
        if not results.get('Estructura de archivos', True):
            print_info("   - Verificar que todos los archivos estén presentes")
        
        if not results.get('Tests unitarios', True):
            print_info("   - Revisar errores en tests: pytest tests/ -v")
        
        print_info("   - Consultar: docs/TROUBLESHOOTING.md")

def main():
    """Función principal"""
    print_header("VERIFICACIÓN COMPLETA DEL SISTEMA A2A v1.5")
    print_info("Framework Multi-Agente para Tesis Doctoral")
    print_info("Verificando todos los componentes del sistema...")
    
    results = {}
    
    # 1. Python
    print_section("1. Versión de Python")
    results['Python'] = check_python_version()
    
    # 2. Paquetes Python
    print_section("2. Paquetes Python Requeridos")
    results['Paquetes Python'] = check_required_packages()
    
    print_section("2.1. Paquetes Opcionales")
    check_optional_packages()
    
    # 3. Estructura de archivos
    print_section("3. Estructura de Archivos")
    results['Estructura de archivos'] = check_file_structure()
    
    # 4. Documentación
    print_section("4. Documentación Clave")
    results['Documentación'] = check_documentation()
    
    # 5. Funcionalidad del sistema
    print_section("5. Funcionalidad del Sistema")
    results['Funcionalidad'] = check_system_functionality()
    
    # 6. Tests unitarios
    print_section("6. Tests Unitarios")
    results['Tests unitarios'] = run_unit_tests()
    
    # 7. Herramientas externas
    print_section("7. Herramientas Externas")
    results['Herramientas externas'] = check_external_tools()
    
    # 8. Generar reporte
    generate_report(results)
    
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Verificación interrumpida por el usuario{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error durante la verificación: {e}{Colors.END}")
        sys.exit(1)
