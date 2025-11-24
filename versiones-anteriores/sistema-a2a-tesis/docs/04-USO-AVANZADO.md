# 🚀 Guía de Uso Avanzado - Sistema A2A

## Características Avanzadas

Esta guía cubre características avanzadas para usuarios experimentados.

---

## Tabla de Contenidos

1. [Ejecución Paralela](#ejecución-paralela)
2. [Barrido de Parámetros](#barrido-de-parámetros)
3. [Integración con Google Colab](#integración-con-google-colab)
4. [Personalización de Agentes](#personalización-de-agentes)
5. [Análisis Estadístico Avanzado](#análisis-estadístico-avanzado)
6. [Exportación de Resultados](#exportación-de-resultados)
7. [Automatización con Scripts](#automatización-con-scripts)
8. [Integración con Git](#integración-con-git)

---

## Ejecución Paralela

### Ejecutar Múltiples Tareas

Para ejecutar varias tareas en paralelo (requiere recursos suficientes):

```bash
# Terminal 1
python main.py --task "Simular AODV con 25 nodos" &

# Terminal 2
python main.py --task "Simular AODV con 50 nodos" &

# Terminal 3
python main.py --task "Simular AODV con 100 nodos" &

# Esperar a que terminen
wait
```

### Script de Ejecución Paralela

Crear `run_parallel.sh`:

```bash
#!/bin/bash

# Lista de tareas
tasks=(
    "Simular AODV con 25 nodos"
    "Simular AODV con 50 nodos"
    "Simular AODV con 100 nodos"
)

# Ejecutar en paralelo
for task in "${tasks[@]}"; do
    python main.py --task "$task" &
done

# Esperar a que terminen todas
wait

echo "✓ Todas las tareas completadas"
```

**Uso**:
```bash
chmod +x run_parallel.sh
./run_parallel.sh
```

---

## Barrido de Parámetros

### Script de Barrido

Crear `scripts/parameter_sweep.py`:

```python
#!/usr/bin/env python3
"""
Script para barrido de parámetros
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from supervisor import SupervisorOrchestrator
import pandas as pd

def parameter_sweep(base_task, parameter_name, values):
    """
    Ejecuta barrido de parámetros
    
    Args:
        base_task: Tarea base
        parameter_name: Nombre del parámetro
        values: Lista de valores a probar
    """
    supervisor = SupervisorOrchestrator()
    results = []
    
    for value in values:
        print(f"\n{'='*80}")
        print(f"Ejecutando con {parameter_name}={value}")
        print(f"{'='*80}\n")
        
        # Construir tarea
        task = f"{base_task} con {parameter_name}={value}"
        
        # Ejecutar
        result = supervisor.run_experiment(task, max_iterations=3)
        
        if result and result.get('metrics'):
            # Guardar resultados
            row = {parameter_name: value}
            row.update(result['metrics'])
            results.append(row)
    
    # Crear DataFrame
    df = pd.DataFrame(results)
    
    # Guardar resultados
    output_file = f"barrido_{parameter_name}.csv"
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Resultados guardados en: {output_file}")
    print(df)
    
    return df

if __name__ == "__main__":
    # Ejemplo: Barrido de número de nodos
    parameter_sweep(
        base_task="Evaluar AODV en red vehicular",
        parameter_name="num_nodos",
        values=[25, 50, 75, 100]
    )
```

**Uso**:
```bash
python scripts/parameter_sweep.py
```

---

## Integración con Google Colab

### Configurar Ollama en Colab

Crear notebook `colab_setup.ipynb`:

```python
# Celda 1: Instalar Ollama
!curl -fsSL https://ollama.com/install.sh | sh

# Celda 2: Iniciar Ollama en background
import subprocess
import time

ollama_process = subprocess.Popen(
    ["ollama", "serve"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
time.sleep(5)
print("✓ Ollama iniciado")

# Celda 3: Descargar modelos
!ollama pull llama3.1:8b
!ollama pull deepseek-coder-v2:16b

# Celda 4: Instalar ngrok para acceso remoto
!pip install pyngrok
from pyngrok import ngrok

# Exponer Ollama
public_url = ngrok.connect(11434)
print(f"Ollama URL: {public_url}")

# Celda 5: Clonar proyecto
!git clone https://github.com/tu-usuario/sistema-a2a-tesis.git
%cd sistema-a2a-tesis

# Celda 6: Instalar dependencias
!pip install -r requirements.txt

# Celda 7: Configurar para usar Ollama remoto
# Editar config/settings.py con la URL de ngrok
with open('config/settings.py', 'r') as f:
    content = f.read()

content = content.replace(
    'OLLAMA_BASE_URL = "http://localhost:11434"',
    f'OLLAMA_BASE_URL = "{public_url}"'
)

with open('config/settings.py', 'w') as f:
    f.write(content)

# Celda 8: Ejecutar tarea
!python main.py --task "Simular AODV con 20 nodos"
```

### Usar Colab desde Local

```python
# En config/settings.py local
OLLAMA_BASE_URL = "https://abc123.ngrok.io"  # URL de Colab
```

---

## Personalización de Agentes

### Crear Agente Personalizado

Crear `agents/custom_agent.py`:

```python
"""
Agente Personalizado
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
from utils.state import AgentState, add_audit_entry

def custom_node(state: AgentState) -> Dict:
    """
    Nodo personalizado para LangGraph
    
    Args:
        state: Estado actual
        
    Returns:
        Actualizaciones al estado
    """
    print("\n" + "="*80)
    print("🔧 AGENTE PERSONALIZADO ACTIVADO")
    print("="*80)
    
    # Tu lógica aquí
    task = state['task']
    
    # Ejemplo: Procesamiento personalizado
    result = f"Procesado: {task}"
    
    return {
        'messages': [result],
        **add_audit_entry(state, "custom", "custom_action", {
            'task': task
        })
    }

if __name__ == "__main__":
    from utils.state import create_initial_state
    
    test_state = create_initial_state("Tarea de prueba")
    result = custom_node(test_state)
    print(result)
```

### Integrar en el Supervisor

```python
# En supervisor.py

from agents.custom_agent import custom_node

# Añadir nodo
self.workflow.add_node("custom", custom_node)

# Añadir al flujo
self.workflow.add_edge("analyst", "custom")
self.workflow.add_edge("custom", "visualizer")
```

---

## Análisis Estadístico Avanzado

### Agente de Análisis Estadístico

Crear `agents/statistical_evaluator.py`:

```python
"""
Agente de Evaluación Estadística Avanzada
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

from utils.state import AgentState, add_audit_entry
from config.settings import SIMULATIONS_DIR

def statistical_evaluator_node(state: AgentState) -> Dict:
    """
    Realiza análisis estadístico avanzado
    """
    print("\n" + "="*80)
    print("📊 AGENTE EVALUADOR ESTADÍSTICO ACTIVADO")
    print("="*80)
    
    analysis_results = state.get('analysis_results', {})
    df_dict = analysis_results.get('dataframe', {})
    df = pd.DataFrame(df_dict)
    
    if df.empty:
        return {'errors': ['No hay datos para análisis estadístico']}
    
    results = {}
    
    # Test de normalidad (Shapiro-Wilk)
    for metric in ['pdr', 'avg_delay_ms', 'throughput_mbps']:
        if metric in df.columns:
            stat, p_value = stats.shapiro(df[metric])
            results[f'{metric}_normality'] = {
                'statistic': stat,
                'p_value': p_value,
                'is_normal': p_value > 0.05
            }
    
    # Estadísticas descriptivas
    results['descriptive'] = df.describe().to_dict()
    
    # Correlaciones
    if len(df.columns) > 1:
        results['correlations'] = df.corr().to_dict()
    
    # Generar gráficos adicionales
    plots_dir = SIMULATIONS_DIR / "plots"
    
    # Q-Q plot para normalidad
    for metric in ['pdr', 'avg_delay_ms']:
        if metric in df.columns:
            plt.figure()
            stats.probplot(df[metric], dist="norm", plot=plt)
            plt.title(f'Q-Q Plot: {metric}')
            plot_path = plots_dir / f"qq_plot_{metric}.png"
            plt.savefig(plot_path, dpi=300)
            plt.close()
    
    print("✓ Análisis estadístico completado")
    
    return {
        'statistical_results': results,
        **add_audit_entry(state, "statistical_evaluator", "analysis_completed", {
            'tests_performed': len(results)
        })
    }
```

---

## Exportación de Resultados

### Exportar a Diferentes Formatos

Crear `scripts/export_results.py`:

```python
#!/usr/bin/env python3
"""
Script para exportar resultados a diferentes formatos
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import json
import xml.etree.ElementTree as ET

def export_to_csv(xml_file, output_file):
    """Exporta XML a CSV"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    data = []
    for flow in root.findall('.//Flow'):
        data.append({
            'flow_id': flow.get('flowId'),
            'tx_packets': flow.get('txPackets'),
            'rx_packets': flow.get('rxPackets'),
            'tx_bytes': flow.get('txBytes'),
            'rx_bytes': flow.get('rxBytes')
        })
    
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"✓ Exportado a CSV: {output_file}")

def export_to_json(xml_file, output_file):
    """Exporta XML a JSON"""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    data = []
    for flow in root.findall('.//Flow'):
        data.append({
            'flow_id': flow.get('flowId'),
            'tx_packets': int(flow.get('txPackets', 0)),
            'rx_packets': int(flow.get('rxPackets', 0))
        })
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Exportado a JSON: {output_file}")

def export_to_latex(csv_file, output_file):
    """Exporta CSV a tabla LaTeX"""
    df = pd.read_csv(csv_file)
    
    latex = df.to_latex(index=False, caption="Resultados de Simulación")
    
    with open(output_file, 'w') as f:
        f.write(latex)
    
    print(f"✓ Exportado a LaTeX: {output_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, help='Archivo de entrada')
    parser.add_argument('--format', required=True, choices=['csv', 'json', 'latex'])
    parser.add_argument('--output', required=True, help='Archivo de salida')
    
    args = parser.parse_args()
    
    if args.format == 'csv':
        export_to_csv(args.input, args.output)
    elif args.format == 'json':
        export_to_json(args.input, args.output)
    elif args.format == 'latex':
        export_to_latex(args.input, args.output)
```

**Uso**:
```bash
# XML a CSV
python scripts/export_results.py \
  --input simulations/results/sim_20241123.xml \
  --format csv \
  --output resultados.csv

# CSV a LaTeX
python scripts/export_results.py \
  --input resultados.csv \
  --format latex \
  --output tabla.tex
```

---

## Automatización con Scripts

### Cron Job para Ejecución Automática

```bash
# Editar crontab
crontab -e

# Añadir línea para ejecutar diariamente a las 2 AM
0 2 * * * cd /ruta/a/sistema-a2a-tesis && source venv/bin/activate && python main.py --task "Tarea diaria" >> logs/cron.log 2>&1
```

### Script de Backup Automático

Crear `scripts/backup_results.sh`:

```bash
#!/bin/bash

# Configuración
BACKUP_DIR="$HOME/backups/a2a"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Crear directorio de backup
mkdir -p "$BACKUP_DIR"

# Backup de resultados
tar -czf "$BACKUP_DIR/results_$DATE.tar.gz" \
  -C "$PROJECT_DIR" \
  simulations/results \
  simulations/plots \
  logs

echo "✓ Backup creado: $BACKUP_DIR/results_$DATE.tar.gz"

# Limpiar backups antiguos (más de 30 días)
find "$BACKUP_DIR" -name "results_*.tar.gz" -mtime +30 -delete

echo "✓ Backups antiguos eliminados"
```

**Uso**:
```bash
chmod +x scripts/backup_results.sh
./scripts/backup_results.sh
```

---

## Integración con Git

### Configurar Git para el Proyecto

```bash
# Inicializar repositorio
git init

# Añadir archivos
git add .

# Commit inicial
git commit -m "Sistema A2A inicial"

# Conectar con repositorio remoto
git remote add origin https://github.com/tu-usuario/sistema-a2a-tesis.git
git push -u origin main
```

### Git Hooks para Automatización

Crear `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Ejecutar verificación antes de commit
python scripts/check_system.py

if [ $? -ne 0 ]; then
    echo "❌ Verificación falló. Commit cancelado."
    exit 1
fi

echo "✓ Verificación exitosa"
```

```bash
chmod +x .git/hooks/pre-commit
```

---

## Monitoreo Avanzado

### Dashboard en Tiempo Real

Crear `scripts/dashboard.py`:

```python
#!/usr/bin/env python3
"""
Dashboard simple para monitoreo
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import sqlite3
from rich.console import Console
from rich.table import Table
from rich.live import Live

console = Console()

def get_recent_experiments():
    """Obtiene experimentos recientes"""
    db_path = Path("logs/langgraph_checkpoints.db")
    
    if not db_path.exists():
        return []
    
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT thread_id, checkpoint_id 
            FROM checkpoints 
            ORDER BY checkpoint_id DESC 
            LIMIT 10
        """)
        return cursor.fetchall()
    except:
        return []
    finally:
        conn.close()

def create_table():
    """Crea tabla de monitoreo"""
    table = Table(title="Sistema A2A - Monitoreo")
    
    table.add_column("Thread ID", style="cyan")
    table.add_column("Checkpoint", style="magenta")
    table.add_column("Estado", style="green")
    
    experiments = get_recent_experiments()
    
    for thread_id, checkpoint_id in experiments:
        table.add_row(
            thread_id[:8] + "...",
            str(checkpoint_id),
            "✓ Completado"
        )
    
    return table

def main():
    """Función principal"""
    with Live(create_table(), refresh_per_second=1) as live:
        while True:
            time.sleep(5)
            live.update(create_table())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Dashboard detenido[/yellow]")
```

**Uso**:
```bash
python scripts/dashboard.py
```

---

## Optimización de Rendimiento

### Caché de Resultados

```python
# En agents/researcher.py

import pickle
from pathlib import Path

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(exist_ok=True)

def search_with_cache(query):
    """Búsqueda con caché"""
    cache_file = CACHE_DIR / f"{hash(query)}.pkl"
    
    # Verificar caché
    if cache_file.exists():
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    
    # Buscar
    results = search_semantic_scholar(query)
    
    # Guardar en caché
    with open(cache_file, 'wb') as f:
        pickle.dump(results, f)
    
    return results
```

---

## Próximos Pasos

Para características aún más avanzadas:

1. Implementar interfaz web con Streamlit
2. Añadir notificaciones por email/Telegram
3. Integrar con sistemas de CI/CD
4. Crear API REST para el sistema

---

**¿Necesitas más personalización?** El código está diseñado para ser extensible. Revisa los agentes existentes como ejemplos.
