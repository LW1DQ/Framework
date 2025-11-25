# Changelog

Todas las mejoras notables del proyecto "Sistema A2A" se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [v1.4.0] - 2025-11-25

### 🚀 Nuevo
- **Agente de IA (PPO)**: Implementación real de Deep Reinforcement Learning usando PyTorch.
  - Red Neuronal Actor-Critic.
  - Entrenamiento episódico automático.
  - Persistencia de modelos (`.pth`).
- **Integración NS-3 AI**: Soporte nativo para `ns3-ai` usando memoria compartida (RingBuffer) para alta velocidad.
- **Manejo de Errores Estructurado**: Sistema robusto de auto-corrección.
  - Nuevas excepciones: `CompilationError`, `SimulationError`, `TimeoutError`.
  - Estrategias de recuperación inteligentes en Agente Programador.
- **Dashboard en Tiempo Real**: Panel de control interactivo con Streamlit.
- **Logging Centralizado**: Sistema de telemetría y auditoría.

### 🐛 Corregido
- Validación de imports en `optimizer.py`.
- Manejo de rutas en `ns3_ai_integration.py`.

---

## [v1.3] - 2025-11-20

### 🚀 Nuevo
- **Trace Analyzer**: Nuevo agente para análisis de archivos PCAP.
- **Estadística Rigurosa**: Cálculo de intervalos de confianza y tests de hipótesis (T-Test, ANOVA).

### ⚡ Mejorado
- **Reproducibilidad**: Gestión centralizada de semillas aleatorias (`RngSeedManager`).
- **Reportes**: Generación de informes académicos en Markdown.

---

## [v1.0 - v1.2]
- Desarrollo inicial del sistema multi-agente.
- Integración básica con LangGraph y Ollama.
- Soporte para protocolos AODV, OLSR, DSDV.
