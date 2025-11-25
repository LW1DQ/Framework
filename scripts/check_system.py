#!/usr/bin/env python3
"""
Script de Verificación del Sistema A2A

Verifica que todos los componentes estén correctamente instalados
y configurados antes de usar el sistema.
"""

import sys
import os
from pathlib import Path
import subprocess

# Añadir el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

console = Console()


def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (se requiere 3.10+)"


def check_virtual_env():
    """Verifica si está en un entorno virtual"""
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    return in_venv, "Entorno virtual activado" if in_venv else "No en entorno virtual"


def check_ollama():
    """Verifica que Ollama esté corriendo"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return True, "Ollama corriendo"
        return False, "Ollama no responde"
    except Exception as e:
        return False, f"Ollama no accesible: {str(e)[:50]}"


def check_ollama_models():
    """Verifica que los modelos de Ollama estén descargados"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            required_models = ['llama3.1', 'deepseek-coder', 'nomic-embed-text']
            found_models = []
            
            for req_model in required_models:
                for model in models:
                    if req_model in model:
                        found_models.append(model)
                        break
            
            if len(found_models) >= 2:  # Al menos 2 modelos
                return True, f"Modelos encontrados: {len(found_models)}"
            return False, f"Solo {len(found_models)} modelos encontrados"
        return False, "No se pudo verificar modelos"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"


def check_ns3():
    """Verifica que NS-3 esté instalado"""
    try:
        from config.settings import NS3_ROOT
        
        if not NS3_ROOT.exists():
            return False, f"NS-3 no encontrado en {NS3_ROOT}"
        
        ns3_executable = NS3_ROOT / "ns3"
        if not ns3_executable.exists():
            return False, "Ejecutable ns3 no encontrado"
        
        return True, f"NS-3 encontrado en {NS3_ROOT}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"


def check_ns3_python_bindings():
    """Verifica que los Python bindings de NS-3 funcionen"""
    try:
        from config.settings import NS3_ROOT
        sys.path.insert(0, str(NS3_ROOT / "build" / "lib" / "python3"))
        
        import ns.core
        version = ns.core.Version()
        return True, f"Python bindings OK (NS-3 {version})"
    except Exception as e:
        return False, f"Python bindings fallan: {str(e)[:50]}"


def check_ns3_ai():
    """Verifica que ns3-ai esté instalado"""
    try:
        import ns3ai_gym_env
        return True, "ns3-ai instalado"
    except ImportError:
        return False, "ns3-ai no instalado"


def check_python_dependencies():
    """Verifica las dependencias Python principales"""
    dependencies = {
        'langgraph': 'LangGraph',
        'langchain': 'LangChain',
        'langchain_ollama': 'LangChain-Ollama',
        'chromadb': 'ChromaDB',
        'pandas': 'Pandas',
        'matplotlib': 'Matplotlib',
        'scipy': 'SciPy',
        'semanticscholar': 'Semantic Scholar'
    }
    
    missing = []
    installed = []
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            installed.append(name)
        except ImportError:
            missing.append(name)
    
    if not missing:
        return True, f"Todas las dependencias instaladas ({len(installed)})"
    return False, f"Faltan: {', '.join(missing)}"


def check_directories():
    """Verifica que los directorios necesarios existan"""
    try:
        from config.settings import SIMULATIONS_DIR, DATA_DIR, LOGS_DIR
        
        dirs = [SIMULATIONS_DIR, DATA_DIR, LOGS_DIR]
        all_exist = all(d.exists() for d in dirs)
        
        if all_exist:
            return True, "Todos los directorios creados"
        return False, "Algunos directorios faltan"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"


def main():
    """Función principal"""
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]🔍 Verificación del Sistema A2A[/bold cyan]",
        border_style="cyan"
    ))
    console.print("\n")
    
    # Tabla de resultados
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Componente", style="cyan", width=30)
    table.add_column("Estado", width=15)
    table.add_column("Detalles", width=40)
    
    checks = [
        ("Python", check_python_version),
        ("Entorno Virtual", check_virtual_env),
        ("Ollama", check_ollama),
        ("Modelos Ollama", check_ollama_models),
        ("NS-3", check_ns3),
        ("Python Bindings NS-3", check_ns3_python_bindings),
        ("ns3-ai", check_ns3_ai),
        ("Dependencias Python", check_python_dependencies),
        ("Directorios", check_directories),
    ]
    
    all_ok = True
    
    for name, check_func in checks:
        try:
            ok, message = check_func()
            status = "[green]✅ OK[/green]" if ok else "[red]❌ FALLO[/red]"
            table.add_row(name, status, message)
            if not ok:
                all_ok = False
        except Exception as e:
            table.add_row(name, "[red]❌ ERROR[/red]", str(e)[:40])
            all_ok = False
    
    console.print(table)
    console.print("\n")
    
    if all_ok:
        console.print(Panel.fit(
            "[bold green]🎉 SISTEMA LISTO PARA USAR[/bold green]\n\n"
            "Todos los componentes están correctamente instalados.\n"
            "Puedes comenzar a usar el sistema con:\n\n"
            "  [cyan]python main.py --task \"Tu tarea de investigación\"[/cyan]",
            border_style="green"
        ))
        return 0
    else:
        console.print(Panel.fit(
            "[bold red]⚠️  SISTEMA INCOMPLETO[/bold red]\n\n"
            "Algunos componentes requieren atención.\n"
            "Consulta la documentación de instalación:\n\n"
            "  [cyan]docs/01-INSTALACION.md[/cyan]",
            border_style="red"
        ))
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Verificación cancelada[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error inesperado: {e}[/red]")
        sys.exit(1)
