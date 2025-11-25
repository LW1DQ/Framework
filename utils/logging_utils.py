import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List

LOG_FILE = "system_state.json"
METRICS_FILE = "simulation_metrics.csv"

def init_logging():
    """Inicializa el archivo de estado si no existe"""
    if not os.path.exists(LOG_FILE):
        initial_state = {
            "status": "idle",
            "current_agent": "None",
            "current_task": "None",
            "logs": [],
            "last_proposal": None,
            "updated_at": time.time()
        }
        save_system_state(initial_state)

def save_system_state(state: Dict[str, Any]):
    """Guarda el estado completo del sistema"""
    try:
        state['updated_at'] = time.time()
        with open(LOG_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        print(f"Error saving system state: {e}")

def update_agent_status(agent_name: str, status: str, task: str = None):
    """Actualiza el estado del agente actual"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                state = json.load(f)
        else:
            state = {"logs": []}
            
        state['current_agent'] = agent_name
        state['status'] = status
        if task:
            state['current_task'] = task
            
        save_system_state(state)
    except Exception as e:
        print(f"Error updating agent status: {e}")

def log_message(agent_name: str, message: str):
    """Registra un mensaje en el log del dashboard"""
    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r') as f:
                state = json.load(f)
        else:
            state = {"logs": []}
            
        log_entry = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": message
        }
        
        # Mantener solo los últimos 50 logs
        state['logs'].append(log_entry)
        if len(state['logs']) > 50:
            state['logs'] = state['logs'][-50:]
            
        save_system_state(state)
    except Exception as e:
        print(f"Error logging message: {e}")

def log_metric(pdr: float, delay: float, throughput: float):
    """Registra métricas en CSV para gráficos históricos"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = "timestamp,pdr,delay,throughput\n"
        row = f"{timestamp},{pdr},{delay},{throughput}\n"
        
        if not os.path.exists(METRICS_FILE):
            with open(METRICS_FILE, 'w') as f:
                f.write(header)
                
        with open(METRICS_FILE, 'a') as f:
            f.write(row)
    except Exception as e:
        print(f"Error logging metrics: {e}")
