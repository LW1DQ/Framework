# 🎓 Guía para Investigadores de Redes - Sistema A2A

## Framework Multi-Agente para Simulación y Optimización de Protocolos de Enrutamiento

**Versión**: 1.3  
**Fecha**: Noviembre 2025  
**Audiencia**: Investigadores en Redes de Comunicación  
**Nivel**: Intermedio - Avanzado

---

## 📋 Tabla de Contenidos

### PARTE I: Fundamentos y Arquitectura
1. [Introducción](#1-introducción)
2. [¿Qué es un Sistema Multi-Agente?](#2-qué-es-un-sistema-multi-agente)
3. [Arquitectura del Sistema A2A](#3-arquitectura-del-sistema-a2a)
4. [Los 8 Agentes Especializados](#4-los-8-agentes-especializados)
5. [Flujo de Trabajo Completo](#5-flujo-de-trabajo-completo)
6. [Tecnologías Utilizadas](#6-tecnologías-utilizadas)

### PARTE II: Guía de Uso Práctica
7. [Instalación Paso a Paso](#7-instalación-paso-a-paso)
8. [Tu Primera Simulación](#8-tu-primera-simulación)
9. [Casos de Uso Comunes](#9-casos-de-uso-comunes)
10. [Interpretación de Resultados](#10-interpretación-de-resultados)
11. [Optimización Avanzada](#11-optimización-avanzada)
12. [Troubleshooting](#12-troubleshooting)

### PARTE III: Recursos Adicionales
13. [Preguntas Frecuentes (FAQ)](#13-preguntas-frecuentes-faq)
14. [Conclusión](#14-conclusión)
15. [Glosario para Investigadores de Redes](#15-glosario-para-investigadores-de-redes)
16. [Referencias](#16-referencias)

---

# PARTE I: FUNDAMENTOS Y ARQUITECTURA

---

## 1. Introducción

### 1.1 ¿Qué Problema Resuelve Este Framework?

Como investigador en redes, probablemente has enfrentado estos desafíos:

**Problema 1: Iteración Manual Tediosa**
```
Tú escribes código NS-3 → Ejecutas → Analizas → Ajustas parámetros → Repites
```
Este ciclo puede tomar **horas o días** por cada experimento.

**Problema 2: Análisis Complejo**
- Calcular KPIs manualmente
- Generar gráficos uno por uno
- Interpretar resultados
- Comparar múltiples configuraciones

**Problema 3: Optimización Difícil**
- ¿Qué parámetros ajustar?
- ¿Cómo mejorar el rendimiento?
- ¿Cuándo usar técnicas avanzadas como Deep Learning?

### 1.2 La Solución: Sistema A2A

**A2A (Agent-to-Agent)** automatiza **todo el ciclo de investigación**:

```
Tú describes lo que quieres → El sistema hace todo → Obtienes resultados completos
```

**Ejemplo Real:**

**Antes (Manual):**
```
1. Investigar sobre AODV (30 min)
2. Escribir código NS-3 (2 horas)
3. Debuggear errores (1 hora)
4. Ejecutar simulación (10 min)
5. Parsear XML de FlowMonitor (30 min)
6. Calcular KPIs (30 min)
7. Generar gráficos (30 min)
8. Analizar resultados (1 hora)
Total: ~6 horas
```

**Ahora (Con A2A):**
```
1. Describir: "Simular MANET con AODV, 20 nodos, 200 segundos"
2. Esperar: 15-20 minutos
3. Obtener: Código + Simulación + Análisis + Gráficos + Reporte
Total: ~20 minutos
```

### 1.3 Beneficios para Investigadores de Redes

✅ **Productividad**: 10-20x más rápido  
✅ **Reproducibilidad**: Semillas aleatorias controladas  
✅ **Rigor**: Tests estadísticos automáticos  
✅ **Profundidad**: Análisis PCAP + overhead de enrutamiento  
✅ **Optimización**: Deep Learning integrado  
✅ **Documentación**: Reportes académicos automáticos

---

## 2. ¿Qué es un Sistema Multi-Agente?

### 2.1 Concepto Básico

Un **agente** es un programa que:
- Tiene un **objetivo específico**
- Puede **tomar decisiones**
- **Actúa de forma autónoma**
- **Se comunica** con otros agentes

**Analogía del Mundo Real:**

Imagina un equipo de investigación donde cada miembro tiene una especialidad:

```
Investigador Junior  → Lee papers, busca información
Programador         → Escribe código
Técnico de Lab      → Ejecuta experimentos
Analista de Datos   → Calcula estadísticas
Diseñador Gráfico   → Crea visualizaciones
Investigador Senior → Propone optimizaciones
Documentalista      → Organiza resultados
Director            → Coordina a todos
```

En A2A, cada uno de estos roles es un **agente de software**.

### 2.2 ¿Por Qué Multi-Agente?

**Ventajas sobre un programa monolítico:**

1. **Especialización**: Cada agente es experto en su tarea
2. **Modularidad**: Fácil de mantener y extender
3. **Robustez**: Si un agente falla, los demás continúan
4. **Escalabilidad**: Puedes añadir más agentes
5. **Inteligencia**: Cada agente puede usar IA especializada

### 2.3 Comunicación Entre Agentes

Los agentes se comunican mediante un **estado compartido**:

```python
Estado = {
    'task': "Simular MANET con AODV...",
    'research_notes': "AODV es un protocolo reactivo...",
    'code_snippet': "import ns.core...",
    'simulation_logs': "resultados.xml",
    'metrics': {'pdr': 95.5, 'delay': 45.2, ...},
    'visualizations': ['grafico1.png', ...]
}
```

Cada agente:
1. **Lee** el estado
2. **Hace su trabajo**
3. **Actualiza** el estado
4. **Pasa** al siguiente agente

---

## 3. Arquitectura del Sistema A2A

### 3.1 Vista General

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Investigador)                    │
│                                                              │
│  Input: "Simular MANET con AODV, 20 nodos, 200 segundos"   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR (LangGraph)                    │
│                                                              │
│  • Orquesta el flujo de trabajo                            │
│  • Decide qué agente ejecutar                              │
│  • Maneja errores y reintentos                             │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    8 AGENTES ESPECIALIZADOS                  │
│                                                              │
│  Researcher → Coder → Simulator → Trace Analyzer →         │
│  Analyst → Visualizer → Optimizer → GitHub Manager          │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESULTADOS COMPLETOS                      │
│                                                              │
│  • Código NS-3 generado                                     │
│  • Archivos PCAP                                            │
│  • Métricas (PDR, delay, throughput, overhead)             │
│  • Tests estadísticos                                       │
│  • Gráficos y dashboard                                     │
│  • Reporte académico                                        │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Componentes Principales

#### 3.2.1 Supervisor (Orquestador)

**Tecnología**: LangGraph (framework de orquestación)

**Función**: Coordina el flujo de trabajo entre agentes

**Decisiones que toma:**
- ¿El código es válido? → Sí: Simular / No: Regenerar
- ¿La simulación fue exitosa? → Sí: Analizar / No: Reintentar
- ¿Los KPIs son buenos? → Sí: Visualizar / No: Optimizar

#### 3.2.2 Estado Compartido

**Tecnología**: TypedDict de Python

**Función**: Almacena toda la información del experimento

**Contenido:**
```python
{
    'task': str,                    # Tarea del usuario
    'research_notes': List[str],    # Notas de investigación
    'code_snippet': str,            # Código NS-3 generado
    'simulation_logs': str,         # Ruta a resultados XML
    'pcap_files': List[str],        # Archivos PCAP generados
    'trace_analysis': List[Dict],   # Análisis de PCAP
    'metrics': Dict,                # KPIs calculados
    'routing_overhead': float,      # Overhead de enrutamiento
    'confidence_intervals': Dict,   # Intervalos de confianza
    'statistical_results': Dict,    # Tests estadísticos
    'visualizations': List[str],    # Gráficos generados
    'optimization_proposal': str,   # Propuesta de optimización
    'iteration_count': int,         # Número de iteración
    'errors': List[str]             # Errores encontrados
}
```

#### 3.2.3 LLMs (Modelos de Lenguaje)

**Tecnología**: Ollama (LLMs locales)

**Modelos Utilizados:**
- **llama3.1:8b** - Para razonamiento y análisis
- **deepseek-coder-v2:16b** - Para generación de código

**¿Por qué locales?**
- ✅ Privacidad (tus datos no salen de tu máquina)
- ✅ Sin costos de API
- ✅ Sin límites de uso
- ✅ Funciona offline

---

## 4. Los 8 Agentes Especializados

### 4.1 Agente 1: Researcher (Investigador)

**Rol**: Experto en protocolos de enrutamiento

**Entrada**: Tarea del usuario

**Proceso:**
1. Analiza la tarea
2. Identifica el protocolo (AODV, OLSR, etc.)
3. Busca información en base de datos de papers
4. Genera notas de investigación

**Salida**: Notas sobre el protocolo, mejores prácticas, parámetros recomendados

**Ejemplo:**
```
Input: "Simular MANET con AODV"

Output:
- AODV es un protocolo reactivo (on-demand)
- Adecuado para redes con movilidad moderada
- Parámetros clave: HELLO_INTERVAL, ACTIVE_ROUTE_TIMEOUT
- Overhead típico: 10-20%
- Referencias: RFC 3561, Perkins et al. 2003
```

### 4.2 Agente 2: Coder (Programador)

**Rol**: Experto en NS-3 Python bindings

**Entrada**: Notas de investigación + tarea

**Proceso:**
1. Genera código Python para NS-3
2. Configura semilla aleatoria (reproducibilidad)
3. Habilita captura PCAP
4. Configura FlowMonitor
5. Valida sintaxis

**Salida**: Código Python completo y ejecutable

**Ejemplo de código generado:**
```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'build/lib/python3')

import ns.core
import ns.network
import ns.wifi
import ns.aodv

def main():
    # Configurar semilla para reproducibilidad
    ns.core.RngSeedManager.SetSeed(12345)
    
    # Crear 20 nodos
    nodes = ns.network.NodeContainer()
    nodes.Create(20)
    
    # Configurar WiFi...
    # Configurar movilidad...
    # Configurar AODV...
    # Habilitar PCAP
    phy.EnablePcapAll("simulacion", True)
    
    # Ejecutar simulación
    ns.core.Simulator.Run()
    ns.core.Simulator.Destroy()
```

### 4.3 Agente 3: Simulator (Ejecutor)

**Rol**: Ejecuta simulaciones en NS-3

**Entrada**: Código Python

**Proceso:**
1. Guarda el código en archivo temporal
2. Ejecuta con NS-3
3. Captura stdout/stderr
4. Detecta archivos PCAP generados
5. Mueve resultados a directorio organizado
6. Extrae información de la simulación

**Salida**: 
- Archivo XML de FlowMonitor
- Archivos PCAP
- Logs de ejecución
- Información de la simulación

**Manejo de Errores:**
- Si falla: Extrae el error y lo pasa al Coder para corrección
- Máximo 5 reintentos
- Timeout: 15 minutos

### 4.4 Agente 4: Trace Analyzer (Analizador de Trazas)

**Rol**: Experto en análisis de tráfico de red

**Entrada**: Archivos PCAP

**Proceso:**
1. Lee archivos PCAP con Scapy
2. Identifica protocolos (IP, UDP, TCP, ICMP, AODV, OLSR, etc.)
3. Calcula estadísticas de tráfico
4. Detecta paquetes de enrutamiento
5. Calcula overhead de enrutamiento

**Salida**:
```python
{
    'pcap_file': 'simulacion-0-0.pcap',
    'basic_stats': {
        'total_packets': 15234,
        'total_bytes': 12456789,
        'duration': 200.5
    },
    'protocol_distribution': {
        'IP': 14500,
        'UDP': 12000,
        'AODV': 1734
    },
    'routing_analysis': {
        'total_routing_bytes': 234567,
        'total_data_bytes': 12222222,
        'routing_overhead': 0.0192  # 1.92%
    }
}
```

**Importancia para Investigadores:**
- Overhead real (no estimado)
- Distribución de tráfico
- Patrones de comunicación
- Validación de protocolos

### 4.5 Agente 5: Analyst (Analista)

**Rol**: Experto en métricas de redes y estadística

**Entrada**: 
- XML de FlowMonitor
- Análisis de trazas PCAP

**Proceso:**
1. Parsea XML de FlowMonitor
2. Calcula KPIs básicos (PDR, delay, throughput)
3. Calcula overhead de enrutamiento
4. Ejecuta tests estadísticos (T-Test, ANOVA)
5. Calcula intervalos de confianza (95% CI)
6. Genera reporte estadístico

**Salida**:
```python
{
    'avg_pdr': 95.5,              # Packet Delivery Ratio
    'std_pdr': 2.3,
    'avg_delay': 45.2,            # ms
    'median_delay': 42.1,
    'p95_delay': 78.5,
    'avg_throughput': 2.45,       # Mbps
    'routing_overhead': 0.0192,   # 1.92%
    'confidence_intervals': {
        'pdr': [94.2, 96.8],
        'delay': [43.1, 47.3]
    },
    'statistical_results': {
        't_test': {
            'statistic': 5.234,
            'p_value': 0.0001,
            'significant': True
        }
    },
    'performance_grade': 'Excelente'
}
```

**Métricas Calculadas:**

| Métrica | Descripción | Rango Típico |
|---------|-------------|--------------|
| PDR | % de paquetes entregados | 70-100% |
| Delay | Latencia promedio | 10-200 ms |
| Throughput | Tasa de datos | 0.5-10 Mbps |
| Overhead | Tráfico de control/datos | 5-50% |
| Jitter | Variación de delay | 1-50 ms |


### 4.6 Agente 6: Visualizer (Visualizador)

**Rol**: Experto en visualización de datos de redes

**Entrada**: Métricas calculadas

**Proceso:**
1. Genera gráficos de métricas clave
2. Crea dashboard HTML interactivo
3. Aplica estilo académico (Seaborn)
4. Exporta en múltiples formatos (PNG, SVG, HTML)

**Salida**:
- Gráfico de PDR vs Tiempo
- Gráfico de Delay vs Tiempo
- Gráfico de Throughput vs Tiempo
- Gráfico de Overhead de Enrutamiento
- Dashboard HTML interactivo

**Ejemplo de Dashboard:**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Resultados - AODV 20 Nodos</title>
</head>
<body>
    <h1>Simulación MANET - AODV</h1>
    
    <div class="metrics">
        <div class="metric">
            <h3>PDR</h3>
            <p class="value">95.5%</p>
            <p class="ci">[94.2%, 96.8%]</p>
        </div>
        <div class="metric">
            <h3>Delay</h3>
            <p class="value">45.2 ms</p>
            <p class="ci">[43.1, 47.3]</p>
        </div>
        <div class="metric">
            <h3>Overhead</h3>
            <p class="value">1.92%</p>
        </div>
    </div>
    
    <img src="pdr_over_time.png">
    <img src="delay_over_time.png">
    <img src="throughput_over_time.png">
</body>
</html>
```

### 4.7 Agente 7: Optimizer (Optimizador)

**Rol**: Experto en optimización de protocolos con Deep Learning

**Entrada**: Métricas + análisis de cuellos de botella

**Proceso:**
1. Analiza KPIs para identificar problemas
2. Clasifica problemas (críticos, moderados, menores)
3. Decide si usar Deep Reinforcement Learning
4. Genera propuesta de arquitectura DL
5. Genera código optimizado (con ns3-ai si aplica)
6. Genera script de entrenamiento

**Salida**:
- Propuesta de optimización
- Código NS-3 optimizado
- Script de entrenamiento DRL (si aplica)

**Criterios para Optimización:**

```python
Optimizar si:
- PDR < 85%
- Delay > 100 ms
- Success Rate < 80%
- Overhead > 40%
```

**Ejemplo de Propuesta:**
```markdown
## Análisis de Cuellos de Botella

### Problemas Críticos:
1. **PDR Bajo (72.3%)**
   - Causa probable: Congestión de red
   - Solución: Ajustar parámetros de AODV o usar DRL

### Propuesta de Arquitectura DRL:

**Tipo de Red**: Deep Q-Network (DQN)

**Espacio de Estados** (10 dimensiones):
- Número de vecinos
- Buffer ocupado (%)
- Paquetes enviados/recibidos
- Energía restante
- Distancia al destino

**Espacio de Acciones** (3 acciones):
- Seleccionar siguiente salto
- Ajustar potencia de transmisión
- Establecer prioridad de paquete

**Función de Recompensa**:
R = 0.4*PDR - 0.3*delay - 0.1*energía + 0.15*throughput - 0.05*overhead

**Hiperparámetros**:
- Learning rate: 0.001
- Batch size: 64
- Epsilon decay: 0.995
- Episodios: 2000
```

### 4.8 Agente 8: GitHub Manager (Gestor de Resultados)

**Rol**: Organizador y documentador

**Entrada**: Todos los resultados

**Proceso:**
1. Organiza archivos en estructura clara
2. Genera README con resumen
3. Crea commits descriptivos
4. Prepara para versionado

**Salida**:
```
resultados/
├── experimento_20251124_143022/
│   ├── README.md
│   ├── codigo/
│   │   └── simulacion.py
│   ├── resultados/
│   │   ├── sim_20251124_143022.xml
│   │   ├── simulacion-0-0.pcap
│   │   └── stdout.txt
│   ├── analisis/
│   │   └── statistical_report.md
│   └── visualizaciones/
│       ├── dashboard.html
│       ├── pdr_over_time.png
│       └── delay_over_time.png
```

---

## 5. Flujo de Trabajo Completo

### 5.1 Flujo Normal (Sin Errores)

```
Usuario
  ↓
  "Simular MANET con AODV, 20 nodos, 200 segundos"
  ↓
┌─────────────┐
│ RESEARCHER  │ → Investiga sobre AODV
└──────┬──────┘   Genera notas de investigación
       ↓
┌─────────────┐
│   CODER     │ → Genera código Python para NS-3
└──────┬──────┘   Configura semilla + PCAP
       ↓
┌─────────────┐
│  SIMULATOR  │ → Ejecuta simulación en NS-3
└──────┬──────┘   Genera XML + PCAP
       ↓
┌─────────────┐
│TRACE        │ → Analiza archivos PCAP
│ANALYZER     │   Calcula overhead real
└──────┬──────┘
       ↓
┌─────────────┐
│  ANALYST    │ → Calcula KPIs
└──────┬──────┘   Tests estadísticos
       │           Intervalos de confianza
       ↓
    ¿KPIs OK?
       │
    ✅ SÍ
       ↓
┌─────────────┐
│ VISUALIZER  │ → Genera gráficos
└──────┬──────┘   Crea dashboard
       ↓
┌─────────────┐
│   GITHUB    │ → Organiza resultados
│   MANAGER   │   Genera documentación
└──────┬──────┘
       ↓
   RESULTADOS COMPLETOS
```

**Tiempo Total**: 15-20 minutos

### 5.2 Flujo con Optimización

```
... (igual hasta Analyst)
       ↓
    ¿KPIs OK?
       │
    ❌ NO (PDR < 85%)
       ↓
┌─────────────┐
│  OPTIMIZER  │ → Analiza cuellos de botella
└──────┬──────┘   Propone mejoras
       │           Genera código optimizado
       │           (con DRL si es necesario)
       ↓
┌─────────────┐
│   CODER     │ → Regenera código con optimizaciones
└──────┬──────┘
       ↓
┌─────────────┐
│  SIMULATOR  │ → Ejecuta nueva simulación
└──────┬──────┘
       ↓
    ... (continúa el flujo)
```

**Límite**: Máximo 2 ciclos de optimización

### 5.3 Flujo con Errores

```
┌─────────────┐
│   CODER     │ → Genera código
└──────┬──────┘
       ↓
    ¿Código válido?
       │
    ❌ NO (error de sintaxis)
       ↓
┌─────────────┐
│   CODER     │ → Regenera código corrigiendo error
└──────┬──────┘   (Máximo 5 intentos)
       ↓
┌─────────────┐
│  SIMULATOR  │ → Ejecuta simulación
└──────┬──────┘
       ↓
    ¿Simulación exitosa?
       │
    ❌ NO (error de ejecución)
       ↓
┌─────────────┐
│   CODER     │ → Regenera código corrigiendo error
└──────┬──────┘   (Máximo 5 intentos)
```

**Robustez**: El sistema se auto-corrige automáticamente

---

## 6. Tecnologías Utilizadas

### 6.1 Stack Tecnológico

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| Orquestación | LangGraph | Coordinar agentes |
| LLMs | Ollama (Llama3, DeepSeek) | Inteligencia de agentes |
| Simulador | NS-3 3.36+ | Simulaciones de red |
| Análisis PCAP | Scapy | Análisis de tráfico |
| Tests Estadísticos | SciPy | T-Test, ANOVA, CI |
| Visualización | Matplotlib, Seaborn | Gráficos |
| Deep Learning | PyTorch + ns3-ai | Optimización DRL |
| Lenguaje | Python 3.10+ | Todo el sistema |

### 6.2 ¿Por Qué Estas Tecnologías?

**LangGraph**:
- ✅ Diseñado para sistemas multi-agente
- ✅ Manejo de estado robusto
- ✅ Flujos condicionales complejos
- ✅ Persistencia automática

**Ollama**:
- ✅ LLMs locales (privacidad)
- ✅ Sin costos de API
- ✅ Modelos especializados
- ✅ Funciona offline

**NS-3**:
- ✅ Estándar en investigación de redes
- ✅ Modelos realistas
- ✅ Ampliamente validado
- ✅ Python bindings

**Scapy**:
- ✅ Análisis profundo de paquetes
- ✅ Detección de protocolos
- ✅ Flexible y potente
- ✅ Bien documentado

---

# PARTE II: GUÍA DE USO PRÁCTICA

---

## 7. Instalación Paso a Paso

### 7.1 Requisitos del Sistema

**Hardware Mínimo:**
- CPU: 4 cores
- RAM: 8 GB
- Disco: 20 GB libres

**Hardware Recomendado:**
- CPU: 8+ cores
- RAM: 16 GB
- Disco: 50 GB libres

**Sistema Operativo:**
- Ubuntu 20.04+ (recomendado)
- Debian 11+
- Fedora 35+
- macOS 12+ (con limitaciones)
- Windows 10+ con WSL2

### 7.2 Instalación en Ubuntu (Recomendado)

#### Paso 1: Descomprimir el Proyecto

```bash
# Descomprimir
unzip sistema-a2a-v1.3-ubuntu.zip -d ~/sistema-a2a-v1.3

# Navegar
cd ~/sistema-a2a-v1.3

# Verificar contenido
ls -la
```

#### Paso 2: Instalar Python 3.10+

```bash
# Verificar versión
python3 --version

# Si es menor a 3.10, instalar:
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip -y
```

#### Paso 3: Crear Entorno Virtual

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Verificar
which python
# Debe mostrar: .../sistema-a2a-v1.3/venv/bin/python
```

#### Paso 4: Instalar Dependencias Python

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt

# Esto instalará:
# - langchain_ollama (LLMs)
# - langgraph (orquestación)
# - scipy (estadística)
# - scapy (análisis PCAP)
# - matplotlib, seaborn (gráficos)
# - pandas, numpy (datos)
```

#### Paso 5: Instalar NS-3

**Opción A: Script Automático (Recomendado)**

```bash
# Dar permisos
chmod +x install.sh

# Ejecutar (tarda ~30-60 minutos)
./install.sh

# El script instalará:
# - Dependencias del sistema
# - NS-3 desde GitLab
# - Compilará NS-3
# - Verificará la instalación
```

**Opción B: Manual**

```bash
# Instalar dependencias
sudo apt install g++ python3-dev pkg-config sqlite3 \
  cmake ninja-build ccache git -y

# Clonar NS-3
cd ~/
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev

# Configurar
./ns3 configure --enable-examples --enable-tests

# Compilar (tarda ~30 minutos)
./ns3 build

# Verificar
./ns3 --version
# Debe mostrar: ns-3.36 o superior
```

#### Paso 6: Instalar Ollama

```bash
# Descargar e instalar
curl -fsSL https://ollama.ai/install.sh | sh

# Verificar
ollama --version

# Descargar modelos (tarda ~10-20 minutos)
ollama pull llama3.1:8b
ollama pull deepseek-coder-v2:16b

# Verificar modelos
ollama list
```

#### Paso 7: Configurar Rutas

```bash
# Editar configuración
nano config/settings.py

# Verificar/actualizar estas líneas:
NS3_ROOT = Path.home() / "ns-3-dev"
OLLAMA_BASE_URL = "http://localhost:11434"
```

#### Paso 8: Verificar Instalación

```bash
# Activar entorno virtual (si no está activo)
source venv/bin/activate

# Ejecutar test de integración
python test_integration.py

# Resultado esperado:
# ✅ PASS - Estructura de Archivos
# ✅ PASS - Imports
# ✅ PASS - Utilidades Estadísticas
# ✅ PASS - Supervisor
```

**Si todos los tests pasan**: ¡Instalación exitosa! ✅

---

## 8. Tu Primera Simulación

### 8.1 Simulación Básica: AODV con 10 Nodos

#### Paso 1: Activar Entorno

```bash
cd ~/sistema-a2a-v1.3
source venv/bin/activate
```

#### Paso 2: Ejecutar el Sistema

```bash
python main.py
```

#### Paso 3: Describir tu Experimento

El sistema te preguntará:
```
🤖 Sistema A2A v1.3
¿Qué simulación deseas ejecutar?
> 
```

Escribe:
```
Simular una red MANET con protocolo AODV, 10 nodos móviles con modelo 
RandomWaypoint, área de 500x500 metros, durante 100 segundos
```

#### Paso 4: Observar el Progreso

El sistema mostrará:

```
🔍 AGENTE RESEARCHER ACTIVADO
   Investigando sobre AODV...
   ✓ Notas generadas

💻 AGENTE CODER ACTIVADO
   Generando código NS-3...
   ✓ Código generado (245 líneas)
   ✓ Código validado

🚀 AGENTE SIMULATOR ACTIVADO
   Ejecutando simulación...
   ⏱️  Tiempo estimado: 2-3 minutos
   ✓ Simulación completada

📡 AGENTE TRACE ANALYZER ACTIVADO
   Analizando archivos PCAP...
   📡 Archivos PCAP encontrados: 10
   ✓ Análisis completado

📊 AGENTE ANALYST ACTIVADO
   Calculando KPIs...
   📈 PDR: 94.5%
   ⏱️  Delay: 38.2 ms
   🚀 Throughput: 1.85 Mbps
   📡 Overhead: 12.3%
   ✅ Clasificación: Excelente
   ✓ Análisis completado

📈 AGENTE VISUALIZER ACTIVADO
   Generando gráficos...
   ✓ 4 gráficos generados
   ✓ Dashboard creado

📦 AGENTE GITHUB MANAGER ACTIVADO
   Organizando resultados...
   ✓ Resultados guardados

✅ PROCESO COMPLETADO
   Tiempo total: 8 minutos
   Resultados en: simulations/results/
```

#### Paso 5: Ver Resultados

```bash
# Ver archivos generados
ls -lh simulations/results/

# Deberías ver:
# - sim_YYYYMMDD_HHMMSS.xml (FlowMonitor)
# - simulacion-*.pcap (Capturas PCAP)
# - sim_YYYYMMDD_HHMMSS_stdout.txt (Logs)

# Ver reporte estadístico
cat simulations/analysis/statistical_report_*.md

# Abrir dashboard (si tienes GUI)
xdg-open simulations/visualizations/dashboard.html
```

### 8.2 Entender los Resultados

#### Archivo XML (FlowMonitor)

```xml
<FlowMonitor>
  <Flow flowId="1" 
        txPackets="1000" 
        rxPackets="945"
        txBytes="1024000"
        rxBytes="967680"
        delaySum="36150000000"
        ...>
  </Flow>
</FlowMonitor>
```

**No necesitas parsear esto manualmente** - El Analyst lo hace por ti.

#### Reporte Estadístico

```markdown
# Reporte Estadístico - Simulación MANET

## Métricas Principales

| Métrica | Valor | 95% CI | Interpretación |
|---------|-------|--------|----------------|
| PDR | 94.5% | [93.2%, 95.8%] | Excelente |
| Delay | 38.2 ms | [35.1, 41.3] | Muy bueno |
| Throughput | 1.85 Mbps | [1.78, 1.92] | Bueno |
| Overhead | 12.3% | - | Típico para AODV |

## Tests Estadísticos

### T-Test: Flujos Exitosos vs Fallidos
- Estadístico t: 5.234
- p-value: 0.0001
- **Conclusión**: Diferencia estadísticamente significativa (p < 0.05)

## Interpretación

El protocolo AODV muestra un rendimiento excelente con un PDR de 94.5%
y un delay promedio de 38.2 ms. El overhead de 12.3% está dentro del
rango esperado para AODV (10-20% según literatura).
```


---

## 9. Casos de Uso Comunes

### 9.1 Comparar Dos Protocolos

**Objetivo**: Comparar AODV vs OLSR en las mismas condiciones

#### Paso 1: Simular AODV

```bash
python main.py
```

Tarea:
```
Simular MANET con AODV, 20 nodos, área 1000x1000m, 200 segundos
```

Guardar resultados:
```bash
# Copiar resultados
cp simulations/results/sim_*.xml resultados_aodv.xml
cp simulations/analysis/statistical_report_*.md reporte_aodv.md
```

#### Paso 2: Simular OLSR

```bash
python main.py
```

Tarea:
```
Simular MANET con OLSR, 20 nodos, área 1000x1000m, 200 segundos
```

Guardar resultados:
```bash
cp simulations/results/sim_*.xml resultados_olsr.xml
cp simulations/analysis/statistical_report_*.md reporte_olsr.md
```

#### Paso 3: Comparar Resultados

```bash
# Ver reportes lado a lado
diff reporte_aodv.md reporte_olsr.md

# O crear tabla comparativa
cat > comparacion.md << EOF
# Comparación AODV vs OLSR

| Métrica | AODV | OLSR | Mejor |
|---------|------|------|-------|
| PDR | 94.5% | 92.1% | AODV |
| Delay | 38.2 ms | 52.7 ms | AODV |
| Throughput | 1.85 Mbps | 1.92 Mbps | OLSR |
| Overhead | 12.3% | 28.5% | AODV |

## Conclusión
AODV muestra mejor rendimiento en PDR y delay, con menor overhead.
OLSR tiene ligeramente mejor throughput pero a costa de mayor overhead.
EOF
```

### 9.2 Evaluar Impacto de la Movilidad

**Objetivo**: Ver cómo afecta la velocidad de los nodos

#### Experimento 1: Baja Movilidad

```
Simular MANET con AODV, 20 nodos, movilidad RandomWaypoint con velocidad 
entre 1-5 m/s, área 1000x1000m, 200 segundos
```

#### Experimento 2: Media Movilidad

```
Simular MANET con AODV, 20 nodos, movilidad RandomWaypoint con velocidad 
entre 5-15 m/s, área 1000x1000m, 200 segundos
```

#### Experimento 3: Alta Movilidad

```
Simular MANET con AODV, 20 nodos, movilidad RandomWaypoint con velocidad 
entre 15-25 m/s, área 1000x1000m, 200 segundos
```

#### Análisis

Crear gráfico comparativo:
```python
import matplotlib.pyplot as plt

velocidades = ['Baja (1-5)', 'Media (5-15)', 'Alta (15-25)']
pdr = [94.5, 87.3, 72.1]
delay = [38.2, 52.7, 89.5]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(velocidades, pdr, marker='o')
ax1.set_title('PDR vs Movilidad')
ax1.set_ylabel('PDR (%)')

ax2.plot(velocidades, delay, marker='o', color='red')
ax2.set_title('Delay vs Movilidad')
ax2.set_ylabel('Delay (ms)')

plt.savefig('movilidad_impact.png')
```

**Conclusión Típica**: A mayor movilidad, menor PDR y mayor delay.

### 9.3 Optimizar un Protocolo con DRL

**Objetivo**: Mejorar AODV usando Deep Reinforcement Learning

#### Paso 1: Simulación Baseline

```
Simular MANET con AODV, 30 nodos, alta densidad, área 500x500m, 200 segundos
```

Supongamos que obtienes:
- PDR: 72.3% (bajo)
- Delay: 125.8 ms (alto)
- Clasificación: Pobre

#### Paso 2: El Sistema Detecta Problemas

El Optimizer se activará automáticamente y mostrará:

```
🔧 AGENTE OPTIMIZER ACTIVADO

🔍 Identificando cuellos de botella...
   Problemas críticos: 2
   Problemas moderados: 1

   ⚠️  PROBLEMAS CRÍTICOS DETECTADOS:
      - PDR: PDR muy bajo - pérdida excesiva de paquetes
      - Delay: Delay alto - latencia excesiva

🤖 Evaluando necesidad de Deep Reinforcement Learning...
   ✅ DRL recomendado para estos problemas
   📚 Generando código con integración ns3-ai...

💻 Generando código optimizado...
   ✓ Código DRL generado
   ✓ Script de entrenamiento: train_drl_YYYYMMDD_HHMMSS.py

🔄 El código optimizado será regenerado por el Agente Programador
```

#### Paso 3: Nueva Simulación con DRL

El sistema automáticamente:
1. Regenera el código con ns3-ai
2. Ejecuta nueva simulación
3. Compara resultados

Resultados esperados:
- PDR: 89.5% (+17.2%)
- Delay: 78.3 ms (-47.5 ms)
- Clasificación: Bueno

#### Paso 4: Entrenar el Modelo (Opcional)

Si quieres entrenar el modelo DRL:

```bash
# El sistema generó el script
python simulations/scripts/train_drl_YYYYMMDD_HHMMSS.py

# Esto entrenará el modelo por 2000 episodios
# Tiempo estimado: 2-4 horas
```

### 9.4 Validar Reproducibilidad

**Objetivo**: Verificar que los resultados son reproducibles

#### Paso 1: Primera Ejecución

```
Simular MANET con AODV, 20 nodos, semilla 12345, área 1000x1000m, 200 segundos
```

Guardar resultados:
```bash
cp simulations/results/sim_*.xml run1.xml
```

#### Paso 2: Segunda Ejecución (Misma Semilla)

```
Simular MANET con AODV, 20 nodos, semilla 12345, área 1000x1000m, 200 segundos
```

Guardar resultados:
```bash
cp simulations/results/sim_*.xml run2.xml
```

#### Paso 3: Comparar

```bash
# Los archivos deben ser idénticos
diff run1.xml run2.xml

# Si no hay output, son idénticos ✅
```

**Importancia**: Esto es crítico para publicaciones científicas.

### 9.5 Análisis de Overhead Detallado

**Objetivo**: Entender el overhead de diferentes protocolos

El sistema calcula overhead automáticamente desde PCAP:

```
📡 AGENTE TRACE ANALYZER ACTIVADO
   Analizando archivos PCAP...
   
   Protocolo: AODV
   Total paquetes: 15,234
   Paquetes de datos: 13,500
   Paquetes de control (AODV): 1,734
   
   📊 Overhead calculado desde PCAP: 0.128 (12.8%)
```

**Comparación Típica:**

| Protocolo | Overhead | Tipo | Características |
|-----------|----------|------|-----------------|
| AODV | 10-20% | Reactivo | Bajo overhead, bueno para movilidad |
| OLSR | 30-40% | Proactivo | Alto overhead, bueno para estabilidad |
| DSDV | 40-50% | Proactivo | Muy alto overhead, simple |
| DSR | 15-25% | Reactivo | Moderado overhead, source routing |

---

## 10. Interpretación de Resultados

### 10.1 Métricas Clave

#### PDR (Packet Delivery Ratio)

**Definición**: Porcentaje de paquetes que llegan al destino

**Fórmula**: PDR = (Paquetes Recibidos / Paquetes Enviados) × 100

**Interpretación:**
- **> 95%**: Excelente - Red muy confiable
- **85-95%**: Bueno - Aceptable para la mayoría de aplicaciones
- **70-85%**: Regular - Problemas de congestión o movilidad
- **< 70%**: Pobre - Red no funcional, requiere optimización

**Factores que Afectan:**
- Movilidad de nodos
- Densidad de red
- Potencia de transmisión
- Protocolo de enrutamiento
- Congestión

#### Delay (Latencia End-to-End)

**Definición**: Tiempo que tarda un paquete desde origen hasta destino

**Unidad**: Milisegundos (ms)

**Interpretación:**
- **< 50 ms**: Excelente - Adecuado para VoIP, video
- **50-100 ms**: Bueno - Aceptable para la mayoría de aplicaciones
- **100-200 ms**: Regular - Perceptible para usuarios
- **> 200 ms**: Pobre - Inaceptable para aplicaciones en tiempo real

**Componentes del Delay:**
- Delay de propagación
- Delay de transmisión
- Delay de procesamiento
- Delay de cola (buffering)

#### Throughput

**Definición**: Tasa de datos efectivamente transmitidos

**Unidad**: Mbps (Megabits por segundo)

**Interpretación:**
- Depende del ancho de banda disponible
- Para WiFi 802.11a: 6-54 Mbps teórico
- Throughput real típicamente 40-60% del teórico

**Factores que Afectan:**
- Ancho de banda del canal
- Interferencia
- Colisiones
- Overhead del protocolo

#### Overhead de Enrutamiento

**Definición**: Proporción de tráfico de control vs tráfico de datos

**Fórmula**: Overhead = Bytes_Control / Bytes_Datos

**Interpretación:**
- **< 20%**: Excelente - Protocolo eficiente
- **20-30%**: Bueno - Aceptable
- **30-40%**: Regular - Protocolo proactivo típico
- **> 40%**: Alto - Considerar protocolo alternativo

**Importancia:**
- Afecta el consumo de energía
- Reduce ancho de banda disponible para datos
- Indicador de eficiencia del protocolo

### 10.2 Tests Estadísticos

#### T-Test

**Propósito**: Comparar dos grupos

**Ejemplo**: Flujos exitosos vs fallidos

**Interpretación:**
```
t-statistic: 5.234
p-value: 0.0001

Si p < 0.05: Diferencia estadísticamente significativa
Si p ≥ 0.05: No hay diferencia significativa
```

**En tu Paper:**
```
"Se realizó un t-test para comparar el PDR entre flujos exitosos y 
fallidos. Los resultados muestran una diferencia estadísticamente 
significativa (t=5.234, p<0.001), indicando que..."
```

#### Intervalos de Confianza (95% CI)

**Propósito**: Rango donde está el valor real con 95% de probabilidad

**Ejemplo:**
```
PDR: 94.5% [93.2%, 95.8%]
```

**Interpretación:**
- Estamos 95% seguros de que el PDR real está entre 93.2% y 95.8%
- Rango estrecho = alta precisión
- Rango amplio = baja precisión (necesita más datos)

**En tu Paper:**
```
"El PDR promedio fue de 94.5% (95% CI: [93.2%, 95.8%]), indicando 
un rendimiento consistente y confiable del protocolo AODV."
```

### 10.3 Clasificación de Rendimiento

El sistema clasifica automáticamente:

```python
def classify_performance(kpis):
    score = 0
    
    # PDR (40 puntos)
    if pdr >= 95: score += 40
    elif pdr >= 85: score += 30
    elif pdr >= 70: score += 20
    else: score += 10
    
    # Delay (30 puntos)
    if delay <= 50: score += 30
    elif delay <= 100: score += 20
    elif delay <= 200: score += 10
    
    # Success Rate (30 puntos)
    if success_rate >= 95: score += 30
    elif success_rate >= 80: score += 20
    elif success_rate >= 60: score += 10
    
    # Clasificación
    if score >= 85: return "Excelente"
    elif score >= 65: return "Bueno"
    elif score >= 45: return "Regular"
    else: return "Pobre"
```

---

## 11. Optimización Avanzada

### 11.1 ¿Cuándo Usar Deep Learning?

El sistema decide automáticamente, pero como investigador debes entender:

**Usar DRL cuando:**
- ✅ PDR < 80%
- ✅ Delay > 150 ms
- ✅ Escenarios complejos (alta movilidad, alta densidad)
- ✅ Quieres optimización adaptativa
- ✅ Tienes tiempo para entrenar (2-4 horas)

**NO usar DRL cuando:**
- ❌ Resultados ya son buenos (PDR > 90%, Delay < 50ms)
- ❌ Escenarios simples
- ❌ Necesitas resultados rápidos
- ❌ No tienes recursos computacionales

### 11.2 Instalar ns3-ai (Opcional)

Si quieres usar DRL, necesitas ns3-ai:

```bash
# Navegar a contrib de NS-3
cd ~/ns-3-dev/contrib

# Clonar ns3-ai
git clone https://github.com/hust-diangroup/ns3-ai.git

# Volver a NS-3
cd ~/ns-3-dev

# Reconfigurar
./ns3 clean
./ns3 configure --enable-examples

# Recompilar (tarda ~30 minutos)
./ns3 build

# Verificar
./ns3 run "ns3-ai-gym-test"
```

**Documentación Completa**: Ver `docs/INSTALACION-NS3-AI.md`

### 11.3 Interpretar Propuestas de Optimización

El Optimizer genera propuestas detalladas:

```markdown
## Propuesta de Optimización

### Problemas Detectados:
1. **PDR Bajo (72.3%)**
   - Causa: Congestión de red
   - Solución: Ajustar parámetros de AODV o usar DRL

### Arquitectura DRL Propuesta:

**Tipo**: Deep Q-Network (DQN)

**Espacio de Estados** (10 dimensiones):
- Número de vecinos: 0-20
- Buffer ocupado: 0-100%
- Paquetes enviados: contador
- Paquetes recibidos: contador
- Energía restante: 0-100%
- Distancia al destino: 0-1000m
- Hops al destino: 0-10
- PDR reciente: 0-100%
- Delay reciente: 0-500ms
- Throughput reciente: 0-10 Mbps

**Espacio de Acciones** (3 acciones):
0. Usar ruta por defecto
1. Buscar ruta alternativa
2. Ajustar potencia de transmisión

**Función de Recompensa**:
R = 0.4×PDR - 0.3×delay_norm - 0.1×energía + 0.15×throughput - 0.05×overhead

Donde:
- PDR: 0-1 (normalizado)
- delay_norm: delay/500 (normalizado)
- energía: consumo normalizado
- throughput: 0-1 (normalizado)
- overhead: 0-1 (normalizado)

**Hiperparámetros**:
- Learning rate: 0.001
- Batch size: 64
- Replay buffer: 10,000
- Epsilon inicial: 1.0
- Epsilon final: 0.01
- Epsilon decay: 0.995
- Gamma (discount): 0.99
- Episodios: 2000
```

**Como Investigador, Puedes:**
1. Usar la propuesta tal cual
2. Ajustar hiperparámetros
3. Modificar la función de recompensa
4. Cambiar el espacio de estados/acciones

---

## 12. Troubleshooting

### 12.1 Problemas Comunes

#### Problema 1: "NS-3 not found"

**Síntoma:**
```
Error: NS-3 not found at /home/user/ns-3-dev
```

**Solución:**
```bash
# Verificar que NS-3 esté instalado
ls ~/ns-3-dev

# Si no existe, instalar
cd ~/
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure --enable-examples
./ns3 build

# Actualizar ruta en config/settings.py
nano config/settings.py
# Cambiar: NS3_ROOT = Path.home() / "ns-3-dev"
```

#### Problema 2: "Ollama not responding"

**Síntoma:**
```
Error: Could not connect to Ollama at http://localhost:11434
```

**Solución:**
```bash
# Verificar que Ollama esté corriendo
curl http://localhost:11434/api/tags

# Si no responde, iniciar Ollama
ollama serve &

# Verificar modelos
ollama list

# Si faltan modelos, descargar
ollama pull llama3.1:8b
ollama pull deepseek-coder-v2:16b
```

#### Problema 3: "Simulation timeout"

**Síntoma:**
```
⚠️  Timeout: Simulación excedió 900s
```

**Solución:**
- Reducir número de nodos
- Reducir tiempo de simulación
- Reducir área de simulación
- Aumentar timeout en `config/settings.py`:
  ```python
  SIMULATION_TIMEOUT = 1800  # 30 minutos
  ```

#### Problema 4: "No PCAP files found"

**Síntoma:**
```
⚠️  No se encontraron archivos PCAP
   Verificar que el código incluya: phy.EnablePcapAll()
```

**Causa**: El código generado no habilitó PCAP

**Solución**: El sistema debería auto-corregirse. Si persiste:
```bash
# Verificar que el template esté en coder.py
grep "EnablePcapAll" agents/coder.py
```

#### Problema 5: "Import Error: scipy"

**Síntoma:**
```
ImportError: No module named 'scipy'
```

**Solución:**
```bash
# Activar entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### 12.2 Logs y Debugging

#### Ver Logs del Sistema

```bash
# Logs de LangGraph
cat logs/langgraph_checkpoints.db

# Logs de simulación
cat simulations/results/sim_*_stdout.txt

# Logs de errores
grep "ERROR" logs/*.log
```

#### Modo Verbose

Para más información de debugging:

```python
# En main.py, añadir:
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 12.3 Obtener Ayuda

**Documentación:**
- `EMPIEZA-AQUI.txt` - Guía de inicio
- `docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md` - Guía completa
- `docs/INSTALACION-COMPLETA.md` - Instalación detallada
- `docs/ESTADO-FINAL-Y-PROXIMOS-PASOS.md` - Estado y soluciones

**Test de Diagnóstico:**
```bash
python test_integration.py
```

---

## 13. Preguntas Frecuentes (FAQ)

### 13.1 Preguntas Generales

**P: ¿Necesito conocimientos de IA o Machine Learning para usar el sistema?**

R: No. El sistema está diseñado para investigadores de redes. Solo necesitas describir tu experimento en lenguaje natural. Los agentes de IA trabajan en segundo plano automáticamente.

**P: ¿Puedo usar el sistema sin conexión a Internet?**

R: Sí, completamente. Ollama ejecuta los LLMs localmente, NS-3 es local, y todas las herramientas funcionan offline. Solo necesitas Internet para la instalación inicial.

**P: ¿Cuánto tiempo tarda una simulación típica?**

R: Depende de la complejidad:
- Simulación simple (10-20 nodos, 100s): 5-10 minutos
- Simulación media (30-50 nodos, 200s): 15-25 minutos
- Simulación compleja (100+ nodos, 500s): 30-60 minutos

**P: ¿Puedo modificar el código generado manualmente?**

R: Sí. El código generado está en `simulations/scripts/` y puedes editarlo libremente. Es código Python estándar de NS-3.

**P: ¿El sistema funciona con otros simuladores además de NS-3?**

R: Actualmente solo NS-3. Sin embargo, la arquitectura es extensible y podrías adaptar los agentes para otros simuladores.

### 13.2 Preguntas Técnicas

**P: ¿Qué protocolos de enrutamiento están soportados?**

R: Todos los protocolos disponibles en NS-3:
- **Reactivos**: AODV, DSR, DYMO
- **Proactivos**: OLSR, DSDV
- **Híbridos**: ZRP (si está instalado)
- **Personalizados**: Puedes describir tu propio protocolo

**P: ¿Cómo aseguro la reproducibilidad de mis experimentos?**

R: El sistema automáticamente:
1. Configura semillas aleatorias fijas (RngSeedManager.SetSeed)
2. Documenta todos los parámetros en el código
3. Guarda logs completos de ejecución
4. Genera reportes con configuración exacta

Para reproducir: usa la misma semilla y parámetros.

**P: ¿Puedo ejecutar múltiples simulaciones en paralelo?**

R: Actualmente el sistema ejecuta una simulación a la vez. Para ejecutar múltiples:
```bash
# Terminal 1
python main.py

# Terminal 2 (en otro directorio)
cp -r sistema-a2a-v1.3 experimento2
cd experimento2
python main.py
```

**P: ¿Cómo exporto los resultados para mi paper?**

R: Los resultados están en:
- **Gráficos**: `simulations/visualizations/*.png` (alta resolución)
- **Datos**: `simulations/results/*.xml` (FlowMonitor)
- **Análisis**: `simulations/analysis/*.md` (reportes estadísticos)
- **Dashboard**: `simulations/visualizations/dashboard.html`

Todos los gráficos están en formato PNG de alta calidad, listos para LaTeX.

**P: ¿Puedo cambiar los modelos de LLM utilizados?**

R: Sí. Edita `config/settings.py`:
```python
OLLAMA_MODEL_REASONING = "llama3.1:8b"  # Cambiar aquí
OLLAMA_MODEL_CODING = "deepseek-coder-v2:16b"  # Cambiar aquí
```

Modelos recomendados:
- Razonamiento: llama3.1:8b, mistral:7b, phi3:14b
- Código: deepseek-coder-v2:16b, codellama:13b

### 13.3 Preguntas sobre Optimización

**P: ¿Cuándo debería usar Deep Reinforcement Learning?**

R: Usa DRL cuando:
- PDR < 80% (pérdida alta de paquetes)
- Delay > 150 ms (latencia alta)
- Escenarios complejos (alta movilidad, alta densidad)
- Quieres optimización adaptativa en tiempo real

NO uses DRL si los resultados ya son buenos (PDR > 90%, Delay < 50ms).

**P: ¿Cuánto tiempo tarda entrenar un modelo DRL?**

R: Típicamente 2-4 horas para 2000 episodios en hardware moderno (8 cores, 16GB RAM). Puedes reducir episodios para pruebas rápidas.

**P: ¿Necesito GPU para DRL?**

R: No es obligatorio pero ayuda. El sistema funciona con CPU. Con GPU (CUDA), el entrenamiento puede ser 3-5x más rápido.

**P: ¿Puedo comparar mi protocolo optimizado con el baseline?**

R: Sí. El sistema guarda ambas versiones:
- Baseline: Primera simulación
- Optimizado: Después de optimización

Compara los reportes estadísticos de ambos.

### 13.4 Preguntas sobre Análisis

**P: ¿Qué significa "routing overhead" y por qué es importante?**

R: Es la proporción de tráfico de control vs datos. Importante porque:
- Afecta consumo de energía (crítico en MANETs)
- Reduce ancho de banda disponible
- Indica eficiencia del protocolo

Valores típicos:
- AODV: 10-20% (eficiente)
- OLSR: 30-40% (alto pero aceptable)
- DSDV: 40-50% (muy alto)

**P: ¿Cómo interpreto los intervalos de confianza?**

R: Un intervalo de confianza del 95% significa que estamos 95% seguros de que el valor real está en ese rango.

Ejemplo: PDR = 94.5% [93.2%, 95.8%]
- Valor promedio: 94.5%
- Rango probable: entre 93.2% y 95.8%
- Rango estrecho = alta precisión

**P: ¿Qué es un p-value y cuándo es significativo?**

R: El p-value indica la probabilidad de que los resultados sean por azar.
- p < 0.05: Estadísticamente significativo (diferencia real)
- p ≥ 0.05: No significativo (podría ser azar)

Ejemplo: Si comparas AODV vs OLSR y p=0.001, la diferencia es real, no azar.

**P: ¿Puedo analizar archivos PCAP con otras herramientas?**

R: Sí. Los archivos PCAP están en formato estándar. Puedes usar:
- **Wireshark**: Análisis visual detallado
- **tcpdump**: Análisis por línea de comandos
- **Scapy**: Análisis programático en Python
- **tshark**: Análisis automatizado

Los archivos están en: `simulations/results/*.pcap`

### 13.5 Preguntas sobre Publicación

**P: ¿Puedo publicar resultados generados por el sistema?**

R: Sí, absolutamente. El sistema es una herramienta de investigación. Los resultados son tuyos. Asegúrate de:
1. Citar NS-3 correctamente
2. Documentar la metodología
3. Incluir parámetros de simulación
4. Mencionar reproducibilidad (semillas)

**P: ¿Cómo cito el sistema en mi paper?**

R: Puedes mencionar que usaste un framework de automatización basado en agentes de IA para NS-3. Ejemplo:

```latex
We used an AI-agent-based framework to automate the simulation workflow,
including code generation, execution, and analysis. All simulations were
conducted using NS-3 3.36 \cite{ns3} with reproducible random seeds.
```

**P: ¿Los revisores aceptarán resultados generados automáticamente?**

R: Sí, siempre que:
- Los resultados sean reproducibles (semillas documentadas)
- La metodología sea clara
- Los tests estadísticos sean rigurosos
- El código NS-3 sea válido y verificable

El sistema genera código estándar de NS-3, no hay diferencia con código escrito manualmente.

**P: ¿Dónde puedo encontrar ejemplos de papers que usen metodologías similares?**

R: Busca papers sobre:
- "Automated network simulation"
- "AI-driven protocol optimization"
- "Deep reinforcement learning for routing"
- "ns3-ai applications"

Conferencias relevantes: IEEE INFOCOM, ACM MobiCom, IEEE ICC, ICNP

---

## 14. Conclusión

### 14.1 Resumen

Has aprendido:

✅ **Qué es un sistema multi-agente** y por qué es útil  
✅ **Arquitectura del Sistema A2A** con sus 8 agentes  
✅ **Cómo instalar** el sistema paso a paso  
✅ **Cómo ejecutar** tu primera simulación  
✅ **Casos de uso comunes** para investigación  
✅ **Cómo interpretar** resultados y métricas  
✅ **Cuándo y cómo usar** optimización con DRL  
✅ **Cómo resolver** problemas comunes

### 14.2 Próximos Pasos

1. **Ejecuta tu primera simulación** siguiendo la Sección 8
2. **Experimenta con diferentes protocolos** (AODV, OLSR, DSDV)
3. **Compara resultados** usando los casos de uso de la Sección 9
4. **Explora optimización avanzada** con DRL (Sección 11)
5. **Publica tus resultados** usando los reportes generados

### 14.3 Para tu Paper

El sistema genera todo lo que necesitas:

✅ **Código NS-3** reproducible  
✅ **Resultados** con semillas documentadas  
✅ **Tests estadísticos** (T-Test, ANOVA, CI)  
✅ **Gráficos** en calidad de publicación  
✅ **Tablas** de métricas  
✅ **Análisis de overhead** desde PCAP  
✅ **Reportes** en formato académico

**Ejemplo de Sección de Resultados:**

```latex
\section{Results}

We conducted simulations using NS-3 3.36 with the AODV routing protocol.
The network consisted of 20 mobile nodes in a 1000×1000m area, using the
RandomWaypoint mobility model with speeds between 5-15 m/s. Each simulation
ran for 200 seconds with a fixed random seed (12345) for reproducibility.

\subsection{Performance Metrics}

Table~\ref{tab:results} shows the main performance metrics. The AODV protocol
achieved a Packet Delivery Ratio (PDR) of 94.5\% (95\% CI: [93.2\%, 95.8\%]),
with an average end-to-end delay of 38.2 ms (95\% CI: [35.1, 41.3]). The
routing overhead, calculated from PCAP traces, was 12.3\%, which is consistent
with the literature \cite{perkins2003}.

A t-test comparing successful and failed flows showed a statistically
significant difference (t=5.234, p<0.001), indicating that...
```

### 14.4 Ventajas para tu Investigación

**Productividad:**
- 10-20x más rápido que manual
- Automatización completa del ciclo

**Calidad:**
- Reproducibilidad garantizada
- Rigor estadístico automático
- Análisis profundo (PCAP + overhead)

**Innovación:**
- Optimización con Deep Learning
- Propuestas automáticas de mejora
- Estado del arte en automatización

---

## 15. Glosario para Investigadores de Redes

**Agente**: Programa autónomo con un objetivo específico

**LLM (Large Language Model)**: Modelo de IA que entiende y genera texto

**LangGraph**: Framework para orquestar sistemas multi-agente

**Ollama**: Plataforma para ejecutar LLMs localmente

**Estado Compartido**: Estructura de datos que los agentes usan para comunicarse

**FlowMonitor**: Módulo de NS-3 para recolectar métricas de flujos

**PCAP**: Formato de archivo para capturas de paquetes

**Scapy**: Librería Python para análisis de paquetes

**DRL (Deep Reinforcement Learning)**: Técnica de IA para optimización

**ns3-ai**: Módulo de NS-3 para integrar IA

**CI (Confidence Interval)**: Intervalo de confianza estadístico

**T-Test**: Test estadístico para comparar dos grupos

**ANOVA**: Test estadístico para comparar múltiples grupos

---

## 16. Referencias

### Papers Relevantes

1. **AODV**: Perkins et al., "Ad hoc On-Demand Distance Vector Routing", RFC 3561, 2003
2. **OLSR**: Clausen et al., "Optimized Link State Routing Protocol", RFC 3626, 2003
3. **ns3-ai**: Yin et al., "ns3-ai: Integrating AI with Network Simulators", 2020
4. **Multi-Agent Systems**: Wooldridge, "An Introduction to MultiAgent Systems", 2009

### Documentación Técnica

- **NS-3**: https://www.nsnam.org/documentation/
- **Ollama**: https://ollama.ai/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Scapy**: https://scapy.net/

---

**¡Éxito en tu investigación!** 🎓🚀

---

**Versión**: 1.3  
**Fecha**: Noviembre 2025  
**Autor**: Sistema A2A  
**Contacto**: Ver documentación en `docs/`
