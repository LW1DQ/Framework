#!/usr/bin/env python3
"""
Dashboard en Tiempo Real - Sistema A2A
Visualización del estado del sistema durante la ejecución

Ejecutar con: streamlit run dashboard.py
"""

import streamlit as st
import json
import time
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuración de la página
st.set_page_config(
    page_title="Sistema A2A Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rutas de archivos
LOGS_DIR = Path("logs")
STATE_FILE = LOGS_DIR / "system_state.json"
METRICS_FILE = LOGS_DIR / "metrics_history.csv"
AGENT_LOGS_FILE = LOGS_DIR / "agent_logs.json"

# Crear directorios si no existen
LOGS_DIR.mkdir(exist_ok=True)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .agent-status {
        padding: 0.5rem;
        border-radius: 0.3rem;
        margin: 0.3rem 0;
    }
    .status-running {
        background-color: #90EE90;
        color: #006400;
    }
    .status-completed {
        background-color: #87CEEB;
        color: #00008B;
    }
    .status-failed {
        background-color: #FFB6C1;
        color: #8B0000;
    }
    .status-idle {
        background-color: #D3D3D3;
        color: #696969;
    }
</style>
""", unsafe_allow_html=True)


def load_system_state():
    """Carga el estado actual del sistema"""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    return {
        'status': 'idle',
        'message': 'Sistema inactivo',
        'timestamp': datetime.now().isoformat()
    }


def load_metrics_history():
    """Carga el historial de métricas"""
    if METRICS_FILE.exists():
        try:
            df = pd.read_csv(METRICS_FILE)
            return df
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def load_agent_logs():
    """Carga los logs de agentes"""
    if AGENT_LOGS_FILE.exists():
        try:
            with open(AGENT_LOGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []
    return []


def get_agent_status_class(status):
    """Retorna la clase CSS según el estado del agente"""
    status_map = {
        'running': 'status-running',
        'completed': 'status-completed',
        'failed': 'status-failed',
        'idle': 'status-idle'
    }
    return status_map.get(status, 'status-idle')


def create_metrics_chart(df):
    """Crea gráfico de métricas en tiempo real"""
    if df.empty:
        return None
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('PDR (%)', 'Delay (ms)', 'Throughput (Mbps)', 'Overhead (%)'),
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # PDR
    if 'pdr' in df.columns:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['pdr'], mode='lines+markers', 
                      name='PDR', line=dict(color='#1f77b4', width=2)),
            row=1, col=1
        )
    
    # Delay
    if 'delay' in df.columns:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['delay'], mode='lines+markers',
                      name='Delay', line=dict(color='#ff7f0e', width=2)),
            row=1, col=2
        )
    
    # Throughput
    if 'throughput' in df.columns:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['throughput'], mode='lines+markers',
                      name='Throughput', line=dict(color='#2ca02c', width=2)),
            row=2, col=1
        )
    
    # Overhead
    if 'overhead' in df.columns:
        fig.add_trace(
            go.Scatter(x=df.index, y=df['overhead']*100, mode='lines+markers',
                      name='Overhead', line=dict(color='#d62728', width=2)),
            row=2, col=2
        )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="Métricas en Tiempo Real",
        title_x=0.5
    )
    
    return fig


def main():
    """Función principal del dashboard"""
    
    # Header
    st.markdown('<div class="main-header">🤖 Sistema A2A - Dashboard en Tiempo Real</div>', 
                unsafe_allow_html=True)
    
    # Sidebar - Configuración
    with st.sidebar:
        st.header("⚙️ Configuración")
        
        auto_refresh = st.checkbox("Auto-refresh", value=True)
        refresh_interval = st.slider("Intervalo (segundos)", 1, 10, 2)
        
        st.markdown("---")
        
        st.header("📊 Estadísticas")
        state = load_system_state()
        
        st.metric("Estado", state.get('status', 'unknown').upper())
        
        if 'iteration' in state:
            st.metric("Iteración", state['iteration'])
        
        if 'timestamp' in state:
            try:
                ts = datetime.fromisoformat(state['timestamp'])
                st.metric("Última actualización", ts.strftime("%H:%M:%S"))
            except:
                pass
        
        st.markdown("---")
        
        # Botones de control
        if st.button("🔄 Refrescar Ahora"):
            st.rerun()
        
        if st.button("🗑️ Limpiar Logs"):
            if STATE_FILE.exists():
                STATE_FILE.unlink()
            if METRICS_FILE.exists():
                METRICS_FILE.unlink()
            if AGENT_LOGS_FILE.exists():
                AGENT_LOGS_FILE.unlink()
            st.success("Logs limpiados")
            time.sleep(1)
            st.rerun()
    
    # Main content
    state = load_system_state()
    
    # Fila 1: Estado general
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status = state.get('status', 'idle')
        status_emoji = {
            'running': '🟢',
            'completed': '✅',
            'failed': '❌',
            'idle': '⚪'
        }.get(status, '⚪')
        st.metric("Estado del Sistema", f"{status_emoji} {status.upper()}")
    
    with col2:
        current_agent = state.get('current_agent', 'N/A')
        st.metric("Agente Activo", current_agent)
    
    with col3:
        iteration = state.get('iteration', 0)
        max_iter = state.get('max_iterations', 5)
        st.metric("Progreso", f"{iteration}/{max_iter}")
    
    with col4:
        task = state.get('task', 'N/A')
        st.metric("Tarea", task[:20] + "..." if len(task) > 20 else task)
    
    st.markdown("---")
    
    # Fila 2: Métricas actuales
    if 'metrics' in state and state['metrics']:
        st.subheader("📊 Métricas Actuales")
        
        metrics = state['metrics']
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdr = metrics.get('pdr', 0)
            delta_pdr = metrics.get('delta_pdr', 0)
            st.metric("PDR", f"{pdr:.1f}%", f"{delta_pdr:+.1f}%")
        
        with col2:
            delay = metrics.get('delay', 0)
            delta_delay = metrics.get('delta_delay', 0)
            st.metric("Delay", f"{delay:.1f} ms", f"{delta_delay:+.1f} ms")
        
        with col3:
            throughput = metrics.get('throughput', 0)
            delta_throughput = metrics.get('delta_throughput', 0)
            st.metric("Throughput", f"{throughput:.2f} Mbps", f"{delta_throughput:+.2f} Mbps")
        
        with col4:
            overhead = metrics.get('overhead', 0)
            st.metric("Overhead", f"{overhead*100:.1f}%")
        
        st.markdown("---")
    
    # Fila 3: Gráficos de métricas
    metrics_df = load_metrics_history()
    if not metrics_df.empty:
        st.subheader("📈 Historial de Métricas")
        fig = create_metrics_chart(metrics_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("---")
    
    # Fila 4: Estado de agentes
    st.subheader("🤖 Estado de Agentes")
    
    agents_state = state.get('agents', {})
    
    if agents_state:
        cols = st.columns(4)
        agent_names = [
            'Researcher', 'Coder', 'Simulator', 'Trace Analyzer',
            'Analyst', 'Visualizer', 'Optimizer', 'GitHub Manager'
        ]
        
        for idx, agent_name in enumerate(agent_names):
            col = cols[idx % 4]
            agent_info = agents_state.get(agent_name, {})
            agent_status = agent_info.get('status', 'idle')
            agent_message = agent_info.get('message', 'Sin actividad')
            
            status_class = get_agent_status_class(agent_status)
            
            with col:
                st.markdown(f"""
                <div class="agent-status {status_class}">
                    <strong>{agent_name}</strong><br>
                    <small>{agent_status.upper()}</small><br>
                    <small>{agent_message[:30]}...</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No hay información de agentes disponible")
    
    st.markdown("---")
    
    # Fila 5: Logs recientes
    st.subheader("📝 Logs Recientes")
    
    logs = load_agent_logs()
    
    if logs:
        # Mostrar últimos 20 logs
        recent_logs = logs[-20:]
        
        for log in reversed(recent_logs):
            timestamp = log.get('timestamp', '')
            agent = log.get('agent', 'System')
            level = log.get('level', 'INFO')
            message = log.get('message', '')
            
            # Color según nivel
            level_colors = {
                'INFO': '🔵',
                'WARNING': '🟡',
                'ERROR': '🔴',
                'SUCCESS': '🟢'
            }
            
            emoji = level_colors.get(level, '⚪')
            
            st.text(f"{emoji} [{timestamp}] {agent}: {message}")
    else:
        st.info("No hay logs disponibles")
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()


if __name__ == "__main__":
    main()
