"""
Agente Analista

Responsable de analizar resultados de simulaciones y proponer optimizaciones.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
import xml.etree.ElementTree as ET
import pandas as pd
from langchain_ollama import ChatOllama

from config.settings import OLLAMA_BASE_URL, MODEL_REASONING
from utils.state import AgentState, add_audit_entry


def parse_flowmonitor_xml(xml_path: str) -> pd.DataFrame:
    """Parsea XML de FlowMonitor de NS-3"""
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
        
        flows = []
        for flow in root.findall('.//Flow'):
            tx_packets = int(flow.get('txPackets', 0))
            rx_packets = int(flow.get('rxPackets', 0))
            tx_bytes = int(flow.get('txBytes', 0))
            rx_bytes = int(flow.get('rxBytes', 0))
            
            # Calcular métricas
            pdr = (rx_packets / tx_packets * 100) if tx_packets > 0 else 0
            throughput = (rx_bytes * 8 / 1000000)  # Mbps
            
            # Delay (convertir de nanosegundos a milisegundos)
            delay_str = flow.get('delaySum', '0ns').replace('ns', '')
            delay_ns = float(delay_str) if delay_str else 0
            avg_delay = (delay_ns / rx_packets / 1e6) if rx_packets > 0 else 0
            
            flows.append({
                'flow_id': flow.get('flowId'),
                'tx_packets': tx_packets,
                'rx_packets': rx_packets,
                'pdr': pdr,
                'throughput_mbps': throughput,
                'avg_delay_ms': avg_delay
            })
        
        return pd.DataFrame(flows)
    except Exception as e:
        print(f"⚠️  Error parseando XML: {e}")
        return pd.DataFrame()


def calculate_kpis(df: pd.DataFrame) -> Dict:
    """Calcula KPIs agregados con estadísticas avanzadas"""
    if df.empty:
        return {}
    
    # KPIs básicos
    kpis = {
        'avg_pdr': float(df['pdr'].mean()),
        'std_pdr': float(df['pdr'].std()),
        'min_pdr': float(df['pdr'].min()),
        'max_pdr': float(df['pdr'].max()),
        
        'avg_throughput': float(df['throughput_mbps'].mean()),
        'std_throughput': float(df['throughput_mbps'].std()),
        'total_throughput': float(df['throughput_mbps'].sum()),
        
        'avg_delay': float(df['avg_delay_ms'].mean()),
        'std_delay': float(df['avg_delay_ms'].std()),
        'median_delay': float(df['avg_delay_ms'].median()),
        'p95_delay': float(df['avg_delay_ms'].quantile(0.95)),
        
        'total_flows': len(df),
        'successful_flows': len(df[df['rx_packets'] > 0]),
        'failed_flows': len(df[df['rx_packets'] == 0]),
        
        'total_tx_packets': int(df['tx_packets'].sum()),
        'total_rx_packets': int(df['rx_packets'].sum()),
        'total_lost_packets': int(df['tx_packets'].sum() - df['rx_packets'].sum()),
    }
    
    # Calcular tasa de éxito
    kpis['success_rate'] = (kpis['successful_flows'] / kpis['total_flows'] * 100) if kpis['total_flows'] > 0 else 0
    
    # Calcular eficiencia de red
    kpis['network_efficiency'] = (kpis['avg_pdr'] * kpis['avg_throughput']) / (kpis['avg_delay'] + 1)
    
    # Clasificar rendimiento
    kpis['performance_grade'] = classify_performance(kpis)
    
    return kpis


def classify_performance(kpis: Dict) -> str:
    """
    Clasifica el rendimiento de la red
    
    Args:
        kpis: Diccionario de KPIs
        
    Returns:
        Clasificación (Excelente/Bueno/Regular/Pobre)
    """
    pdr = kpis.get('avg_pdr', 0)
    delay = kpis.get('avg_delay', 999)
    success_rate = kpis.get('success_rate', 0)
    
    score = 0
    
    # Evaluar PDR (40 puntos)
    if pdr >= 95:
        score += 40
    elif pdr >= 85:
        score += 30
    elif pdr >= 70:
        score += 20
    else:
        score += 10
    
    # Evaluar Delay (30 puntos)
    if delay <= 50:
        score += 30
    elif delay <= 100:
        score += 20
    elif delay <= 200:
        score += 10
    
    # Evaluar Success Rate (30 puntos)
    if success_rate >= 95:
        score += 30
    elif success_rate >= 80:
        score += 20
    elif success_rate >= 60:
        score += 10
    
    # Clasificar
    if score >= 85:
        return "Excelente"
    elif score >= 65:
        return "Bueno"
    elif score >= 45:
        return "Regular"
    else:
        return "Pobre"


def propose_optimization(kpis: Dict, task: str) -> str:
    """Propone optimizaciones usando LLM con análisis profundo"""
    try:
        llm = ChatOllama(
            model=MODEL_REASONING,
            temperature=0.3,
            base_url=OLLAMA_BASE_URL
        )
        
        # Preparar estadísticas detalladas
        stats_summary = f"""
**MÉTRICAS ACTUALES (Protocolo Baseline):**

Packet Delivery Ratio (PDR):
- Promedio: {kpis.get('avg_pdr', 0):.2f}% ± {kpis.get('std_pdr', 0):.2f}%
- Rango: [{kpis.get('min_pdr', 0):.2f}%, {kpis.get('max_pdr', 0):.2f}%]

Throughput:
- Promedio: {kpis.get('avg_throughput', 0):.3f} Mbps ± {kpis.get('std_throughput', 0):.3f} Mbps
- Total: {kpis.get('total_throughput', 0):.3f} Mbps

Delay End-to-End:
- Promedio: {kpis.get('avg_delay', 0):.2f} ms ± {kpis.get('std_delay', 0):.2f} ms
- Mediana: {kpis.get('median_delay', 0):.2f} ms
- Percentil 95: {kpis.get('p95_delay', 0):.2f} ms

Flujos:
- Total: {kpis.get('total_flows', 0)}
- Exitosos: {kpis.get('successful_flows', 0)} ({kpis.get('success_rate', 0):.1f}%)
- Fallidos: {kpis.get('failed_flows', 0)}

Paquetes:
- Transmitidos: {kpis.get('total_tx_packets', 0):,}
- Recibidos: {kpis.get('total_rx_packets', 0):,}
- Perdidos: {kpis.get('total_lost_packets', 0):,}

Eficiencia de Red: {kpis.get('network_efficiency', 0):.2f}
Clasificación: {kpis.get('performance_grade', 'N/A')}
"""
        
        prompt = f"""
Eres un experto en optimización de protocolos de enrutamiento con Deep Reinforcement Learning y Graph Neural Networks.

**TAREA ORIGINAL:**
{task}

{stats_summary}

**ANÁLISIS PROFUNDO REQUERIDO:**

1. **Diagnóstico del Rendimiento Actual** (2-3 párrafos):
   - Evaluación crítica: ¿Es aceptable para una red de este tipo?
   - Comparación con benchmarks típicos de la literatura
   - Identificación de métricas problemáticas y sus causas probables
   - Análisis de variabilidad (desviaciones estándar altas/bajas)

2. **Identificación de Cuellos de Botella** (específico):
   - Problemas de congestión (si PDR < 85%)
   - Problemas de latencia (si delay > 100ms)
   - Problemas de throughput (si < 1 Mbps)
   - Problemas de estabilidad (si std alta)
   - Factores del protocolo de enrutamiento que limitan rendimiento

3. **Propuesta de Arquitectura Deep Learning** (detallado):
   
   a) **Tipo de Red Neuronal**:
      - DQN (Deep Q-Network) para decisiones discretas
      - A3C (Asynchronous Advantage Actor-Critic) para entornos distribuidos
      - GNN (Graph Neural Network) para topologías dinámicas
      - Transformer para secuencias temporales
      - Justifica tu elección basándote en las métricas

   b) **Espacio de Estados** (qué observa el agente):
      - Información local del nodo (buffer, vecinos, energía)
      - Información de red (topología, tráfico, congestión)
      - Métricas históricas (PDR reciente, delay promedio)
      - Dimensionalidad sugerida

   c) **Espacio de Acciones** (qué puede decidir):
      - Selección de siguiente salto
      - Ajuste de parámetros del protocolo
      - Control de tasa de transmisión
      - Gestión de rutas alternativas

   d) **Función de Recompensa** (ecuación específica):
      - Componentes: PDR, delay, throughput, overhead
      - Pesos sugeridos para cada componente
      - Penalizaciones (paquetes perdidos, colisiones)
      - Ejemplo: R = w1*PDR - w2*delay - w3*overhead + w4*throughput

4. **Plan de Implementación en NS-3** (paso a paso):
   
   a) **Integración con ns3-ai**:
      - Configurar interfaz Python-C++ con ns3-ai
      - Definir mensajes de comunicación (estado/acción)
      - Frecuencia de decisiones del agente

   b) **Arquitectura del Sistema**:
      - NS-3 como simulador de red
      - PyTorch/TensorFlow para red neuronal
      - Gym environment para interfaz RL
      - Buffer de experiencias para training

   c) **Proceso de Entrenamiento**:
      - Número de episodios sugerido (1000-5000)
      - Duración de cada episodio
      - Estrategia de exploración (ε-greedy)
      - Criterio de convergencia

   d) **Configuración Específica**:
      - Modificaciones al protocolo baseline
      - Puntos de instrumentación en NS-3
      - Logging y debugging

5. **Mejoras Incrementales Sugeridas** (antes de DL):
   - Ajustes de parámetros del protocolo actual
   - Optimizaciones simples que podrían mejorar métricas
   - Quick wins

6. **Métricas de Éxito** (objetivos cuantitativos):
   - PDR objetivo: X%
   - Delay objetivo: Y ms
   - Throughput objetivo: Z Mbps
   - Mejora esperada vs baseline: W%

**FORMATO:**
- Sé extremadamente específico y técnico
- Incluye ecuaciones cuando sea relevante
- Proporciona valores numéricos concretos
- Cita papers relevantes si es posible
- Prioriza implementabilidad
"""
        
        response = llm.invoke(prompt)
        
        # Añadir resumen ejecutivo al inicio
        executive_summary = f"""
═══════════════════════════════════════════════════════════════
RESUMEN EJECUTIVO
═══════════════════════════════════════════════════════════════

Rendimiento Actual: {kpis.get('performance_grade', 'N/A')}
PDR: {kpis.get('avg_pdr', 0):.1f}% | Delay: {kpis.get('avg_delay', 0):.1f}ms | Throughput: {kpis.get('avg_throughput', 0):.2f}Mbps

Recomendación Principal: {"Optimización con Deep Learning necesaria" if kpis.get('avg_pdr', 0) < 85 else "Ajustes finos recomendados"}

═══════════════════════════════════════════════════════════════

"""
        
        return executive_summary + response.content
        
    except Exception as e:
        return f"Error en propuesta: {str(e)}"


def analyst_node(state: AgentState) -> Dict:
    """Nodo del agente analista para LangGraph"""
    print("\n" + "="*80)
    print("🔬 AGENTE ANALISTA ACTIVADO")
    print("="*80)
    
    results_path = state.get('simulation_logs', '')
    
    if not results_path:
        print("❌ No hay resultados para analizar")
        return {
            'errors': ['No hay resultados de simulación para analizar'],
            **add_audit_entry(state, "analyst", "no_results", {})
        }
    
    print(f"📊 Analizando: {results_path}\n")
    
    try:
        # Parsear resultados
        df = parse_flowmonitor_xml(results_path)
        
        if df.empty:
            print("⚠️  No se pudieron extraer métricas")
            return {
                'analysis_results': {'error': 'No se pudieron parsear resultados'},
                **add_audit_entry(state, "analyst", "parse_failed", {})
            }
        
        # Calcular KPIs
        kpis = calculate_kpis(df)
        
        print("📈 KPIs Calculados:")
        for key, value in kpis.items():
            print(f"   {key}: {value}")
        print()
        
        # Proponer optimización
        print("🧠 Generando propuesta de optimización...")
        proposal = propose_optimization(kpis, state['task'])
        
        print("✅ Análisis completado")
        
        return {
            'analysis_results': {
                'dataframe': df.to_dict(),
                'kpis': kpis,
                'proposal': proposal
            },
            'metrics': kpis,
            'messages': [f"Análisis completado. PDR: {kpis['avg_pdr']:.2f}%"],
            **add_audit_entry(state, "analyst", "analysis_completed", {
                'kpis': kpis
            })
        }
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        return {
            'errors': [f'Error en análisis: {str(e)}'],
            **add_audit_entry(state, "analyst", "analysis_error", {
                'error': str(e)
            })
        }


if __name__ == "__main__":
    print("Agente Analista - Prueba")
    print("Requiere un archivo XML de FlowMonitor para probar")
