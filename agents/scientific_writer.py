"""
Agente de Escritura Científica
Genera informes, briefings y documentos académicos a partir de resultados experimentales
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import json
import yaml

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import MODEL_REASONING, OLLAMA_BASE_URL
from utils.logging_utils import log_info, log_error, log_warning
from utils.errors import DocumentGenerationError
from utils.state import AgentState


# Inicializar modelo
llm = ChatOllama(
    model=MODEL_REASONING,
    base_url=OLLAMA_BASE_URL,
    temperature=0.3  # Más bajo para escritura técnica precisa
)


def scientific_writer_node(state: AgentState) -> AgentState:
    """
    Nodo del agente de escritura científica
    Genera documentos académicos a partir de resultados experimentales
    """
    log_info("ScientificWriter", "🖊️ Agente de Escritura Científica iniciado")
    
    try:
        # Obtener tipo de documento solicitado
        doc_type = state.get("document_type", "briefing")
        experiment_results = state.get("experiment_results", {})
        
        if doc_type == "briefing":
            document = generate_experiment_briefing(experiment_results, state)
        elif doc_type == "detailed_report":
            document = generate_detailed_report(experiment_results, state)
        elif doc_type == "thesis_section":
            document = generate_thesis_section(experiment_results, state)
        elif doc_type == "paper_draft":
            document = generate_paper_draft(experiment_results, state)
        else:
            raise DocumentGenerationError(f"Tipo de documento no soportado: {doc_type}")
        
        # Guardar documento
        output_path = save_document(document, doc_type, state)
        
        state["generated_document"] = document
        state["document_path"] = str(output_path)
        state["messages"].append(f"✅ Documento generado: {output_path}")
        
        log_info("ScientificWriter", f"✅ Documento generado exitosamente: {output_path}")
        return state
        
    except Exception as e:
        log_error("ScientificWriter", f"❌ Error en agente de escritura científica: {e}")
        state["error"] = str(e)
        state["messages"].append(f"❌ Error generando documento: {e}")
        return state


def generate_experiment_briefing(results: Dict[str, Any], state: AgentState) -> str:
    """
    Genera un briefing conciso del experimento
    Ideal para reportes rápidos y actualizaciones
    """
    log_info("ScientificWriter", "📝 Generando briefing de experimento...")
    
    # Extraer información clave
    experiment_name = results.get("experiment_name", "Experimento")
    config = results.get("configuration", {})
    metrics = results.get("metrics", {})
    timestamp = results.get("timestamp", datetime.now().isoformat())
    
    # Construir prompt
    prompt = f"""Genera un briefing técnico conciso (máximo 2 páginas) del siguiente experimento de simulación de redes:

INFORMACIÓN DEL EXPERIMENTO:
- Nombre: {experiment_name}
- Fecha: {timestamp}
- Configuración: {json.dumps(config, indent=2)}

RESULTADOS OBTENIDOS:
{json.dumps(metrics, indent=2)}

El briefing debe incluir:
1. RESUMEN EJECUTIVO (3-4 líneas)
2. CONFIGURACIÓN DE LA SIMULACIÓN
   - Protocolo evaluado
   - Número de nodos
   - Área de simulación
   - Duración
   - Modelo de movilidad
3. SCRIPT UTILIZADO
   - Comando ejecutado
   - Parámetros principales
4. RESULTADOS PRINCIPALES
   - PDR (Packet Delivery Ratio)
   - Delay promedio
   - Throughput
   - Overhead
   - Con intervalos de confianza si están disponibles
5. OBSERVACIONES CLAVE
   - Hallazgos principales
   - Anomalías detectadas
   - Recomendaciones

Formato: Markdown profesional con tablas y listas.
Tono: Técnico pero accesible.
"""

    messages = [
        SystemMessage(content="Eres un experto en redacción científica especializado en redes de computadoras y simulaciones NS-3."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content


def generate_detailed_report(results: Dict[str, Any], state: AgentState) -> str:
    """
    Genera un informe detallado del experimento
    Incluye análisis estadístico completo y gráficos
    """
    log_info("ScientificWriter", "📊 Generando informe detallado...")
    
    experiment_name = results.get("experiment_name", "Experimento")
    config = results.get("configuration", {})
    metrics = results.get("metrics", {})
    statistical_analysis = results.get("statistical_analysis", {})
    timestamp = results.get("timestamp", datetime.now().isoformat())
    
    prompt = f"""Genera un informe técnico detallado (5-10 páginas) del siguiente experimento de simulación de redes:

INFORMACIÓN DEL EXPERIMENTO:
- Nombre: {experiment_name}
- Fecha: {timestamp}
- Configuración: {json.dumps(config, indent=2)}

RESULTADOS:
{json.dumps(metrics, indent=2)}

ANÁLISIS ESTADÍSTICO:
{json.dumps(statistical_analysis, indent=2)}

El informe debe incluir:

1. PORTADA
   - Título del experimento
   - Fecha
   - Autor/Sistema

2. RESUMEN EJECUTIVO
   - Objetivo del experimento
   - Metodología
   - Resultados principales
   - Conclusiones

3. INTRODUCCIÓN
   - Contexto del experimento
   - Objetivos específicos
   - Hipótesis

4. METODOLOGÍA
   - Configuración de la simulación
   - Parámetros utilizados
   - Herramientas (NS-3, versión, módulos)
   - Script de simulación (comando completo)
   - Número de repeticiones
   - Semillas aleatorias

5. RESULTADOS
   - Métricas principales con tablas
   - Intervalos de confianza (95%)
   - Desviación estándar
   - Valores mínimos y máximos
   - Gráficos generados (referencias)

6. ANÁLISIS ESTADÍSTICO
   - Tests de significancia aplicados
   - Interpretación de resultados
   - Comparación con valores esperados
   - Validación de hipótesis

7. DISCUSIÓN
   - Interpretación de hallazgos
   - Comparación con literatura
   - Limitaciones del estudio
   - Implicaciones prácticas

8. CONCLUSIONES
   - Resumen de hallazgos
   - Respuesta a objetivos
   - Trabajo futuro

9. REFERENCIAS
   - NS-3 documentation
   - Protocolos evaluados (RFCs)
   - Literatura relevante

10. ANEXOS
    - Configuración completa
    - Datos crudos (resumen)
    - Scripts utilizados

Formato: Markdown académico con secciones numeradas, tablas LaTeX-style, y referencias a figuras.
Tono: Académico y riguroso.
"""

    messages = [
        SystemMessage(content="Eres un investigador senior especializado en redes de computadoras, con experiencia en redacción de papers científicos y tesis doctorales."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content


def generate_thesis_section(results: Dict[str, Any], state: AgentState) -> str:
    """
    Genera una sección de tesis doctoral
    Formato académico completo con referencias
    """
    log_info("ScientificWriter", "🎓 Generando sección de tesis...")
    
    section_type = state.get("thesis_section_type", "results")  # results, methodology, discussion
    experiment_name = results.get("experiment_name", "Experimento")
    config = results.get("configuration", {})
    metrics = results.get("metrics", {})
    
    if section_type == "methodology":
        prompt = f"""Genera la sección de METODOLOGÍA de una tesis doctoral para el siguiente experimento:

EXPERIMENTO: {experiment_name}
CONFIGURACIÓN: {json.dumps(config, indent=2)}

La sección debe incluir:

### 5.X Diseño del Experimento: {experiment_name}

#### 5.X.1 Objetivos del Experimento
- Objetivo general
- Objetivos específicos
- Hipótesis a validar

#### 5.X.2 Configuración de la Simulación
- Parámetros de red (tabla)
- Modelo de movilidad
- Configuración de tráfico
- Justificación de parámetros

#### 5.X.3 Herramientas Utilizadas
- NS-3 (versión, módulos)
- Scripts desarrollados
- Herramientas de análisis

#### 5.X.4 Métricas de Evaluación
- PDR: definición y relevancia
- Delay: definición y relevancia
- Throughput: definición y relevancia
- Overhead: definición y relevancia

#### 5.X.5 Metodología Experimental
- Número de repeticiones
- Control de semillas aleatorias
- Validación de resultados
- Análisis estadístico aplicado

#### 5.X.6 Reproducibilidad
- Configuración completa
- Scripts disponibles
- Datos crudos almacenados

Formato: LaTeX-compatible, con referencias bibliográficas [X], ecuaciones si es necesario.
Tono: Académico formal, tesis doctoral.
"""
    
    elif section_type == "results":
        prompt = f"""Genera la sección de RESULTADOS de una tesis doctoral para el siguiente experimento:

EXPERIMENTO: {experiment_name}
RESULTADOS: {json.dumps(metrics, indent=2)}

La sección debe incluir:

### 6.X Resultados del Experimento: {experiment_name}

#### 6.X.1 Resultados Generales
- Tabla resumen de métricas
- Intervalos de confianza
- Significancia estadística

#### 6.X.2 Packet Delivery Ratio (PDR)
- Valores obtenidos
- Análisis de tendencias
- Comparación con literatura
- Figura X.Y (referencia)

#### 6.X.3 End-to-End Delay
- Valores obtenidos
- Distribución de delays
- Análisis de outliers
- Figura X.Y (referencia)

#### 6.X.4 Throughput
- Valores obtenidos
- Variabilidad temporal
- Análisis de saturación
- Figura X.Y (referencia)

#### 6.X.5 Routing Overhead
- Valores obtenidos
- Eficiencia del protocolo
- Trade-offs identificados
- Figura X.Y (referencia)

#### 6.X.6 Análisis de Significancia
- Tests estadísticos aplicados
- Valores p obtenidos
- Interpretación de resultados
- Validación de hipótesis

Formato: LaTeX-compatible, con tablas, referencias a figuras, y citas bibliográficas.
Tono: Académico formal, presentación objetiva de resultados.
"""
    
    else:  # discussion
        prompt = f"""Genera la sección de DISCUSIÓN de una tesis doctoral para el siguiente experimento:

EXPERIMENTO: {experiment_name}
RESULTADOS: {json.dumps(metrics, indent=2)}

La sección debe incluir:

### 6.X Discusión de Resultados: {experiment_name}

#### 6.X.1 Interpretación de Hallazgos
- Explicación de resultados principales
- Relación con objetivos planteados
- Validación de hipótesis

#### 6.X.2 Comparación con Estado del Arte
- Benchmarking con literatura
- Mejoras obtenidas
- Limitaciones identificadas

#### 6.X.3 Análisis de Factores Influyentes
- Impacto de parámetros de red
- Condiciones de movilidad
- Patrones de tráfico

#### 6.X.4 Implicaciones Prácticas
- Aplicabilidad en escenarios reales
- Recomendaciones de configuración
- Trade-offs a considerar

#### 6.X.5 Limitaciones del Estudio
- Supuestos realizados
- Restricciones de simulación
- Áreas no cubiertas

#### 6.X.6 Contribuciones
- Aportes al conocimiento
- Innovaciones metodológicas
- Resultados novedosos

Formato: LaTeX-compatible, con argumentación sólida y referencias bibliográficas.
Tono: Académico analítico, crítico pero constructivo.
"""

    messages = [
        SystemMessage(content="Eres un profesor universitario con 20 años de experiencia dirigiendo tesis doctorales en redes de computadoras."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content


def generate_paper_draft(results: Dict[str, Any], state: AgentState) -> str:
    """
    Genera un borrador de paper científico
    Formato IEEE o ACM
    """
    log_info("ScientificWriter", "📄 Generando borrador de paper...")
    
    experiment_name = results.get("experiment_name", "Experimento")
    config = results.get("configuration", {})
    metrics = results.get("metrics", {})
    
    prompt = f"""Genera un borrador de paper científico (formato IEEE, 6-8 páginas) basado en:

EXPERIMENTO: {experiment_name}
CONFIGURACIÓN: {json.dumps(config, indent=2)}
RESULTADOS: {json.dumps(metrics, indent=2)}

El paper debe incluir:

# [Título Sugerido]

## Abstract
(150-200 palabras)
- Contexto y motivación
- Problema abordado
- Metodología propuesta
- Resultados principales
- Conclusiones

## I. INTRODUCTION
- Contexto de redes móviles ad-hoc
- Desafíos actuales
- Motivación del estudio
- Contribuciones principales
- Organización del paper

## II. RELATED WORK
- Protocolos de enrutamiento existentes
- Trabajos previos en simulación
- Gaps identificados
- Posicionamiento de este trabajo

## III. METHODOLOGY
### A. Simulation Setup
- NS-3 configuration
- Network parameters
- Mobility model
- Traffic patterns

### B. Evaluation Metrics
- PDR, Delay, Throughput, Overhead
- Statistical analysis approach

### C. Experimental Design
- Number of runs
- Confidence intervals
- Reproducibility measures

## IV. RESULTS
### A. Overall Performance
- Summary table
- Statistical significance

### B. Detailed Analysis
- PDR analysis
- Delay analysis
- Throughput analysis
- Overhead analysis

### C. Comparative Evaluation
- Comparison with baseline
- Performance trade-offs

## V. DISCUSSION
- Interpretation of findings
- Practical implications
- Limitations
- Future work

## VI. CONCLUSION
- Summary of contributions
- Key findings
- Impact and applications

## REFERENCES
[1-15] (sugerencias de referencias relevantes)

Formato: IEEE two-column style (indicar dónde van las figuras/tablas)
Tono: Académico conciso, estilo paper de conferencia.
Longitud: ~3000-4000 palabras
"""

    messages = [
        SystemMessage(content="Eres un investigador senior con múltiples publicaciones en IEEE INFOCOM, GLOBECOM y IEEE Transactions on Mobile Computing."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content


def save_document(content: str, doc_type: str, state: AgentState) -> Path:
    """
    Guarda el documento generado en el directorio apropiado
    """
    # Crear directorio de documentos si no existe
    docs_dir = Path("generated_documents")
    docs_dir.mkdir(exist_ok=True)
    
    # Crear subdirectorio por tipo
    type_dir = docs_dir / doc_type
    type_dir.mkdir(exist_ok=True)
    
    # Generar nombre de archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_name = state.get("experiment_results", {}).get("experiment_name", "experiment")
    experiment_name = experiment_name.replace(" ", "_").lower()
    
    filename = f"{experiment_name}_{doc_type}_{timestamp}.md"
    filepath = type_dir / filename
    
    # Guardar documento
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    log_info("ScientificWriter", f"📁 Documento guardado en: {filepath}")
    return filepath


def generate_comparative_analysis(results_list: List[Dict[str, Any]], state: AgentState) -> str:
    """
    Genera un análisis comparativo de múltiples experimentos
    Útil para comparar protocolos o configuraciones
    """
    log_info("ScientificWriter", "📊 Generando análisis comparativo...")
    
    prompt = f"""Genera un análisis comparativo detallado de los siguientes experimentos:

EXPERIMENTOS:
{json.dumps(results_list, indent=2)}

El análisis debe incluir:

## ANÁLISIS COMPARATIVO

### 1. Resumen de Experimentos
- Tabla comparativa de configuraciones
- Diferencias clave entre experimentos

### 2. Comparación de Métricas

#### 2.1 Packet Delivery Ratio (PDR)
- Tabla comparativa
- Gráfico de barras (descripción)
- Análisis de diferencias
- Significancia estadística

#### 2.2 End-to-End Delay
- Tabla comparativa
- Gráfico de barras (descripción)
- Análisis de diferencias
- Significancia estadística

#### 2.3 Throughput
- Tabla comparativa
- Gráfico de barras (descripción)
- Análisis de diferencias

#### 2.4 Routing Overhead
- Tabla comparativa
- Gráfico de barras (descripción)
- Trade-offs identificados

### 3. Análisis de Trade-offs
- PDR vs Overhead
- Delay vs Throughput
- Eficiencia general

### 4. Recomendaciones
- Mejor configuración según escenario
- Casos de uso recomendados
- Consideraciones prácticas

### 5. Conclusiones
- Hallazgos principales
- Protocolo/configuración ganador
- Justificación de la elección

Formato: Markdown con tablas comparativas
Tono: Analítico y objetivo
"""

    messages = [
        SystemMessage(content="Eres un experto en análisis comparativo de protocolos de red y evaluación de rendimiento."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content


def generate_presentation_slides(results: Dict[str, Any], state: AgentState) -> str:
    """
    Genera contenido para slides de presentación
    Formato Markdown compatible con Marp o reveal.js
    """
    log_info("ScientificWriter", "🎤 Generando slides de presentación...")
    
    experiment_name = results.get("experiment_name", "Experimento")
    metrics = results.get("metrics", {})
    
    prompt = f"""Genera el contenido para una presentación de 10-15 slides sobre:

EXPERIMENTO: {experiment_name}
RESULTADOS: {json.dumps(metrics, indent=2)}

Formato: Markdown para Marp/reveal.js

---
# [Título del Experimento]

Presentación de Resultados

---
## Agenda

1. Motivación
2. Objetivos
3. Metodología
4. Resultados
5. Conclusiones

---
## Motivación

- Contexto del problema
- Por qué es importante
- Desafíos actuales

---
## Objetivos

- Objetivo principal
- Objetivos específicos
- Hipótesis

---
## Metodología

### Configuración de Simulación
- Parámetros clave
- Herramientas utilizadas
- Métricas evaluadas

---
## Resultados: PDR

[Gráfico de barras]

- Valor obtenido: X%
- Intervalo de confianza: [X, Y]
- Interpretación

---
## Resultados: Delay

[Gráfico de líneas]

- Delay promedio: X ms
- Desviación estándar: Y ms
- Análisis

---
## Resultados: Throughput

[Gráfico de área]

- Throughput promedio: X Mbps
- Picos observados
- Análisis

---
## Resultados: Overhead

[Gráfico de barras]

- Overhead: X%
- Eficiencia del protocolo
- Trade-offs

---
## Análisis Comparativo

[Tabla comparativa]

- Comparación con literatura
- Mejoras obtenidas
- Limitaciones

---
## Conclusiones

✅ Hallazgo 1
✅ Hallazgo 2
✅ Hallazgo 3

---
## Trabajo Futuro

- Extensión 1
- Extensión 2
- Extensión 3

---
## ¡Gracias!

Preguntas?

---

Incluye notas de presentador para cada slide.
Sugiere dónde colocar gráficos y tablas.
"""

    messages = [
        SystemMessage(content="Eres un experto en comunicación científica y presentaciones académicas."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content


# Función auxiliar para integrar con el supervisor
def create_scientific_writer_workflow():
    """
    Crea el workflow del agente de escritura científica
    """
    from langgraph.graph import StateGraph, END
    
    workflow = StateGraph(AgentState)
    workflow.add_node("scientific_writer", scientific_writer_node)
    workflow.set_entry_point("scientific_writer")
    workflow.add_edge("scientific_writer", END)
    
    return workflow.compile()


if __name__ == "__main__":
    # Test del agente
    print("🧪 Probando agente de escritura científica...")
    
    # Datos de prueba
    test_results = {
        "experiment_name": "Comparación AODV vs OLSR",
        "timestamp": "2025-11-25T14:00:00",
        "configuration": {
            "protocols": ["AODV", "OLSR"],
            "nodes": 20,
            "area": "1000x1000m",
            "duration": "200s",
            "mobility": "RandomWaypoint",
            "speed": "5-15 m/s"
        },
        "metrics": {
            "AODV": {
                "pdr": {"mean": 0.87, "std": 0.05, "ci": [0.85, 0.89]},
                "delay": {"mean": 45.2, "std": 8.3, "ci": [42.1, 48.3]},
                "throughput": {"mean": 2.3, "std": 0.4, "ci": [2.1, 2.5]},
                "overhead": {"mean": 0.15, "std": 0.03, "ci": [0.14, 0.16]}
            },
            "OLSR": {
                "pdr": {"mean": 0.91, "std": 0.04, "ci": [0.89, 0.93]},
                "delay": {"mean": 38.7, "std": 6.2, "ci": [36.2, 41.2]},
                "throughput": {"mean": 2.5, "std": 0.3, "ci": [2.3, 2.7]},
                "overhead": {"mean": 0.22, "std": 0.04, "ci": [0.20, 0.24]}
            }
        }
    }
    
    test_state = {
        "document_type": "briefing",
        "experiment_results": test_results,
        "messages": []
    }
    
    result_state = scientific_writer_node(test_state)
    
    if "generated_document" in result_state:
        print("\n✅ Documento generado exitosamente!")
        print(f"📁 Guardado en: {result_state.get('document_path')}")
        print("\n📄 Primeras líneas del documento:")
        print(result_state["generated_document"][:500] + "...")
    else:
        print(f"\n❌ Error: {result_state.get('error')}")
