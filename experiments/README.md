# 🧪 Framework de Experimentación - Sistema A2A

Framework completo para ejecutar experimentos científicos reproducibles y generar análisis estadístico riguroso para publicación.

---

## 📋 Contenido

- [Estructura](#estructura)
- [Uso Rápido](#uso-rápido)
- [Configuración de Experimentos](#configuración-de-experimentos)
- [Análisis Estadístico](#análisis-estadístico)
- [Resultados](#resultados)

---

## 📁 Estructura

```
experiments/
├── experiment_runner.py       # Ejecutor de experimentos
├── statistical_analyzer.py    # Analizador estadístico
├── configs/                   # Configuraciones de experimentos
│   ├── comparison.yaml        # Comparación de protocolos
│   ├── scalability.yaml       # Análisis de escalabilidad
│   └── mobility.yaml          # Impacto de movilidad
├── results/                   # Resultados de experimentos
│   └── [experiment_name]/
│       ├── results.csv        # Datos crudos
│       ├── results.json       # Datos en JSON
│       ├── analysis.csv       # Análisis agregado
│       ├── REPORT.md          # Reporte en Markdown
│       └── analysis/          # Análisis estadístico
│           ├── descriptive_statistics.csv
│           ├── protocol_comparison.json
│           ├── *.png          # Gráficos
│           └── results_table.tex  # Tabla LaTeX
└── README.md                  # Este archivo
```

---

## 🚀 Uso Rápido

### 1. Ejecutar Experimento de Comparación

```bash
# Comparar AODV, OLSR y DSDV
python experiments/experiment_runner.py --config experiments/configs/comparison.yaml
```

**Resultado:**
- 3 escenarios × 5 repeticiones = 15 simulaciones
- Tiempo estimado: 2-3 horas
- Resultados en: `experiments/results/protocol_comparison/`

### 2. Ejecutar Análisis de Escalabilidad

```bash
# Evaluar AODV con 10, 20, 30, 40, 50 nodos
python experiments/experiment_runner.py --config experiments/configs/scalability.yaml
```

**Resultado:**
- 5 escenarios × 5 repeticiones = 25 simulaciones
- Tiempo estimado: 4-5 horas
- Resultados en: `experiments/results/scalability_analysis/`

### 3. Analizar Resultados

```bash
# Análisis estadístico completo
python experiments/statistical_analyzer.py experiments/results/protocol_comparison/results.csv
```

**Genera:**
- Estadísticas descriptivas
- Tests estadísticos (T-test, ANOVA)
- Gráficos para publicación (PNG, 300 DPI)
- Tabla LaTeX para paper

---

## ⚙️ Configuración de Experimentos

### Formato YAML

```yaml
experiment:
  name: "mi_experimento"
  description: "Descripción del experimento"
  repetitions: 5  # Repeticiones por escenario
  max_iterations: 5  # Máximo de reintentos

scenarios:
  - name: "escenario_1"
    protocol: "AODV"
    nodes: 20
    area: 1000
    duration: 200
    mobility: "RandomWaypoint"
    speed: "5-15"
    base_seed: 10000

metrics:
  - pdr
  - delay
  - throughput
  - overhead

analysis:
  confidence_level: 0.95
  tests:
    - t_test
    - anova
```

### Parámetros de Escenario

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `name` | Nombre del escenario | "AODV_20nodes" |
| `protocol` | Protocolo de enrutamiento | "AODV", "OLSR", "DSDV" |
| `nodes` | Número de nodos | 10, 20, 50 |
| `area` | Área de simulación (m) | 500, 1000, 2000 |
| `duration` | Duración (segundos) | 100, 200, 300 |
| `mobility` | Modelo de movilidad | "RandomWaypoint" |
| `speed` | Rango de velocidad (m/s) | "5-15", "1-5" |
| `base_seed` | Semilla base | 10000, 20000 |

---

## 📊 Análisis Estadístico

### Estadísticas Calculadas

**Por cada métrica:**
- Media (mean)
- Desviación estándar (std)
- Mínimo y máximo
- Mediana
- Intervalo de confianza 95%

**Tests estadísticos:**
- T-test (comparación de pares)
- ANOVA (comparación múltiple)
- Correlación
- Regresión lineal

### Gráficos Generados

1. **Boxplots** - Distribución de métricas por protocolo
2. **Barplots con CI** - Comparación con intervalos de confianza
3. **Resumen múltiple** - 4 métricas en un gráfico

**Formato:** PNG, 300 DPI (listo para publicación)

### Tabla LaTeX

Genera tabla formateada para incluir directamente en paper:

```latex
\begin{table}[htbp]
\centering
\caption{Resultados de Simulación por Protocolo}
\label{tab:results}
\begin{tabular}{lcccc}
\hline
Protocolo & PDR (\%) & Delay (ms) & Throughput (Mbps) & n \\
\hline
AODV & 95.50 $\pm$ 2.30 & 45.20 $\pm$ 3.10 & 1.85 $\pm$ 0.15 & 5 \\
OLSR & 92.10 $\pm$ 3.50 & 52.70 $\pm$ 4.20 & 1.92 $\pm$ 0.18 & 5 \\
\hline
\end{tabular}
\end{table}
```

---

## 📈 Resultados

### Estructura de Resultados

```
experiments/results/protocol_comparison/
├── results.csv                 # Datos crudos (todas las simulaciones)
├── results.json                # Datos en JSON
├── analysis.csv                # Estadísticas agregadas por escenario
├── REPORT.md                   # Reporte legible
└── analysis/                   # Análisis estadístico
    ├── descriptive_statistics.csv
    ├── protocol_comparison.json
    ├── pdr_by_protocol.png
    ├── delay_by_protocol.png
    ├── throughput_by_protocol.png
    ├── comparison_summary.png
    └── results_table.tex
```

### Formato de results.csv

```csv
experiment,scenario,repetition,seed,protocol,nodes,area,duration,avg_pdr,avg_delay,avg_throughput,routing_overhead
protocol_comparison,AODV_20nodes,1,10001,AODV,20,1000,200,95.5,45.2,1.85,0.123
protocol_comparison,AODV_20nodes,2,10002,AODV,20,1000,200,94.8,46.1,1.82,0.125
...
```

### Formato de REPORT.md

```markdown
# Reporte de Experimento: protocol_comparison

**Fecha:** 2025-11-25 15:30:00

## Configuración
- **Escenarios:** 3
- **Repeticiones:** 5
- **Total simulaciones:** 15

## Resultados

### Resumen por Escenario
| scenario | protocol | pdr_mean | pdr_std | delay_mean | delay_std |
|----------|----------|----------|---------|------------|-----------|
| AODV_20nodes | AODV | 95.50 | 2.30 | 45.20 | 3.10 |
| OLSR_20nodes | OLSR | 92.10 | 3.50 | 52.70 | 4.20 |

## Interpretación
- **Mejor PDR:** AODV (95.50% ± 2.30%)
- **Menor latencia:** AODV (45.20 ms ± 3.10 ms)
```

---

## 🎓 Para Tu Tesis

### Checklist de Validación Experimental

- [ ] Ejecutar experimento de comparación (3 protocolos)
- [ ] Ejecutar experimento de escalabilidad (5 tamaños)
- [ ] Ejecutar experimento de movilidad (4 velocidades)
- [ ] Generar análisis estadístico completo
- [ ] Verificar intervalos de confianza < 5%
- [ ] Comparar con resultados de literatura
- [ ] Generar gráficos para paper
- [ ] Generar tablas LaTeX
- [ ] Documentar configuraciones
- [ ] Archivar datos crudos

### Recomendaciones

1. **Repeticiones:** Mínimo 5, ideal 10-30
2. **Semillas:** Usar semillas diferentes para cada repetición
3. **Duración:** Mínimo 200 segundos para estabilidad
4. **Área:** Ajustar según densidad deseada
5. **Comparación:** Incluir al menos 3 protocolos
6. **Validación:** Comparar con papers de referencia

---

## 🐛 Troubleshooting

### Error: "No module named 'yaml'"

```bash
pip install pyyaml
```

### Error: "No module named 'tqdm'"

```bash
pip install tqdm
```

### Simulaciones muy lentas

- Reducir `duration` a 100 segundos
- Reducir número de `nodes`
- Reducir `repetitions` a 3

### Resultados inconsistentes

- Verificar que `base_seed` sea diferente para cada escenario
- Aumentar número de `repetitions`
- Verificar que NS-3 esté instalado correctamente

---

## 📚 Referencias

### Papers Relevantes

1. Perkins et al. (2003) - "Ad hoc On-Demand Distance Vector (AODV) Routing"
2. Clausen & Jacquet (2003) - "Optimized Link State Routing Protocol (OLSR)"
3. Perkins & Bhagwat (1994) - "Highly Dynamic Destination-Sequenced Distance-Vector Routing (DSDV)"

### Métricas Típicas en Literatura

| Protocolo | PDR | Delay | Overhead |
|-----------|-----|-------|----------|
| AODV | 85-95% | 40-80 ms | 10-20% |
| OLSR | 80-92% | 50-100 ms | 30-40% |
| DSDV | 75-88% | 60-120 ms | 40-50% |

---

## ✅ Ejemplo Completo

```bash
# 1. Ejecutar experimento
python experiments/experiment_runner.py --config experiments/configs/comparison.yaml

# 2. Esperar a que termine (2-3 horas)

# 3. Analizar resultados
python experiments/statistical_analyzer.py experiments/results/protocol_comparison/results.csv

# 4. Revisar resultados
cat experiments/results/protocol_comparison/REPORT.md

# 5. Ver gráficos
open experiments/results/protocol_comparison/analysis/*.png

# 6. Copiar tabla LaTeX para paper
cat experiments/results/protocol_comparison/analysis/results_table.tex
```

---

**Autor:** Sistema A2A Team  
**Versión:** 1.0  
**Fecha:** Noviembre 2025
