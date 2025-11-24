# 🚀 Guía de Uso - Nuevas Funcionalidades v1.3

## Sistema A2A para Tesis Doctoral

---

## 📋 Índice

1. [Reproducibilidad con Semillas](#1-reproducibilidad-con-semillas)
2. [Captura y Análisis de Trazas PCAP](#2-captura-y-análisis-de-trazas-pcap)
3. [Overhead de Enrutamiento](#3-overhead-de-enrutamiento)
4. [Tests Estadísticos](#4-tests-estadísticos)
5. [Intervalos de Confianza](#5-intervalos-de-confianza)
6. [Reportes Automáticos](#6-reportes-automáticos)
7. [Ejemplos Prácticos](#7-ejemplos-prácticos)

---

## 1. Reproducibilidad con Semillas

### ¿Qué es?
Control total sobre la aleatoriedad de las simulaciones para garantizar resultados reproducibles.

### ¿Cómo funciona?
El sistema configura automáticamente la semilla aleatoria en NS-3 antes de crear nodos.

### Uso Básico

```python
# El sistema genera automáticamente código con semilla
# No necesitas hacer nada especial

# Ejemplo de código generado:
ns.core.RngSeedManager.SetSeed(12345)
ns.core.RngSeedManager.SetRun(1)
```

### Uso Avanzado: Múltiples Semillas

Para validación estadística robusta, ejecuta la misma simulación con diferentes semillas:

```python
# Crear script personalizado
seeds = [12345, 23456, 34567, 45678, 56789]

for seed in seeds:
    print(f"Ejecutando con semilla: {seed}")
    # Modificar el código generado para usar esta semilla
    # O pasar como parámetro al sistema
```

### Verificar Reproducibilidad

```bash
# Ejecutar simulación 1
python main.py

# Guardar resultados
copy simulations\results\sim_*.xml resultados_run1.xml

# Ejecutar simulación 2 (con misma semilla)
python main.py

# Comparar resultados (deben ser idénticos)
fc resultados_run1.xml simulations\results\sim_*.xml
```

### Beneficios
- ✅ Resultados 100% reproducibles
- ✅ Validación por pares
- ✅ Debugging más fácil
- ✅ Cumple estándares científicos

---

## 2. Captura y Análisis de Trazas PCAP

### ¿Qué es?
Captura de todos los paquetes transmitidos durante la simulación para análisis detallado.

### ¿Cómo funciona?
El sistema habilita automáticamente la captura PCAP en el código generado.

### Archivos Generados

```
simulations/results/
├── simulacion-0-0_20251124_143022.pcap  # Nodo 0, interfaz 0
├── simulacion-0-1_20251124_143022.pcap  # Nodo 0, interfaz 1
├── simulacion-1-0_20251124_143022.pcap  # Nodo 1, interfaz 0
└── ...
```

### Análisis Automático

El agente **Trace Analyzer** analiza automáticamente los archivos PCAP y genera:

- Estadísticas básicas (paquetes, bytes, duración)
- Distribución por protocolo (IP, UDP, TCP, ICMP, etc.)
- Detección de protocolos de enrutamiento (AODV, OLSR, DSDV, DSR)
- Cálculo de overhead de enrutamiento
- Análisis de latencias

### Análisis Manual con Wireshark

```bash
# Abrir archivo PCAP en Wireshark
wireshark simulations\results\simulacion-0-0_*.pcap

# Filtros útiles:
# - Paquetes AODV: aodv
# - Paquetes UDP: udp
# - Paquetes de un nodo específico: ip.src == 10.1.1.1
```

### Análisis Manual con Scapy

```python
from scapy.all import rdpcap, IP, UDP

# Leer archivo PCAP
packets = rdpcap('simulations/results/simulacion-0-0_*.pcap')

# Analizar paquetes
for pkt in packets:
    if IP in pkt:
        print(f"IP: {pkt[IP].src} → {pkt[IP].dst}")
        if UDP in pkt:
            print(f"  UDP: {pkt[UDP].sport} → {pkt[UDP].dport}")
```

### Beneficios
- ✅ Análisis a nivel de paquetes
- ✅ Detección de problemas de red
- ✅ Validación de protocolos
- ✅ Análisis forense de tráfico

---

## 3. Overhead de Enrutamiento

### ¿Qué es?
Ratio entre bytes de control (enrutamiento) y bytes de datos.

```
Overhead = Bytes_Control / Bytes_Datos
```

### ¿Cómo se calcula?

#### Método 1: Desde PCAP (Preciso)
El Trace Analyzer analiza los archivos PCAP y cuenta:
- Bytes de paquetes de enrutamiento (AODV, OLSR, etc.)
- Bytes de paquetes de datos (UDP, TCP)

#### Método 2: Estimación (Fallback)
Si no hay PCAP, se estima basándose en literatura:
- AODV: ~15%
- OLSR: ~35%
- DSDV: ~45%
- DSR: ~20%

### Interpretación

```
Overhead < 20%  → Excelente (protocolo eficiente)
Overhead 20-30% → Bueno (aceptable)
Overhead 30-40% → Regular (protocolo proactivo)
Overhead > 40%  → Alto (considerar optimización)
```

### Ejemplo de Salida

```
📡 Calculando overhead de enrutamiento...
  📊 Overhead calculado desde PCAP: 0.152 (15.2%)
  ✓ Overhead: 0.152 (15.2%)
```

### Uso en Tesis

```markdown
## Resultados

El protocolo AODV presentó un overhead de enrutamiento de 15.2%,
calculado a partir del análisis de trazas PCAP. Este valor es
consistente con la literatura [1], que reporta overheads entre
10-20% para AODV en redes MANET.

[1] Perkins et al., "Ad hoc On-Demand Distance Vector Routing", 2003
```

---

## 4. Tests Estadísticos

### ¿Qué son?
Pruebas para determinar si las diferencias observadas son estadísticamente significativas.

### Tests Disponibles

#### T-Test (Dos Muestras)
Compara dos grupos para ver si sus medias son diferentes.

**Ejemplo**: Comparar PDR de flujos exitosos vs fallidos

```python
# El sistema ejecuta automáticamente:
t_test_result = t_test_two_samples(
    successful_flows['pdr'].values,
    failed_flows['pdr'].values
)

# Resultado:
{
    't_statistic': 5.234,
    'p_value': 0.0001,
    'significant': True,
    'interpretation': 'Diferencia estadísticamente significativa (p < 0.05)'
}
```

#### ANOVA (Múltiples Grupos)
Compara tres o más grupos.

**Ejemplo**: Comparar PDR entre diferentes protocolos

### Interpretación de p-value

```
p < 0.001  → Altamente significativo (***)
p < 0.01   → Muy significativo (**)
p < 0.05   → Significativo (*)
p ≥ 0.05   → No significativo (ns)
```

### Uso en Tesis

```markdown
## Análisis Estadístico

Se realizó un t-test para comparar el PDR entre flujos exitosos
y fallidos. Los resultados muestran una diferencia estadísticamente
significativa (t = 5.234, p < 0.001), indicando que los flujos
exitosos tienen un PDR significativamente mayor.
```

---

## 5. Intervalos de Confianza

### ¿Qué son?
Rango de valores donde se espera que esté el valor real con cierta probabilidad (95%).

### Formato

```
Métrica: [Límite Inferior, Límite Superior]
```

### Ejemplo de Salida

```
📊 Calculando intervalos de confianza (95% CI)...
  ✓ Intervalos calculados para 3 métricas
     pdr: [94.234, 96.876]
     avg_delay_ms: [45.321, 52.789]
     throughput_mbps: [2.123, 2.567]
```

### Interpretación

```
PDR: [94.2%, 96.9%]
→ Estamos 95% seguros de que el PDR real está entre 94.2% y 96.9%
→ Rango estrecho = alta precisión
→ Rango amplio = baja precisión (necesita más datos)
```

### Uso en Tesis

```markdown
## Resultados

El PDR promedio fue de 95.5% (95% CI: [94.2%, 96.9%]), indicando
un rendimiento consistente y confiable del protocolo AODV en las
condiciones evaluadas.
```

---

## 6. Reportes Automáticos

### Reporte Estadístico

El sistema genera automáticamente un reporte en Markdown:

```
simulations/analysis/statistical_report_20251124_143022.md
```

### Contenido del Reporte

```markdown
# Reporte Estadístico - Simulación NS-3

## Fecha: 2025-11-24 14:30:22

## Tests Estadísticos

### T-Test: Flujos Exitosos vs Fallidos
- **Estadístico t**: 5.234
- **p-value**: 0.0001
- **Significativo**: Sí (p < 0.05)
- **Interpretación**: Diferencia estadísticamente significativa

## Intervalos de Confianza (95%)

| Métrica | Límite Inferior | Límite Superior | Rango |
|---------|----------------|-----------------|-------|
| PDR | 94.234% | 96.876% | 2.642% |
| Delay | 45.321 ms | 52.789 ms | 7.468 ms |
| Throughput | 2.123 Mbps | 2.567 Mbps | 0.444 Mbps |

## Conclusiones

Los resultados muestran un rendimiento consistente con intervalos
de confianza estrechos, indicando alta precisión en las mediciones.
```

### Uso del Reporte

1. **Copiar a tesis**: Incluir tablas y gráficos directamente
2. **Validación**: Verificar significancia estadística
3. **Comparación**: Comparar con otros experimentos

---

## 7. Ejemplos Prácticos

### Ejemplo 1: Simulación Básica con Todas las Funcionalidades

```bash
# 1. Ejecutar simulación
python main.py

# 2. Verificar archivos generados
dir simulations\results

# Deberías ver:
# - sim_*.xml (FlowMonitor)
# - simulacion-*.pcap (Capturas PCAP)
# - sim_*_stdout.txt (Logs)

# 3. Verificar análisis
dir simulations\analysis

# Deberías ver:
# - statistical_report_*.md (Reporte estadístico)

# 4. Abrir dashboard
start simulations\visualizations\dashboard.html
```

### Ejemplo 2: Comparar Dos Protocolos

```python
# Ejecutar simulación con AODV
# Modificar tarea: "Simular MANET con AODV, 20 nodos"
python main.py

# Guardar resultados
copy simulations\results\sim_*.xml resultados_aodv.xml
copy simulations\analysis\statistical_report_*.md reporte_aodv.md

# Ejecutar simulación con OLSR
# Modificar tarea: "Simular MANET con OLSR, 20 nodos"
python main.py

# Guardar resultados
copy simulations\results\sim_*.xml resultados_olsr.xml
copy simulations\analysis\statistical_report_*.md reporte_olsr.md

# Comparar reportes
fc reporte_aodv.md reporte_olsr.md
```

### Ejemplo 3: Validación Estadística con Múltiples Semillas

```python
# Script personalizado: run_multiple_seeds.py

seeds = [12345, 23456, 34567, 45678, 56789]
results = []

for seed in seeds:
    print(f"\n{'='*80}")
    print(f"Ejecutando con semilla: {seed}")
    print(f"{'='*80}\n")
    
    # Ejecutar simulación con esta semilla
    # (modificar código generado o pasar como parámetro)
    
    # Guardar resultados
    results.append({
        'seed': seed,
        'pdr': ...,  # Extraer de resultados
        'delay': ...,
        'throughput': ...
    })

# Calcular estadísticas agregadas
import pandas as pd
df = pd.DataFrame(results)

print("\n" + "="*80)
print("RESULTADOS AGREGADOS")
print("="*80)
print(f"PDR: {df['pdr'].mean():.2f}% ± {df['pdr'].std():.2f}%")
print(f"Delay: {df['delay'].mean():.2f} ms ± {df['delay'].std():.2f} ms")
print(f"Throughput: {df['throughput'].mean():.3f} Mbps ± {df['throughput'].std():.3f} Mbps")
```

### Ejemplo 4: Análisis Profundo de PCAP

```python
from scapy.all import rdpcap, IP, UDP
import pandas as pd

# Leer todos los archivos PCAP
pcap_files = list(Path('simulations/results').glob('simulacion-*.pcap'))

all_packets = []
for pcap_file in pcap_files:
    packets = rdpcap(str(pcap_file))
    
    for pkt in packets:
        if IP in pkt:
            all_packets.append({
                'time': float(pkt.time),
                'src': pkt[IP].src,
                'dst': pkt[IP].dst,
                'protocol': pkt[IP].proto,
                'size': len(pkt)
            })

# Crear DataFrame
df = pd.DataFrame(all_packets)

# Análisis
print(f"Total paquetes: {len(df)}")
print(f"Bytes totales: {df['size'].sum():,}")
print(f"\nDistribución por protocolo:")
print(df['protocol'].value_counts())

# Análisis temporal
df['time_relative'] = df['time'] - df['time'].min()
print(f"\nDuración: {df['time_relative'].max():.2f} segundos")
print(f"Tasa promedio: {len(df) / df['time_relative'].max():.2f} paquetes/segundo")
```

---

## 🎓 Checklist para Tesis Doctoral

### Antes de Ejecutar Simulaciones

- [ ] Verificar que NS-3 esté instalado correctamente
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Definir semillas para reproducibilidad
- [ ] Planificar número de repeticiones (mínimo 5)

### Durante las Simulaciones

- [ ] Verificar generación de archivos PCAP
- [ ] Monitorear logs de simulación
- [ ] Guardar resultados de cada ejecución

### Después de las Simulaciones

- [ ] Revisar reportes estadísticos generados
- [ ] Verificar intervalos de confianza (rangos estrechos = bueno)
- [ ] Validar significancia estadística (p < 0.05)
- [ ] Calcular overhead de enrutamiento
- [ ] Generar gráficos para tesis

### Para la Tesis

- [ ] Incluir tabla de resultados con intervalos de confianza
- [ ] Reportar tests estadísticos (t-test, ANOVA)
- [ ] Incluir gráficos de métricas clave
- [ ] Documentar overhead de enrutamiento
- [ ] Mencionar reproducibilidad (semillas usadas)

---

## 📚 Referencias

### Papers Relevantes

1. **AODV**: Perkins et al., "Ad hoc On-Demand Distance Vector Routing", RFC 3561, 2003
2. **OLSR**: Clausen et al., "Optimized Link State Routing Protocol", RFC 3626, 2003
3. **Statistical Analysis**: Montgomery, "Design and Analysis of Experiments", 2017

### Herramientas

- **NS-3**: https://www.nsnam.org/
- **Scapy**: https://scapy.net/
- **Wireshark**: https://www.wireshark.org/
- **SciPy**: https://scipy.org/

---

## 💡 Tips y Mejores Prácticas

### Reproducibilidad
- Siempre usar semillas fijas para experimentos finales
- Documentar todas las semillas usadas
- Ejecutar mínimo 5 repeticiones con diferentes semillas

### Análisis Estadístico
- Verificar normalidad de datos antes de t-test
- Usar ANOVA para comparar más de 2 grupos
- Reportar siempre intervalos de confianza

### PCAP
- Los archivos PCAP pueden ser grandes (>100MB)
- Comprimir antes de archivar: `gzip *.pcap`
- Analizar solo cuando sea necesario

### Overhead
- Comparar con valores de literatura
- Considerar tipo de red (MANET, VANET, WSN)
- Overhead alto no siempre es malo (depende del contexto)

---

**Versión**: 1.3  
**Fecha**: 24 de Noviembre de 2025  
**Autor**: Sistema A2A
