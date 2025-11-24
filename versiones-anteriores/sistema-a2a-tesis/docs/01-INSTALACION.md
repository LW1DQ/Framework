# 📦 Guía de Instalación Completa - Sistema A2A

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Etapa 1: Preparación del Sistema](#etapa-1-preparación-del-sistema)
3. [Etapa 2: Instalación de Ollama](#etapa-2-instalación-de-ollama)
4. [Etapa 3: Compilación de NS-3](#etapa-3-compilación-de-ns-3)
5. [Etapa 4: Configuración del Proyecto Python](#etapa-4-configuración-del-proyecto-python)
6. [Etapa 5: Verificación Final](#etapa-5-verificación-final)
7. [Instalación Automática](#instalación-automática)

---

## Requisitos Previos

### Hardware Mínimo

| Componente | Mínimo | Recomendado | Óptimo |
|------------|--------|-------------|--------|
| **RAM** | 16 GB | 32 GB | 64 GB |
| **CPU** | 4 cores @ 2.5GHz | 8 cores @ 3.0GHz | 16 cores |
| **Almacenamiento** | 100 GB SSD | 250 GB NVMe | 500 GB NVMe |
| **GPU** | No requerida | NVIDIA RTX 3060 | RTX 4090 |

### Sistema Operativo

**Recomendado**: Ubuntu 22.04 LTS o Ubuntu 24.04 LTS

**Alternativas**:
- Ubuntu 20.04 LTS (con actualizaciones)
- Debian 11+
- Windows 10/11 con WSL2 (Ubuntu)
- macOS 12+ (con limitaciones en NS-3)

### Software Base Requerido

- Python 3.10 o superior
- Git
- Curl/Wget
- Compilador C++ (g++ 9+)
- CMake 3.16+

---

## Etapa 1: Preparación del Sistema

### 1.1 Actualizar el Sistema (Ubuntu/Debian)

```bash
# Actualizar lista de paquetes
sudo apt update

# Actualizar paquetes instalados
sudo apt upgrade -y

# Instalar herramientas básicas
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    vim \
    htop
```

**Tiempo estimado**: 5-10 minutos

### 1.2 Instalar Dependencias de Desarrollo

```bash
# Dependencias para Python
sudo apt install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip

# Dependencias para NS-3
sudo apt install -y \
    g++ \
    cmake \
    ninja-build \
    pkg-config \
    sqlite3 \
    libsqlite3-dev \
    libxml2 \
    libxml2-dev \
    libboost-all-dev \
    libeigen3-dev \
    gsl-bin \
    libgsl-dev

# Dependencias opcionales para NS-3 (visualización)
sudo apt install -y \
    gir1.2-goocanvas-2.0 \
    python3-gi \
    python3-gi-cairo \
    python3-pygraphviz \
    gir1.2-gtk-3.0 \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools
```

**Tiempo estimado**: 10-15 minutos

### 1.3 Verificar Versiones

```bash
# Verificar Python
python3 --version
# Debe mostrar: Python 3.10.x o superior

# Verificar Git
git --version
# Debe mostrar: git version 2.x.x

# Verificar g++
g++ --version
# Debe mostrar: g++ (Ubuntu) 9.x.x o superior

# Verificar CMake
cmake --version
# Debe mostrar: cmake version 3.16.x o superior
```

✅ **Checkpoint**: Si todos los comandos anteriores funcionan, puedes continuar.

---

## Etapa 2: Instalación de Ollama

### 2.1 Instalar Ollama

**Para Linux/Mac**:

```bash
# Descargar e instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

**Para Windows**:

1. Descargar el instalador desde: https://ollama.com/download
2. Ejecutar el instalador `.exe`
3. Seguir las instrucciones en pantalla

**Tiempo estimado**: 2-3 minutos

### 2.2 Verificar Instalación de Ollama

```bash
# Verificar que Ollama está instalado
ollama --version

# Iniciar el servidor Ollama (si no está corriendo)
ollama serve &

# Esperar 5 segundos
sleep 5

# Verificar que el servidor responde
curl http://localhost:11434/api/tags
```

**Salida esperada**: Un JSON con la lista de modelos (puede estar vacía inicialmente)

### 2.3 Descargar Modelos de IA

```bash
# Modelo para razonamiento general (8B, cuantizado)
ollama pull llama3.1:8b

# Modelo para generación de código (recomendado)
ollama pull deepseek-coder-v2:16b

# Modelo alternativo para código (más ligero)
ollama pull qwen2.5-coder:7b

# Modelo para embeddings (búsqueda semántica)
ollama pull nomic-embed-text
```

**Tiempo estimado**: 15-30 minutos (depende de tu conexión a internet)

**Tamaños aproximados**:
- llama3.1:8b → ~4.7 GB
- deepseek-coder-v2:16b → ~9 GB
- qwen2.5-coder:7b → ~4 GB
- nomic-embed-text → ~274 MB

### 2.4 Probar los Modelos

```bash
# Probar modelo de razonamiento
ollama run llama3.1:8b "Explica qué es un protocolo de enrutamiento"

# Probar modelo de código
ollama run deepseek-coder-v2:16b "Escribe una función Python para calcular factorial"
```

✅ **Checkpoint**: Si los modelos responden correctamente, Ollama está listo.

---

## Etapa 3: Compilación de NS-3

### 3.1 Descargar NS-3

```bash
# Crear directorio de trabajo
mkdir -p ~/tesis-a2a
cd ~/tesis-a2a

# Descargar NS-3 versión 3.43 (estable)
wget https://www.nsnam.org/releases/ns-allinone-3.43.tar.bz2

# Extraer el archivo
tar xjf ns-allinone-3.43.tar.bz2

# Entrar al directorio
cd ns-allinone-3.43/ns-3.43
```

**Tiempo estimado**: 5 minutos

**Nota**: Si prefieres la versión más reciente (3.45), reemplaza `3.43` por `3.45` en los comandos.

### 3.2 Configurar NS-3 con Python Bindings

```bash
# Configurar NS-3 (IMPORTANTE: habilitar Python bindings)
./ns3 configure --enable-python-bindings --enable-examples --enable-tests

# Ver resumen de configuración
# Busca la línea: "Python Bindings: enabled"
```

**Salida esperada**:
```
-- Python Bindings: enabled
-- Python version: 3.10.x
```

**Tiempo estimado**: 2-3 minutos

### 3.3 Compilar NS-3

```bash
# Compilar usando todos los cores disponibles
./ns3 build --jobs=$(nproc)
```

**Tiempo estimado**: 20-40 minutos (depende de tu CPU)

**Nota**: Este es el paso más largo. Puedes tomar un café ☕

### 3.4 Verificar Compilación de NS-3

```bash
# Ejecutar un ejemplo simple
./ns3 run hello-simulator

# Salida esperada: "Hello Simulator"

# Probar Python bindings
python3 << EOF
import sys
sys.path.insert(0, 'build/lib/python3')
import ns.core
print("✅ Python bindings funcionando correctamente")
print(f"NS-3 versión: {ns.core.Version()}")
EOF
```

✅ **Checkpoint**: Si ves "✅ Python bindings funcionando correctamente", NS-3 está listo.

### 3.5 Instalar ns3-ai (Integración con IA)

```bash
# Entrar al directorio contrib
cd contrib

# Clonar repositorio ns3-ai
git clone https://github.com/hust-diangroup/ns3-ai.git

# Volver al directorio raíz de NS-3
cd ..

# Reconfigurar NS-3 con ns3-ai
./ns3 configure --enable-python-bindings --enable-examples

# Recompilar
./ns3 build

# Instalar interfaz Python de ns3-ai
pip3 install ./contrib/ns3-ai/py_interface
```

**Tiempo estimado**: 10-15 minutos

### 3.6 Verificar ns3-ai

```bash
# Probar ejemplo básico de ns3-ai
cd contrib/ns3-ai/examples/a-plus-b

# Ejecutar ejemplo (requiere dos terminales)
# Terminal 1:
../../build/ns3ai_apb_gym &

# Terminal 2:
python3 run_gym.py
```

**Salida esperada**: Mensajes de suma (A + B = C)

✅ **Checkpoint**: Si el ejemplo funciona, ns3-ai está correctamente instalado.

---

## Etapa 4: Configuración del Proyecto Python

### 4.1 Clonar/Copiar el Proyecto

```bash
# Volver al directorio de trabajo
cd ~/tesis-a2a

# Si tienes el proyecto en Git
git clone <URL_DEL_REPOSITORIO> sistema-a2a-tesis

# O copiar la carpeta del proyecto
# cp -r /ruta/al/proyecto sistema-a2a-tesis

cd sistema-a2a-tesis
```

### 4.2 Crear Entorno Virtual Python

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

**Nota**: Verás `(venv)` al inicio de tu prompt cuando esté activado.

### 4.3 Instalar Dependencias Python

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt
```

**Tiempo estimado**: 5-10 minutos

**Dependencias principales**:
- langgraph
- langchain
- langchain-community
- langchain-ollama
- chromadb
- pandas
- matplotlib
- seaborn
- scipy
- semanticscholar

### 4.4 Configurar Variables de Entorno

```bash
# Crear archivo de configuración
cp config/settings.example.py config/settings.py

# Editar configuración
nano config/settings.py
```

**Editar las siguientes líneas**:

```python
# Ruta a NS-3
NS3_ROOT = Path.home() / "tesis-a2a" / "ns-allinone-3.43" / "ns-3.43"

# URL de Ollama
OLLAMA_BASE_URL = "http://localhost:11434"

# Modelos a usar
MODEL_REASONING = "llama3.1:8b"
MODEL_CODING = "deepseek-coder-v2:16b"
MODEL_EMBEDDING = "nomic-embed-text"
```

### 4.5 Crear Directorios Necesarios

```bash
# El script lo hace automáticamente, pero por si acaso:
mkdir -p logs
mkdir -p simulations/scripts
mkdir -p simulations/results
mkdir -p simulations/plots
mkdir -p data/papers
mkdir -p data/vector_db
```

---

## Etapa 5: Verificación Final

### 5.1 Ejecutar Script de Verificación

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate

# Ejecutar verificación completa
python scripts/check_system.py
```

**Salida esperada**:

```
🔍 Verificando Sistema A2A...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Python 3.10.12
✅ Entorno virtual activado
✅ Ollama corriendo (http://localhost:11434)
✅ Modelos Ollama:
   - llama3.1:8b
   - deepseek-coder-v2:16b
   - nomic-embed-text
✅ NS-3 encontrado: /home/user/tesis-a2a/ns-allinone-3.43/ns-3.43
✅ Python bindings de NS-3 funcionando
✅ ns3-ai instalado
✅ Dependencias Python instaladas:
   - langgraph ✓
   - langchain ✓
   - chromadb ✓
   - pandas ✓
   - matplotlib ✓
✅ Directorios creados correctamente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 SISTEMA LISTO PARA USAR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 5.2 Ejecutar Prueba Básica

```bash
# Ejecutar ejemplo básico
python examples/ejemplo_basico.py
```

**Salida esperada**: El sistema debe ejecutar un flujo simple sin errores.

---

## Instalación Automática

Si prefieres una instalación automática, usa el script incluido:

```bash
# Dar permisos de ejecución
chmod +x scripts/install.sh

# Ejecutar instalador
./scripts/install.sh
```

El script ejecutará todas las etapas automáticamente y te mostrará el progreso.

**Tiempo total estimado**: 60-90 minutos

---

## Solución de Problemas Comunes

### Problema: "Ollama no responde"

```bash
# Reiniciar Ollama
pkill ollama
ollama serve &
sleep 5
curl http://localhost:11434/api/tags
```

### Problema: "NS-3 no compila"

```bash
# Limpiar y recompilar
./ns3 clean
./ns3 configure --enable-python-bindings
./ns3 build
```

### Problema: "Python bindings no funcionan"

```bash
# Verificar que Python 3.10+ está instalado
python3 --version

# Reconfigurar con Python específico
./ns3 configure --enable-python-bindings \
    --with-python=/usr/bin/python3.10
./ns3 build
```

### Problema: "Memoria insuficiente durante compilación"

```bash
# Compilar con menos jobs
./ns3 build --jobs=2
```

---

## Próximos Pasos

Una vez completada la instalación:

1. Lee la [Guía de Configuración](02-CONFIGURACION.md)
2. Prueba el [Uso Básico](03-USO-BASICO.md)
3. Explora los [Ejemplos](../examples/)

---

## Notas Adicionales

### Para Windows con WSL2

1. Instalar WSL2: `wsl --install -d Ubuntu-22.04`
2. Abrir terminal de Ubuntu
3. Seguir las instrucciones de Linux

### Para macOS

1. Instalar Homebrew: https://brew.sh
2. Instalar dependencias: `brew install python cmake boost eigen gsl`
3. Seguir las instrucciones generales (NS-3 puede tener limitaciones)

### Recursos Adicionales

- Documentación NS-3: https://www.nsnam.org/documentation/
- Documentación Ollama: https://ollama.com/docs
- Documentación LangGraph: https://langchain-ai.github.io/langgraph/

---

**¿Problemas durante la instalación?** Consulta [Troubleshooting](05-TROUBLESHOOTING.md) o contacta al administrador del sistema.
