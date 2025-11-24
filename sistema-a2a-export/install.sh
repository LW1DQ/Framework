#!/bin/bash

###############################################################################
#                                                                             #
#           Script de Instalación Automática - Sistema A2A v1.2              #
#                                                                             #
#     Framework Multi-Agente para Optimización de Protocolos de Enrutamiento #
#                                                                             #
###############################################################################

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
print_header "INSTALACIÓN SISTEMA A2A v1.2"
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

# Paso 1: Verificar Python
print_header "PASO 1: Verificar Python"
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
    print_info "Instalar con: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi
echo ""

# Paso 2: Crear entorno virtual
print_header "PASO 2: Crear Entorno Virtual"
if [ -d "venv" ]; then
    print_warning "Entorno virtual ya existe"
    read -p "¿Desea recrearlo? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        rm -rf venv
        print_info "Entorno virtual eliminado"
    fi
fi

if [ ! -d "venv" ]; then
    print_info "Creando entorno virtual..."
    python3 -m venv venv
    print_success "Entorno virtual creado"
else
    print_success "Usando entorno virtual existente"
fi
echo ""

# Paso 3: Activar entorno virtual e instalar dependencias
print_header "PASO 3: Instalar Dependencias Python"
print_info "Activando entorno virtual..."
source venv/bin/activate

print_info "Actualizando pip..."
pip install --upgrade pip --quiet

print_info "Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt --quiet

print_success "Dependencias instaladas correctamente"
echo ""

# Paso 4: Verificar Ollama
print_header "PASO 4: Verificar Ollama"
if command -v ollama &> /dev/null; then
    print_success "Ollama encontrado"
    
    # Verificar si está corriendo
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        print_success "Ollama está corriendo"
        
        # Listar modelos
        print_info "Modelos instalados:"
        ollama list
    else
        print_warning "Ollama no está corriendo"
        print_info "Iniciando Ollama..."
        ollama serve > /dev/null 2>&1 &
        sleep 3
        
        if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
            print_success "Ollama iniciado correctamente"
        else
            print_error "No se pudo iniciar Ollama"
        fi
    fi
else
    print_warning "Ollama no encontrado"
    print_info "Instalar desde: https://ollama.ai/"
    print_info "O ejecutar: curl -fsSL https://ollama.com/install.sh | sh"
fi
echo ""

# Paso 5: Descargar modelos de Ollama
print_header "PASO 5: Verificar Modelos LLM"
if command -v ollama &> /dev/null && curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    MODELS=("llama3.1:8b" "codellama:13b" "nomic-embed-text")
    
    for MODEL in "${MODELS[@]}"; do
        if ollama list | grep -q "$MODEL"; then
            print_success "Modelo $MODEL ya instalado"
        else
            print_warning "Modelo $MODEL no encontrado"
            read -p "¿Desea descargarlo ahora? (s/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Ss]$ ]]; then
                print_info "Descargando $MODEL (esto puede tardar varios minutos)..."
                ollama pull $MODEL
                print_success "Modelo $MODEL descargado"
            else
                print_warning "Modelo $MODEL omitido"
            fi
        fi
    done
else
    print_warning "Ollama no disponible, omitiendo descarga de modelos"
fi
echo ""

# Paso 6: Verificar NS-3
print_header "PASO 6: Verificar NS-3"
print_info "Buscando instalación de NS-3..."

# Buscar en ubicaciones comunes
NS3_PATHS=(
    "$HOME/ns-allinone-3.38/ns-3.38"
    "$HOME/ns-allinone-3.37/ns-3.37"
    "$HOME/ns-allinone-3.36/ns-3.36"
    "/usr/local/ns-3.38"
    "/opt/ns-3.38"
)

NS3_FOUND=false
for PATH_TO_CHECK in "${NS3_PATHS[@]}"; do
    if [ -d "$PATH_TO_CHECK" ]; then
        print_success "NS-3 encontrado en: $PATH_TO_CHECK"
        NS3_ROOT="$PATH_TO_CHECK"
        NS3_FOUND=true
        break
    fi
done

if [ "$NS3_FOUND" = false ]; then
    print_warning "NS-3 no encontrado en ubicaciones comunes"
    print_info "Ubicaciones verificadas:"
    for PATH_TO_CHECK in "${NS3_PATHS[@]}"; do
        echo "  - $PATH_TO_CHECK"
    done
    echo ""
    read -p "Ingrese la ruta a NS-3 (o Enter para omitir): " NS3_ROOT
    
    if [ -n "$NS3_ROOT" ] && [ -d "$NS3_ROOT" ]; then
        print_success "NS-3 encontrado en: $NS3_ROOT"
        NS3_FOUND=true
    else
        print_warning "NS-3 no configurado"
        print_info "Descargar desde: https://www.nsnam.org/releases/"
        NS3_ROOT="/ruta/a/ns-3"
    fi
fi
echo ""

# Paso 7: Configurar settings.py
print_header "PASO 7: Configurar Sistema"
print_info "Actualizando config/settings.py..."

# Backup del archivo original
if [ -f "config/settings.py" ]; then
    cp config/settings.py config/settings.py.backup
    print_info "Backup creado: config/settings.py.backup"
fi

# Actualizar NS3_ROOT si se encontró
if [ "$NS3_FOUND" = true ]; then
    # Escapar barras para sed
    NS3_ROOT_ESCAPED=$(echo "$NS3_ROOT" | sed 's/\//\\\//g')
    
    # Actualizar en settings.py (si existe la línea)
    if grep -q "NS3_ROOT" config/settings.py; then
        sed -i.bak "s/NS3_ROOT = Path(\".*\")/NS3_ROOT = Path(\"$NS3_ROOT_ESCAPED\")/" config/settings.py
        print_success "NS3_ROOT actualizado en config/settings.py"
    fi
fi

print_success "Configuración actualizada"
echo ""

# Paso 8: Crear directorios necesarios
print_header "PASO 8: Crear Directorios"
DIRS=(
    "logs"
    "data/papers"
    "data/vector_db"
    "simulations/scripts"
    "simulations/scripts/backups"
    "simulations/results"
    "simulations/plots"
    "simulations/optimizations"
)

for DIR in "${DIRS[@]}"; do
    if [ ! -d "$DIR" ]; then
        mkdir -p "$DIR"
        print_success "Creado: $DIR"
    else
        print_info "Ya existe: $DIR"
    fi
done
echo ""

# Paso 9: Verificar instalación
print_header "PASO 9: Verificar Instalación"
print_info "Ejecutando script de verificación..."
echo ""

python scripts/check_system.py

echo ""

# Paso 10: Resumen
print_header "INSTALACIÓN COMPLETADA"
echo ""
print_success "Sistema A2A v1.2 instalado correctamente"
echo ""
echo "📋 Resumen:"
echo "  ✅ Python ${PYTHON_VERSION}"
echo "  ✅ Entorno virtual creado"
echo "  ✅ Dependencias instaladas"

if command -v ollama &> /dev/null; then
    echo "  ✅ Ollama instalado"
else
    echo "  ⚠️  Ollama no instalado"
fi

if [ "$NS3_FOUND" = true ]; then
    echo "  ✅ NS-3 configurado"
else
    echo "  ⚠️  NS-3 no configurado"
fi

echo ""
echo "📚 Próximos pasos:"
echo ""
echo "  1. Activar entorno virtual:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Ejecutar ejemplo básico:"
echo "     python examples/ejemplo_basico.py"
echo ""
echo "  3. Ejecutar sistema completo:"
echo "     python main.py"
echo ""
echo "  4. Leer documentación:"
echo "     cat INICIO-RAPIDO-v1.2.md"
echo ""

if [ "$NS3_FOUND" = false ]; then
    print_warning "IMPORTANTE: Configurar NS-3 antes de ejecutar simulaciones"
    echo "  1. Instalar NS-3 desde: https://www.nsnam.org/releases/"
    echo "  2. Actualizar NS3_ROOT en config/settings.py"
    echo ""
fi

if ! command -v ollama &> /dev/null; then
    print_warning "IMPORTANTE: Instalar Ollama para usar el sistema"
    echo "  curl -fsSL https://ollama.com/install.sh | sh"
    echo "  ollama pull llama3.1:8b"
    echo "  ollama pull codellama:13b"
    echo ""
fi

print_header "¡Buena suerte con tu investigación! 🎓🚀"
echo ""
