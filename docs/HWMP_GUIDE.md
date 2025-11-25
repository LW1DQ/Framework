# 📡 Guía de Uso: HWMP (IEEE 802.11s Mesh)

## Introducción

HWMP (Hybrid Wireless Mesh Protocol) es el protocolo de enrutamiento por defecto para redes mesh IEEE 802.11s. Es un protocolo híbrido que combina enrutamiento reactivo (basado en AODV) y proactivo (tree-based routing).

**Características principales**:
- **Tipo**: Híbrido (reactivo + proactivo)
- **Estándar**: IEEE 802.11s-2012
- **Uso típico**: Redes mesh WiFi urbanas, smart cities, infraestructura IoT
- **Soporte en NS-3**: Nativo vía módulo `mesh`

---

## ¿Por Qué HWMP para Smart Cities?

### Ventajas

1. **Escalabilidad Superior**
   - Soporta redes de 50-100+ nodos
   - Mejor que protocolos MANET tradicionales en redes densas

2. **Overhead Optimizado**
   - Overhead: 15-25% (intermedio entre AODV y OLSR)
   - Adaptativo según topología

3. **Latencia Baja**
   - Delay típico: 30-60 ms
   - Rutas proactivas reducen latencia inicial

4. **Ideal para Infraestructura Estática**
   - Iluminación inteligente
   - Sensores ambientales
   - Cámaras de videovigilancia
   - Puntos de acceso WiFi públicos

### Comparación con Protocolos MANET

| Aspecto | HWMP | AODV | OLSR |
|---------|------|------|------|
| **Tipo** | Híbrido | Reactivo | Proactivo |
| **Overhead** | Medio (15-25%) | Bajo (10-20%) | Alto (30-40%) |
| **Latencia inicial** | Baja | Alta | Muy baja |
| **Escalabilidad** | Alta (100+ nodos) | Media (50 nodos) | Baja (30 nodos) |
| **Movilidad** | Baja-Media | Alta | Alta |
| **Uso ideal** | Infraestructura urbana | Redes móviles | Redes vehiculares |

---

## Uso en el Framework A2A

### 1. Simulación Básica

```bash
cd "d:\Nueva carpeta\OneDrive\AGENTES A2A\repositorio framework\Framework"

# Activar entorno virtual (si aplica)
venv\Scripts\activate

# Ejecutar simulación HWMP
python main.py --task "Simular red mesh con HWMP, 20 nodos, 200 segundos"
```

**Resultado esperado**:
- Código NS-3 generado con `MeshHelper`
- Configuración IEEE 802.11s
- Simulación ejecutada (si NS-3 disponible)
- Resultados en XML y PCAP

### 2. Experimento de Comparación

Compara HWMP con AODV y OLSR en condiciones estáticas:

```bash
python experiments/experiment_runner.py --config experiments/configs/hwmp_comparison.yaml
```

**Configuración**:
- 3 protocolos: HWMP, AODV, OLSR
- 20 nodos por escenario
- Movilidad: Estática (típico de mesh)
- 10 repeticiones por protocolo
- Total: 30 simulaciones

**Resultados generados**:
- `experiments/results/hwmp_vs_manet_comparison/results.csv`
- Análisis estadístico (T-test, ANOVA)
- Gráficos comparativos
- Reporte en Markdown

### 3. Experimento de Escalabilidad

Evalúa el rendimiento de HWMP con diferentes tamaños de red:

```bash
python experiments/experiment_runner.py --config experiments/configs/hwmp_mesh_scalability.yaml
```

**Configuración**:
- 5 tamaños: 10, 20, 30, 50, 75 nodos
- Área escalada proporcionalmente
- 10 repeticiones por tamaño
- Total: 50 simulaciones

**Análisis**:
- Regresión lineal (escalabilidad)
- Correlación entre tamaño y métricas
- Identificación de límites de escalabilidad

---

## Configuración Típica

### Archivo YAML

```yaml
scenario:
  name: "HWMP_smart_city"
  protocol: "HWMP"
  nodes: 30
  area: 1000  # metros
  duration: 200  # segundos
  mobility: "ConstantPosition"  # Mesh típicamente estático
  speed: "0-0"  # Sin movilidad
  base_seed: 12345
```

### Código NS-3 Generado (Ejemplo)

```python
import ns.mesh

# Configurar mesh helper
mesh = ns.mesh.MeshHelper()
mesh.SetStackInstaller("ns3::Dot11sStack")
mesh.SetSpreadInterfaceChannels(ns.mesh.MeshHelper.SPREAD_CHANNELS)
mesh.SetNumberOfInterfaces(1)

# Configurar WiFi 802.11s
wifi = ns.wifi.WifiHelper()
wifi.SetStandard(ns.wifi.WIFI_STANDARD_80211s)

# Instalar mesh en nodos
devices = mesh.Install(wifi, phy, nodes)
```

---

## Métricas Esperadas

### Valores Típicos

| Métrica | Valor Típico | Rango | Notas |
|---------|--------------|-------|-------|
| **PDR** | 90-98% | 85-99% | Mayor que AODV en redes densas |
| **Delay** | 30-60 ms | 20-80 ms | Menor que OLSR, mayor que AODV |
| **Throughput** | 2-4 Mbps | 1-5 Mbps | Depende de densidad |
| **Overhead** | 15-25% | 10-30% | Intermedio entre AODV y OLSR |
| **Escalabilidad** | Hasta 100+ nodos | 50-150 | Mejor que protocolos MANET |

### Factores que Afectan el Rendimiento

1. **Densidad de nodos**: Mayor densidad → mejor PDR, mayor overhead
2. **Área de cobertura**: Área grande → mayor delay, menor PDR
3. **Tráfico**: Alto tráfico → mayor overhead, menor throughput
4. **Interferencia**: Alta interferencia → menor PDR

---

## Aplicaciones en Smart Cities

### 1. Iluminación Inteligente

**Escenario**: Red mesh de 50-100 farolas con sensores

```yaml
protocol: "HWMP"
nodes: 75
area: 1500
mobility: "ConstantPosition"
traffic: "periodic"  # Reportes cada 5 minutos
```

**Ventajas**:
- Cobertura amplia
- Bajo overhead
- Alta confiabilidad

### 2. Monitoreo Ambiental

**Escenario**: Red de sensores de calidad del aire

```yaml
protocol: "HWMP"
nodes: 30
area: 1000
mobility: "ConstantPosition"
traffic: "constant_bit_rate"
```

**Métricas críticas**:
- PDR > 95% (datos críticos)
- Delay < 50 ms (tiempo real)

### 3. Videovigilancia Distribuida

**Escenario**: Cámaras de seguridad en espacios públicos

```yaml
protocol: "HWMP"
nodes: 20
area: 800
mobility: "ConstantPosition"
traffic: "high_bandwidth"  # Video streaming
```

**Requisitos**:
- Throughput > 3 Mbps por cámara
- Jitter < 10 ms
- PDR > 98%

---

## Troubleshooting

### Error: "ns.mesh module not found"

**Causa**: NS-3 no tiene el módulo mesh instalado

**Solución**:
```bash
cd ~/ns-3-dev
./ns3 show modules | grep mesh

# Si no aparece, recompilar NS-3 con mesh
./ns3 configure --enable-examples --enable-tests
./ns3 build
```

### Error: "MeshHelper not defined"

**Causa**: Import incorrecto o código mal generado

**Solución**:
Verificar que el código incluya:
```python
import ns.mesh
mesh = ns.mesh.MeshHelper()
```

### PDR muy bajo (<80%)

**Causas posibles**:
1. Área muy grande para número de nodos
2. Interferencia alta
3. Configuración de potencia TX incorrecta

**Solución**:
- Reducir área o aumentar nodos
- Ajustar potencia de transmisión
- Verificar modelo de propagación

---

## Mejores Prácticas

### 1. Diseño de Topología

- **Densidad**: 1 nodo cada 50-100 metros
- **Conectividad**: Mínimo 3-4 vecinos por nodo
- **Redundancia**: Múltiples rutas entre nodos críticos

### 2. Configuración de Tráfico

- **Tráfico periódico**: Para sensores (cada 1-10 min)
- **Tráfico constante**: Para monitoreo continuo
- **Tráfico bajo demanda**: Para eventos

### 3. Validación

- **Repeticiones**: Mínimo 10 por escenario
- **Semillas**: Diferentes para cada repetición
- **Análisis estadístico**: Siempre calcular CI 95%

---

## Referencias

1. **IEEE 802.11s-2012**: "IEEE Standard for Information technology—Telecommunications and information exchange between systems Local and metropolitan area networks—Specific requirements Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications Amendment 10: Mesh Networking"

2. **NS-3 Mesh Module**: https://www.nsnam.org/docs/models/html/mesh.html

3. **HWMP Specification**: IEEE 802.11s-2012, Section 13.10

4. **NS-3 Examples**: `~/ns-3-dev/src/mesh/examples/`

---

## Próximos Pasos

1. **Ejecutar experimento de comparación**:
   ```bash
   python experiments/experiment_runner.py --config experiments/configs/hwmp_comparison.yaml
   ```

2. **Analizar resultados**:
   ```bash
   python experiments/statistical_analyzer.py experiments/results/hwmp_vs_manet_comparison/results.csv
   ```

3. **Revisar dashboard**:
   ```bash
   streamlit run dashboard.py
   ```

4. **Generar documento académico**:
   ```python
   from agents.scientific_writer import generate_thesis_section
   chapter = generate_thesis_section(section_type="results", experiment_results=results)
   ```

---

**Autor**: Sistema A2A  
**Versión**: 1.0  
**Fecha**: 25 de Noviembre de 2025  
**Estado**: ✅ Guía Completa
