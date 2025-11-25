# 🔧 INSTRUCCIONES: Integración del Trace Analyzer en Supervisor

**Archivo a modificar**: `supervisor.py`

---

## 📋 CAMBIOS NECESARIOS

### 1. Importar el Nuevo Agente

**Ubicación**: Inicio del archivo, sección de imports

```python
from agents import (
    research_node,
    coder_node,
    simulator_node,
    analyst_node,
    visualizer_node,
    github_manager_node,
    optimizer_node,
    trace_analyzer_node  # ← AÑADIR ESTA LÍNEA
)
```

---

### 2. Añadir Nodo al Grafo

**Ubicación**: Método `__init__` de `SupervisorOrchestrator`

```python
def __init__(self):
    """Inicializa el orquestador"""
    # Crear grafo de estados
    self.workflow = StateGraph(AgentState)
    
    # Añadir nodos (agentes)
    self.workflow.add_node("researcher", research_node)
    self.workflow.add_node("coder", coder_node)
    self.workflow.add_node("simulator", simulator_node)
    self.workflow.add_node("trace_analyzer", trace_analyzer_node)  # ← AÑADIR
    self.workflow.add_node("analyst", analyst_node)
    self.workflow.add_node("visualizer", visualizer_node)
    self.workflow.add_node("optimizer", optimizer_node)
    self.workflow.add_node("github_manager", github_manager_node)
    
    # ... resto del código
```

---

### 3. Actualizar Flujo de Trabajo

**Ubicación**: Método `_define_workflow`

**OPCIÓN A: Trace Analyzer Siempre Activo**

```python
def _define_workflow(self):
    """Define el flujo de trabajo entre agentes"""
    
    # ... código existente hasta simulator ...
    
    # Lógica condicional: ¿La simulación fue exitosa?
    self.workflow.add_conditional_edges(
        "simulator",
        self._should_retry_simulation,
        {
            "trace_analyzer": "trace_analyzer",  # ← CAMBIAR de "analyst"
            "retry_code": "coder",
            "end": END
        }
    )
    
    # Trace Analyzer → Analyst (NUEVO)
    self.workflow.add_edge("trace_analyzer", "analyst")
    
    # ... resto del flujo sin cambios ...
```

**OPCIÓN B: Trace Analyzer Condicional (Recomendado)**

```python
def _define_workflow(self):
    """Define el flujo de trabajo entre agentes"""
    
    # ... código existente hasta simulator ...
    
    # Lógica condicional: ¿La simulación fue exitosa?
    self.workflow.add_conditional_edges(
        "simulator",
        self._should_retry_simulation,
        {
            "trace_analyzer": "trace_analyzer",  # ← CAMBIAR
            "retry_code": "coder",
            "end": END
        }
    )
    
    # Trace Analyzer → Analyst (condicional)
    self.workflow.add_conditional_edges(
        "trace_analyzer",
        self._should_skip_trace_analysis,
        {
            "analyst": "analyst",
            "skip": "analyst"  # Si no hay PCAP o tshark, saltar
        }
    )
    
    # ... resto del flujo sin cambios ...
```

---

### 4. Añadir Función de Decisión (Solo para Opción B)

**Ubicación**: Después de `_should_optimize`

```python
def _should_skip_trace_analysis(self, state: AgentState) -> Literal["analyst", "skip"]:
    """
    Decide si saltar el análisis de trazas
    
    Args:
        state: Estado actual
        
    Returns:
        Siguiente nodo a ejecutar
    """
    # Si no hay archivos PCAP, saltar
    if not state.get('pcap_files'):
        print("\nℹ️  No hay archivos PCAP - Saltando análisis de trazas")
        return "skip"
    
    # Si hay error en trace_analysis, saltar
    if state.get('trace_analysis') and 'error' in str(state.get('trace_analysis')):
        print("\n⚠️  Error en análisis de trazas - Continuando sin análisis")
        return "skip"
    
    # Continuar normalmente
    return "analyst"
```

---

### 5. Actualizar Función `_should_retry_simulation`

**Ubicación**: Método existente

```python
def _should_retry_simulation(self, state: AgentState) -> Literal["trace_analyzer", "retry_code", "end"]:
    """
    Decide qué hacer después de simulación
    
    Args:
        state: Estado actual
        
    Returns:
        Siguiente nodo a ejecutar
    """
    sim_status = state.get('simulation_status', '')
    
    # Si simulación exitosa
    if sim_status == 'completed':
        return "trace_analyzer"  # ← CAMBIAR de "analyst"
    
    # Si falló y no se excedió límite
    if sim_status == 'failed' and state['iteration_count'] < state['max_iterations']:
        print(f"\n🔄 Reintentando desde código (iteración {state['iteration_count']}/{state['max_iterations']})")
        return "retry_code"
    
    # Si se excedió límite
    print(f"\n⚠️  Límite de iteraciones alcanzado ({state['max_iterations']})")
    return "end"
```

---

## 🎯 FLUJO FINAL

```
Investigador
    ↓
Programador (genera código con PCAP)
    ↓
Simulador (ejecuta y genera .xml + .pcap)
    ↓
Trace Analyzer (analiza PCAP con tshark) ← NUEVO
    ↓
Analista (calcula KPIs + tests estadísticos)
    ↓
[Decisión de optimización]
    ├─ Visualizador → GitHub Manager → FIN
    └─ Optimizador → Programador (ciclo)
```

---

## ✅ VERIFICACIÓN

Después de hacer los cambios, verificar:

```python
# En supervisor.py, al final del archivo:
if __name__ == "__main__":
    supervisor = SupervisorOrchestrator()
    
    # Verificar que trace_analyzer esté en el grafo
    print("Nodos en el grafo:")
    for node in supervisor.workflow.nodes:
        print(f"  - {node}")
    
    # Debe aparecer: trace_analyzer
```

---

## 🔧 CÓDIGO COMPLETO DE REFERENCIA

### Imports Completos:

```python
from agents import (
    research_node,
    coder_node,
    simulator_node,
    trace_analyzer_node,
    analyst_node,
    visualizer_node,
    github_manager_node,
    optimizer_node
)
```

### Nodos Completos:

```python
self.workflow.add_node("researcher", research_node)
self.workflow.add_node("coder", coder_node)
self.workflow.add_node("simulator", simulator_node)
self.workflow.add_node("trace_analyzer", trace_analyzer_node)
self.workflow.add_node("analyst", analyst_node)
self.workflow.add_node("visualizer", visualizer_node)
self.workflow.add_node("optimizer", optimizer_node)
self.workflow.add_node("github_manager", github_manager_node)
```

### Flujo Completo (Opción Recomendada):

```python
def _define_workflow(self):
    """Define el flujo de trabajo entre agentes"""
    
    # Punto de entrada: Investigador
    self.workflow.set_entry_point("researcher")
    
    # Flujo: Investigador → Programador
    self.workflow.add_edge("researcher", "coder")
    
    # Lógica condicional: ¿El código es válido?
    self.workflow.add_conditional_edges(
        "coder",
        self._should_retry_code,
        {
            "simulator": "simulator",
            "retry": "coder",
            "end": END
        }
    )
    
    # Lógica condicional: ¿La simulación fue exitosa?
    self.workflow.add_conditional_edges(
        "simulator",
        self._should_retry_simulation,
        {
            "trace_analyzer": "trace_analyzer",
            "retry_code": "coder",
            "end": END
        }
    )
    
    # Trace Analyzer → Analyst
    self.workflow.add_edge("trace_analyzer", "analyst")
    
    # Análisis → Decisión de optimización
    self.workflow.add_conditional_edges(
        "analyst",
        self._should_optimize,
        {
            "visualizer": "visualizer",
            "optimizer": "optimizer"
        }
    )
    
    # Optimizador → Programador (ciclo de optimización)
    self.workflow.add_edge("optimizer", "coder")
    
    # Visualización → GitHub Manager
    self.workflow.add_edge("visualizer", "github_manager")
    
    # GitHub Manager → Fin
    self.workflow.add_edge("github_manager", END)
```

---

## 📝 NOTAS IMPORTANTES

1. **Orden de Nodos**: El Trace Analyzer debe ir DESPUÉS del Simulator y ANTES del Analyst

2. **Manejo de Errores**: Si tshark no está disponible, el Trace Analyzer lo detecta y continúa sin fallar

3. **Archivos PCAP**: El Simulator debe actualizar el estado con `pcap_files` para que el Trace Analyzer los encuentre

4. **Rendimiento**: El análisis de PCAP puede tomar tiempo, considerar timeout si es necesario

---

## 🚀 TESTING

Después de integrar, probar con:

```python
supervisor = SupervisorOrchestrator()
result = supervisor.run_experiment(
    task="Simular protocolo AODV con 10 nodos",
    max_iterations=2
)

# Verificar que se ejecutó trace_analyzer
if result and 'trace_analysis' in result:
    print("✅ Trace Analyzer ejecutado correctamente")
    print(f"   Archivos analizados: {len(result.get('pcap_files', []))}")
else:
    print("⚠️  Trace Analyzer no se ejecutó")
```

---

**Versión**: 1.4  
**Fecha**: 2024-11-23  
**Estado**: Instrucciones Completas
