# ⚙️ Guía de Configuración - Sistema A2A

## Tabla de Contenidos

1. [Configuración Básica](#configuración-básica)
2. [Configuración de Ollama](#configuración-de-ollama)
3. [Configuración de NS-3](#configuración-de-ns-3)
4. [Configuración de Modelos](#configuración-de-modelos)
5. [Configuración Avanzada](#configuración-avanzada)
6. [Variables de Entorno](#variables-de-entorno)
7. [Configuración por Proyecto](#configuración-por-proyecto)

---

## Configuración Básica

### Archivo Principal: `config/settings.py`

Este es el archivo central de configuración. Después de la instalación, debes ajustarlo según tu entorno.

### Configuraciones Esenciales

#### 1. Ruta a NS-3

```python
# Línea ~18 en config/settings.py
NS3_ROOT = Path.home() / "tesis-a2a" / "ns-allinone-3.43" / "ns-3.43"
```

**Ajustar si**:
- Instalaste NS-3 en otra ubicación
- Usas una versión diferente (ej: 3.45)

**Ejemplo para versión 3.45**:
```python
NS3_ROOT = Path.home() / "tesis-a2a" / "ns-allinone-3.45" / "ns-3.45"
```

**Ejemplo para ruta personalizada**:
```python
NS3_ROOT = Path("/opt/ns3/ns-3.43")
```

#### 2. URL de Ollama

```python
# Línea ~30
OLLAMA_BASE_URL = "http://localhost:11434"
```

**Ajustar si**:
- Ollama corre en otro puerto
- Usas Ollama remoto (ej: en Colab)

**Ejemplo para puerto diferente**:
```python
OLLAMA_BASE_URL = "http://localhost:8080"
```

**Ejemplo para servidor remoto**:
```python
OLLAMA_BASE_URL = "http://192.168.1.100:11434"
```

#### 3. Modelos de IA

```python
# Líneas ~33-35
MODEL_REASONING = "llama3.1:8b"
MODEL_CODING = "deepseek-coder-v2:16b"
MODEL_EMBEDDING = "nomic-embed-text"
```

**Ajustar según tu hardware**:

| Hardware | Configuración Recomendada |
|----------|---------------------------|
| **16 GB RAM** | `llama3.1:8b`, `qwen2.5-coder:7b` |
| **32 GB RAM** | `llama3.1:8b`, `deepseek-coder-v2:16b` |
| **64 GB RAM** | `llama3.1:70b`, `deepseek-coder-v2:236b` |

**Ejemplo para hardware limitado**:
```python
MODEL_REASONING = "llama3.1:8b"
MODEL_CODING = "qwen2.5-coder:7b"  # Más ligero
MODEL_EMBEDDING = "nomic-embed-text"
```

---

## Configuración de Ollama

### Verificar Modelos Instalados

```bash
ollama list
```

**Salida esperada**:
```
NAME                        ID              SIZE      MODIFIED
llama3.1:8b                abc123          4.7 GB    2 days ago
deepseek-coder-v2:16b      def456          9.0 GB    2 days ago
nomic-embed-text           ghi789          274 MB    2 days ago
```

### Descargar Modelos Adicionales

```bash
# Modelo más grande para mejor razonamiento
ollama pull llama3.1:70b

# Modelo alternativo de código
ollama pull qwen2.5-coder:32b

# Modelo para español
ollama pull llama3.1:8b-spanish
```

### Configurar Ollama

Crear archivo `~/.ollama/config.json`:

```json
{
  "origins": ["http://localhost:*"],
  "models_path": "/home/usuario/.ollama/models",
  "keep_alive": "5m",
  "num_parallel": 2,
  "num_ctx": 8192,
  "num_gpu": 1
}
```

**Parámetros**:
- `keep_alive`: Tiempo que el modelo permanece en memoria
- `num_parallel`: Número de solicitudes paralelas
- `num_ctx`: Tamaño del contexto (tokens)
- `num_gpu`: Número de GPUs a usar (0 para solo CPU)

### Reiniciar Ollama

```bash
# Detener Ollama
pkill ollama

# Iniciar con nueva configuración
ollama serve &

# Verificar
curl http://localhost:11434/api/tags
```

---

## Configuración de NS-3

### Verificar Instalación

```bash
cd ~/tesis-a2a/ns-allinone-3.43/ns-3.43

# Ver configuración actual
./ns3 show config

# Ver módulos instalados
./ns3 show modules
```

### Reconfigurar NS-3

Si necesitas cambiar opciones:

```bash
# Limpiar compilación anterior
./ns3 clean

# Reconfigurar con opciones específicas
./ns3 configure \
  --enable-python-bindings \
  --enable-examples \
  --enable-tests \
  --build-profile=optimized

# Recompilar
./ns3 build
```

### Opciones de Compilación

| Opción | Descripción | Recomendado |
|--------|-------------|-------------|
| `--enable-python-bindings` | Habilita Python | ✅ Sí |
| `--enable-examples` | Incluye ejemplos | ✅ Sí |
| `--enable-tests` | Incluye tests | ⚠️ Opcional |
| `--build-profile=optimized` | Optimiza velocidad | ✅ Sí |
| `--build-profile=debug` | Para debugging | ⚠️ Solo si debuggeas |

### Configurar Python Bindings

Si los bindings no funcionan:

```bash
# Especificar Python explícitamente
./ns3 configure \
  --enable-python-bindings \
  --with-python=/usr/bin/python3.10

# Verificar
python3 << EOF
import sys
sys.path.insert(0, 'build/lib/python3')
import ns.core
print("✓ Bindings OK")
EOF
```

---

## Configuración de Modelos

### Parámetros de Temperatura

En `config/settings.py`:

```python
# Líneas ~38-40
MODEL_TEMPERATURE_REASONING = 0.1   # Baja para respuestas deterministas
MODEL_TEMPERATURE_CODING = 0.05     # Muy baja para código preciso
MODEL_TEMPERATURE_CREATIVE = 0.3    # Moderada para análisis
```

**Guía de temperatura**:
- `0.0 - 0.1`: Muy determinista (código, cálculos)
- `0.1 - 0.3`: Balanceado (análisis, síntesis)
- `0.3 - 0.7`: Creativo (propuestas, ideas)
- `0.7 - 1.0`: Muy creativo (brainstorming)

### Límites y Timeouts

```python
# Líneas ~47-52
MAX_ITERATIONS = 5              # Reintentos máximos
SIMULATION_TIMEOUT = 900        # 15 minutos
LLM_TIMEOUT = 120              # 2 minutos
```

**Ajustar según necesidad**:

```python
# Para simulaciones grandes
SIMULATION_TIMEOUT = 1800  # 30 minutos

# Para tareas complejas
MAX_ITERATIONS = 10

# Para modelos lentos
LLM_TIMEOUT = 300  # 5 minutos
```

---

## Configuración Avanzada

### ChromaDB

```python
# Líneas ~59-63
CHROMA_COLLECTION_PAPERS = "thesis_papers"
CHROMA_N_RESULTS = 5
```

**Personalizar**:

```python
# Colección por proyecto
CHROMA_COLLECTION_PAPERS = "proyecto_vanet_2025"

# Más resultados en búsquedas
CHROMA_N_RESULTS = 10
```

### Semantic Scholar

```python
# Líneas ~68-71
SEMANTIC_SCHOLAR_MAX_RESULTS = 10
SEMANTIC_SCHOLAR_YEAR_FROM = 2020
SEMANTIC_SCHOLAR_YEAR_TO = 2025
```

**Ajustar rango de años**:

```python
# Solo papers recientes
SEMANTIC_SCHOLAR_YEAR_FROM = 2023
SEMANTIC_SCHOLAR_YEAR_TO = 2025

# Más papers
SEMANTIC_SCHOLAR_MAX_RESULTS = 20
```

### Visualización

```python
# Líneas ~76-82
PLOT_DPI = 300
PLOT_FIGSIZE = (10, 6)
PLOT_STYLE = "seaborn-v0_8-whitegrid"
```

**Personalizar gráficos**:

```python
# Alta resolución para publicación
PLOT_DPI = 600

# Figuras más grandes
PLOT_FIGSIZE = (12, 8)

# Estilo diferente
PLOT_STYLE = "ggplot"
```

### Logging

```python
# Líneas ~87-93
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

**Niveles de logging**:

```python
# Más detalle (debugging)
LOG_LEVEL = "DEBUG"

# Solo errores
LOG_LEVEL = "ERROR"

# Formato personalizado
LOG_FORMAT = "[%(levelname)s] %(message)s"
```

---

## Variables de Entorno

### Crear Archivo `.env`

```bash
# En el directorio raíz del proyecto
nano .env
```

**Contenido**:

```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
MODEL_REASONING=llama3.1:8b
MODEL_CODING=deepseek-coder-v2:16b

# NS-3
NS3_ROOT=/home/usuario/tesis-a2a/ns-allinone-3.43/ns-3.43

# Límites
MAX_ITERATIONS=5
SIMULATION_TIMEOUT=900

# Logging
LOG_LEVEL=INFO
```

### Cargar Variables

El sistema carga automáticamente `.env` si existe:

```python
# En config/settings.py
from dotenv import load_dotenv
load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
```

---

## Configuración por Proyecto

### Crear Configuración Específica

Para diferentes proyectos de investigación:

```bash
# Crear archivo de configuración
cp config/settings.py config/settings_vanet.py
```

**Editar `config/settings_vanet.py`**:

```python
# Configuración específica para proyecto VANET

# Modelos optimizados para VANETs
MODEL_REASONING = "llama3.1:70b"  # Mejor análisis
MODEL_CODING = "deepseek-coder-v2:236b"  # Código más complejo

# Timeouts más largos
SIMULATION_TIMEOUT = 1800  # 30 minutos

# Colección específica
CHROMA_COLLECTION_PAPERS = "vanet_research_2025"

# Búsqueda enfocada
SEMANTIC_SCHOLAR_YEAR_FROM = 2023
```

**Usar configuración específica**:

```python
# En main.py
import sys
if '--config' in sys.argv:
    config_file = sys.argv[sys.argv.index('--config') + 1]
    exec(open(f'config/{config_file}').read())
```

```bash
# Ejecutar con configuración específica
python main.py --config settings_vanet.py --task "Tu tarea"
```

---

## Configuración de Hardware

### Para Hardware Limitado (16 GB RAM)

```python
# config/settings_low.py

# Modelos pequeños
MODEL_REASONING = "llama3.1:8b"
MODEL_CODING = "qwen2.5-coder:7b"

# Límites conservadores
MAX_ITERATIONS = 3
SIMULATION_TIMEOUT = 600

# Menos resultados
SEMANTIC_SCHOLAR_MAX_RESULTS = 5
CHROMA_N_RESULTS = 3
```

### Para Hardware Potente (64 GB RAM + GPU)

```python
# config/settings_high.py

# Modelos grandes
MODEL_REASONING = "llama3.1:70b"
MODEL_CODING = "deepseek-coder-v2:236b"

# Límites generosos
MAX_ITERATIONS = 10
SIMULATION_TIMEOUT = 3600  # 1 hora

# Más resultados
SEMANTIC_SCHOLAR_MAX_RESULTS = 20
CHROMA_N_RESULTS = 10
```

---

## Verificar Configuración

### Script de Verificación

```bash
# Verificar configuración actual
python -c "from config.settings import *; print_configuration()"
```

**Salida esperada**:
```
================================================================================
CONFIGURACIÓN DEL SISTEMA A2A
================================================================================
Directorio del proyecto: /home/usuario/sistema-a2a-tesis
NS-3: /home/usuario/tesis-a2a/ns-allinone-3.43/ns-3.43
Ollama: http://localhost:11434
Modelo de razonamiento: llama3.1:8b
Modelo de código: deepseek-coder-v2:16b
Modelo de embeddings: nomic-embed-text
Máximo de iteraciones: 5
Timeout de simulación: 900s
================================================================================
```

### Validar Configuración

```bash
# Validar que todo esté correcto
python -c "from config.settings import validate_configuration; errors = validate_configuration(); print('✓ OK' if not errors else errors)"
```

---

## Troubleshooting de Configuración

### Problema: NS-3 no encontrado

```python
# Verificar ruta
from config.settings import NS3_ROOT
print(NS3_ROOT)
print(NS3_ROOT.exists())

# Si es False, ajustar en settings.py
```

### Problema: Ollama no responde

```bash
# Verificar URL
curl http://localhost:11434/api/tags

# Si falla, verificar que Ollama esté corriendo
ps aux | grep ollama

# Reiniciar si es necesario
pkill ollama
ollama serve &
```

### Problema: Modelos no encontrados

```bash
# Listar modelos instalados
ollama list

# Descargar faltantes
ollama pull llama3.1:8b
ollama pull deepseek-coder-v2:16b
```

---

## Configuración Recomendada por Escenario

### Escenario 1: Desarrollo y Pruebas

```python
MODEL_REASONING = "llama3.1:8b"
MODEL_CODING = "qwen2.5-coder:7b"
MAX_ITERATIONS = 3
SIMULATION_TIMEOUT = 300
LOG_LEVEL = "DEBUG"
```

### Escenario 2: Investigación Intensiva

```python
MODEL_REASONING = "llama3.1:70b"
MODEL_CODING = "deepseek-coder-v2:236b"
MAX_ITERATIONS = 10
SIMULATION_TIMEOUT = 1800
LOG_LEVEL = "INFO"
```

### Escenario 3: Producción (Resultados Finales)

```python
MODEL_REASONING = "llama3.1:70b"
MODEL_CODING = "deepseek-coder-v2:236b"
MAX_ITERATIONS = 5
SIMULATION_TIMEOUT = 900
LOG_LEVEL = "WARNING"
PLOT_DPI = 600  # Alta resolución
```

---

## Backup de Configuración

### Guardar Configuración Actual

```bash
# Crear backup
cp config/settings.py config/settings.backup.$(date +%Y%m%d).py

# O con Git
git add config/settings.py
git commit -m "Configuración actualizada"
```

### Restaurar Configuración

```bash
# Desde backup
cp config/settings.backup.20241123.py config/settings.py

# O con Git
git checkout config/settings.py
```

---

## Próximos Pasos

Una vez configurado el sistema:

1. Verifica con: `python scripts/check_system.py`
2. Prueba con: `python main.py --task "Tarea simple"`
3. Ajusta según resultados
4. Lee: [Uso Básico](03-USO-BASICO.md)

---

**¿Problemas con la configuración?** Consulta [Troubleshooting](05-TROUBLESHOOTING.md)
