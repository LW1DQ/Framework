# 📚 Índice de Documentación - Sistema A2A v1.3

## Guía de Navegación

---

## 🚀 Para Empezar (Leer en Orden)

### 1. Inicio Rápido
- **EMPIEZA-AQUI.txt** ⭐ - Punto de entrada principal
- **QUICK-START-v1.3.txt** - Inicio en 5 minutos
- **README.md** - Descripción general del proyecto

### 2. Instalación
- **docs/INSTALACION-COMPLETA.md** - Instalación de NS-3 y dependencias
- **requirements.txt** - Lista de dependencias Python
- **install.sh** - Script de instalación automática (Linux/Mac)

### 3. Uso Básico
- **docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md** - Guía completa de uso
- **docs/FLUJO-ACTUALIZADO-v1.3.txt** - Diagrama de flujo del sistema
- **docs/MAPA-VISUAL-v1.3.txt** - Mapa visual de la arquitectura

---

## 📖 Documentación Técnica

### Mejoras Implementadas
- **docs/MEJORAS-IMPLEMENTADAS-FINAL.md** - Detalles de todas las mejoras v1.3
- **docs/IMPLEMENTACION-RECOMENDACIONES-TUTOR.md** - Recomendaciones del tutor

### Instalación Avanzada
- **docs/INSTALACION-NS3-AI.md** - Instalación de ns3-ai para DRL

### Estado del Proyecto
- **docs/ESTADO-FINAL-Y-PROXIMOS-PASOS.md** - Estado actual y próximos pasos

---

## 🧪 Pruebas y Verificación

- **test_integration.py** - Script de prueba de integración
- Ejecutar: `python test_integration.py`

---

## 💻 Código Fuente

### Estructura Principal

```
agents/
├── researcher.py          # Agente de investigación
├── coder.py              # Generador de código NS-3
├── simulator.py          # Ejecutor de simulaciones
├── trace_analyzer.py     # Analizador de PCAP
├── analyst.py            # Calculador de KPIs
├── visualizer.py         # Generador de gráficos
├── optimizer.py          # Optimizador con DRL
├── github_manager.py     # Gestor de resultados
└── ns3_ai_integration.py # Integración ns3-ai

config/
└── settings.py           # Configuración global

utils/
├── state.py              # Gestión de estado
├── statistical_tests.py  # Tests estadísticos
└── logging.py            # Sistema de logs

main.py                   # Punto de entrada
supervisor.py             # Orquestador LangGraph
```

---

## 📊 Ejemplos

### Directorio examples/

- **ejemplo_basico.py** - Simulación básica
- **ejemplo_completo.py** - Simulación con todas las funcionalidades
- **ejemplo_drl.py** - Simulación con Deep Learning

---

## 🎯 Casos de Uso

### 1. Simulación Básica

```bash
python main.py
# Tarea: "Simular MANET con AODV, 20 nodos, 200 segundos"
```

### 2. Análisis de Overhead

Ver: `docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md` - Sección 3

### 3. Tests Estadísticos

Ver: `docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md` - Secciones 4-5

### 4. Optimización con DRL

Ver: `docs/INSTALACION-NS3-AI.md`

---

## 🔍 Búsqueda Rápida

### ¿Cómo hacer X?

**¿Cómo ejecutar una simulación?**
→ QUICK-START-v1.3.txt

**¿Cómo analizar archivos PCAP?**
→ docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md (Sección 2)

**¿Cómo calcular overhead de enrutamiento?**
→ docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md (Sección 3)

**¿Cómo hacer tests estadísticos?**
→ docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md (Secciones 4-5)

**¿Cómo garantizar reproducibilidad?**
→ docs/GUIA-USO-NUEVAS-FUNCIONALIDADES.md (Sección 1)

**¿Cómo instalar ns3-ai?**
→ docs/INSTALACION-NS3-AI.md

**¿Qué cambió en v1.3?**
→ docs/MEJORAS-IMPLEMENTADAS-FINAL.md

---

## 🆘 Troubleshooting

### Problemas Comunes

1. **Error de imports**
   - Solución: `pip install -r requirements.txt`

2. **NS-3 no encontrado**
   - Solución: Verificar `config/settings.py`

3. **Ollama no disponible**
   - Solución: Instalar desde https://ollama.ai

4. **ns3-ai no funciona**
   - Solución: Ver `docs/INSTALACION-NS3-AI.md`

---

## 📞 Soporte

Para más ayuda:
1. Revisar este índice
2. Consultar documentación específica
3. Ejecutar `python test_integration.py` para diagnóstico

---

## 📊 Estadísticas

- **Documentos totales**: 10
- **Ejemplos**: 3
- **Scripts de prueba**: 1
- **Agentes**: 8

---

**Versión**: 1.3  
**Fecha**: Noviembre 2025  
**Estado**: ✅ Completo
