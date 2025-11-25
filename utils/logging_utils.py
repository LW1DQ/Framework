"""
Utilidades de Logging para el Sistema A2A

Proporciona funciones centralizadas para logging y telemetría con soporte para dashboard.
"""

import json
import os
import time
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Configurar directorios
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# Archivos de log
LOG_FILE = LOGS_DIR / "sistema_a2a.log"
STATE_FILE = LOGS_DIR / "system_state.json"
METRICS_FILE = LOGS_DIR / "metrics_history.csv"
AGENT_LOGS_FILE = LOGS_DIR / "agent_logs.json"

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('A2A')

# Estado global del sistema
_system_state = {
    'status': 'idle',
    'current_agent': None,
    'task': None,
    'iteration': 0,
    'max_iterations': 5,
    'metrics': {},
    'agents': {},
    'timestamp': datetime.now().isoformat()
}


def init_logging():
    """Inicializa el sistema de logging"""
    _save_state()
    logger.info("Sistema de logging inicializado")


def _save_state():
    """Guarda el estado del sistema en archivo JSON"""
    try:
        _system_state['updated_at'] = time.time()
        _system_state['timestamp'] = datetime.now().isoformat()
        
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(_system_state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error guardando estado: {e}")


def _append_agent_log(agent_name: str, message: str, level: str = "INFO"):
    """Añade un log de agente al archivo de logs"""
    try:
        # Cargar logs existentes
        if AGENT_LOGS_FILE.exists():
            with open(AGENT_LOGS_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Añadir nuevo log
        logs.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'agent': agent_name,
            'level': level,
            'message': message
        })
        
        # Mantener solo últimos 100 logs
        if len(logs) > 100:
            logs = logs[-100:]
        
        # Guardar
        with open(AGENT_LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error guardando log de agente: {e}")


def save_system_state(state: Dict[str, Any]):
    """
    Guarda el estado completo del sistema (compatibilidad con código anterior)
    
    Args:
        state: Diccionario con el estado del sistema
    """
    global _system_state
    _system_state.update(state)
    _save_state()


def update_agent_status(agent_name: str, status: str, task: str = None, message: str = ""):
    """
    Actualiza el estado de un agente
    
    Args:
        agent_name: Nombre del agente
        status: Estado (running, completed, failed, idle)
        task: Tarea actual (opcional, para compatibilidad)
        message: Mensaje descriptivo
    """
    # Usar task como message si message está vacío (compatibilidad)
    if not message and task:
        message = task
    
    logger.info(f"[{agent_name}] Status: {status} - {message}")
    
    # Actualizar estado global
    _system_state['current_agent'] = agent_name
    _system_state['agents'][agent_name] = {
        'status': status,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    
    if task:
        _system_state['current_task'] = task
    
    # Guardar estado
    _save_state()
    
    # Añadir a logs de agentes
    _append_agent_log(agent_name, f"Status: {status} - {message}", "INFO")


def log_message(agent_name: str, message: str, level: str = "INFO"):
    """
    Registra un mensaje de un agente
    
    Args:
        agent_name: Nombre del agente
        message: Mensaje a registrar
        level: Nivel de log (INFO, WARNING, ERROR)
    """
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(f"[{agent_name}] {message}")
    
    # Añadir a logs de agentes
    _append_agent_log(agent_name, message, level)


def log_metric(pdr: float = 0, delay: float = 0, throughput: float = 0, overhead: float = 0):
    """
    Registra métricas del sistema
    
    Args:
        pdr: Packet Delivery Ratio
        delay: Delay promedio
        throughput: Throughput promedio
        overhead: Overhead de enrutamiento
    """
    logger.info(f"Metrics - PDR: {pdr:.2f}%, Delay: {delay:.2f}ms, "
                f"Throughput: {throughput:.2f}Mbps, Overhead: {overhead:.3f}")
    
    # Calcular deltas si hay métricas previas
    prev_metrics = _system_state.get('metrics', {})
    delta_pdr = pdr - prev_metrics.get('pdr', pdr)
    delta_delay = delay - prev_metrics.get('delay', delay)
    delta_throughput = throughput - prev_metrics.get('throughput', throughput)
    
    # Actualizar métricas en estado
    _system_state['metrics'] = {
        'pdr': pdr,
        'delay': delay,
        'throughput': throughput,
        'overhead': overhead,
        'delta_pdr': delta_pdr,
        'delta_delay': delta_delay,
        'delta_throughput': delta_throughput,
        'timestamp': datetime.now().isoformat()
    }
    
    # Guardar estado
    _save_state()
    
    # Añadir a historial de métricas (CSV)
    try:
        # Verificar si el archivo existe
        file_exists = METRICS_FILE.exists()
        
        with open(METRICS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Escribir header si es nuevo archivo
            if not file_exists:
                writer.writerow(['timestamp', 'pdr', 'delay', 'throughput', 'overhead'])
            
            # Escribir métricas
            writer.writerow([
                datetime.now().isoformat(),
                pdr,
                delay,
                throughput,
                overhead
            ])
    except Exception as e:
        logger.error(f"Error guardando métricas en CSV: {e}")


def set_system_status(status: str, task: str = None, iteration: int = None, max_iterations: int = None):
    """
    Actualiza el estado general del sistema
    
    Args:
        status: Estado del sistema (running, completed, failed, idle)
        task: Tarea actual
        iteration: Iteración actual
        max_iterations: Máximo de iteraciones
    """
    _system_state['status'] = status
    
    if task is not None:
        _system_state['task'] = task
    
    if iteration is not None:
        _system_state['iteration'] = iteration
    
    if max_iterations is not None:
        _system_state['max_iterations'] = max_iterations
    
    _save_state()
    
    logger.info(f"System status: {status}")


def get_system_state() -> Dict[str, Any]:
    """
    Obtiene el estado actual del sistema
    
    Returns:
        Diccionario con el estado del sistema
    """
    return _system_state.copy()


# Inicializar al importar
init_logging()
