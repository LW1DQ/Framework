#!/bin/bash
# Script de instalación del módulo DRL Routing para NS-3
# Sistema A2A - Tesis Doctoral

set -e  # Salir si hay error

echo "=================================================="
echo "  Instalación de Módulo DRL Routing para NS-3"
echo "=================================================="
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Verificar que NS-3 esté instalado
print_info "Verificando instalación de NS-3..."

if [ -z "$NS3_ROOT" ]; then
    NS3_ROOT="$HOME/ns-3-dev"
    print_warn "Variable NS3_ROOT no definida, usando: $NS3_ROOT"
fi

if [ ! -d "$NS3_ROOT" ]; then
    print_error "NS-3 no encontrado en: $NS3_ROOT"
    echo ""
    echo "Por favor, instala NS-3 primero:"
    echo "  cd ~"
    echo "  git clone https://gitlab.com/nsnam/ns-3-dev.git"
    echo "  cd ns-3-dev"
    echo "  ./ns3 configure --enable-examples"
    echo "  ./ns3 build"
    exit 1
fi

print_info "NS-3 encontrado en: $NS3_ROOT"

# 2. Crear directorio del módulo
MODULE_DIR="$NS3_ROOT/contrib/drl-routing"
print_info "Creando directorio del módulo: $MODULE_DIR"

mkdir -p "$MODULE_DIR"
mkdir -p "$MODULE_DIR/model"
mkdir -p "$MODULE_DIR/helper"
mkdir -p "$MODULE_DIR/examples"
mkdir -p "$MODULE_DIR/test"

# 3. Copiar archivos del módulo
print_info "Copiando archivos del módulo..."

# Copiar header y source
cp drl-routing-agent.h "$MODULE_DIR/model/"
cp drl-routing-agent.cc "$MODULE_DIR/model/"

print_info "Archivos copiados:"
print_info "  - drl-routing-agent.h"
print_info "  - drl-routing-agent.cc"

# 4. Crear wscript para el módulo
print_info "Creando wscript..."

cat > "$MODULE_DIR/wscript" << 'EOF'
# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

def build(bld):
    module = bld.create_ns3_module('drl-routing', ['core', 'network', 'internet', 'mobility'])
    module.source = [
        'model/drl-routing-agent.cc',
        ]

    module_test = bld.create_ns3_module_test_library('drl-routing')
    module_test.source = [
        ]

    headers = bld(features='ns3header')
    headers.module = 'drl-routing'
    headers.source = [
        'model/drl-routing-agent.h',
        ]

    if bld.env.ENABLE_EXAMPLES:
        bld.recurse('examples')

    # bld.ns3_python_bindings()
EOF

print_info "wscript creado"

# 5. Crear ejemplo básico
print_info "Creando ejemplo básico..."

cat > "$MODULE_DIR/examples/drl-routing-example.cc" << 'EOF'
/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Ejemplo básico de uso del DRL Routing Agent
 */

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/mobility-module.h"
#include "ns3/drl-routing-agent.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("DrlRoutingExample");

int
main (int argc, char *argv[])
{
    // Habilitar logs
    LogComponentEnable ("DrlRoutingExample", LOG_LEVEL_INFO);
    LogComponentEnable ("DrlRoutingAgent", LOG_LEVEL_INFO);

    // Crear nodos
    NodeContainer nodes;
    nodes.Create (5);

    // Configurar movilidad
    MobilityHelper mobility;
    mobility.SetPositionAllocator ("ns3::GridPositionAllocator",
                                    "MinX", DoubleValue (0.0),
                                    "MinY", DoubleValue (0.0),
                                    "DeltaX", DoubleValue (100.0),
                                    "DeltaY", DoubleValue (100.0),
                                    "GridWidth", UintegerValue (3),
                                    "LayoutType", StringValue ("RowFirst"));
    mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
    mobility.Install (nodes);

    // Crear agentes DRL para cada nodo
    for (uint32_t i = 0; i < nodes.GetN (); i++)
    {
        Ptr<DrlRoutingAgent> agent = CreateObject<DrlRoutingAgent> ();
        agent->Initialize (nodes.Get (i));
        
        NS_LOG_INFO ("Agente DRL creado para nodo " << i);
        
        // Obtener estado inicial
        EnvState state = agent->GetCurrentState ();
        NS_LOG_INFO ("  Estado inicial: neighbors=" << state.num_neighbors
                     << " pdr=" << state.recent_pdr);
    }

    // Ejecutar simulación
    Simulator::Stop (Seconds (10.0));
    Simulator::Run ();
    Simulator::Destroy ();

    NS_LOG_INFO ("Simulación completada");

    return 0;
}
EOF

# Crear wscript para ejemplos
cat > "$MODULE_DIR/examples/wscript" << 'EOF'
# -*- Mode: python; py-indent-offset: 4; indent-tabs-mode: nil; coding: utf-8; -*-

def build(bld):
    obj = bld.create_ns3_program('drl-routing-example',
                                  ['drl-routing', 'core', 'network', 'internet', 'mobility'])
    obj.source = 'drl-routing-example.cc'
EOF

print_info "Ejemplo creado: drl-routing-example.cc"

# 6. Reconfigurar y compilar NS-3
print_info "Reconfigurando NS-3..."
cd "$NS3_ROOT"

./ns3 configure --enable-examples --enable-tests

print_info "Compilando NS-3 con el nuevo módulo..."
./ns3 build

# 7. Verificar compilación
if [ $? -eq 0 ]; then
    print_info "✅ Compilación exitosa!"
    echo ""
    print_info "Módulo DRL Routing instalado correctamente"
    echo ""
    echo "Para probar el módulo:"
    echo "  cd $NS3_ROOT"
    echo "  ./ns3 run drl-routing-example"
    echo ""
else
    print_error "❌ Error en la compilación"
    exit 1
fi

# 8. Ejecutar ejemplo de prueba
print_info "Ejecutando ejemplo de prueba..."
./ns3 run drl-routing-example

echo ""
echo "=================================================="
echo "  ✅ Instalación completada exitosamente"
echo "=================================================="
echo ""
echo "Próximos pasos:"
echo "  1. Instalar ns3-ai para comunicación Python-C++"
echo "  2. Integrar con el agente Python de Sistema A2A"
echo "  3. Entrenar el modelo DRL"
echo ""
