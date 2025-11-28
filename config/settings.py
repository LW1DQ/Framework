"""
Configuración Global del Sistema A2A
Ajusta estos valores según tu entorno
"""

import os
from pathlib import Path

# ============================================================================
# RUTAS DEL PROYECTO
# ============================================================================

# Directorio raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent

# Ruta a NS-3 (AJUSTAR SEGÚN TU INSTALACIÓN)
# Ejemplo: /home/usuario/tesis-a2a/ns-allinone-3.43/ns-3.43
NS3_ROOT = Path.home() / "ns-3.45"

# Directorios del proyecto
SIMULATIONS_DIR = PROJECT_ROOT / "simulations"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
CHROMA_PATH = DATA_DIR / "vector_db"

# ============================================================================
# CONFIGURACIÓN DE OLLAMA
# ============================================================================

# URL base de Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Modelos a utilizar
MODEL_REASONING = os.getenv("MODEL_REASONING", "llama3.1:8b")
MODEL_CODING = os.getenv("MODEL_CODING", "llama3.1:8b")
MODEL_EMBEDDING = os.getenv("MODEL_EMBEDDING", "nomic-embed-text")

# Parámetros de los modelos
MODEL_TEMPERATURE_REASONING = 0.1  # Baja para respuestas más deterministas
MODEL_TEMPERATURE_CODING = 0.05    # Muy baja para código preciso
MODEL_TEMPERATURE_CREATIVE = 0.3   # Moderada para análisis

# ============================================================================
# LÍMITES Y TIMEOUTS
# ============================================================================

# Número máximo de iteraciones para corrección de errores
MAX_ITERATIONS = 5

# Timeout para simulaciones NS-3 (en segundos)
SIMULATION_TIMEOUT = 900  # 15 minutos

# Timeout para llamadas a LLM (en segundos)
LLM_TIMEOUT = 120  # 2 minutos

# ============================================================================
# CONFIGURACIÓN DE CHROMADB
# ============================================================================

# Nombre de la colección para papers
CHROMA_COLLECTION_PAPERS = "thesis_papers"

# Número de resultados en búsquedas
CHROMA_N_RESULTS = 5

# ============================================================================
# CONFIGURACIÓN DE SEMANTIC SCHOLAR
# ============================================================================

# Número máximo de papers a buscar
SEMANTIC_SCHOLAR_MAX_RESULTS = 10

# Años de publicación a considerar
SEMANTIC_SCHOLAR_YEAR_FROM = 2020
SEMANTIC_SCHOLAR_YEAR_TO = 2025

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================

# DPI para gráficos
PLOT_DPI = 300

# Tamaño de figura por defecto
PLOT_FIGSIZE = (10, 6)

# Estilo de gráficos
PLOT_STYLE = "seaborn-v0_8-whitegrid"

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

# Nivel de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Formato de logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Archivo de log principal
LOG_FILE = LOGS_DIR / "sistema_a2a.log"

# ============================================================================
# CREAR DIRECTORIOS SI NO EXISTEN
# ============================================================================

for directory in [SIMULATIONS_DIR, DATA_DIR, LOGS_DIR, CHROMA_PATH]:
    directory.mkdir(parents=True, exist_ok=True)

# Crear subdirectorios de simulaciones
(SIMULATIONS_DIR / "scripts").mkdir(exist_ok=True)
(SIMULATIONS_DIR / "results").mkdir(exist_ok=True)
(SIMULATIONS_DIR / "plots").mkdir(exist_ok=True)

# Crear subdirectorios de datos
(DATA_DIR / "papers").mkdir(exist_ok=True)

# ============================================================================
# VALIDACIONES
# ============================================================================

def validate_configuration():
    """
    Valida que la configuración sea correcta
    """
    errors = []
    
    # Verificar que NS-3 existe
    if not NS3_ROOT.exists():
        errors.append(f"NS-3 no encontrado en: {NS3_ROOT}")
    
    # Verificar que el ejecutable ns3 existe
    ns3_executable = NS3_ROOT / "ns3"
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
    print(f"NS-3: {NS3_ROOT}")
    print(f"Ollama: {OLLAMA_BASE_URL}")
    print(f"Modelo de razonamiento: {MODEL_REASONING}")
    print(f"Modelo de código: {MODEL_CODING}")
    print(f"Modelo de embeddings: {MODEL_EMBEDDING}")
    print(f"Máximo de iteraciones: {MAX_ITERATIONS}")
    print(f"Timeout de simulación: {SIMULATION_TIMEOUT}s")
    print("=" * 80)

if __name__ == "__main__":
    print_configuration()
    errors = validate_configuration()
    if errors:
        print("\n⚠️  ERRORES DE CONFIGURACIÓN:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("\n✅ Configuración válida")
