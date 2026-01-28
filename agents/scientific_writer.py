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
from utils.prompts import get_prompt


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
    prompt = get_prompt(
        'scientific_writer',
        'briefing',
        experiment_name=experiment_name,
        timestamp=timestamp,
        config=json.dumps(config, indent=2),
        metrics=json.dumps(metrics, indent=2)
    )

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
    
    prompt = get_prompt(
        'scientific_writer',
        'detailed_report',
        experiment_name=experiment_name,
        timestamp=timestamp,
        config=json.dumps(config, indent=2),
        metrics=json.dumps(metrics, indent=2),
        statistical_analysis=json.dumps(statistical_analysis, indent=2)
    )

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
        prompt = get_prompt(
            'scientific_writer',
            'thesis_section.methodology',
            experiment_name=experiment_name,
            config=json.dumps(config, indent=2)
        )
    
    elif section_type == "results":
        prompt = get_prompt(
            'scientific_writer',
            'thesis_section.results',
            experiment_name=experiment_name,
            metrics=json.dumps(metrics, indent=2)
        )
    
    else:  # discussion
        prompt = get_prompt(
            'scientific_writer',
            'thesis_section.discussion',
            experiment_name=experiment_name,
            metrics=json.dumps(metrics, indent=2)
        )

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
    
    prompt = get_prompt(
        'scientific_writer',
        'paper_draft',
        experiment_name=experiment_name,
        config=json.dumps(config, indent=2),
        metrics=json.dumps(metrics, indent=2)
    )

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
    
    prompt = get_prompt(
        'scientific_writer',
        'comparative_analysis',
        experiments=json.dumps(results_list, indent=2)
    )

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
    
    prompt = get_prompt(
        'scientific_writer',
        'presentation_slides',
        experiment_name=experiment_name,
        metrics=json.dumps(metrics, indent=2)
    )

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
