#!/bin/bash

###############################################################################
#                                                                             #
#           Script de Instalación Local - Sistema A2A v1.5                   #
#                                                                             #
#     Versión modificada para instalación sin privilegios de root (sudo)      #
#                                                                             #
###############################################################################

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables Globales
NS3_VERSION="3.45"
NS3_DIR="$HOME/ns-$NS3_VERSION"

# Funciones de utilidad
print_header() {
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  $1"
    echo "═══════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Banner
clear
print_header "INSTALACIÓN LOCAL SISTEMA A2A v1.5 + NS-3 $NS3_VERSION"
echo ""
echo "  NOTA: Este script asume que las dependencias del sistema ya están instaladas."
echo "  Se omitirá la instalación de paquetes con apt/sudo."
echo ""

# Paso 1: Verificar Herramientas Básicas
print_header "PASO 1: Verificación de Herramientas"

REQUIRED_TOOLS=("git" "cmake" "g++" "python3" "wget" "tar")
MISSING_TOOLS=0

for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v $tool &> /dev/null; then
        print_success "$tool encontrado"
    else
        print_error "$tool NO encontrado"
        MISSING_TOOLS=$((MISSING_TOOLS+1))
    fi
done

if [ $MISSING_TOOLS -gt 0 ]; then
    print_error "Faltan herramientas necesarias. Por favor, instálelas o contacte al administrador."
    exit 1
fi
echo ""

# Paso 2: Verificar Python
print_header "PASO 2: Configuración de Python"
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python encontrado: ${PYTHON_VERSION}"

# Crear entorno virtual
if [ -d "venv" ]; then
    print_info "Entorno virtual 'venv' ya existe."
else
    print_info "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Instalar dependencias Python con uv (más rápido)
print_info "Instalando dependencias de Python en venv..."
source venv/bin/activate
pip install uv --quiet
print_info "Usando uv para instalar dependencias..."
    # Instalar PyTorch CPU primero para evitar descargar CUDA
    print_info "Instalando PyTorch (CPU only)..."
    uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
if uv pip install -r requirements.txt; then
    print_success "Dependencias de requirements.txt instaladas"
else
    print_error "Error instalando requirements.txt"
    exit 1
fi
echo ""

# Paso 3: Verificar Ollama (Opcional)
print_header "PASO 3: Verificar Ollama (LLM Local)"
if command -v ollama &> /dev/null; then
    print_success "Ollama instalado"
else
    print_warning "Ollama no encontrado. Algunas funciones de IA no estarán disponibles."
    print_info "Puede instalarlo localmente si tiene permisos, o usar un servidor remoto."
fi
echo ""

# Paso 4: Instalación de NS-3 y 5G-LENA
print_header "PASO 4: Instalación de NS-3 $NS3_VERSION + 5G-LENA"

install_5g_lena() {
    local NS3_PATH=$1
    print_info "Instalando módulo 5G-LENA..."
    
    cd "$NS3_PATH/contrib"
    
    if [ -d "nr" ]; then
        print_warning "Módulo 5G-LENA ya existe en contrib/nr"
        return 0
    fi
    
    print_info "Clonando repositorio 5G-LENA..."
    if git clone https://gitlab.com/cttc-lena/nr.git; then
        cd nr
        print_info "Seleccionando rama compatible 5g-lena-v4.1.y..."
        if git checkout -b 5g-lena-v4.1.y origin/5g-lena-v4.1.y; then
            print_success "Módulo 5G-LENA preparado"
        else
            print_error "Error checkout rama 5g-lena"
            return 1
        fi
        cd ../.. # Volver a root ns3
    else
        print_error "Error clonando 5G-LENA"
        return 1
    fi
}

# Verificar si ya está instalado
if [ -d "$NS3_DIR" ]; then
    print_warning "Directorio NS-3 ya existe en: $NS3_DIR"
    print_info "Usando instalación existente."
    NS3_ROOT="$NS3_DIR"
    NS3_FOUND=true
else
    NS3_FOUND=false
fi

if [ "$NS3_FOUND" = false ]; then
    print_info "Iniciando instalación de NS-3 $NS3_VERSION..."
    
    cd "$HOME"
    
    # Descargar
    if [ ! -f "ns-3.45.tar.bz2" ]; then
        print_info "Descargando código fuente..."
        wget https://www.nsnam.org/releases/ns-3.45.tar.bz2
    fi
    
    print_info "Extrayendo..."
    tar xjf ns-3.45.tar.bz2
    
    # Instalar 5G-LENA
    install_5g_lena "$NS3_DIR"
    
    cd "$NS3_DIR"
    
    # Configurar
    print_info "Configurando NS-3 (incluyendo módulo 'nr')..."
    # Habilitamos módulos clave incluyendo 'nr' (5G) y 'mesh' (HWMP)
    ./ns3 configure --enable-examples --enable-tests --build-profile=optimized --enable-modules=core,network,internet,mobility,wifi,mesh,energy,flow-monitor,aodv,dsdv,olsr,applications,csma,point-to-point,wave,nr
    
    # Compilar
    CORES=$(nproc)
    print_info "Compilando con $CORES núcleos (esto tomará tiempo)..."
    if ./ns3 build -j$CORES; then
        print_success "NS-3 compilado exitosamente"
        NS3_ROOT="$NS3_DIR"
        NS3_FOUND=true
        
        # Agregar al PATH (opcional, solo para la sesión actual si no podemos escribir en .bashrc)
        export PATH=$PATH:$NS3_DIR
    else
        print_error "Error en la compilación de NS-3"
        exit 1
    fi
fi
echo ""

# Paso 5: Configurar settings.py
print_header "PASO 5: Configurar Framework"
print_info "Actualizando config/settings.py..."

# Volver al directorio del framework
# Asumimos que el script se ejecuta desde el directorio del framework o conocemos la ruta
# En este caso, volvemos a donde estaba el script
cd "$(dirname "$(readlink -f "$0")")"

if [ "$NS3_FOUND" = true ]; then
    # Escapar barras para sed
    NS3_ROOT_ESCAPED=$(echo "$NS3_ROOT" | sed 's/\//\\\//g')
    
    if grep -q "NS3_ROOT" config/settings.py; then
        sed -i.bak "s/NS3_ROOT = Path(\".*\")/NS3_ROOT = Path(\"$NS3_ROOT_ESCAPED\")/" config/settings.py
        print_success "NS3_ROOT actualizado a: $NS3_ROOT"
    fi
fi

# Paso 6: Crear Estructura de Directorios
print_header "PASO 6: Estructura de Directorios"
DIRS=(
    "logs"
    "data/papers"
    "data/vector_db"
    "simulations/scripts"
    "simulations/scripts/backups"
    "simulations/results"
    "simulations/plots"
    "simulations/optimizations"
    "workspace" 
    "docs"
)

for DIR in "${DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        mkdir -p "$DIR"
        print_success "Creado: $DIR"
    fi
done
echo ""

# Paso 7: Verificación Final
print_header "PASO 7: Verificación del Sistema"
print_info "Ejecutando script de diagnóstico..."

# Asegurarse de estar en el entorno virtual
source venv/bin/activate
python3 scripts/check_system.py

echo ""
print_header "INSTALACIÓN LOCAL COMPLETADA"
echo ""
print_success "Sistema A2A instalado y configurado (Modo Local)."
echo "📋 Resumen:"
echo "  ✅ Python ${PYTHON_VERSION}"
echo "  ✅ Entorno Virtual (venv)"
echo "  ✅ NS-3 $NS3_VERSION + 5G-LENA (en $NS3_ROOT)"
echo ""
print_info "Para empezar:"
echo "  source venv/bin/activate"
echo "  python main.py --task \"Tu experimento\""
echo ""
