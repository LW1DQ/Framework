#!/usr/bin/env python3
"""
Script de Verificación de Instalación NS3-AI
Sistema A2A - Tesis Doctoral

Verifica que todos los componentes estén instalados correctamente.
"""

import sys
import os
from pathlib import Path
import subprocess

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_python_version():
    """Verifica versión de Python"""
    print_info("Verificando versión de Python...")
    version = sys.version_info
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} (se requiere 3.8+)")
        return False

def check_ns3_installation():
    """Verifica instalación de NS-3"""
    print_info("Verificando instalación de NS-3...")
    
    # Buscar NS-3 en ubicaciones comunes
    ns3_paths = [
        Path.home() / "ns-3-dev",
        Path.home() / "ns-allinone-3.43" / "ns-3.43",
        Path("/usr/local/ns-3-dev"),
    ]
    
    for path in ns3_paths:
        if path.exists() and (path / "ns3").exists():
            print_success(f"NS-3 encontrado en: {path}")
            
            # Verificar versión
            try:
                result = subprocess.run(
                    [str(path / "ns3"), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print_info(f"Versión: {version}")
                return True, path
            except Exception as e:
                print_warning(f"Error verificando versión: {e}")
                return True, path
    
    print_error("NS-3 no encontrado")
    print_info("Instalar con:")
    print_info("  git clone https://gitlab.com/nsnam/ns-3-dev.git ~/ns-3-dev")
    print_info("  cd ~/ns-3-dev && ./ns3 configure && ./ns3 build")
    return False, None

def check_ns3_ai_module(ns3_path):
    """Verifica módulo ns3-ai"""
    print_info("Verificando módulo ns3-ai...")
    
    ns3_ai_path = ns3_path / "contrib" / "ns3-ai"
    
    if ns3_ai_path.exists():
        print_success(f"Módulo ns3-ai encontrado en: {ns3_ai_path}")
        
        # Verificar que esté compilado
        try:
            result = subprocess.run(
                [str(ns3_path / "ns3"), "show", "modules"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=str(ns3_path)
            )
            if "ns3-ai" in result.stdout:
                print_success("Módulo ns3-ai compilado")
                return True
            else:
                print_warning("Módulo ns3-ai no compilado")
                print_info("Recompilar con: cd ~/ns-3-dev && ./ns3 build")
                return False
        except Exception as e:
            print_warning(f"Error verificando compilación: {e}")
            return False
    else:
        print_error("Módulo ns3-ai no encontrado")
        print_info("Instalar con:")
        print_info(f"  cd {ns3_path}/contrib")
        print_info("  git clone https://github.com/hust-diangroup/ns3-ai.git")
        print_info(f"  cd {ns3_path} && ./ns3 build")
        return False

def check_drl_routing_module(ns3_path):
    """Verifica módulo drl-routing"""
    print_info("Verificando módulo drl-routing...")
    
    drl_path = ns3_path / "contrib" / "drl-routing"
    
    if drl_path.exists():
        print_success(f"Módulo drl-routing encontrado en: {drl_path}")
        
        # Verificar archivos clave
        required_files = [
            "model/drl-routing-agent.h",
            "model/drl-routing-agent.cc",
            "wscript"
        ]
        
        all_exist = True
        for file in required_files:
            if not (drl_path / file).exists():
                print_error(f"Falta archivo: {file}")
                all_exist = False
        
        if all_exist:
            print_success("Todos los archivos del módulo presentes")
            
            # Verificar compilación
            try:
                result = subprocess.run(
                    [str(ns3_path / "ns3"), "show", "modules"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    cwd=str(ns3_path)
                )
                if "drl-routing" in result.stdout:
                    print_success("Módulo drl-routing compilado")
                    return True
                else:
                    print_warning("Módulo drl-routing no compilado")
                    return False
            except Exception as e:
                print_warning(f"Error verificando compilación: {e}")
                return False
        else:
            return False
    else:
        print_error("Módulo drl-routing no encontrado")
        print_info("Instalar con:")
        print_info("  cd ns3-integration")
        print_info("  chmod +x install-drl-module.sh")
        print_info("  ./install-drl-module.sh")
        return False

def check_python_packages():
    """Verifica paquetes Python necesarios"""
    print_info("Verificando paquetes Python...")
    
    required_packages = {
        'torch': 'PyTorch',
        'numpy': 'NumPy',
        'ns3_ai': 'ns3-ai Python interface'
    }
    
    all_installed = True
    
    for package, name in required_packages.items():
        try:
            __import__(package)
            print_success(f"{name} instalado")
        except ImportError:
            print_error(f"{name} NO instalado")
            all_installed = False
            
            if package == 'ns3_ai':
                print_info("Instalar con:")
                print_info("  cd ~/ns-3-dev/contrib/ns3-ai/py_interface")
                print_info("  pip install -e .")
            elif package == 'torch':
                print_info("Instalar con: pip install torch")
            else:
                print_info(f"Instalar con: pip install {package}")
    
    return all_installed

def check_system_dependencies():
    """Verifica dependencias del sistema"""
    print_info("Verificando dependencias del sistema...")
    
    dependencies = {
        'cmake': 'CMake',
        'g++': 'G++ Compiler',
        'protoc': 'Protocol Buffers'
    }
    
    all_installed = True
    
    for cmd, name in dependencies.items():
        try:
            result = subprocess.run(
                [cmd, '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                print_success(f"{name} instalado")
            else:
                print_error(f"{name} NO instalado")
                all_installed = False
        except FileNotFoundError:
            print_error(f"{name} NO instalado")
            all_installed = False
        except Exception:
            print_warning(f"No se pudo verificar {name}")
    
    if not all_installed:
        print_info("\nInstalar dependencias con:")
        print_info("  Ubuntu: sudo apt install cmake g++ protobuf-compiler")
        print_info("  Fedora: sudo dnf install cmake gcc-c++ protobuf-compiler")
        print_info("  macOS: brew install cmake protobuf")
    
    return all_installed

def run_integration_test(ns3_path):
    """Ejecuta test de integración"""
    print_info("Ejecutando test de integración...")
    
    try:
        # Intentar ejecutar ejemplo de drl-routing
        result = subprocess.run(
            [str(ns3_path / "ns3"), "run", "drl-routing-example"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(ns3_path)
        )
        
        if result.returncode == 0:
            print_success("Test de integración PASADO")
            return True
        else:
            print_error("Test de integración FALLIDO")
            print_info("Error:")
            print(result.stderr[:500])
            return False
    except subprocess.TimeoutExpired:
        print_error("Test de integración TIMEOUT")
        return False
    except Exception as e:
        print_error(f"Error ejecutando test: {e}")
        return False

def main():
    """Función principal"""
    print_header("VERIFICACIÓN DE INSTALACIÓN NS3-AI")
    print_info("Sistema A2A - Tesis Doctoral")
    print()
    
    results = {}
    
    # 1. Python
    print_header("1. Python")
    results['python'] = check_python_version()
    
    # 2. NS-3
    print_header("2. NS-3")
    ns3_ok, ns3_path = check_ns3_installation()
    results['ns3'] = ns3_ok
    
    if not ns3_ok:
        print_error("\n❌ NS-3 no instalado. No se pueden verificar módulos.")
        print_summary(results)
        return 1
    
    # 3. ns3-ai
    print_header("3. Módulo ns3-ai")
    results['ns3_ai'] = check_ns3_ai_module(ns3_path)
    
    # 4. drl-routing
    print_header("4. Módulo drl-routing")
    results['drl_routing'] = check_drl_routing_module(ns3_path)
    
    # 5. Paquetes Python
    print_header("5. Paquetes Python")
    results['python_packages'] = check_python_packages()
    
    # 6. Dependencias del sistema
    print_header("6. Dependencias del Sistema")
    results['system_deps'] = check_system_dependencies()
    
    # 7. Test de integración (solo si todo lo demás está OK)
    if all([results['ns3'], results['drl_routing']]):
        print_header("7. Test de Integración")
        results['integration_test'] = run_integration_test(ns3_path)
    else:
        print_header("7. Test de Integración")
        print_warning("Saltando test de integración (faltan componentes)")
        results['integration_test'] = False
    
    # Resumen
    print_summary(results)
    
    # Código de salida
    if all(results.values()):
        return 0
    else:
        return 1

def print_summary(results):
    """Imprime resumen de resultados"""
    print_header("RESUMEN")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    print(f"Tests pasados: {passed}/{total}\n")
    
    for test, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {test}")
    
    print()
    
    if all(results.values()):
        print_success("🎉 ¡Instalación completa y funcional!")
        print_info("\nPróximos pasos:")
        print_info("  1. Ejecutar simulación con DRL:")
        print_info("     python main.py --task 'Simular AODV con DRL'")
        print_info("  2. Entrenar modelo:")
        print_info("     python agents/ns3_ai_integration.py")
    else:
        print_error("⚠️  Instalación incompleta")
        print_info("\nConsultar:")
        print_info("  - ns3-integration/INSTALL-NS3-AI.md")
        print_info("  - docs/TROUBLESHOOTING.md")

if __name__ == "__main__":
    sys.exit(main())
