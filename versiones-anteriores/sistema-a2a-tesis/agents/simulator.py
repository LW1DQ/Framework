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

from config.settings import NS3_ROOT, SIMULATION_TIMEOUT, SIMULATIONS_DIR
from utils.state import AgentState, add_audit_entry


def validate_code_before_execution(code: str) -> tuple[bool, str]:
    """
    Valida el código antes de ejecutarlo
    
    Args:
        code: Código a validar
        
    Returns:
        (es_válido, mensaje)
    """
    # Verificar imports críticos
    required_imports = ['ns.core', 'ns.network']
    missing = [imp for imp in required_imports if imp not in code]
    
    if missing:
        return False, f"Faltan imports críticos: {', '.join(missing)}"
    
    # Verificar estructura básica
    if 'def main()' not in code and 'if __name__' not in code:
        return False, "Falta función main() o bloque if __name__"
    
    # Verificar que tenga Simulator.Run()
    if 'Simulator.Run()' not in code:
        return False, "Falta llamada a Simulator.Run()"
    
    # Verificar que tenga Simulator.Destroy()
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
    
    code = state.get('code_snippet', '')
    iteration = state.get('iteration', 0)
    
    if not code:
        print("❌ No hay código para ejecutar")
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
        return {
            'simulation_status': 'failed',
            'errors': [f"Validación pre-ejecución falló: {validation_msg}"],
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
        
        start_time = datetime.datetime.now()
        
        result = subprocess.run(
            ["./ns3", "run", f"scratch/{scratch_file.name}"],
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
            print(f"  📝 Error detallado:")
            
            # Mostrar primeras líneas del error
            error_lines = error_msg.split('\n')[:10]
            for line in error_lines:
                if line.strip():
                    print(f"     {line}")
            
            # Identificar tipo de error
            error_type = "unknown"
            if "ImportError" in error_msg or "ModuleNotFoundError" in error_msg:
                error_type = "import_error"
            elif "AttributeError" in error_msg:
                error_type = "attribute_error"
            elif "SyntaxError" in error_msg:
                error_type = "syntax_error"
            elif "NameError" in error_msg:
                error_type = "name_error"
            
            return {
                'simulation_status': 'failed',
                'errors': [f"NS-3 Error ({error_type}): {error_msg[:500]}"],
                'simulation_info': sim_info,
                **add_audit_entry(state, "simulator", "simulation_failed", {
                    'return_code': result.returncode,
                    'error': error_msg[:500],
                    'error_type': error_type,
                    'execution_time': execution_time,
                    'backup_file': str(backup_file)
                })
            }
        
        # Mostrar warnings si existen
        if sim_info['warnings']:
            print(f"\n  ⚠️  Warnings detectados ({len(sim_info['warnings'])}):")
            for warning in sim_info['warnings'][:3]:
                print(f"     {warning}")
        
        # Buscar archivo de resultados
        results_file = NS3_ROOT / "resultados.xml"
        
        if not results_file.exists():
            print("\n  ⚠️  Simulación ejecutó pero no generó resultados.xml")
            print(f"  📝 Stdout de la simulación:")
            stdout_lines = result.stdout.split('\n')[:15]
            for line in stdout_lines:
                if line.strip():
                    print(f"     {line}")
            
            return {
                'simulation_status': 'completed_no_results',
                'simulation_logs': '',
                'simulation_info': sim_info,
                'messages': ['Simulación completada sin archivo de resultados'],
                **add_audit_entry(state, "simulator", "no_results_file", {
                    'execution_time': execution_time,
                    'stdout': result.stdout[:500]
                })
            }
        
        # Verificar tamaño del archivo de resultados
        file_size = results_file.stat().st_size
        print(f"\n  ✓ Archivo de resultados generado: {file_size:,} bytes")
        
        if file_size < 100:
            print("  ⚠️  Archivo de resultados muy pequeño, posiblemente vacío")
        
        # Mover resultados a directorio de resultados
        new_results_path = SIMULATIONS_DIR / "results" / f"sim_{timestamp}.xml"
        new_results_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy(results_file, new_results_path)
        
        # Guardar también el stdout
        stdout_file = SIMULATIONS_DIR / "results" / f"sim_{timestamp}_stdout.txt"
        with open(stdout_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
        
        print(f"  ✅ Simulación completada exitosamente")
        print(f"  📊 Resultados guardados en: {new_results_path.name}")
        print(f"  📝 Stdout guardado en: {stdout_file.name}")
        
        if sim_info['nodes_created'] > 0:
            print(f"  🔢 Nodos simulados: {sim_info['nodes_created']}")
        if sim_info['simulation_time'] > 0:
            print(f"  ⏱️  Tiempo simulado: {sim_info['simulation_time']}s")
        
        return {
            'simulation_status': 'completed',
            'simulation_logs': str(new_results_path),
            'simulation_info': sim_info,
            'execution_time': execution_time,
            **add_audit_entry(state, "simulator", "simulation_completed", {
                'results_path': str(new_results_path),
                'stdout_path': str(stdout_file),
                'execution_time': execution_time,
                'file_size': file_size,
                'nodes': sim_info['nodes_created'],
                'sim_time': sim_info['simulation_time'],
                'warnings_count': len(sim_info['warnings'])
            })
        }
        
    except subprocess.TimeoutExpired:
        print(f"\n  ❌ Timeout: Simulación excedió {SIMULATION_TIMEOUT}s")
        print(f"  💡 Sugerencia: Reducir tiempo de simulación o número de nodos")
        
        return {
            'simulation_status': 'failed',
            'errors': [f'Timeout: Simulación excedió {SIMULATION_TIMEOUT} segundos. Reducir complejidad.'],
            **add_audit_entry(state, "simulator", "timeout", {
                'timeout': SIMULATION_TIMEOUT,
                'suggestion': 'Reducir tiempo de simulación o número de nodos'
            })
        }
        
    except FileNotFoundError as e:
        print(f"\n  ❌ Error: NS-3 no encontrado en {NS3_ROOT}")
        print(f"  💡 Verificar que NS3_ROOT esté configurado correctamente")
        
        return {
            'simulation_status': 'failed',
            'errors': [f'NS-3 no encontrado: {str(e)}'],
            **add_audit_entry(state, "simulator", "ns3_not_found", {
                'ns3_root': str(NS3_ROOT),
                'error': str(e)
            })
        }
        
    except Exception as e:
        print(f"\n  ❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            'simulation_status': 'failed',
            'errors': [f'Error de ejecución: {str(e)}'],
            **add_audit_entry(state, "simulator", "execution_error", {
                'error': str(e),
                'traceback': traceback.format_exc()[:500]
            })
        }
    
    finally:
        # Limpiar archivo temporal de scratch (mantener backup)
        if scratch_file.exists():
            try:
                scratch_file.unlink()
                print(f"\n  🧹 Limpieza: archivo temporal eliminado")
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
