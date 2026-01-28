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
from utils.logging_utils import update_agent_status, log_message
from utils.validation import validate_code
from utils.errors import CodeGenerationError
from utils.prompts import get_prompt


# Template movido a config/prompts.yaml


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





from utils.memory import memory

def generate_code(task: str, research_notes: str, previous_error: str = None, error_type: str = None, iteration: int = 0) -> str:
    """
    Genera código NS-3 usando Chain-of-Thought mejorado con auto-corrección y memoria episódica
    
    Args:
        task: Tarea de simulación
        research_notes: Notas de investigación
        previous_error: Error previo a corregir (si existe)
        error_type: Tipo de error (CompilationError, SimulationError, etc.)
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
        
        # Recuperar experiencia de memoria si hay error previo
        memory_context = ""
        if previous_error:
            experiences = memory.retrieve_experience(task, previous_error)
            if experiences:
                exp = experiences[0]
                print(f"🧠 Memoria activada: Solución similar encontrada ({exp['relevance']:.2f})")
                log_message("Coder", f"Memoria activada: Solución similar encontrada ({exp['relevance']:.2f})")
                memory_context = f"""
**💡 SOLUCIÓN PASADA RECUPERADA:**
En una tarea similar ("{exp['task']}") con un error similar ("{exp['error']}"), 
esta solución funcionó:
{exp['solution']}
"""

        # Paso 1: Chain of Thought - Planificación detallada
        print("  🧠 Generando plan de simulación...")
        log_message("Coder", "Planificando simulación con Chain-of-Thought...")
        
        cot_prompt = get_prompt(
            'coder', 
            'chain_of_thought',
            task=task,
            research_notes=research_notes[:2000] if research_notes else "Sin contexto específico",
            memory_context=memory_context
        )
        print(f"  DEBUG: Invoking LLM for CoT with model {MODEL_CODING}...")
        reasoning = llm.invoke(cot_prompt)
        print(f"  DEBUG: LLM CoT response received. Length: {len(reasoning.content)}")
        print(f"  ✓ Planificación completada")
        
        # Paso 2: Generación de código
        error_context = ""
        if previous_error:
            # Obtener estrategia de error
            strategy = get_prompt('coder', 'error_strategy.general')
            if error_type == "CompilationError":
                strategy = get_prompt('coder', 'error_strategy.compilation')
            elif error_type == "SimulationError":
                strategy = get_prompt('coder', 'error_strategy.simulation')
            elif error_type == "TimeoutError":
                strategy = get_prompt('coder', 'error_strategy.timeout')
                
            error_context = f"""
**⚠️ ERROR ANTERIOR (Iteración {iteration}):**
Tipo: {error_type or 'Desconocido'}
Detalle: {previous_error[:500]}

ESTRATEGIA DE CORRECCIÓN:
{strategy}

IMPORTANTE: Este es el intento #{iteration+1}. Sé más cuidadoso.
"""

        code_prompt = get_prompt(
            'coder',
            'generation',
            task=task,
            plan=reasoning.content,
            error_context=error_context
        )
        
        print(f"  💻 Generando código (intento #{iteration+1})...")
        log_message("Coder", f"Generando código (Iteración {iteration+1})...")
        print(f"  DEBUG: Invoking LLM for Code Generation with model {MODEL_CODING}...")
        response = llm.invoke(code_prompt)
        print(f"  DEBUG: LLM Code Generation response received.")
        print(f"  ✓ Respuesta LLM recibida. Longitud: {len(response.content)}")
        code = extract_code_from_response(response.content)
        print(f"  ✓ Código extraído. Longitud: {len(code)}")
        
        # Post-procesamiento: asegurar imports básicos
        code = ensure_basic_imports(code)
        
        print(f"  ✓ Código generado ({len(code)} caracteres)")
        log_message("Coder", f"Código generado ({len(code)} bytes)")
        
        return code
        
    except Exception as e:
        print(f"  ❌ Error generando código: {e}")
        log_message("Coder", f"Error generando código: {e}", level="ERROR")
        raise CodeGenerationError(f"Error en generación LLM: {e}")


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
    
    # Si el código menciona HWMP o mesh, agregar import ns.mesh
    if 'HWMP' in code or 'mesh' in code.lower() or 'MeshHelper' in code:
        if "import ns.mesh" not in code:
            required_imports.append("import ns.mesh")
    
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
    error_type = state.get('error_type')
    iteration = state.get('iteration', 0)
    
    # Actualizar estado en Dashboard
    update_agent_status("Coder", "running", f"Generando código (Iteración {iteration+1})")
    log_message("Coder", f"Iniciando generación de código para: {task}")
    
    print(f"📋 Tarea: {task}")
    print(f"🔄 Iteración: {iteration + 1}")
    if previous_error:
        print(f"⚠️  Corrigiendo error previo ({error_type}): {previous_error[:150]}...")
        log_message("Coder", f"Corrigiendo error previo ({error_type}): {previous_error[:100]}...", level="WARNING")
    print()
    
    # Generar código con contexto de iteración
    try:
        code = generate_code(task, research_notes, previous_error, error_type, iteration)
    except CodeGenerationError as e:
        print(f"⚠️  Fallo en generación: {e}")
        print("⚠️  Usando código de respaldo (fallback)...")
        log_message("Coder", f"Fallo generación: {e}. Usando fallback.", level="WARNING")
        code = generate_fallback_code(task)
    
    # Validar código
    is_valid, validation_msg = validate_code(code)
    
    if not is_valid:
        print(f"❌ Validación falló: {validation_msg}")
        log_message("Coder", f"Validación falló: {validation_msg}", level="ERROR")
        
        # Si es la primera iteración, intentar auto-corrección inmediata
        if iteration == 0:
            print("🔧 Intentando auto-corrección...")
            log_message("Coder", "Intentando auto-corrección inmediata...")
            code = generate_code(task, research_notes, validation_msg, "CompilationError", 1)
            is_valid, validation_msg = validate_code(code)
            
            if is_valid:
                print("✅ Auto-corrección exitosa")
                log_message("Coder", "Auto-corrección exitosa")
            else:
                print(f"❌ Auto-corrección falló: {validation_msg}")
                log_message("Coder", f"Auto-corrección falló: {validation_msg}", level="ERROR")
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
    
    # MEMORIA EPISÓDICA: Si hubo error previo y ahora es exitoso, guardar experiencia
    if previous_error:
        try:
            print("🧠 Guardando experiencia en memoria episódica...")
            memory.add_experience(
                task=task,
                code=code, # El código exitoso es la solución
                error=previous_error,
                solution=code
            )
            log_message("Coder", "Experiencia guardada en memoria episódica")
        except Exception as e:
            print(f"⚠️ Error guardando memoria: {e}")
            log_message("Coder", f"Error guardando memoria: {e}", level="WARNING")
    
    log_message("Coder", f"Código guardado en: {filename}")
    update_agent_status("Coder", "completed", "Código generado y validado")
    
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
