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

from config.settings import NS3_ROOT, SIMULATION_TIMEOUT, SIMULATIONS_DIR
from utils.state import AgentState, add_audit_entry
from utils.logging_utils import update_agent_status, log_message, log_metric


def validate_code_before_execution(code: str) -> tuple[bool, str]:
    """
    Valida el código antes de ejecutarlo usando AST y compilación
    
    Args:
        code: Código a validar
        
    Returns:
        (es_válido, mensaje)
    """
    import ast
    
    # 1. Validación sintáctica con AST
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error al analizar código: {str(e)}"

    # 2. Validación de imports críticos
    required_imports = ['ns.core', 'ns.network']
    missing = [imp for imp in required_imports if imp not in code]
    
    if missing:
        return False, f"Faltan imports críticos: {', '.join(missing)}"
    
    # 3. Verificar estructura básica
    if 'def main()' not in code and 'if __name__' not in code:
        return False, "Falta función main() o bloque if __name__"
    
    # 4. Verificar llamadas esenciales de NS-3
    if 'Simulator.Run()' not in code:
        return False, "Falta llamada a Simulator.Run()"
    
    if 'Simulator.Destroy()' not in code:
        return False, "Falta llamada a Simulator.Destroy()"
    
    return True, "Código válido para ejecución"


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
    is_valid, validation_msg = validate_code_before_execution(code)
    
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
        
        start_time = datetime.datetime.now()
        
        # Usamos sys.executable para asegurar que usamos el mismo intérprete Python
        cmd = [sys.executable, str(scratch_file)]
        
        result = subprocess.run(
            cmd,
            cwd=str(NS3_ROOT),
            capture_output=True,
            text=True,
            timeout=SIMULATION_TIMEOUT
        )
        
        end_time = datetime.datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print(f"  ⏱️  Tiempo de ejecución: {execution_time:.2f}s")
        
        # Extraer información del stdout
        sim_info = extract_simulation_info(result.stdout)
        
        # Verificar resultado
        if result.returncode != 0:
            error_msg = result.stderr if result.stderr else result.stdout
            print(f"\n  ❌ Simulación falló (código: {result.returncode})")
            
            # Identificar tipo de error
            error_type = "SimulationError"
            if "ImportError" in error_msg or "ModuleNotFoundError" in error_msg:
                error_type = "CompilationError" # Import error counts as compilation/setup
            elif "SyntaxError" in error_msg:
                error_type = "CompilationError"
            
            log_message("Simulator", f"Simulación falló: {error_type}", level="ERROR")
            
            return {
                'simulation_status': 'failed',
                'errors': [f"NS-3 Error ({error_type}): {error_msg[:500]}"],
                'error_type': error_type,
                'simulation_info': sim_info,
                **add_audit_entry(state, "simulator", "simulation_failed", {
                    'return_code': result.returncode,
                    'error': error_msg[:500],
                    'error_type': error_type,
                    'execution_time': execution_time
                })
            }
        
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
            f.write(result.stdout)
        
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
        
    except subprocess.TimeoutExpired:
        print(f"\n  ❌ Timeout: Simulación excedió {SIMULATION_TIMEOUT}s")
        log_message("Simulator", f"Timeout: Simulación excedió {SIMULATION_TIMEOUT}s", level="ERROR")
        
        return {
            'simulation_status': 'failed',
            'errors': [f'Timeout: Simulación excedió {SIMULATION_TIMEOUT} segundos.'],
            'error_type': 'TimeoutError',
            **add_audit_entry(state, "simulator", "timeout", {
                'timeout': SIMULATION_TIMEOUT
            })
        }
        
    except Exception as e:
        print(f"\n  ❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        log_message("Simulator", f"Error inesperado: {e}", level="ERROR")
        
        return {
            'simulation_status': 'failed',
            'errors': [f'Error de ejecución: {str(e)}'],
            'error_type': 'A2AError',
            **add_audit_entry(state, "simulator", "execution_error", {
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
