#!/bin/bash

###############################################################################
#                                                                             #
#           A2A FRAMEWORK - UNIVERSAL INSTALLER & SANDBOX CREATOR            #
#                                                                             #
#   Este script descarga e instala todo el sistema A2A en tu máquina.         #
#   Crea un entorno aislado (Sandbox) listo para investigar.                  #
#                                                                             #
#   Repositorio: https://github.com/LW1DQ/Framework                           #
#                                                                             #
###############################################################################

set -e  # Salir si hay error

# --- CONFIGURACIÓN ---
REPO_URL="https://github.com/LW1DQ/Framework.git"
DEFAULT_INSTALL_DIR="$HOME/A2A_Research_Sandbox"
NS3_VERSION="3.45"
NS3_DIR_NAME="ns-3.45"
PYTHON_VERSION="3.10"

# --- COLORES ---
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# --- FUNCIONES ---
log() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[EXITO]${NC} $1"; }
warn() { echo -e "${YELLOW}[AVISO]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

print_banner() {
    clear
    echo -e "${BLUE}"
    echo "═══════════════════════════════════════════════════════════════════"
    echo "      🚀  A2A FRAMEWORK - INSTALADOR DE ENTORNO DE INVESTIGACIÓN"
    echo "═══════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo "Este script preparará tu entorno de investigación completo:"
    echo " 1. Creará la carpeta Sandbox en: $INSTALL_DIR"
    echo " 2. Descargará el Framework A2A (Agentes, Scripts, Documentación)"
    echo " 3. Instalará/Detectará el simulador NS-3 ($NS3_VERSION)"
    echo " 4. Configurará el entorno Python y las dependencias"
    echo ""
}

# --- INICIO ---

# 1. Definir directorio de instalación
if [ -z "$1" ]; then
    INSTALL_DIR="$DEFAULT_INSTALL_DIR"
else
    INSTALL_DIR="$1"
fi

print_banner

echo -e "Directorio de instalación: ${YELLOW}$INSTALL_DIR${NC}"
read -p "¿Deseas continuar? (s/n): " confirm
if [[ $confirm != "s" && $confirm != "S" ]]; then
    exit 0
fi

# 2. Verificar dependencias base
log "Verificando dependencias del sistema..."
sudo apt update -qq

DEPENDENCIES=(git curl wget python3 python3-venv python3-dev build-essential cmake)
MISSING_DEPS=()

for dep in "${DEPENDENCIES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $dep"; then
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
    log "Instalando dependencias faltantes: ${MISSING_DEPS[*]}"
    sudo apt install -y "${MISSING_DEPS[@]}"
else
    success "Dependencias base OK"
fi

# 3. Preparar Directorio Sandbox
log "Preparando Sandbox en $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# 4. Clonar/Actualizar Framework
if [ -d "$INSTALL_DIR/.git" ]; then
    log "Actualizando repositorio existente..."
    cd "$INSTALL_DIR"
    git pull
else
    log "Clonando repositorio..."
    git clone "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
fi

# 5. Configurar Entorno Python
log "Configurando entorno virtual Python..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip --quiet
log "Instalando librerías del Framework (esto puede tardar)..."
pip install -r requirements.txt --quiet
success "Entorno Python listo"

# 6. Instalar/Verificar NS-3
log "Verificando instalación de NS-3..."

# Buscar NS-3 en ubicaciones comunes
NS3_FOUND=false
POSSIBLE_NS3_PATHS=(
    "$HOME/ns3"
    "$HOME/ns-3-allinone/ns-3.$NS3_VERSION"
    "$HOME/ns-3.$NS3_VERSION"
    "$INSTALL_DIR/ns3"
)

FINAL_NS3_PATH=""

for path in "${POSSIBLE_NS3_PATHS[@]}"; do
    if [ -f "$path/ns3" ]; then
        log "NS-3 detectado en: $path"
        FINAL_NS3_PATH="$path"
        NS3_FOUND=true
        break
    fi
done

if [ "$NS3_FOUND" = false ]; then
    warn "NS-3 no encontrado. Se procederá a instalarlo."
    read -p "¿Deseas instalar NS-3 ahora? (Recomendado) (s/n): " install_ns3
    
    if [[ $install_ns3 == "s" || $install_ns3 == "S" ]]; then
        log "Descargando e instalando NS-3 (Paciencia, tomará tiempo)..."
        
        # Instalar deps de NS-3
        sudo apt install -y libsqlite3-dev libboost-all-dev libssl-dev libgsl-dev libgtk-3-dev
        
        cd "$HOME"
        wget "https://www.nsnam.org/releases/ns-allinone-$NS3_VERSION.tar.bz2"
        tar xjf "ns-allinone-$NS3_VERSION.tar.bz2"
        
        FINAL_NS3_PATH="$HOME/ns-allinone-$NS3_VERSION/ns-$NS3_VERSION"
        
        cd "$FINAL_NS3_PATH"
        ./ns3 configure --enable-examples --enable-tests --build-profile=optimized
        ./ns3 build -j$(nproc)
        
        success "NS-3 instalado en $FINAL_NS3_PATH"
        cd "$INSTALL_DIR"
    else
        warn "Se omitió la instalación de NS-3. Deberás configurarlo manualmente en config/settings.py"
    fi
fi

# 7. Configurar settings.py
if [ ! -z "$FINAL_NS3_PATH" ]; then
    log "Configurando ruta de NS-3 en el Framework..."
    SETTINGS_FILE="config/settings.py"
    
    # Escapar ruta para sed
    ESCAPED_PATH=$(echo "$FINAL_NS3_PATH" | sed 's/\//\\\//g')
    
    # Reemplazar la línea que define NS3_ROOT
    # Busca cualquier asignación a NS3_ROOT y la reemplaza
    sed -i "s/^NS3_ROOT = .*/NS3_ROOT = Path(\"$ESCAPED_PATH\")/" "$SETTINGS_FILE"
    
    # Asegurar import Path si no está (aunque debería estar)
    if ! grep -q "from pathlib import Path" "$SETTINGS_FILE"; then
        sed -i '1i from pathlib import Path' "$SETTINGS_FILE"
    fi
    
    success "Configuración actualizada"
fi

# 8. Crear script de lanzamiento rápido
cat > launch.sh << EOL
#!/bin/bash
source venv/bin/activate
echo "🤖 Iniciando A2A Framework..."
python main.py "\$@"
EOL
chmod +x launch.sh

# 9. Verificación Final
log "Ejecutando verificación del sistema..."
python verify-system-complete.py

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "   ✅ INSTALACIÓN COMPLETADA"
echo "═══════════════════════════════════════════════════════════════════"
echo "Tu Sandbox de investigación está listo en: $INSTALL_DIR"
echo ""
echo "Para empezar:"
echo "  cd $INSTALL_DIR"
echo "  ./launch.sh --help"
echo ""
echo "Documentación disponible en: $INSTALL_DIR/docs"
echo ""
