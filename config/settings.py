"""
Configuración Global del Sistema A2A - Versión con Inyección de Dependencias
Ajusta estos valores según tu entorno o usa variables de entorno
"""

import os
from pathlib import Path
from typing import List

# ============================================================================
# RUTAS DEL PROYECTO (BACKUP para compatibilidad)
# ============================================================================

# Directorio raíz del proyecto (auto-detectado)
PROJECT_ROOT = Path(__file__).parent.parent

# Directorios del proyecto
SIMULATIONS_DIR = PROJECT_ROOT / "simulations"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

# ============================================================================
# CONFIGURACIÓN DE OLLAMA (BACKUP para compatibilidad)
# ============================================================================

# URL base de Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Modelos a utilizar
MODEL_REASONING = os.getenv("MODEL_REASONING", "llama3.1:8b")
MODEL_CODING = os.getenv("MODEL_CODING", "llama3.1:8b")
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING", "nomic-embed-text")

# Parámetros de los modelos
MODEL_TEMPERATURE_REASONING = float(os.getenv("MODEL_TEMPERATURE_REASONING", "0.1"))
MODEL_TEMPERATURE_CODING = float(os.getenv("MODEL_TEMPERATURE_CODING", "0.05"))
MODEL_TEMPERATURE_CREATIVE = float(os.getenv("MODEL_TEMPERATURE_CREATIVE", "0.3"))

# ============================================================================
# LÍMITES Y TIMEOUTS
# ============================================================================

# Número máximo de iteraciones para corrección de errores
MAX_ITERATIONS = int(os.getenv("MAX_ITERATIONS", "5"))

# Timeout para simulaciones NS-3 (en segundos)
SIMULATION_TIMEOUT = int(os.getenv("SIMULATION_TIMEOUT", "900"))

# Timeout para llamadas a LLM (en segundos)
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "120"))

# ============================================================================
# CONFIGURACIÓN DE CHROMADB
# ============================================================================

# Nombre de la colección para papers
CHROMA_COLLECTION_PAPERS = os.getenv("CHROMA_COLLECTION", "thesis_papers")

# Número de resultados en búsquedas
CHROMA_N_RESULTS = int(os.getenv("CHROMA_N_RESULTS", "5"))

# ============================================================================
# CONFIGURACIÓN DE SEMANTIC SCHOLAR
# ============================================================================

# Número máximo de papers a buscar
SEMANTIC_SCHOLAR_MAX_RESULTS = int(os.getenv("SEMANTIC_SCHOLAR_MAX_RESULTS", "10"))

# Años de publicación a considerar
SEMANTIC_SCHOLAR_YEAR_FROM = int(os.getenv("SEMANTIC_SCHOLAR_YEAR_FROM", "2020"))
SEMANTIC_SCHOLAR_YEAR_TO = int(os.getenv("SEMANTIC_SCHOLAR_YEAR_TO", "2025"))

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================

# DPI para gráficos
PLOT_DPI = int(os.getenv("PLOT_DPI", "300"))

# Tamaño de figura por defecto
PLOT_FIGSIZE = (10, 6)

# Estilo de gráficos
PLOT_STYLE = os.getenv("PLOT_STYLE", "seaborn-v0_8-whitegrid")

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

# Nivel de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Formato de logs
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Archivo de log principal
LOG_FILE = LOGS_DIR / "sistema_a2a.log"

# ============================================================================
# CREAR DIRECTORIOS SI NO EXISTEN
# ============================================================================

def ensure_directories():
    """Crea directorios necesarios si no existen"""
    directories = [
        SIMULATIONS_DIR,
        DATA_DIR,
        LOGS_DIR,
        DATA_DIR / "vector_db",
        SIMULATIONS_DIR / "scripts",
        SIMULATIONS_DIR / "results",
        SIMULATIONS_DIR / "plots",
        DATA_DIR / "papers"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Crear directorios
ensure_directories()

# ============================================================================
# FUNCIONES DE VALIDACIÓN (ACTUALIZADAS PARA USAR DI)
# ============================================================================

def validate_configuration() -> List[str]:
    """
    Valida que la configuración sea correcta.
    
    Returns:
        Lista de errores encontrados
    """
    # Importar sistema de DI si está disponible
    try:
        from utils.dependency_injection import validate_system_configuration
        return validate_system_configuration()
    except ImportError:
        # Fallback a validación básica
        return validate_configuration_basic()


def validate_configuration_basic() -> List[str]:
    """
    Validación básica sin DI (fallback)
    """
    errors = []
    
    # Verificar NS-3
    ns3_root = os.getenv("NS3_ROOT", str(Path.home() / "ns-3.45"))
    if not Path(ns3_root).exists():
        errors.append(f"NS-3 no encontrado en: {ns3_root}")
    
    # Verificar que el ejecutable ns3 existe
    ns3_executable = Path(ns3_root) / "ns3"
    if not ns3_executable.exists():
        errors.append(f"Ejecutable ns3 no encontrado en: {ns3_executable}")
    
    # Verificar que Ollama está accesible
    try:
        import requests
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code != 200:
            errors.append(f"Ollama no responde en: {OLLAMA_BASE_URL}")
    except Exception as e:
        errors.append(f"No se puede conectar a Ollama: {e}")
    
    return errors


# ============================================================================
# INFORMACIÓN DEL SISTEMA
# ============================================================================

def print_configuration():
    """
    Imprime la configuración actual
    """
    print("=" * 80)
    print("CONFIGURACIÓN DEL SISTEMA A2A")
    print("=" * 80)
    print(f"Directorio del proyecto: {PROJECT_ROOT}")
    print(f"NS-3: {os.getenv('NS3_ROOT', str(Path.home() / 'ns-3.45'))}")
    print(f"Ollama: {OLLAMA_BASE_URL}")
    print(f"Modelo de razonamiento: {MODEL_REASONING}")
    print(f"Modelo de código: {MODEL_CODING}")
    print(f"Modelo de embeddings: {MODEL_EMBEDDING}")
    print(f"Máximo de iteraciones: {MAX_ITERATIONS}")
    print(f"Timeout de simulación: {SIMULATION_TIMEOUT}s")
    print(f"Ambiente: {os.getenv('ENVIRONMENT', 'development')}")
    print("=" * 80)


def setup_environment():
    """
    Configura el ambiente basado en variables de entorno
    """
    # Configurar PYTHONPATH para NS-3 si está disponible
    ns3_root = os.getenv("NS3_ROOT")
    if ns3_root:
        python_bindings = Path(ns3_root) / "build" / "bindings" / "python"
        if python_bindings.exists():
            python_path = str(python_bindings)
            if "PYTHONPATH" in os.environ:
                os.environ["PYTHONPATH"] = python_path + ":" + os.environ["PYTHONPATH"]
            else:
                os.environ["PYTHONPATH"] = python_path


# Configurar ambiente automáticamente
setup_environment()


if __name__ == "__main__":
    print_configuration()
    errors = validate_configuration()
    if errors:
        print("\n⚠️  ERRORES DE CONFIGURACIÓN:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ Configuración válida")