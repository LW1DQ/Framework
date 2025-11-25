"""
Agente Visualizador

Responsable de generar gráficos académicos de los resultados.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime

from config.settings import SIMULATIONS_DIR, PLOT_DPI, PLOT_FIGSIZE
from utils.state import AgentState, add_audit_entry

# Configurar estilo académico
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = PLOT_FIGSIZE
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titleweight'] = 'bold'


def create_plots(df: pd.DataFrame, kpis: Dict) -> List[str]:
    """
    Crea gráficos académicos profesionales de métricas
    
    Args:
        df: DataFrame con datos de flujos
        kpis: KPIs calculados
        
    Returns:
        Lista de rutas a gráficos generados
    """
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    plots_dir = SIMULATIONS_DIR / "plots" / timestamp
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    plots = []
    
    # 1. Dashboard de métricas principales (2x2)
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'Dashboard de Métricas - {timestamp}', fontsize=16, fontweight='bold')
    
    # 1.1 PDR por flujo
    ax = axes[0, 0]
    bars = ax.bar(range(len(df)), df['pdr'], color='steelblue', alpha=0.7, edgecolor='navy')
    ax.axhline(y=kpis['avg_pdr'], color='red', linestyle='--', linewidth=2,
               label=f'μ = {kpis["avg_pdr"]:.2f}%')
    ax.axhline(y=kpis['avg_pdr'] + kpis['std_pdr'], color='orange', linestyle=':', linewidth=1,
               label=f'μ ± σ')
    ax.axhline(y=kpis['avg_pdr'] - kpis['std_pdr'], color='orange', linestyle=':', linewidth=1)
    ax.set_xlabel('Flujo ID', fontweight='bold')
    ax.set_ylabel('PDR (%)', fontweight='bold')
    ax.set_title('Packet Delivery Ratio por Flujo')
    ax.legend(loc='lower right')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 1.2 Distribución de Delay
    ax = axes[0, 1]
    n, bins, patches = ax.hist(df['avg_delay_ms'], bins=25, color='coral', alpha=0.7, 
                                edgecolor='darkred', density=True)
    ax.axvline(x=kpis['avg_delay'], color='red', linestyle='--', linewidth=2,
               label=f'μ = {kpis["avg_delay"]:.2f} ms')
    ax.axvline(x=kpis['median_delay'], color='green', linestyle='-.', linewidth=2,
               label=f'Mediana = {kpis["median_delay"]:.2f} ms')
    ax.axvline(x=kpis['p95_delay'], color='purple', linestyle=':', linewidth=2,
               label=f'P95 = {kpis["p95_delay"]:.2f} ms')
    ax.set_xlabel('Delay (ms)', fontweight='bold')
    ax.set_ylabel('Densidad de Probabilidad', fontweight='bold')
    ax.set_title('Distribución de Delay End-to-End')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # 1.3 Throughput acumulado
    ax = axes[1, 0]
    df_sorted = df.sort_values('throughput_mbps', ascending=False)
    cumulative_throughput = df_sorted['throughput_mbps'].cumsum()
    ax.plot(range(len(cumulative_throughput)), cumulative_throughput.values, 
            marker='o', color='green', linewidth=2, markersize=4, alpha=0.7)
    ax.fill_between(range(len(cumulative_throughput)), cumulative_throughput.values, 
                     alpha=0.3, color='green')
    ax.set_xlabel('Número de Flujos (ordenados)', fontweight='bold')
    ax.set_ylabel('Throughput Acumulado (Mbps)', fontweight='bold')
    ax.set_title(f'Throughput Total: {kpis["total_throughput"]:.2f} Mbps')
    ax.grid(True, alpha=0.3)
    
    # 1.4 Resumen de KPIs (tabla)
    ax = axes[1, 1]
    ax.axis('off')
    
    kpi_data = [
        ['Métrica', 'Valor', 'Clasificación'],
        ['PDR Promedio', f'{kpis["avg_pdr"]:.2f}%', get_pdr_grade(kpis["avg_pdr"])],
        ['Delay Promedio', f'{kpis["avg_delay"]:.2f} ms', get_delay_grade(kpis["avg_delay"])],
        ['Throughput Total', f'{kpis["total_throughput"]:.2f} Mbps', ''],
        ['Flujos Exitosos', f'{kpis["successful_flows"]}/{kpis["total_flows"]}', 
         f'{kpis["success_rate"]:.1f}%'],
        ['Paquetes Perdidos', f'{kpis["total_lost_packets"]:,}', ''],
        ['Eficiencia de Red', f'{kpis["network_efficiency"]:.2f}', ''],
        ['Rendimiento Global', kpis["performance_grade"], '']
    ]
    
    table = ax.table(cellText=kpi_data, cellLoc='left', loc='center',
                     colWidths=[0.4, 0.3, 0.3])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)
    
    # Estilo de la tabla
    for i in range(len(kpi_data)):
        if i == 0:
            for j in range(3):
                table[(i, j)].set_facecolor('#4472C4')
                table[(i, j)].set_text_props(weight='bold', color='white')
        else:
            for j in range(3):
                table[(i, j)].set_facecolor('#E7E6E6' if i % 2 == 0 else 'white')
    
    ax.set_title('Resumen de KPIs', fontweight='bold', pad=20)
    
    plt.tight_layout()
    plot_path = plots_dir / "dashboard_metricas.png"
    plt.savefig(plot_path, dpi=PLOT_DPI, bbox_inches='tight')
    plt.close()
    plots.append(str(plot_path))
    
    # 2. Gráfico de dispersión: PDR vs Delay
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['avg_delay_ms'], df['pdr'], 
                         c=df['throughput_mbps'], cmap='viridis',
                         s=100, alpha=0.6, edgecolors='black', linewidth=0.5)
    plt.colorbar(scatter, label='Throughput (Mbps)')
    plt.xlabel('Delay Promedio (ms)', fontweight='bold', fontsize=12)
    plt.ylabel('PDR (%)', fontweight='bold', fontsize=12)
    plt.title('Relación entre PDR, Delay y Throughput', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)
    
    # Añadir líneas de referencia
    plt.axhline(y=kpis['avg_pdr'], color='red', linestyle='--', alpha=0.5, label='PDR promedio')
    plt.axvline(x=kpis['avg_delay'], color='blue', linestyle='--', alpha=0.5, label='Delay promedio')
    plt.legend()
    
    plt.tight_layout()
    plot_path = plots_dir / "scatter_pdr_delay.png"
    plt.savefig(plot_path, dpi=PLOT_DPI, bbox_inches='tight')
    plt.close()
    plots.append(str(plot_path))
    
    # 3. Box plots comparativos
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Distribuciones de Métricas (Box Plots)', fontsize=14, fontweight='bold')
    
    # PDR
    bp1 = axes[0].boxplot([df['pdr']], labels=['PDR'], patch_artist=True)
    bp1['boxes'][0].set_facecolor('steelblue')
    axes[0].set_ylabel('PDR (%)', fontweight='bold')
    axes[0].grid(True, alpha=0.3, axis='y')
    axes[0].set_title(f'μ = {kpis["avg_pdr"]:.2f}%')
    
    # Delay
    bp2 = axes[1].boxplot([df['avg_delay_ms']], labels=['Delay'], patch_artist=True)
    bp2['boxes'][0].set_facecolor('coral')
    axes[1].set_ylabel('Delay (ms)', fontweight='bold')
    axes[1].grid(True, alpha=0.3, axis='y')
    axes[1].set_title(f'μ = {kpis["avg_delay"]:.2f} ms')
    
    # Throughput
    bp3 = axes[2].boxplot([df['throughput_mbps']], labels=['Throughput'], patch_artist=True)
    bp3['boxes'][0].set_facecolor('green')
    axes[2].set_ylabel('Throughput (Mbps)', fontweight='bold')
    axes[2].grid(True, alpha=0.3, axis='y')
    axes[2].set_title(f'μ = {kpis["avg_throughput"]:.3f} Mbps')
    
    plt.tight_layout()
    plot_path = plots_dir / "boxplots_metricas.png"
    plt.savefig(plot_path, dpi=PLOT_DPI, bbox_inches='tight')
    plt.close()
    plots.append(str(plot_path))
    
    # 4. Gráfico de barras: Top 10 y Bottom 10 flujos por PDR
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Mejores y Peores Flujos por PDR', fontsize=14, fontweight='bold')
    
    # Top 10
    top10 = df.nlargest(10, 'pdr')
    axes[0].barh(range(len(top10)), top10['pdr'], color='green', alpha=0.7)
    axes[0].set_yticks(range(len(top10)))
    axes[0].set_yticklabels([f'Flujo {i}' for i in top10.index])
    axes[0].set_xlabel('PDR (%)', fontweight='bold')
    axes[0].set_title('Top 10 Flujos (Mayor PDR)')
    axes[0].grid(True, alpha=0.3, axis='x')
    axes[0].invert_yaxis()
    
    # Bottom 10
    bottom10 = df.nsmallest(10, 'pdr')
    axes[1].barh(range(len(bottom10)), bottom10['pdr'], color='red', alpha=0.7)
    axes[1].set_yticks(range(len(bottom10)))
    axes[1].set_yticklabels([f'Flujo {i}' for i in bottom10.index])
    axes[1].set_xlabel('PDR (%)', fontweight='bold')
    axes[1].set_title('Bottom 10 Flujos (Menor PDR)')
    axes[1].grid(True, alpha=0.3, axis='x')
    axes[1].invert_yaxis()
    
    plt.tight_layout()
    plot_path = plots_dir / "top_bottom_flows.png"
    plt.savefig(plot_path, dpi=PLOT_DPI, bbox_inches='tight')
    plt.close()
    plots.append(str(plot_path))
    
    return plots


def get_pdr_grade(pdr: float) -> str:
    """Clasifica PDR"""
    if pdr >= 95:
        return "Excelente"
    elif pdr >= 85:
        return "Bueno"
    elif pdr >= 70:
        return "Regular"
    else:
        return "Pobre"


def get_delay_grade(delay: float) -> str:
    """Clasifica Delay"""
    if delay <= 50:
        return "Excelente"
    elif delay <= 100:
        return "Bueno"
    elif delay <= 200:
        return "Regular"
    else:
        return "Pobre"


def visualizer_node(state: AgentState) -> Dict:
    """Nodo del agente visualizador para LangGraph"""
    print("\n" + "="*80)
    print("📊 AGENTE VISUALIZADOR ACTIVADO")
    print("="*80)
    
    analysis_results = state.get('analysis_results', {})
    
    if not analysis_results:
        print("⚠️  No hay resultados de análisis para visualizar")
        return {
            'messages': ['No hay datos para visualizar'],
            **add_audit_entry(state, "visualizer", "no_data", {})
        }
    
    try:
        # Reconstruir DataFrame
        df_dict = analysis_results.get('dataframe', {})
        df = pd.DataFrame(df_dict)
        kpis = analysis_results.get('kpis', {})
        
        if df.empty:
            print("⚠️  DataFrame vacío")
            return {
                'messages': ['DataFrame vacío, no se pueden generar gráficos'],
                **add_audit_entry(state, "visualizer", "empty_dataframe", {})
            }
        
        print(f"📈 Generando gráficos para {len(df)} flujos...")
        
        # Crear gráficos
        plots = create_plots(df, kpis)
        
        print(f"✅ Generados {len(plots)} gráficos:")
        for plot in plots:
            print(f"   📊 {Path(plot).name}")
        
        return {
            'plots_generated': plots,
            **add_audit_entry(state, "visualizer", "plots_generated", {
                'count': len(plots),
                'plots': [str(Path(p).name) for p in plots]
            })
        }
        
    except Exception as e:
        print(f"❌ Error generando gráficos: {e}")
        return {
            'errors': [f'Error en visualización: {str(e)}'],
            **add_audit_entry(state, "visualizer", "visualization_error", {
                'error': str(e)
            })
        }


if __name__ == "__main__":
    print("Agente Visualizador - Prueba")
    print("Requiere datos de análisis para probar")
