#!/bin/bash

###############################################################################
#                                                                             #
#           Script de Instalación MAESTRO - Sistema A2A v1.5                 #
#                                                                             #
#     Instalación completa desde CERO para usuarios nuevos en Ubuntu/Debian  #
#                                                                             #
###############################################################################

set -e  # Salir inmediatamente si hay un error

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variables
NS3_VERSION="3.45"
NS3_DIR="$HOME/ns3"
FRAMEWORK_DIR="$(pwd)"
LOG_FILE="install_log.txt"

# Funciones de log
log() {
    echo -e "${BLUE}[INFO]${NC} $1"
    echo "[INFO] $1" >> $LOG_FILE
}

success() {
    echo -e "${GREEN}[EXITO]${NC} $1"
    echo "[EXITO] $1" >> $LOG_FILE
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    echo "[ERROR] $1" >> $LOG_FILE
    exit 1
}

warn() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
    echo "[AVISO] $1" >> $LOG_FILE
}

# Inicio
clear
echo "═══════════════════════════════════════════════════════════════════"
echo "   INSTALACIÓN COMPLETA SISTEMA A2A"
echo "═══════════════════════════════════════════════════════════════════"
echo "Este script instalará TODO lo necesario:"
echo "1. Dependencias del sistema (apt)"
echo "2. Python 3.10 y entorno virtual"
echo "3. Simulador NS-3 $NS3_VERSION"
echo "4. Ollama y modelos de IA"
echo "5. Configuración del Framework"
echo ""
echo "⚠️  Se requieren permisos de sudo."
echo "⚠️  Tiempo estimado: 20-40 minutos."
echo ""
read -p "Presiona ENTER para comenzar..."

# 1. Actualizar Sistema
log "Actualizando sistema..."
sudo apt update -qq && sudo apt upgrade -y -qq || error "Fallo al actualizar sistema"

# 2. Instalar Dependencias
log "Instalando dependencias del sistema..."
DEPENDENCIES=(
    "git" "curl" "wget" "build-essential" "htop" "python3" "python3-pip" 
    "python3-venv" "python3-dev" "cmake" "libsqlite3-dev" "libboost-all-dev" 
    "libssl-dev" "libxml2-dev" "libgtk-3-dev" "wireshark" "tcpdump"
)
sudo apt install -y "${DEPENDENCIES[@]}" || error "Fallo al instalar dependencias"

# Verificar Python
if ! command -v python3.10 &> /dev/null; then
    log "Python 3.10 no encontrado. Instalando..."
    sudo add-apt-repository ppa:deadsnakes/ppa -y
    sudo apt update -qq
    sudo apt install -y python3.10 python3.10-venv python3.10-dev || error "Fallo instalando Python 3.10"
fi
success "Dependencias instaladas"

# 3. Configurar Framework
log "Configurando entorno Python..."
if [ -d "venv" ]; then
    warn "Entorno virtual ya existe. Recreando..."
    rm -rf venv
fi

python3.10 -m venv venv || error "Fallo creando venv"
source venv/bin/activate || error "Fallo activando venv"

log "Instalando librerías Python..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet || error "Fallo instalando requirements.txt"
success "Entorno Python configurado"

# 4. Instalar NS-3
if [ -d "$NS3_DIR" ]; then
    warn "NS-3 ya existe en $NS3_DIR. Saltando instalación."
else
    log "Instalando NS-3 (esto tardará)..."
    cd "$HOME"
    wget https://www.nsnam.org/releases/ns-3.45.tar.bz2 -O ns3.tar.bz2 || error "Fallo descargando NS-3"
    tar xjf ns3.tar.bz2
    mv ns-3.45 ns3
    rm ns3.tar.bz2
    
    cd ns3
    
    # Instalar ns3-ai
    log "Instalando ns3-ai..."
    cd contrib
    if [ ! -d "ns3-ai" ]; then
        git clone https://github.com/hust-diangroup/ns3-ai.git || error "Fallo clonando ns3-ai"
    else
        log "ns3-ai ya existe en contrib"
    fi
    cd ..

    log "Configurando NS-3..."
    ./ns3 configure --enable-examples --enable-tests --build-profile=optimized || error "Fallo configurando NS-3"
    
    log "Compilando NS-3 (paciencia)..."
    ./ns3 build -j$(nproc) || error "Fallo compilando NS-3"
    
    cd "$FRAMEWORK_DIR"
    success "NS-3 instalado en $NS3_DIR"
fi

# 5. Instalar Ollama
if command -v ollama &> /dev/null; then
    success "Ollama ya está instalado"
else
    log "Instalando Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh || error "Fallo instalando Ollama"
fi

# Iniciar servicio si es necesario
if ! systemctl is-active --quiet ollama; then
    log "Iniciando servicio Ollama..."
    sudo systemctl start ollama
fi

log "Descargando modelo Llama 3.1 (8B)..."
ollama pull llama3.1:8b || error "Fallo descargando modelo"
success "IA configurada"

# 6. Configuración Final
log "Actualizando configuración..."
SETTINGS_FILE="config/settings.py"
# Escapar ruta para sed
NS3_PATH_ESCAPED=$(echo "$NS3_DIR" | sed 's/\//\\\//g')
sed -i "s/NS3_ROOT = Path(\".*\")/NS3_ROOT = Path(\"$NS3_PATH_ESCAPED\")/" "$SETTINGS_FILE"

# 7. Verificación
log "Verificando instalación..."
python verify-system-complete.py

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "   ✅ INSTALACIÓN COMPLETADA CON ÉXITO"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Para comenzar:"
echo "1. source venv/bin/activate"
echo "2. python main.py --task \"Tu experimento\""
echo ""
