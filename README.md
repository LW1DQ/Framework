# 🚀 Sistema A2A v1.3 - Framework Multi-Agente para Simulación de Redes

[![Version](https://img.shields.io/badge/version-1.3-blue.svg)](https://github.com/tu-usuario/sistema-a2a)
[![NS-3](https://img.shields.io/badge/NS--3-3.36+-green.svg)](https://www.nsnam.org/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Descripción

**Sistema A2A (Agent-to-Agent)** es un framework multi-agente que automatiza completamente el ciclo de investigación en simulaciones de redes MANET/VANET usando NS-3. Diseñado para investigadores de redes que quieren enfocarse en la investigación, no en la programación repetitiva.

### ✨ Características Principales

- 🤖 **8 Agentes Especializados** - Cada uno experto en su tarea
- 🎲 **Reproducibilidad Total** - Control de semillas aleatorias
- 📡 **Análisis PCAP Automático** - Captura y análisis de tráfico
- 📊 **Tests Estadísticos** - T-Test, ANOVA, Intervalos de Confianza
- 🚀 **Optimización con DRL** - Deep Reinforcement Learning integrado
- 📈 **Visualización Automática** - Gráficos y dashboards
- 📝 **Reportes Académicos** - Listos para papers

---

## 🎯 ¿Para Quién es Este Sistema?

✅ **Investigadores de redes** sin experiencia en IA/ML  
✅ **Estudiantes de posgrado** en redes de comunicación  
✅ **Profesores** que enseñan simulación de redes  
✅ **Ingenieros** que trabajan con protocolos de enrutamiento

**No necesitas saber de IA** - Solo describe tu experimento en lenguaje natural.

---

## 🚀 Inicio Rápido

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/sistema-a2a.git
cd sistema-a2a
```

### 2. Elegir la Versión

```bash
cd sistema-a2a-v1.3-final
```

### 3. Instalar Dependencias

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar NS-3 y Ollama

Ver [Guía de Instalación Completa](INSTRUCCIONES-UBUNTU.md) para instrucciones detalladas.

### 5. Ejecutar Primera Simulación

```bash
python main.py
```

Describe tu experimento:
```
Simular una red MANET con protocolo AODV, 20 nodos móviles, 
área de 1000x1000 metros, durante 200 segundos
```

---

## 📚 Documentación

### 📖 Guías Principales

| Guía | Descripción | Audiencia |
|------|-------------|-----------|
| [**Guía para Investigadores de Redes**](GUIA-INVESTIGADORES-REDES.md) | Guía completa de 50+ páginas | Investigadores sin experiencia en IA |
| [**Instrucciones de Instalación Ubuntu**](INSTRUCCIONES-UBUNTU.md) | Instalación paso a paso en Ubuntu | Todos los usuarios |
| [**Inicio Rápido**](sistema-a2a-v1.3-final/EMPIEZA-AQUI.txt) | Empieza en 5 minutos | Usuarios con experiencia |

### 📑 Documentación Adicional

- [**Índice de Navegación**](INDICE-GUIA-INVESTIGADORES.md) - Encuentra temas rápidamente
- [**FAQ**](GUIA-INVESTIGADORES-REDES.md#13-preguntas-frecuentes-faq) - 25 preguntas frecuentes
- [**Casos de Uso**](GUIA-INVESTIGADORES-REDES.md#9-casos-de-uso-comunes) - 5 ejemplos prácticos
- [**Troubleshooting**](GUIA-INVESTIGADORES-REDES.md#12-troubleshooting) - Solución de problemas

### 🔧 Documentación Técnica

En `sistema-a2a-v1.3-final/docs/`:
- `GUIA-USO-NUEVAS-FUNCIONALIDADES.md` - Funcionalidades v1.3
- `INSTALACION-COMPLETA.md` - Instalación de NS-3
- `INSTALACION-NS3-AI.md` - Instalación de ns3-ai para DRL
- `MEJORAS-IMPLEMENTADAS-FINAL.md` - Detalles técnicos

---

## 🎓 Ejemplo de Uso

### Comparar AODV vs OLSR

```python
# Simulación 1: AODV
python main.py
> "Simular MANET con AODV, 20 nodos, 200 segundos"

# Simulación 2: OLSR
python main.py
> "Simular MANET con OLSR, 20 nodos, 200 segundos"

# El sistema genera automáticamente:
# - Código NS-3
# - Archivos PCAP
# - Métricas (PDR, delay, throughput, overhead)
# - Tests estadísticos
# - Gráficos comparativos
# - Reporte académico
```

### Resultados Obtenidos

```
📊 RESULTADOS - AODV
PDR: 94.5% [93.2%, 95.8%] (95% CI)
Delay: 38.2 ms [35.1, 41.3]
Throughput: 1.85 Mbps
Overhead: 12.3%
Clasificación: Excelente ✅

📊 RESULTADOS - OLSR
PDR: 92.1% [90.8%, 93.4%]
Delay: 52.7 ms [49.2, 56.2]
Throughput: 1.92 Mbps
Overhead: 28.5%
Clasificación: Bueno ✅
```

---

## 🏗️ Arquitectura

### Los 8 Agentes Especializados

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO (Investigador)                    │
│  Input: "Simular MANET con AODV, 20 nodos, 200 segundos"   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SUPERVISOR (LangGraph)                    │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  🔍 Researcher → 💻 Coder → 🚀 Simulator → 📡 Trace Analyzer │
│  📊 Analyst → 📈 Visualizer → 🔧 Optimizer → 📦 GitHub Mgr   │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESULTADOS COMPLETOS                      │
│  • Código NS-3  • PCAP  • Métricas  • Gráficos  • Reporte  │
└─────────────────────────────────────────────────────────────┘
```

### Flujo de Trabajo

1. **Researcher** - Investiga sobre el protocolo
2. **Coder** - Genera código NS-3 con semillas y PCAP
3. **Simulator** - Ejecuta la simulación
4. **Trace Analyzer** - Analiza archivos PCAP
5. **Analyst** - Calcula KPIs y tests estadísticos
6. **Visualizer** - Genera gráficos y dashboard
7. **Optimizer** - Propone mejoras con DRL (si es necesario)
8. **GitHub Manager** - Organiza y documenta resultados

---

## 📊 Métricas Calculadas

| Métrica | Descripción | Análisis |
|---------|-------------|----------|
| **PDR** | Packet Delivery Ratio | % de paquetes entregados |
| **Delay** | Latencia end-to-end | Tiempo promedio de entrega |
| **Throughput** | Tasa de datos | Mbps efectivos |
| **Overhead** | Tráfico de control | Calculado desde PCAP |
| **Jitter** | Variación de delay | Estabilidad de la red |

### Tests Estadísticos

- ✅ **T-Test** - Comparar dos grupos
- ✅ **ANOVA** - Comparar múltiples grupos
- ✅ **Intervalos de Confianza (95% CI)** - Precisión de resultados
- ✅ **P-values** - Significancia estadística

---

## 🔧 Requisitos

### Software Necesario

- **Python 3.8+**
- **NS-3 3.36+** ([Instalación](INSTRUCCIONES-UBUNTU.md))
- **Ollama** ([Instalación](https://ollama.ai))

### Dependencias Python

```txt
langchain_ollama>=0.1.0
langgraph>=0.2.0
scipy>=1.11.0
numpy>=1.24.0
pandas>=2.0.0
scapy>=2.5.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

### Hardware Recomendado

- **CPU**: 8+ cores
- **RAM**: 16 GB
- **Disco**: 50 GB libres

---

## 🎯 Casos de Uso

### 1. Comparar Protocolos
Compara AODV, OLSR, DSDV, DSR en las mismas condiciones.

### 2. Evaluar Movilidad
Analiza el impacto de diferentes velocidades de nodos.

### 3. Optimizar con DRL
Mejora protocolos usando Deep Reinforcement Learning.

### 4. Validar Reproducibilidad
Verifica que tus resultados sean reproducibles.

### 5. Análisis de Overhead
Calcula el overhead real desde capturas PCAP.

Ver [Casos de Uso Completos](GUIA-INVESTIGADORES-REDES.md#9-casos-de-uso-comunes)

---

## 📈 Resultados para Papers

El sistema genera todo lo necesario para publicaciones:

✅ **Código NS-3** reproducible con semillas documentadas  
✅ **Resultados** con tests estadísticos rigurosos  
✅ **Gráficos** en calidad de publicación (PNG, SVG)  
✅ **Tablas** de métricas con intervalos de confianza  
✅ **Análisis de overhead** calculado desde PCAP  
✅ **Reportes** en formato académico

### Ejemplo para LaTeX

```latex
\section{Results}
We conducted simulations using NS-3 3.36 with the AODV routing protocol.
The network consisted of 20 mobile nodes in a 1000×1000m area. Each 
simulation ran for 200 seconds with a fixed random seed (12345) for 
reproducibility.

The AODV protocol achieved a Packet Delivery Ratio (PDR) of 94.5\% 
(95\% CI: [93.2\%, 95.8\%]), with an average end-to-end delay of 38.2 ms 
(95\% CI: [35.1, 41.3]). The routing overhead, calculated from PCAP traces, 
was 12.3\%, consistent with the literature.

A t-test comparing successful and failed flows showed a statistically 
significant difference (t=5.234, p<0.001)...
```

---

## 🆘 Soporte

### Problemas Comunes

| Problema | Solución |
|----------|----------|
| NS-3 not found | Ver [Instalación NS-3](INSTRUCCIONES-UBUNTU.md) |
| Ollama not responding | `ollama serve` |
| Import errors | `pip install -r requirements.txt` |
| Simulation timeout | Reducir nodos o tiempo |

### Obtener Ayuda

1. **Consulta el [FAQ](GUIA-INVESTIGADORES-REDES.md#13-preguntas-frecuentes-faq)** - 25 preguntas comunes
2. **Revisa [Troubleshooting](GUIA-INVESTIGADORES-REDES.md#12-troubleshooting)** - Problemas típicos
3. **Abre un Issue** en GitHub
4. **Lee la [Guía Completa](GUIA-INVESTIGADORES-REDES.md)** - 50+ páginas

---

## 🗂️ Estructura del Proyecto

```
sistema-a2a/
├── sistema-a2a-v1.3-final/          ← 🎯 VERSIÓN ACTUAL
│   ├── agents/                       • 8 agentes especializados
│   │   ├── researcher.py
│   │   ├── coder.py
│   │   ├── simulator.py
│   │   ├── trace_analyzer.py
│   │   ├── analyst.py
│   │   ├── visualizer.py
│   │   ├── optimizer.py
│   │   └── github_manager.py
│   ├── config/                       • Configuración
│   ├── utils/                        • Utilidades
│   ├── docs/                         • Documentación técnica
│   ├── main.py                       • Punto de entrada
│   ├── supervisor.py                 • Orquestador LangGraph
│   └── requirements.txt              • Dependencias
│
├── GUIA-INVESTIGADORES-REDES.md     • Guía completa (50+ páginas)
├── INSTRUCCIONES-UBUNTU.md          • Instalación en Ubuntu
├── INDICE-GUIA-INVESTIGADORES.md    • Navegación rápida
├── README.md                         • Este archivo
└── versiones-anteriores/            • Versiones previas
```

---

## 📝 Changelog

### v1.3 (Noviembre 2025) - Actual

**Nuevas Funcionalidades:**
- ✅ Control de semillas aleatorias (reproducibilidad)
- ✅ Captura y análisis automático de PCAP
- ✅ Cálculo de overhead de enrutamiento desde PCAP
- ✅ Tests estadísticos (T-Test, ANOVA, CI)
- ✅ Integración ns3-ai para Deep Reinforcement Learning
- ✅ Trace Analyzer como agente independiente
- ✅ Reportes estadísticos automáticos

**Mejoras:**
- 📈 Análisis más profundo de tráfico
- 🎲 Reproducibilidad científica garantizada
- 📊 Rigor estadístico mejorado
- 🤖 Optimización con DRL

### v1.2 (Octubre 2025)

- Mejoras iniciales en análisis
- Trace analyzer básico

### v1.1 (Septiembre 2025)

- Versión base del sistema
- 8 agentes especializados

---

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **NS-3 Team** - Por el excelente simulador
- **LangChain** - Por el framework de agentes
- **Ollama** - Por los LLMs locales
- **Scapy** - Por el análisis de paquetes
- **Comunidad de investigadores** - Por el feedback

---

## 📞 Contacto

- **GitHub Issues**: Para reportar bugs o solicitar funcionalidades
- **Documentación**: Ver [Guía Completa](GUIA-INVESTIGADORES-REDES.md)
- **Email**: [tu-email@ejemplo.com]

---

## 🌟 Star History

Si este proyecto te ayuda en tu investigación, considera darle una ⭐ en GitHub!

---

## 📊 Estadísticas

- **Líneas de código**: ~5,000+
- **Agentes**: 8 especializados
- **Protocolos soportados**: AODV, OLSR, DSDV, DSR, y más
- **Tests estadísticos**: 3 tipos
- **Documentación**: 50+ páginas

---

## 🎓 Citar Este Trabajo

Si usas este sistema en tu investigación, por favor cita:

```bibtex
@software{sistema_a2a_2025,
  title = {Sistema A2A: Framework Multi-Agente para Simulación de Redes},
  author = {Tu Nombre},
  year = {2025},
  version = {1.3},
  url = {https://github.com/tu-usuario/sistema-a2a}
}
```

---

**¡Éxito en tu investigación!** 🎓🚀

---

**Versión**: 1.3 Final  
**Fecha**: Noviembre 2025  
**Estado**: ✅ Producción
