#!/bin/bash
#
# Script de Instalación Automática del Sistema A2A
# 
# Este script instala todos los componentes necesarios:
# - Ollama y modelos
# - NS-3 con Python bindings
# - Dependencias Python
# - Configuración del proyecto
#
# Uso: ./scripts/install.sh
#

set -e  # Salir si hay errores

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    print_error "Este script debe ejecutarse desde el directorio raíz del proyecto"
    exit 1
fi

print_header "INSTALACIÓN DEL SISTEMA A2A"
print_info "Este proceso puede tardar 60-90 minutos"
print_info "Asegúrate de tener conexión a internet estable"
echo ""

read -p "¿Continuar con la instalación? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    print_warning "Instalación cancelada"
    exit 0
fi

# ============================================================================
# ETAPA 1: VERIFICAR SISTEMA BASE
# ============================================================================

print_header "ETAPA 1: Verificando Sistema Base"

# Verificar Ubuntu/Debian
if [ -f /etc/os-release ]; then
    . /etc/os-release
    print_success "Sistema operativo: $NAME $VERSION"
else
    print_warning "No se pudo detectar el sistema operativo"
fi

# Verificar Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION instalado"
else
    print_error "Python 3 no encontrado"
    exit 1
fi

# Verificar Git
if command -v git &> /dev/null; then
    print_success "Git instalado"
else
    print_error "Git no encontrado. Instala con: sudo apt install git"
    exit 1
fi

# ============================================================================
# ETAPA 2: INSTALAR DEPENDENCIAS DEL SISTEMA
# ============================================================================

print_header "ETAPA 2: Instalando Dependencias del Sistema"

print_info "Actualizando lista de paquetes..."
sudo apt update

print_info "Instalando dependencias básicas..."
sudo apt install -y \
    build-essential \
    g++ \
    cmake \
    ninja-build \
    pkg-config \
    sqlite3 \
    libsqlite3-dev \
    python3-dev \
    python3-pip \
    python3-venv \
    curl \
    wget

print_success "Dependencias básicas instaladas"

print_info "Instalando dependencias de NS-3..."
sudo apt install -y \
    libxml2 \
    libxml2-dev \
    libboost-all-dev \
    libeigen3-dev \
    gsl-bin \
    libgsl-dev

print_success "Dependencias de NS-3 instaladas"

# ============================================================================
# ETAPA 3: INSTALAR OLLAMA
# ============================================================================

print_header "ETAPA 3: Instalando Ollama"

if command -v ollama &> /dev/null; then
    print_warning "Ollama ya está instalado"
else
    print_info "Descargando e instalando Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    print_success "Ollama instalado"
fi

# Iniciar Ollama
print_info "Iniciando servidor Ollama..."
ollama serve &> /dev/null &
sleep 5

# Verificar que Ollama responde
if curl -s http://localhost:11434/api/tags &> /dev/null; then
    print_success "Ollama corriendo correctamente"
else
    print_error "Ollama no responde"
    exit 1
fi

# Descargar modelos
print_info "Descargando modelos de IA (esto puede tardar 20-30 minutos)..."

print_info "  Descargando llama3.1:8b..."
ollama pull llama3.1:8b
print_success "  llama3.1:8b descargado"

print_info "  Descargando deepseek-coder-v2:16b..."
ollama pull deepseek-coder-v2:16b
print_success "  deepseek-coder-v2:16b descargado"

print_info "  Descargando nomic-embed-text..."
ollama pull nomic-embed-text
print_success "  nomic-embed-text descargado"

print_success "Todos los modelos descargados"

# ============================================================================
# ETAPA 4: COMPILAR NS-3
# ============================================================================

print_header "ETAPA 4: Compilando NS-3"

# Crear directorio de trabajo
WORK_DIR="$HOME/tesis-a2a"
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# Descargar NS-3
if [ ! -d "ns-allinone-3.43" ]; then
    print_info "Descargando NS-3 3.43..."
    wget https://www.nsnam.org/releases/ns-allinone-3.43.tar.bz2
    tar xjf ns-allinone-3.43.tar.bz2
    print_success "NS-3 descargado"
else
    print_warning "NS-3 ya descargado"
fi

cd ns-allinone-3.43/ns-3.43

# Configurar NS-3
print_info "Configurando NS-3 con Python bindings..."
./ns3 configure --enable-python-bindings --enable-examples
print_success "NS-3 configurado"

# Compilar NS-3
print_info "Compilando NS-3 (esto puede tardar 20-40 minutos)..."
./ns3 build --jobs=$(nproc)
print_success "NS-3 compilado"

# Verificar compilación
if ./ns3 run hello-simulator &> /dev/null; then
    print_success "NS-3 funciona correctamente"
else
    print_error "NS-3 no funciona correctamente"
    exit 1
fi

# Instalar ns3-ai
print_info "Instalando ns3-ai..."
cd contrib
if [ ! -d "ns3-ai" ]; then
    git clone https://github.com/hust-diangroup/ns3-ai.git
fi
cd ..
./ns3 configure --enable-python-bindings
./ns3 build
print_success "ns3-ai instalado"

# ============================================================================
# ETAPA 5: CONFIGURAR PROYECTO PYTHON
# ============================================================================

print_header "ETAPA 5: Configurando Proyecto Python"

# Volver al directorio del proyecto
cd "$OLDPWD"

# Crear entorno virtual
print_info "Creando entorno virtual..."
python3 -m venv venv
print_success "Entorno virtual creado"

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
print_info "Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar dependencias
print_info "Instalando dependencias Python (esto puede tardar 5-10 minutos)..."
pip install -r requirements.txt --quiet
print_success "Dependencias Python instaladas"

# Instalar ns3-ai Python interface
print_info "Instalando interfaz Python de ns3-ai..."
pip install "$WORK_DIR/ns-allinone-3.43/ns-3.43/contrib/ns3-ai/py_interface" --quiet
print_success "Interfaz ns3-ai instalada"

# Configurar settings.py
print_info "Configurando settings.py..."
cat > config/settings_local.py << EOF
# Configuración local generada automáticamente
from pathlib import Path

NS3_ROOT = Path.home() / "tesis-a2a" / "ns-allinone-3.43" / "ns-3.43"
EOF
print_success "Configuración creada"

# ============================================================================
# ETAPA 6: VERIFICACIÓN FINAL
# ============================================================================

print_header "ETAPA 6: Verificación Final"

print_info "Ejecutando verificación del sistema..."
python scripts/check_system.py

# ============================================================================
# FINALIZACIÓN
# ============================================================================

print_header "INSTALACIÓN COMPLETADA"

echo -e "${GREEN}✓ Ollama instalado y modelos descargados${NC}"
echo -e "${GREEN}✓ NS-3 compilado con Python bindings${NC}"
echo -e "${GREEN}✓ ns3-ai instalado${NC}"
echo -e "${GREEN}✓ Dependencias Python instaladas${NC}"
echo -e "${GREEN}✓ Proyecto configurado${NC}"

echo ""
print_info "Para usar el sistema:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta una tarea: python main.py --task \"Tu tarea\""
echo ""
print_info "Consulta la documentación en: docs/03-USO-BASICO.md"
echo ""

print_success "¡Sistema listo para usar!"
