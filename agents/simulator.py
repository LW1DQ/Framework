"""
Agente Simulador

Responsable de ejecutar scripts NS-3 y capturar resultados/errores.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
import subprocess
import tempfile
import shutil
import datetime
import re
import time
import json

from config.settings import NS3_ROOT, SIMULATION_TIMEOUT, SIMULATIONS_DIR
from utils.state import AgentState, add_audit_entry
from utils.logging_utils import update_agent_status, log_message, log_metric
from utils.validation import validate_code





def extract_simulation_info(stdout: str) -> Dict:
    """
    Extrae información útil del stdout de la simulación
    
    Args:
        stdout: Salida estándar de la simulación
        
    Returns:
        Diccionario con información extraída
    """
    info = {
        'nodes_created': 0,
        'simulation_time': 0,
        'warnings': [],
        'errors': []
    }
    
    for line in stdout.split('\n'):
        # Buscar número de nodos
        if 'nodos' in line.lower() or 'nodes' in line.lower():
            import re
            numbers = re.findall(r'\d+', line)
            if numbers:
                info['nodes_created'] = int(numbers[0])
        
        # Buscar tiempo de simulación
        if 'segundos' in line.lower() or 'seconds' in line.lower():
            import re
            numbers = re.findall(r'\d+\.?\d*', line)
            if numbers:
                info['simulation_time'] = float(numbers[0])
        
        # Buscar warnings
        if 'warning' in line.lower():
            info['warnings'].append(line.strip())
        
        # Buscar errores
        if 'error' in line.lower() and 'error:' in line.lower():
            info['errors'].append(line.strip())
    
    return info


from utils.errors import SimulationError, TimeoutError, CompilationError, A2AError

def run_ns3_simulation(scratch_file: Path, timeout: int) -> Dict:
    """
    Ejecuta la simulación NS-3 y maneja errores a bajo nivel
    
    Args:
        scratch_file: Ruta al script en scratch
        timeout: Tiempo máximo de ejecución
        
    Returns:
        Diccionario con resultados de ejecución (stdout, returncode, etc.)
    
    Raises:
        TimeoutError: Si excede el tiempo
        CompilationError: Si hay error de sintaxis/imports
        SimulationError: Si falla la simulación (runtime)
    """
    import sys
    start_time = datetime.datetime.now()
    
    try:
        # Usamos sys.executable para asegurar que usamos el mismo intérprete Python
        cmd = [sys.executable, str(scratch_file)]
        
        result = subprocess.run(
            cmd,
            cwd=str(NS3_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        execution_time = (datetime.datetime.now() - start_time).total_seconds()
        
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            
            # Identificar tipo de error
            if "ImportError" in error_msg or "ModuleNotFoundError" in error_msg:
                raise CompilationError(f"Error de importación: {error_msg}")
            elif "SyntaxError" in error_msg:
                raise CompilationError(f"Error de sintaxis: {error_msg}")
            else:
                raise SimulationError(f"Error de ejecución (código {result.returncode}): {error_msg}")
                
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'execution_time': execution_time
        }
        
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"Simulación excedió {timeout} segundos")
    except Exception as e:
        # Re-raise custom exceptions
        if isinstance(e, (TimeoutError, CompilationError, SimulationError)):
            raise
        raise SimulationError(f"Error inesperado al ejecutar simulación: {e}")


def simulator_node(state: AgentState) -> Dict:
    """
    Nodo del agente simulador para LangGraph con validación y retry mejorados
    
    Args:
        state: Estado actual del sistema
        
    Returns:
        Diccionario con actualizaciones al estado
    """
    print("\n" + "="*80)
    print("⚡ AGENTE SIMULADOR ACTIVADO")
    print("="*80)
    
    # Actualizar estado en dashboard
    update_agent_status("Simulator", "running", state.get('task', 'Unknown'))
    log_message("Simulator", "Iniciando simulación...")
    
    code = state.get('code_snippet', '')
    iteration = state.get('iteration', 0)
    
    if not code:
        print("❌ No hay código para ejecutar")
        log_message("Simulator", "Error: No hay código para ejecutar", level="ERROR")
        return {
            'simulation_status': 'failed',
            'errors': ['No hay código para ejecutar'],
            **add_audit_entry(state, "simulator", "no_code", {})
        }
    
    print(f"📄 Código recibido: {len(code)} caracteres")
    print(f"🔄 Iteración: {iteration + 1}")
    print(f"🎯 Ejecutando en NS-3: {NS3_ROOT}")
    print()
    
    # Validación pre-ejecución
    print("🔍 Validando código antes de ejecutar...")
    is_valid, validation_msg = validate_code(code)
    
    if not is_valid:
        print(f"  ❌ Validación falló: {validation_msg}")
        log_message("Simulator", f"Validación falló: {validation_msg}", level="ERROR")
        return {
            'simulation_status': 'failed',
            'errors': [f"Validación pre-ejecución falló: {validation_msg}"],
            'error_type': 'CompilationError',
            **add_audit_entry(state, "simulator", "pre_validation_failed", {
                'reason': validation_msg
            })
        }
    
    print("  ✓ Validación pre-ejecución exitosa")
    
    # Guardar código en scratch de NS-3
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    scratch_file = NS3_ROOT / "scratch" / f"tesis_sim_{timestamp}.py"
    
    # Crear backup del código
    backup_dir = SIMULATIONS_DIR / "scripts" / "backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"sim_{timestamp}.py"
    
    try:
        # Escribir código
        with open(scratch_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Guardar backup
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"  ✓ Código guardado en: {scratch_file.name}")
        print(f"  ✓ Backup creado en: {backup_file}")
        
        # Ejecutar simulación
        print(f"\n  ⏳ Ejecutando simulación (timeout: {SIMULATION_TIMEOUT}s)...")
        print(f"  📊 Monitoreando progreso...")
        log_message("Simulator", f"Ejecutando script: {scratch_file.name}")
        
        # --- LLAMADA A FUNCIÓN EXTRACTADA ---
        result_data = run_ns3_simulation(scratch_file, SIMULATION_TIMEOUT)
        # ------------------------------------
        
        execution_time = result_data['execution_time']
        print(f"  ⏱️  Tiempo de ejecución: {execution_time:.2f}s")
        
        # Extraer información del stdout (Fallback)
        sim_info = extract_simulation_info(result_data['stdout'])
        
        # Intentar leer metadatos JSON para mayor precisión
        metadata_file = NS3_ROOT / "simulation_metadata.json"
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                
                print("  ✅ Metadatos JSON encontrados")
                # Actualizar sim_info con datos precisos
                sim_info['nodes_created'] = metadata.get('nodes_count', sim_info['nodes_created'])
                sim_info['simulation_time'] = metadata.get('simulation_time', sim_info['simulation_time'])
                
                if metadata.get('status') == 'failed':
                    sim_info['errors'].append(f"Error reportado en metadatos: {metadata.get('error')}")
                    
            except Exception as e:
                print(f"  ⚠️  Error leyendo metadatos JSON: {e}")
        else:
            print("  ⚠️  No se encontró simulation_metadata.json (usando parsing de stdout)")
        
        # Mostrar warnings si existen
        if sim_info['warnings']:
            print(f"\n  ⚠️  Warnings detectados ({len(sim_info['warnings'])}):")
            for warning in sim_info['warnings'][:3]:
                print(f"     {warning}")
        
        # Buscar archivo de resultados XML
        results_file = NS3_ROOT / "resultados.xml"
        results_dir = SIMULATIONS_DIR / "results" / timestamp
        results_dir.mkdir(parents=True, exist_ok=True)
        
        moved_results_file = None
        if results_file.exists():
            # Mover XML a directorio de resultados
            moved_results_file = results_dir / f"sim_{timestamp}.xml"
            shutil.move(str(results_file), str(moved_results_file))
            print(f"\n  ✅ Resultados XML: {moved_results_file.name}")
        else:
            print("\n  ⚠️  No se generó resultados.xml")
        
        # Buscar y mover archivos PCAP
        print(f"\n  🔍 Buscando archivos PCAP...")
        pcap_pattern = "simulacion-*.pcap"
        pcap_files_found = list(NS3_ROOT.glob(pcap_pattern))
        
        moved_pcaps = []
        if pcap_files_found:
            print(f"  📡 Archivos PCAP encontrados: {len(pcap_files_found)}")
            
            for pcap_file in pcap_files_found:
                dest = results_dir / pcap_file.name
                shutil.move(str(pcap_file), str(dest))
                moved_pcaps.append(str(dest))
                print(f"     ✓ {pcap_file.name} → {dest.name}")
        else:
            print(f"  ⚠️  No se encontraron archivos PCAP (patrón: {pcap_pattern})")
        
        # Guardar stdout
        stdout_file = results_dir / f"sim_{timestamp}_stdout.txt"
        with open(stdout_file, 'w', encoding='utf-8') as f:
            f.write(result_data['stdout'])
            
        # Mover metadata file si existe
        if metadata_file.exists():
            shutil.move(str(metadata_file), str(results_dir / f"metadata_{timestamp}.json"))
        
        print(f"  ✅ Simulación completada exitosamente")
        print(f"  📁 Resultados en: {results_dir}")
        
        log_message("Simulator", f"Simulación completada. Archivos: XML={moved_results_file is not None}, PCAP={len(moved_pcaps)}")
        update_agent_status("Simulator", "completed", "Simulación finalizada")
        
        return {
            'simulation_status': 'completed',
            'simulation_logs': str(moved_results_file) if moved_results_file else str(stdout_file),
            'pcap_files': moved_pcaps,
            'simulation_info': sim_info,
            'execution_time': execution_time,
            **add_audit_entry(state, "simulator", "simulation_completed", {
                'execution_time': execution_time,
                'nodes': sim_info['nodes_created'],
                'pcap_files_count': len(moved_pcaps),
                'results_dir': str(results_dir)
            })
        }
        
    except TimeoutError as e:
        print(f"\n  ❌ Timeout: {e}")
        log_message("Simulator", f"Timeout: {e}", level="ERROR")
        return {
            'simulation_status': 'failed',
            'errors': [str(e)],
            'error_type': 'TimeoutError',
            **add_audit_entry(state, "simulator", "timeout", {'error': str(e)})
        }
        
    except CompilationError as e:
        print(f"\n  ❌ Error de compilación/setup: {e}")
        log_message("Simulator", f"Error de compilación: {e}", level="ERROR")
        return {
            'simulation_status': 'failed',
            'errors': [str(e)],
            'error_type': 'CompilationError',
            **add_audit_entry(state, "simulator", "compilation_error", {'error': str(e)})
        }
        
    except SimulationError as e:
        print(f"\n  ❌ Error de simulación: {e}")
        log_message("Simulator", f"Error de simulación: {e}", level="ERROR")
        return {
            'simulation_status': 'failed',
            'errors': [str(e)],
            'error_type': 'SimulationError',
            **add_audit_entry(state, "simulator", "simulation_error", {'error': str(e)})
        }
        
    except Exception as e:
        print(f"\n  ❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        log_message("Simulator", f"Error inesperado: {e}", level="ERROR")
        
        return {
            'simulation_status': 'failed',
            'errors': [f'Error de sistema: {str(e)}'],
            'error_type': 'A2AError',
            **add_audit_entry(state, "simulator", "system_error", {
                'error': str(e)
            })
        }
    
    finally:
        # Limpiar archivo temporal de scratch
        if scratch_file.exists():
            try:
                scratch_file.unlink()
            except:
                pass


if __name__ == "__main__":
    # Prueba del agente
    from utils.state import create_initial_state
    
    # Código de prueba simple
    test_code = '''
import sys
sys.path.insert(0, 'build/lib/python3')
import ns.core

def main():
    print("Prueba de simulación")
    ns.core.Simulator.Stop(ns.core.Seconds(1))
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    test_state = create_initial_state("Prueba de simulación")
    test_state['code_snippet'] = test_code
    test_state['code_validated'] = True
    
    result = simulator_node(test_state)
    
    print("\n" + "="*80)
    print("RESULTADO DE PRUEBA")
    print("="*80)
    print(f"Estado: {result['simulation_status']}")
    if result.get('simulation_logs'):
        print(f"Resultados: {result['simulation_logs']}")
    if result.get('errors'):
        print(f"Errores: {result['errors']}")
