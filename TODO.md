# 📋 TODO - Sistema A2A v1.4

## Tareas Pendientes y Mejoras Identificadas

**Fecha de análisis:** 25 de Noviembre de 2025  
**Versión actual:** 1.4  
## 🔴 PRIORIDAD ALTA (Crítico)

### 1. Conectar Dashboard al Flujo Principal (COMPLETADO)
**Problema:** El dashboard lee archivos estáticos pero no se actualiza durante la ejecución de `main.py`

**Estado:** ✅ Completado en v1.4

**Solución Implementada:**
```python
# En cada agente (researcher.py, coder.py, simulator.py, etc.)
from utils.logging_utils import update_agent_status, log_message, log_metric

def agent_node(state: AgentState) -> Dict:
    # Al inicio del agente
    update_agent_status("NombreAgente", "running", state['task'])
    log_message("NombreAgente", "Iniciando procesamiento...")
    
    # Durante el procesamiento
    log_message("NombreAgente", "Analizando resultados...")
    
    # Al finalizar (si hay métricas)
    if 'metrics' in result:
        log_metric(
            pdr=result['metrics']['avg_pdr'],
            delay=result['metrics']['avg_delay'],
            throughput=result['metrics']['avg_throughput']
        )
    
    return result
```

**Estimación:** 2-3 horas  
**Impacto:** Alto - Mejora experiencia de usuario significativamente

---

### 2. Integración Real con ns3-ai
**Problema:** La comunicación con NS-3 está simulada con datos aleatorios

**Archivo afectado:**
- `agents/ns3_ai_integration.py` línea ~95

**Código actual:**
```python
def get_network_state(node_id):
    """Placeholder: En producción conectar con Tracing de NS-3"""
    return np.random.rand(STATE_DIM)  # ⚠️ Datos simulados
```

**Solución requerida:**
1. Instalar ns3-ai en NS-3:
   ```bash
   cd ~/ns-3-dev/contrib
   git clone https://github.com/hust-diangroup/ns3-ai.git
   cd ~/ns-3-dev
   ./ns3 configure --enable-examples
   ./ns3 build
   ```

2. Implementar shared memory communication:
   ```python
   from ns3ai_gym_env import Ns3Env
   
   def get_network_state(node_id):
       # Leer desde shared memory de ns3-ai
       state = ns3_env.get_state()
       return state
   ```

3. Modificar código generado para escribir estados a shared memory

**Estimación:** 1-2 semanas (requiere aprendizaje de ns3-ai)  
**Impacto:** Crítico para DRL funcional real

**Referencias:**
- https://github.com/hust-diangroup/ns3-ai
- https://github.com/hust-diangroup/ns3-ai/wiki

---

### 3. Validación Sintáctica Robusta
**Problema:** La validación de código solo verifica imports y estructura básica

**Archivo afectado:**
- `agents/simulator.py` función `validate_code_before_execution()`

**Código actual:**
```python
def validate_code_before_execution(code: str) -> tuple[bool, str]:
    # Solo verifica strings en el código
    if 'def main()' not in code:
        return False, "Falta función main()"
```

**Solución:**
```python
import ast
import subprocess

def validate_code_before_execution(code: str) -> tuple[bool, str]:
    # 1. Validación sintáctica con AST
    try:
        ast.parse(code)
    except SyntaxError as e:
        return False, f"Error de sintaxis en línea {e.lineno}: {e.msg}"
    
    # 2. Validación de imports (opcional)
    try:
        result = subprocess.run(
            ['python', '-m', 'py_compile', '-'],
            input=code.encode(),
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            return False, f"Error de compilación: {result.stderr.decode()}"
    except subprocess.TimeoutExpired:
        return False, "Timeout en validación"
    
    # 3. Verificaciones específicas de NS-3
    required_imports = ['ns.core', 'ns.network']
    missing = [imp for imp in required_imports if imp not in code]
    if missing:
        return False, f"Faltan imports críticos: {', '.join(missing)}"
    
    return True, "Código válido"
```

**Estimación:** 2-3 horas  
**Impacto:** Alto - Previene errores de ejecución

---

## 🟡 PRIORIDAD MEDIA (Importante)

### 4. Tests Unitarios y de Integración
**Problema:** Cobertura de tests ~10%, solo existe `tests/test_basic.py`

**Archivos a crear:**
```
tests/
├── test_optimizer.py          # Tests del optimizador
├── test_ns3_integration.py    # Tests de integración NS-3
├── test_state_management.py   # Tests del estado
├── test_agents.py             # Tests de cada agente
└── test_end_to_end.py         # Test completo del flujo
```

**Ejemplo de test:**
```python
# tests/test_optimizer.py
import pytest
from agents.optimizer import analyze_performance_bottlenecks

def test_analyze_bottlenecks_critical():
    kpis = {
        'avg_pdr': 65.0,
        'avg_delay': 180.0,
        'avg_throughput': 0.3
    }
    result = analyze_performance_bottlenecks(kpis)
    
    assert len(result['critical']) > 0
    assert any(b['metric'] == 'PDR' for b in result['critical'])
    assert any(b['metric'] == 'Delay' for b in result['critical'])

def test_analyze_bottlenecks_optimal():
    kpis = {
        'avg_pdr': 95.0,
        'avg_delay': 45.0,
        'avg_throughput': 2.5
    }
    result = analyze_performance_bottlenecks(kpis)
    
    assert len(result['critical']) == 0
    assert len(result['moderate']) == 0

# Ejecutar: pytest tests/ -v --cov=agents
```

**Estimación:** 1 semana  
**Impacto:** Medio - Mejora confiabilidad y mantenibilidad

---

### 5. Manejo de Errores Estructurado
**Problema:** Uso excesivo de `except Exception as e` genérico

**Archivos afectados:**
- Múltiples archivos en `agents/`
- `supervisor.py`
- `main.py`

**Solución:**
```python
# Crear utils/exceptions.py
class A2AException(Exception):
    """Excepción base del sistema A2A"""
    pass

class SimulationError(A2AException):
    """Error durante la simulación NS-3"""
    pass

class CodeGenerationError(A2AException):
    """Error generando código"""
    pass

class OptimizationError(A2AException):
    """Error en optimización"""
    pass

# Usar en agentes
import logging
from utils.exceptions import SimulationError

logger = logging.getLogger(__name__)

def simulator_node(state):
    try:
        # código de simulación
        pass
    except subprocess.TimeoutExpired:
        raise SimulationError("Simulación excedió timeout")
    except FileNotFoundError as e:
        raise SimulationError(f"Archivo no encontrado: {e}")
    except Exception as e:
        logger.error(f"Error inesperado: {e}", exc_info=True)
        raise SimulationError(f"Error inesperado: {e}")
```

**Estimación:** 3-4 horas  
**Impacto:** Medio - Mejora debugging y mantenimiento

---

### 6. Caché de Resultados de LLM
**Problema:** Llamadas repetidas a Ollama con los mismos prompts

**Solución:**
```python
# Crear utils/llm_cache.py
import hashlib
import json
from pathlib import Path

CACHE_DIR = Path("cache/llm_responses")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_key(prompt: str, model: str) -> str:
    """Genera clave única para prompt+modelo"""
    content = f"{model}:{prompt}"
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_response(prompt: str, model: str):
    """Obtiene respuesta cacheada si existe"""
    key = get_cache_key(prompt, model)
    cache_file = CACHE_DIR / f"{key}.json"
    
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            return json.load(f)['response']
    return None

def cache_response(prompt: str, model: str, response: str):
    """Guarda respuesta en caché"""
    key = get_cache_key(prompt, model)
    cache_file = CACHE_DIR / f"{key}.json"
    
    with open(cache_file, 'w') as f:
        json.dump({
            'prompt': prompt[:200],  # Solo inicio
            'model': model,
            'response': response
        }, f)

# Usar en agentes
def call_llm_with_cache(prompt, model):
    cached = get_cached_response(prompt, model)
    if cached:
        print("✓ Usando respuesta cacheada")
        return cached
    
    response = llm.invoke(prompt)
    cache_response(prompt, model, response.content)
    return response.content
```

**Estimación:** 4-5 horas  
**Impacto:** Medio - Reduce tiempo de ejecución y costos

---

---

## 🟣 MEJORAS EXPERTAS (Basadas en 'AI Agents in Action')

### 13. Memoria Episódica (Episodic Memory)
**Concepto:** Permitir que el sistema "recuerde" experimentos pasados para no repetir errores.
**Implementación:**
- Almacenar tuplas `(tarea, código, error, solución)` en ChromaDB.
- Antes de generar código, el `Coder` consulta: "¿He resuelto un error similar antes?"
**Impacto:** Reduce costos de LLM y tiempo de depuración drásticamente.

### 14. Agente Crítico (Reflection Pattern)
**Concepto:** Un agente dedicado a "criticar" el plan antes de ejecutarlo.
**Implementación:**
- Añadir nodo `Critic` entre `Coder` y `Simulator`.
- Verifica lógica de negocio (no solo sintaxis): "¿Este código realmente testea la hipótesis?"
**Impacto:** Aumenta la calidad científica de los experimentos.

### 15. Herramientas Dinámicas (Dynamic Tools)
**Concepto:** Agentes que crean sus propias herramientas.
**Implementación:**
- Permitir al `Coder` definir funciones Python que se registran como herramientas para el `Researcher`.
- Ejemplo: Crear un parser específico para un log extraño y usarlo inmediatamente.
**Impacto:** Flexibilidad total para escenarios no previstos.

---

## 🟢 PRIORIDAD BAJA (Mejoras)

### 7. Entrenamiento Online de DRL
**Problema:** Entrenamiento es offline (después de simulación)

**Mejora:** Implementar entrenamiento durante la simulación

**Requiere:**
- ns3-ai funcional (ver tarea #2)
- Comunicación bidireccional Python-C++
- Actualización de política en tiempo real

**Estimación:** 2-3 semanas  
**Impacto:** Bajo - Funcionalidad avanzada

---

### 8. API REST para Acceso Remoto
**Mejora:** Permitir ejecutar experimentos remotamente

**Implementación sugerida:**
```python
# api/server.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

class ExperimentRequest(BaseModel):
    task: str
    max_iterations: int = 5

@app.post("/experiments")
async def create_experiment(req: ExperimentRequest, bg: BackgroundTasks):
    experiment_id = str(uuid4())
    bg.add_task(run_experiment_async, experiment_id, req.task)
    return {"experiment_id": experiment_id, "status": "queued"}

@app.get("/experiments/{experiment_id}")
async def get_experiment_status(experiment_id: str):
    # Leer estado desde DB
    return {"status": "running", "progress": 45}
```

**Estimación:** 1 semana  
**Impacto:** Bajo - Funcionalidad adicional

---

### 9. Paralelización de Simulaciones
**Mejora:** Ejecutar múltiples simulaciones en paralelo

**Implementación:**
```python
from concurrent.futures import ProcessPoolExecutor

def run_parallel_simulations(tasks, max_workers=4):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(run_simulation, task) for task in tasks]
        results = [f.result() for f in futures]
    return results
```

**Estimación:** 3-4 días  
**Impacto:** Bajo - Optimización de rendimiento

---

### 10. Visualizaciones Avanzadas
**Mejora:** Gráficos más sofisticados en el dashboard

**Ideas:**
- Mapa de topología de red en tiempo real
- Heatmap de congestión
- Animación de paquetes en tránsito
- Comparación lado a lado de protocolos

**Tecnologías:**
- Plotly Dash para interactividad
- NetworkX para grafos
- D3.js para animaciones

**Estimación:** 1-2 semanas  
**Impacto:** Bajo - Mejora visual

---

## 📝 DOCUMENTACIÓN

### 11. Completar Docstrings
**Problema:** Algunas funciones carecen de documentación

**Estándar a seguir:**
```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """
    Descripción breve de la función.
    
    Descripción más detallada si es necesario, explicando
    el propósito y comportamiento de la función.
    
    Args:
        param1: Descripción del primer parámetro
        param2: Descripción del segundo parámetro
        
    Returns:
        Descripción del valor retornado
        
    Raises:
        ExceptionType: Cuándo se lanza esta excepción
        
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        Expected output
    """
    pass
```

**Estimación:** 2-3 días  
**Impacto:** Bajo - Mejora mantenibilidad

---

### 12. Tutorial en Video
**Mejora:** Crear video demostrativo del sistema

**Contenido sugerido:**
1. Instalación (5 min)
2. Primera simulación (10 min)
3. Análisis de resultados (5 min)
4. Dashboard en tiempo real (5 min)
5. Optimización con DRL (10 min)

**Herramientas:** OBS Studio, DaVinci Resolve

**Estimación:** 1 semana  
**Impacto:** Bajo - Mejora adopción

---

## 🐛 BUGS CONOCIDOS

### Bug #1: Dashboard no se actualiza automáticamente
**Descripción:** Aunque hay checkbox "Auto-refresco", no funciona correctamente en todas las plataformas

**Solución temporal:** Usar `st.rerun()` con `time.sleep()`

**Solución definitiva:** Implementar WebSocket para actualizaciones push

---

### Bug #2: Timeout en simulaciones largas
**Descripción:** Simulaciones >15 minutos se cancelan

**Archivo:** `config/settings.py` línea 42
```python
SIMULATION_TIMEOUT = 900  # 15 minutos
```

**Solución:** Hacer configurable por línea de comandos
```python
parser.add_argument('--timeout', type=int, default=900)
```

---

## 📊 MÉTRICAS DE PROGRESO

| Categoría | Completado | Pendiente | Progreso |
|-----------|------------|-----------|----------|
| Funcionalidad Core | 85% | 15% | ████████░░ |
| Tests | 10% | 90% | █░░░░░░░░░ |
| Documentación | 80% | 20% | ████████░░ |
| Optimización | 60% | 40% | ██████░░░░ |
| **TOTAL** | **70%** | **30%** | **███████░░░** |

---

## 🎯 ROADMAP

### Versión 1.5 (Enero 2026)
- [x] Dashboard funcional
- [x] DRL con PyTorch
- [ ] Dashboard conectado al flujo
- [ ] Tests unitarios básicos
- [ ] Validación sintáctica robusta

### Versión 1.6 (Febrero 2026)
- [ ] Integración real con ns3-ai
- [ ] Caché de LLM
- [ ] Manejo de errores estructurado
- [ ] Cobertura de tests >50%

### Versión 2.0 (Marzo 2026)
- [ ] Entrenamiento online
- [ ] API REST
- [ ] Paralelización
- [ ] Visualizaciones avanzadas

---

## 💡 CONTRIBUIR

Si deseas contribuir a resolver alguna de estas tareas:

1. Crea un issue en GitHub referenciando el número de tarea
2. Haz fork del repositorio
3. Crea una rama: `git checkout -b feature/TODO-#X`
4. Implementa la solución con tests
5. Envía Pull Request

**Contacto:** [Tu email o GitHub]

---

## 📚 REFERENCIAS

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [NS-3 Documentation](https://www.nsnam.org/documentation/)
- [ns3-ai GitHub](https://github.com/hust-diangroup/ns3-ai)
- [PyTorch DRL Tutorial](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Última actualización:** 25 de Noviembre de 2025  
**Mantenedor:** Sistema A2A Team  
**Versión del documento:** 1.0
