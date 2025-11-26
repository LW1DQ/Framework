#!/bin/bash

###############################################################################
#                                                                             #
#           Script de Instalación Automática - Sistema A2A v1.5              #
#                                                                             #
#     Framework Multi-Agente para Optimización de Protocolos de Enrutamiento #
#                  Incluye NS-3 3.45 + 5G-LENA + Herramientas                #
#                                                                             #
###############################################################################

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Variables Globales
NS3_VERSION="3.45"
NS3_DIR="$HOME/ns-$NS3_VERSION"
REQUIRED_SPACE_KB=8000000 # 8GB

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

check_disk_space() {
    print_info "Verificando espacio en disco..."
    local available_space=$(df / | awk 'NR==2 {print $4}')
    if [[ $available_space -lt $REQUIRED_SPACE_KB ]]; then
        print_error "Espacio insuficiente. Se requieren al menos 8GB libres"
        return 1
    fi
    print_success "Espacio en disco suficiente"
    return 0
}

# Banner
clear
print_header "INSTALACIÓN SISTEMA A2A v1.5 + NS-3 $NS3_VERSION"
echo ""
echo "  Framework Multi-Agente para Tesis Doctoral"
echo "  Optimización de Protocolos de Enrutamiento con Deep Learning"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Verificar sistema operativo
print_info "Detectando sistema operativo..."
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac
print_success "Sistema operativo: ${MACHINE}"
echo ""

# Verificar espacio
check_disk_space || exit 1

# Paso 1: Actualizar Sistema e Instalar Dependencias Base (Solo Linux/Debian/Ubuntu)
print_header "PASO 1: Dependencias del Sistema"

if [ "$MACHINE" == "Linux" ]; then
    if [ -f /etc/debian_version ]; then
        print_info "Detectado sistema basado en Debian/Ubuntu. Instalando dependencias..."
        
        # Lista de paquetes combinada (Framework + NS-3 + Herramientas)
        PACKAGES=(
            "build-essential"
            "gcc"
            "g++"
            "python3"
            "python3-pip"
            "python3-venv"
            "python3-dev"
            "git"
            "wget"
            "curl"
            "unzip"
            "tar"
            "bzip2"
            "cmake"
            "pkg-config"
            "libsqlite3-dev"
            "libboost-all-dev"
            "libssl-dev"
            "libxml2-dev"
            "libgtk-3-dev"
            "wireshark"
            "tcpdump"
            "tshark"
            "nmap"
            "iperf3"
            "htop"
            "sqlite3"
        )

        print_info "Actualizando repositorios..."
        sudo apt update -qq

        print_info "Instalando paquetes (esto puede tardar)..."
        # Instalar en lote para eficiencia
        if sudo apt install -y "${PACKAGES[@]}"; then
            print_success "Dependencias del sistema instaladas"
            
            # Configurar Wireshark para no-root
            if getent group wireshark >/dev/null; then
                print_info "Configurando permisos de Wireshark..."
                sudo usermod -a -G wireshark $USER
            fi
        else
            print_error "Hubo un error instalando dependencias. Verifique su conexión o permisos."
            exit 1
        fi
    else
        print_warning "Sistema Linux no Debian/Ubuntu. Instale las dependencias manualmente."
    fi
else
    print_warning "Sistema no Linux. Asegúrese de tener instaladas las herramientas de compilación (C++, CMake, etc.)."
fi
echo ""

# Paso 2: Verificar Python
print_header "PASO 2: Configuración de Python"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python encontrado: ${PYTHON_VERSION}"
    
    # Verificar versión mínima (3.8)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_success "Versión de Python compatible (>= 3.8)"
    else
        print_error "Python 3.8+ requerido. Versión actual: ${PYTHON_VERSION}"
        exit 1
    fi
else
    print_error "Python 3 no encontrado"
    exit 1
fi

# Crear entorno virtual
if [ -d "venv" ]; then
    print_info "Entorno virtual 'venv' ya existe."
else
    print_info "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
fi

# Instalar dependencias Python
print_info "Instalando dependencias de Python en venv..."
source venv/bin/activate
pip install --upgrade pip --quiet
if pip install -r requirements.txt --quiet; then
    print_success "Dependencias de requirements.txt instaladas"
else
    print_error "Error instalando requirements.txt"
    exit 1
fi
echo ""

# Paso 3: Verificar Ollama
print_header "PASO 3: Verificar Ollama (LLM Local)"
if command -v ollama &> /dev/null; then
    print_success "Ollama instalado"
    
    # Verificar servicio
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_success "Servicio Ollama activo"
        
        # Descargar modelos necesarios
        MODELS=("llama3.1:8b" "codellama:13b" "nomic-embed-text")
        for MODEL in "${MODELS[@]}"; do
            if ollama list | grep -q "$MODEL"; then
                print_success "Modelo $MODEL listo"
            else
                print_info "Descargando modelo $MODEL..."
                ollama pull $MODEL
            fi
        done
    else
        print_warning "Servicio Ollama no responde. Ejecute 'ollama serve' en otra terminal."
    fi
else
    print_warning "Ollama no encontrado. Se recomienda instalarlo para funcionalidad completa de IA."
    print_info "Instalar: curl -fsSL https://ollama.com/install.sh | sh"
fi
echo ""

# Paso 4: Instalación Robusta de NS-3 y 5G-LENA
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
    read -p "¿Desea reinstalar/recompilar NS-3? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        print_info "Usando instalación existente."
        NS3_ROOT="$NS3_DIR"
        NS3_FOUND=true
    else
        print_info "Eliminando instalación anterior..."
        rm -rf "$NS3_DIR"
        NS3_FOUND=false
    fi
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
        
        # Agregar al PATH
        if ! grep -q "ns-3.45" ~/.bashrc; then
            echo "export PATH=\$PATH:$NS3_DIR" >> ~/.bashrc
            print_info "Agregado NS-3 al PATH en .bashrc"
        fi
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
cd "$(dirname "$0")"

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

python3 scripts/check_system.py

echo ""
print_header "INSTALACIÓN COMPLETADA"
echo ""
print_success "Sistema A2A instalado y configurado."
echo "📋 Resumen:"
echo "  ✅ Python ${PYTHON_VERSION}"
echo "  ✅ Entorno Virtual (venv)"
echo "  ✅ NS-3 $NS3_VERSION + 5G-LENA (en $NS3_ROOT)"
echo "  ✅ Herramientas de Red (Wireshark, tcpdump, etc.)"
echo ""
echo "📚 Para empezar:"
echo "  1. source venv/bin/activate"
echo "  2. python main.py --task \"Tu experimento\""
echo ""
print_info "Nota: Si instaló Wireshark, es posible que necesite reiniciar sesión para capturar paquetes sin sudo."
echo ""
