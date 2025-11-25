# NOTA: Estoy trabajando ... 


# 🤖 Sistema A2A v1.4 - Framework Multi-Agente para Optimización de Protocolos de Enrutamiento

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![NS-3](https://img.shields.io/badge/NS--3-3.30%2B-orange)](https://www.nsnam.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-red)](https://pytorch.org/)

Sistema Multi-Agente inteligente para investigación en redes de telecomunicaciones, con capacidades de Deep Reinforcement Learning y análisis automatizado de protocolos de enrutamiento MANET/VANET/WSN.

---

## 📋 Tabla de Contenidos

- [Novedades v1.4](#-novedades-v14)
- [Características](#-características)
- [Inicio Rápido](#-inicio-rápido)
- [Arquitectura](#-arquitectura)
- [Agentes](#-agentes)
- [Documentación](#-documentación)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Para Tesis Doctoral](#-para-tesis-doctoral)
- [Contribuir](CONTRIBUTING.md)
- [Licencia](#-licencia)

---

## ✨ Novedades v1.4

### 🚀 Nuevas Funcionalidades (Noviembre 2025)

1. **🤖 Deep Reinforcement Learning Real (PPO con PyTorch)**
   - Implementación completa de Proximal Policy Optimization
   - Red neuronal Actor-Critic funcional
   - Entrenamiento episódico automático
   - Persistencia de modelos (.pth)
   - Integración preparada con ns3-ai

2. **📊 Dashboard en Tiempo Real (Streamlit)**
   - Monitoreo visual del estado del sistema
   - Gráficos interactivos de métricas (PDR, Delay, Throughput)
   - Logs en vivo de agentes
   - Auto-refresh configurable
   - Visualización de propuestas de optimización

3. **📝 Sistema de Logging y Telemetría**
   - Logging centralizado con `logging_utils`
   - Estado del sistema en JSON
   - Métricas históricas en CSV
   - Auditoría completa de acciones

### 🎯 Mejoras de v1.3 (Incluidas)

1. **🎲 Reproducibilidad Total**
   - Control de semillas aleatorias
   - Resultados 100% reproducibles
   - Validación científica garantizada

2. **📡 Análisis de Trazas PCAP**
   - Captura automática de tráfico
   - Nuevo agente Trace Analyzer
   - Análisis a nivel de paquetes

3. **📊 Overhead de Enrutamiento**
   - Cálculo preciso desde PCAP
   - Estimación basada en literatura
   - Comparación entre protocolos

4. **📈 Tests Estadísticos**
   - T-Test y ANOVA
   - Intervalos de confianza (95% CI)
   - Reportes automáticos en Markdown

5. **📝 Rigor Académico**
   - Reportes en formato académico
   - Métricas avanzadas
   - Validación estadística

---

## 🌟 Características

### Sistema Multi-Agente Inteligente

- **8 Agentes Especializados** trabajando en colaboración
- **Orquestación con LangGraph** para flujo de trabajo robusto
- **LLMs (Ollama)** para generación inteligente de código
- **Integración con NS-3** para simulaciones realistas

### Capacidades Avanzadas

- ✅ Generación automática de código NS-3
- ✅ Simulación y análisis de redes MANET/VANET/WSN
- ✅ Captura y análisis de trazas PCAP
- ✅ Cálculo de overhead de enrutamiento
- ✅ Tests estadísticos rigurosos
- ✅ Visualizaciones interactivas
- ✅ Optimización con Deep Learning
- ✅ Gestión de resultados en GitHub

### Protocolos Soportados

- **AODV** (Ad hoc On-Demand Distance Vector)
- **OLSR** (Optimized Link State Routing)
- **DSDV** (Destination-Sequenced Distance Vector)
- **DSR** (Dynamic Source Routing)

---

## 🚀 Inicio Rápido

### Instalación en 3 Pasos

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd sistema-a2a-export

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar primera simulación
python main.py
```

### Primera Simulación

```bash
python main.py
```

Cuando se te pregunte, ingresa:
```
Simular una red MANET con protocolo AODV, 20 nodos móviles,
área de 1000x1000 metros, durante 200 segundos
```

El sistema automáticamente:
1. 🔍 Investiga sobre AODV y MANET
2. 💻 Genera código Python para NS-3
3. 🚀 Ejecuta la simulación
4. 📡 Analiza archivos PCAP
5. 📊 Calcula KPIs y overhead
6. 📈 Genera gráficos y reportes

---

## 🏗️ Arquitectura

```
┌─────────────┐
│  Researcher │ → Investiga protocolos y mejores prácticas
└──────┬──────┘
       ↓
┌─────────────┐
│    Coder    │ → Genera código Python para NS-3
└──────┬──────┘
       ↓
┌─────────────┐
│  Simulator  │ → Ejecuta simulación en NS-3
└──────┬──────┘
       ↓
┌─────────────┐
│Trace Analyzer│ → Analiza archivos PCAP (NUEVO v1.3)
└──────┬──────┘
       ↓
┌─────────────┐
│   Analyst   │ → Calcula KPIs, overhead, tests estadísticos
└──────┬──────┘
       ↓
┌─────────────┐
│ Visualizer  │ → Genera gráficos y dashboard
└──────┬──────┘
       ↓
┌─────────────┐
│GitHub Manager│ → Organiza y prepara resultados
└─────────────┘
```

---

## 🤖 Agentes

### 1. 🔍 Researcher
- Investiga protocolos de enrutamiento
- Busca mejores prácticas
- Genera notas de investigación

### 2. 💻 Coder
- Genera código Python para NS-3
- Configura semillas aleatorias (v1.3)
- Habilita captura PCAP (v1.3)
- Incluye FlowMonitor para métricas

### 3. 🚀 Simulator
- Ejecuta código en NS-3
- Detecta archivos PCAP (v1.3)
- Gestiona resultados
- Maneja errores

### 4. 📡 Trace Analyzer (NUEVO v1.3)
- Analiza archivos PCAP con Scapy
- Detecta protocolos de enrutamiento
- Calcula overhead de enrutamiento
- Genera estadísticas de tráfico

### 5. 📊 Analyst
- Parsea resultados de FlowMonitor
- Calcula KPIs (PDR, delay, throughput)
- Calcula overhead de enrutamiento (v1.3)
- Ejecuta tests estadísticos (v1.3)
- Calcula intervalos de confianza (v1.3)
- Propone optimizaciones

### 6. 📈 Visualizer
- Genera gráficos de métricas
- Crea dashboard interactivo
- Exporta visualizaciones

### 7. 🔧 Optimizer
- Propone mejoras basadas en KPIs
- Ajusta parámetros
- Itera hasta alcanzar objetivos

### 8. 📦 GitHub Manager
- Organiza resultados
- Genera README
- Prepara para commit

---

## 📚 Documentación

- **[Manual de Usuario](MANUAL_USUARIO.md)**: Guía completa para investigadores.
- **[Guía de Instalación](INSTALL.md)**: Pasos detallados para configurar el entorno.
- **[Guía de Contribución](CONTRIBUTING.md)**: Estándares para desarrolladores.
- **[Changelog](CHANGELOG.md)**: Historial de cambios y versiones.

### Documentación Técnica
- `docs/`: Documentación detallada de arquitectura.
- `tests/`: Suites de pruebas unitarias.

---

## 💻 Requisitos

### Software Requerido

- **Python 3.8+**
- **NS-3 3.x** (instalado y configurado)
- **Ollama** (para LLMs locales)

### Dependencias Python

```
langchain_ollama>=0.1.0
langgraph>=0.2.0
scipy>=1.11.0
numpy>=1.24.0
pandas>=2.0.0
scapy>=2.5.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

---

## 🔧 Instalación

Para instrucciones detalladas de instalación en **Ubuntu** y **Windows**, consulta la guía oficial:

👉 **[GUÍA DE INSTALACIÓN (INSTALL.md)](INSTALL.md)**

### Resumen Rápido (Ubuntu)

```bash
# 1. Clonar
git clone <url-repo>
cd sistema-a2a

# 2. Instalar dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configurar NS-3
# Editar config/settings.py con la ruta a tu instalación de NS-3
```

## 📖 Uso

### Uso Básico

```bash
python main.py
```

### Uso Avanzado

```python
from supervisor import A2ASupervisor

# Crear supervisor
supervisor = A2ASupervisor()

# Definir tarea
task = """
Simular una red MANET con protocolo AODV,
20 nodos móviles con modelo RandomWaypoint,
área de 1000x1000 metros, durante 200 segundos.
Analizar PDR, delay, throughput y overhead de enrutamiento.
"""

# Ejecutar
result = supervisor.run(task)

# Acceder a resultados
print(f"PDR: {result['metrics']['avg_pdr']:.2f}%")
print(f"Delay: {result['metrics']['avg_delay']:.2f} ms")
print(f"Overhead: {result['routing_overhead']*100:.1f}%")
```

### Verificar Resultados

```bash
# Ver archivos PCAP
dir simulations\results\*.pcap

# Leer reporte estadístico
type simulations\analysis\statistical_report_*.md

# Abrir dashboard
start simulations\visualizations\dashboard.html
```

---

## 💡 Ejemplos

### Ejemplo 1: Comparar Protocolos

```python
protocols = ['AODV', 'OLSR', 'DSDV']
results = {}

for protocol in protocols:
    task = f"Simular MANET con {protocol}, 20 nodos, 200 segundos"
    result = supervisor.run(task)
    results[protocol] = result['metrics']

# Comparar overhead
for protocol, metrics in results.items():
    print(f"{protocol}: {metrics['routing_overhead']*100:.1f}% overhead")
```

### Ejemplo 2: Validación Estadística

```python
# Ejecutar múltiples semillas
seeds = [12345, 23456, 34567, 45678, 56789]
pdrs = []

for seed in seeds:
    # Configurar semilla en el código generado
    result = supervisor.run(task, seed=seed)
    pdrs.append(result['metrics']['avg_pdr'])

# Calcular estadísticas
import numpy as np
print(f"PDR: {np.mean(pdrs):.2f}% ± {np.std(pdrs):.2f}%")
print(f"95% CI: [{np.percentile(pdrs, 2.5):.2f}, {np.percentile(pdrs, 97.5):.2f}]")
```

### Ejemplo 3: Análisis de PCAP

```python
from scapy.all import rdpcap

# Leer archivo PCAP
packets = rdpcap('simulations/results/simulacion-0-0_*.pcap')

# Analizar
for pkt in packets[:10]:
    if IP in pkt:
        print(f"{pkt[IP].src} → {pkt[IP].dst}")
```

---

## 🎓 Para Tesis Doctoral

### Reproducibilidad

El sistema garantiza reproducibilidad total:

```python
# Configurar semilla
ns.core.RngSeedManager.SetSeed(12345)
ns.core.RngSeedManager.SetRun(1)
```

✅ Resultados idénticos con la misma semilla  
✅ Validación por pares  
✅ Cumple estándares científicos

### Rigor Estadístico

Tests automáticos incluidos:

- **T-Test**: Comparar dos grupos
- **ANOVA**: Comparar múltiples grupos
- **Intervalos de Confianza**: 95% CI para todas las métricas

### Métricas Avanzadas

- **PDR** (Packet Delivery Ratio)
- **Delay** (End-to-End)
- **Throughput**
- **Overhead de Enrutamiento** (NUEVO v1.3)
- **Jitter**
- **Tasa de éxito de flujos**

### Reportes Automáticos

Generación automática de reportes en formato académico:

```markdown
## Resultados

El protocolo AODV presentó un PDR de 95.5% (95% CI: [94.2%, 96.9%])
y un overhead de enrutamiento de 15.2%, calculado a partir del análisis
de trazas PCAP. Los resultados muestran una diferencia estadísticamente
significativa (t=5.234, p<0.001) comparado con OLSR.
```

### Checklist para Tesis

- [ ] Ejecutar mínimo 5 repeticiones con diferentes semillas
- [ ] Verificar generación de archivos PCAP
- [ ] Calcular intervalos de confianza
- [ ] Ejecutar tests estadísticos
- [ ] Comparar con valores de literatura
- [ ] Incluir gráficos y tablas
- [ ] Documentar overhead de enrutamiento

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

## 📞 Contacto

- **Autor**: Sistema A2A
- **Versión**: 1.3
- **Fecha**: Noviembre 2025
- **Estado**: ✅ Producción

---

## 🙏 Agradecimientos

- **NS-3 Team** - Por el simulador de redes
- **LangChain** - Por el framework de agentes
- **Ollama** - Por los LLMs locales
- **Scapy** - Por el análisis de paquetes

---

## 📊 Estadísticas del Proyecto

- **Agentes**: 8
- **Líneas de código**: ~5,000
- **Documentación**: 65+ páginas
- **Tests**: 4 suites
- **Protocolos soportados**: 4
- **Métricas calculadas**: 15+

---

## 🎯 Roadmap

### v1.4 (Futuro)
- [ ] Soporte para más protocolos (BATMAN, Babel)
- [ ] Integración con TensorFlow para DRL
- [ ] API REST para acceso remoto
- [ ] Dashboard web en tiempo real
- [ ] Soporte para simulaciones distribuidas

---

**¡Gracias por usar Sistema A2A v1.3!** 🚀

Si encuentras útil este proyecto, considera darle una ⭐ en GitHub.
