"""
Agente Programador

Responsable de generar código Python para simulaciones NS-3
usando Chain-of-Thought y auto-corrección basada en errores.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
import re
from langchain_ollama import ChatOllama

from config.settings import (
    OLLAMA_BASE_URL,
    MODEL_CODING,
    MODEL_TEMPERATURE_CODING,
    SIMULATIONS_DIR
)
from utils.state import AgentState, add_audit_entry, increment_iteration


# Template base para scripts NS-3
NS3_TEMPLATE = '''#!/usr/bin/env python3
"""
Script de simulación NS-3 generado automáticamente
Objetivo: {objective}
"""

import sys
sys.path.insert(0, 'build/lib/python3')

import ns.core
import ns.network
import ns.internet
import ns.mobility
import ns.wifi
import ns.applications
import ns.flow_monitor

def main():
    """Función principal de simulación"""
    
    print("Iniciando simulación...")
    
    # Configuración básica
    ns.core.Config.SetDefault("ns3::WifiRemoteStationManager::RtsCtsThreshold", 
                              ns.core.StringValue("2200"))
    
    {code_body}
    
    # Configurar FlowMonitor para métricas
    flowmon_helper = ns.flow_monitor.FlowMonitorHelper()
    monitor = flowmon_helper.InstallAll()
    
    # Ejecutar simulación
    print(f"Ejecutando simulación por {{simulation_time}} segundos...")
    ns.core.Simulator.Stop(ns.core.Seconds(simulation_time))
    ns.core.Simulator.Run()
    
    # Exportar resultados
    monitor.SerializeToXmlFile("resultados.xml", True, True)
    print("✅ Simulación completada. Resultados en resultados.xml")
    
    ns.core.Simulator.Destroy()
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''


def extract_code_from_response(response: str) -> str:
    """
    Extrae código Python limpio de la respuesta del LLM
    
    Args:
        response: Respuesta del LLM
        
    Returns:
        Código Python limpio
    """
    # Buscar bloques de código markdown
    code_pattern = r'```python\n(.*?)\n```'
    matches = re.findall(code_pattern, response, re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    # Si no hay bloques markdown, buscar solo ```
    code_pattern = r'```\n(.*?)\n```'
    matches = re.findall(code_pattern, response, re.DOTALL)
    
    if matches:
        return matches[0].strip()
    
    # Si no hay bloques, retornar todo
    return response.strip()


def validate_code(code: str) -> tuple[bool, str]:
    """
    Valida que el código tenga los elementos necesarios
    
    Args:
        code: Código a validar
        
    Returns:
        (es_válido, mensaje)
    """
    required_imports = ['ns.core', 'ns.network']
    missing_imports = [imp for imp in required_imports if imp not in code]
    
    if missing_imports:
        return False, f"Faltan imports: {', '.join(missing_imports)}"
    
    if 'def main()' not in code and 'if __name__' not in code:
        return False, "Falta función main() o bloque if __name__"
    
    return True, "Código válido"


def generate_code(task: str, research_notes: str, previous_error: str = None, iteration: int = 0) -> str:
    """
    Genera código NS-3 usando Chain-of-Thought mejorado con auto-corrección
    
    Args:
        task: Tarea de simulación
        research_notes: Notas de investigación
        previous_error: Error previo a corregir (si existe)
        iteration: Número de iteración (para ajustar estrategia)
        
    Returns:
        Código Python generado
    """
    try:
        llm = ChatOllama(
            model=MODEL_CODING,
            temperature=MODEL_TEMPERATURE_CODING,
            base_url=OLLAMA_BASE_URL
        )
        
        # Paso 1: Chain of Thought - Planificación detallada
        cot_prompt = f"""
Planifica una simulación NS-3 paso a paso con máximo detalle:

**TAREA:** {task}

**CONTEXTO DE INVESTIGACIÓN:**
{research_notes[:800] if research_notes else "Sin contexto específico"}

Responde con precisión:
1. **Tipo de red**: MANET/VANET/WSN/Mesh - justifica
2. **Topología**: Número de nodos, área de simulación (mxm), densidad
3. **Protocolo de enrutamiento**: AODV/OLSR/DSDV/DSR - razón de elección
4. **Métricas objetivo**: PDR, latencia, throughput, overhead, jitter
5. **Modelo de movilidad**: RandomWaypoint/ConstantPosition/GaussMarkov - parámetros
6. **Tráfico**: Tipo (UDP/TCP), tasa de paquetes, tamaño
7. **Duración**: Tiempo de simulación en segundos (100-300s)
8. **Configuración WiFi**: Estándar (802.11a/b/g/n), potencia TX, rango
"""
        
        print("  📋 Planificando simulación (análisis profundo)...")
        reasoning = llm.invoke(cot_prompt)
        print(f"  ✓ Planificación completada")
        
        # Paso 2: Generación de código con template mejorado
        code_prompt = f"""
Eres un experto en NS-3 Python bindings. Genera un script COMPLETO, EJECUTABLE y ROBUSTO.

**OBJETIVO:**
{task}

**TU PLANIFICACIÓN DETALLADA:**
{reasoning.content}

**INSTRUCCIONES CRÍTICAS:**
1. USA SOLO Python bindings de NS-3 (NO C++)
2. Imports correctos: import ns.core, import ns.network, import ns.internet, import ns.wifi, import ns.mobility, import ns.applications, import ns.flow_monitor
3. Para protocolos de enrutamiento: import ns.aodv, import ns.olsr, import ns.dsdv
4. Configura FlowMonitor CORRECTAMENTE para exportar a "resultados.xml"
5. **IMPORTANTE: Habilita captura PCAP con phy.EnablePcapAll("simulacion", True)**
6. Usa modelos de movilidad apropiados con parámetros realistas
7. Configura aplicaciones de tráfico (UdpEchoClient/Server o OnOffApplication)
8. Duración: 100-300 segundos
9. Incluye logging para debugging
10. Manejo de errores básico
11. Comentarios en español explicando cada sección

**ESTRUCTURA OBLIGATORIA:**
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'build/lib/python3')

# Imports de NS-3
import ns.core
import ns.network
import ns.internet
import ns.wifi
import ns.mobility
import ns.applications
import ns.flow_monitor
# import ns.aodv  # Si usas AODV
# import ns.olsr  # Si usas OLSR

def main():
    # 1. Configuración básica y logging
    # 2. Configurar semilla aleatoria para reproducibilidad
    #    ns.core.RngSeedManager.SetSeed(simulation_seed)
    # 3. Crear nodos
    # 4. Configurar WiFi (guardar referencia a phy)
    # 5. Configurar movilidad
    # 6. Instalar stack de Internet
    # 7. Configurar protocolo de enrutamiento
    # 8. Asignar direcciones IP
    # 9. Configurar aplicaciones
    # 10. HABILITAR CAPTURA PCAP: phy.EnablePcapAll("simulacion", True)
    # 11. Configurar FlowMonitor
    # 12. Ejecutar simulación
    # 13. Exportar resultados (XML + PCAP)
    # 14. Cleanup
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

**ERRORES COMUNES A EVITAR:**
- No olvidar import ns.flow_monitor
- FlowMonitor debe instalarse DESPUÉS de configurar aplicaciones
- Usar ns.core.Seconds() para tiempos
- Usar ns.core.StringValue() para configuraciones
- **CRÍTICO: Configurar semilla ANTES de crear nodos**
- **CRÍTICO: Habilitar PCAP ANTES de Simulator.Run()**
- Llamar Simulator.Destroy() al final

**TEMPLATE PARA REPRODUCIBILIDAD Y PCAP:**
```python
def main():
    # 1. Configurar semilla para reproducibilidad (PRIMERO)
    simulation_seed = 12345  # Usar valor del state o fijo
    ns.core.RngSeedManager.SetSeed(simulation_seed)
    ns.core.RngSeedManager.SetRun(1)
    print(f"🎲 Semilla configurada: {{simulation_seed}}")
    
    # 2. Crear nodos y configurar red...
    nodes = ns.network.NodeContainer()
    nodes.Create(num_nodes)
    
    # 3. Configurar WiFi (GUARDAR referencia a phy)
    wifi = ns.wifi.WifiHelper()
    phy = ns.wifi.YansWifiPhyHelper()
    # ... configuración WiFi ...
    
    # 4. Configurar movilidad, routing, aplicaciones...
    
    # 5. ANTES de Simulator.Run(), habilitar PCAP
    phy.EnablePcapAll("simulacion", True)
    print("📡 Captura PCAP habilitada: simulacion-X-Y.pcap")
    
    # 6. Ejecutar simulación
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()
```

**FORMATO:**
Devuelve SOLO el código Python completo entre ```python y ```, sin explicaciones adicionales.
"""
        
        # Si hay error previo, agregar contexto de corrección
        if previous_error:
            code_prompt += f"""

**⚠️ ERROR ANTERIOR (Iteración {iteration}):**
{previous_error[:500]}

**ESTRATEGIA DE CORRECCIÓN:**
1. Identifica la causa raíz del error
2. Verifica imports faltantes
3. Corrige sintaxis de NS-3 Python bindings
4. Asegura que todos los objetos se inicialicen correctamente
5. Valida que FlowMonitor esté bien configurado

IMPORTANTE: Este es el intento #{iteration+1}. Sé más cuidadoso con la sintaxis.
"""
        
        print(f"  💻 Generando código (intento #{iteration+1})...")
        response = llm.invoke(code_prompt)
        code = extract_code_from_response(response.content)
        
        # Post-procesamiento: asegurar imports básicos
        code = ensure_basic_imports(code)
        
        print(f"  ✓ Código generado ({len(code)} caracteres)")
        
        return code
        
    except Exception as e:
        print(f"  ❌ Error generando código: {e}")
        return generate_fallback_code(task)


def ensure_basic_imports(code: str) -> str:
    """
    Asegura que el código tenga los imports básicos de NS-3
    
    Args:
        code: Código generado
        
    Returns:
        Código con imports asegurados
    """
    required_imports = [
        "import ns.core",
        "import ns.network",
        "import ns.internet",
        "import ns.flow_monitor"
    ]
    
    # Verificar si faltan imports
    missing = [imp for imp in required_imports if imp not in code]
    
    if missing:
        # Insertar imports faltantes después de sys.path.insert
        import_section = "\n".join(missing) + "\n"
        
        if "sys.path.insert" in code:
            code = code.replace(
                "sys.path.insert(0, 'build/lib/python3')",
                f"sys.path.insert(0, 'build/lib/python3')\n\n{import_section}"
            )
    
    return code


def generate_fallback_code(task: str) -> str:
    """
    Genera código de respaldo simple cuando falla la generación principal
    
    Args:
        task: Tarea de simulación
        
    Returns:
        Código básico funcional
    """
    return f'''#!/usr/bin/env python3
"""
Script de simulación NS-3 - Versión de respaldo
Objetivo: {task}
"""

import sys
sys.path.insert(0, 'build/lib/python3')

import ns.core
import ns.network
import ns.internet
import ns.wifi
import ns.mobility
import ns.applications
import ns.flow_monitor

def main():
    """Simulación básica de red MANET"""
    
    print("Iniciando simulación básica...")
    
    # Configuración
    num_nodes = 10
    simulation_time = 100.0
    
    # Crear nodos
    nodes = ns.network.NodeContainer()
    nodes.Create(num_nodes)
    print(f"Creados {{num_nodes}} nodos")
    
    # Configurar WiFi
    wifi = ns.wifi.WifiHelper()
    wifi.SetStandard(ns.wifi.WIFI_STANDARD_80211a)
    
    phy = ns.wifi.YansWifiPhyHelper()
    channel = ns.wifi.YansWifiChannelHelper.Default()
    phy.SetChannel(channel.Create())
    
    mac = ns.wifi.WifiMacHelper()
    mac.SetType("ns3::AdhocWifiMac")
    
    devices = wifi.Install(phy, mac, nodes)
    
    # Movilidad
    mobility = ns.mobility.MobilityHelper()
    mobility.SetPositionAllocator(
        "ns3::RandomRectanglePositionAllocator",
        "X", ns.core.StringValue("ns3::UniformRandomVariable[Min=0.0|Max=500.0]"),
        "Y", ns.core.StringValue("ns3::UniformRandomVariable[Min=0.0|Max=500.0]")
    )
    mobility.SetMobilityModel(
        "ns3::ConstantPositionMobilityModel"
    )
    mobility.Install(nodes)
    
    # Stack de Internet
    internet = ns.internet.InternetStackHelper()
    internet.Install(nodes)
    
    # Asignar IPs
    ipv4 = ns.internet.Ipv4AddressHelper()
    ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), 
                 ns.network.Ipv4Mask("255.255.255.0"))
    interfaces = ipv4.Assign(devices)
    
    # FlowMonitor
    flowmon_helper = ns.flow_monitor.FlowMonitorHelper()
    monitor = flowmon_helper.InstallAll()
    
    # Ejecutar
    print(f"Ejecutando simulación por {{simulation_time}} segundos...")
    ns.core.Simulator.Stop(ns.core.Seconds(simulation_time))
    ns.core.Simulator.Run()
    
    # Exportar resultados
    monitor.SerializeToXmlFile("resultados.xml", True, True)
    print("✅ Simulación completada. Resultados en resultados.xml")
    
    ns.core.Simulator.Destroy()
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''


def save_code(code: str, filename: str = "tesis_sim.py") -> str:
    """
    Guarda el código en el directorio de simulaciones
    
    Args:
        code: Código a guardar
        filename: Nombre del archivo
        
    Returns:
        Ruta completa del archivo guardado
    """
    filepath = SIMULATIONS_DIR / "scripts" / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(code)
    
    # Hacer ejecutable (Linux/Mac)
    try:
        filepath.chmod(0o755)
    except:
        pass
    
    return str(filepath)


def coder_node(state: AgentState) -> Dict:
    """
    Nodo del agente programador para LangGraph con auto-corrección mejorada
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Diccionario con actualizaciones al estado
    """
    print("\n" + "="*80)
    print("💻 AGENTE PROGRAMADOR ACTIVADO")
    print("="*80)
    
    task = state['task']
    research_notes = "\n".join(state.get('research_notes', []))
    previous_error = state['errors'][-1] if state.get('errors') else None
    iteration = state.get('iteration', 0)
    
    print(f"📋 Tarea: {task}")
    print(f"🔄 Iteración: {iteration + 1}")
    if previous_error:
        print(f"⚠️  Corrigiendo error previo: {previous_error[:150]}...")
    print()
    
    # Generar código con contexto de iteración
    code = generate_code(task, research_notes, previous_error, iteration)
    
    # Validar código
    is_valid, validation_msg = validate_code(code)
    
    if not is_valid:
        print(f"❌ Validación falló: {validation_msg}")
        
        # Si es la primera iteración, intentar auto-corrección inmediata
        if iteration == 0:
            print("🔧 Intentando auto-corrección...")
            code = generate_code(task, research_notes, validation_msg, 1)
            is_valid, validation_msg = validate_code(code)
            
            if is_valid:
                print("✅ Auto-corrección exitosa")
            else:
                print(f"❌ Auto-corrección falló: {validation_msg}")
                return {
                    'code_snippet': code,
                    'code_validated': False,
                    'errors': [f"Código inválido tras auto-corrección: {validation_msg}"],
                    **increment_iteration(state),
                    **add_audit_entry(state, "coder", "code_validation_failed", {
                        'reason': validation_msg,
                        'iteration': iteration
                    })
                }
        else:
            return {
                'code_snippet': code,
                'code_validated': False,
                'errors': [f"Código inválido: {validation_msg}"],
                **increment_iteration(state),
                **add_audit_entry(state, "coder", "code_validation_failed", {
                    'reason': validation_msg,
                    'iteration': iteration
                })
            }
    
    # Guardar código
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tesis_sim_{timestamp}.py"
    filepath = save_code(code, filename)
    
    print(f"✅ Código guardado en: {filepath}")
    print(f"✅ Validación exitosa")
    print(f"📊 Estadísticas: {len(code)} caracteres, {code.count('def ')} funciones")
    
    return {
        'code_snippet': code,
        'code_validated': True,
        'code_filepath': filepath,
        **increment_iteration(state),
        **add_audit_entry(state, "coder", "code_generated", {
            'filepath': filepath,
            'code_length': len(code),
            'iteration': iteration,
            'functions_count': code.count('def ')
        })
    }


if __name__ == "__main__":
    # Prueba del agente
    from utils.state import create_initial_state
    
    test_state = create_initial_state(
        "Simular protocolo AODV con 20 nodos en área de 500x500m"
    )
    test_state['research_notes'] = [
        "AODV es un protocolo reactivo. Métricas clave: PDR, latencia."
    ]
    
    result = coder_node(test_state)
    
    print("\n" + "="*80)
    print("RESULTADO DE PRUEBA")
    print("="*80)
    print(f"Código validado: {result['code_validated']}")
    print(f"Longitud del código: {len(result['code_snippet'])} caracteres")
    print(f"\nPrimeras líneas del código:")
    print(result['code_snippet'][:300])
