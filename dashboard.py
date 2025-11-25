import streamlit as st
import pandas as pd
import json
import time
import os
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(
    page_title="AGENTES A2A - Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constantes
LOG_FILE = "system_state.json"
METRICS_FILE = "simulation_metrics.csv"

def load_system_state():
    """Carga el estado actual del sistema desde JSON"""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def load_metrics():
    """Carga métricas históricas desde CSV"""
    if os.path.exists(METRICS_FILE):
        try:
            return pd.read_csv(METRICS_FILE)
        except:
            return pd.DataFrame()
    return pd.DataFrame(columns=['timestamp', 'pdr', 'delay', 'throughput'])

# Sidebar
st.sidebar.title("📡 Panel de Control")
st.sidebar.markdown("---")
refresh_rate = st.sidebar.slider("Tasa de refresco (s)", 1, 10, 2)
auto_refresh = st.sidebar.checkbox("Auto-refresco", value=True)

st.sidebar.markdown("### Estado del Sistema")
state = load_system_state()
if state:
    status_color = "🟢" if state.get('status') == 'running' else "🔴"
    st.sidebar.markdown(f"**Estado:** {status_color} {state.get('status', 'Unknown')}")
    st.sidebar.markdown(f"**Agente Activo:** `{state.get('current_agent', 'None')}`")
    st.sidebar.markdown(f"**Tarea:** {state.get('current_task', 'None')}")
else:
    st.sidebar.warning("Esperando datos del sistema...")

# Main Content
st.title("📡 AGENTES A2A: Monitor en Tiempo Real")

# Layout de métricas principales
col1, col2, col3, col4 = st.columns(4)

metrics = load_metrics()
if not metrics.empty:
    last_pdr = metrics['pdr'].iloc[-1]
    last_delay = metrics['delay'].iloc[-1]
    last_thr = metrics['throughput'].iloc[-1]
    
    col1.metric("PDR Promedio", f"{last_pdr:.2f}%", delta=f"{metrics['pdr'].diff().iloc[-1]:.2f}")
    col2.metric("Delay Promedio", f"{last_delay:.2f} ms", delta=f"{metrics['delay'].diff().iloc[-1]:.2f}", delta_color="inverse")
    col3.metric("Throughput", f"{last_thr:.3f} Mbps", delta=f"{metrics['throughput'].diff().iloc[-1]:.3f}")
    col4.metric("Simulaciones", len(metrics))
else:
    col1.metric("PDR Promedio", "--")
    col2.metric("Delay Promedio", "--")
    col3.metric("Throughput", "--")
    col4.metric("Simulaciones", "0")

# Gráficos en tiempo real
st.markdown("### 📈 Evolución de Métricas")
if not metrics.empty:
    tab1, tab2 = st.tabs(["PDR & Throughput", "Latencia"])
    
    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=metrics.index, y=metrics['pdr'], name='PDR (%)', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=metrics.index, y=metrics['throughput']*100, name='Throughput (x100 Mbps)', line=dict(color='blue', dash='dot')))
        fig.update_layout(title="Rendimiento de Red", xaxis_title="Iteración", yaxis_title="Valor")
        st.plotly_chart(fig, use_container_width=True)
        
    with tab2:
        fig_delay = px.line(metrics, y='delay', title="Latencia Extremo a Extremo (ms)")
        fig_delay.update_traces(line_color='red')
        st.plotly_chart(fig_delay, use_container_width=True)

# Logs y Actividad
st.markdown("### 📝 Actividad de Agentes")
log_col, prop_col = st.columns([2, 1])

with log_col:
    st.subheader("Log del Sistema")
    if state and 'logs' in state:
        for log in reversed(state['logs'][-10:]):
            st.text(f"[{log['time']}] [{log['agent']}] {log['message']}")
    else:
        st.info("No hay logs recientes")

with prop_col:
    st.subheader("Última Propuesta IA")
    if state and 'last_proposal' in state:
        st.info(state['last_proposal'])
    else:
        st.markdown("*Esperando propuesta de optimización...*")

# Auto-refresh logic
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()
