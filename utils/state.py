"""
Definición del Estado Global del Sistema A2A

Este estado se comparte entre todos los agentes y contiene
toda la información necesaria para el flujo de trabajo.
"""

from typing import TypedDict, List, Annotated, Dict, Any, Optional
import operator


class AgentState(TypedDict):
    """
    Estado compartido entre todos los agentes del sistema.
    
    Este es el "cerebro" del sistema que pasa de un agente a otro,
    acumulando información y resultados en cada paso.
    """
    
    # ========================================================================
    # TAREA Y CONTEXTO
    # ========================================================================
    
    task: str
    """Descripción de la tarea de investigación actual"""
    
    research_notes: Annotated[List[str], operator.add]
    """Notas de investigación y síntesis de papers"""
    
    papers_found: Annotated[List[Dict[str, Any]], operator.add]
    """Lista de papers encontrados con metadatos"""
    
    # ========================================================================
    # CÓDIGO Y SIMULACIÓN
    # ========================================================================
    
    code_snippet: str
    """Código Python de simulación NS-3 generado"""
    
    code_validated: bool
    """Indica si el código ha sido validado"""
    
    simulation_logs: str
    """Ruta al archivo de logs de la simulación (XML/CSV)"""
    
    simulation_status: str
    """Estado de la simulación: 'pending', 'running', 'completed', 'failed'"""
    
    pcap_files: Annotated[List[str], operator.add]
    """Lista de archivos PCAP generados por la simulación"""
    
    trace_analysis: Optional[List[Dict[str, Any]]]
    """Análisis detallado de trazas PCAP"""
    
    trace_analysis_report: Optional[str]
    """Reporte de análisis de trazas generado por LLM"""
    
    # ========================================================================
    # ANÁLISIS Y RESULTADOS
    # ========================================================================
    
    analysis_results: Dict[str, Any]
    """Resultados del análisis (KPIs, estadísticas, propuestas)"""
    
    metrics: Dict[str, float]
    """Métricas calculadas (PDR, throughput, delay, etc.)"""
    
    plots_generated: Annotated[List[str], operator.add]
    """Lista de rutas a gráficos generados"""
    
    # ========================================================================
    # CONTROL DE ERRORES Y FLUJO
    # ========================================================================
    
    errors: Annotated[List[str], operator.add]
    """Lista de errores encontrados durante la ejecución"""
    
    iteration_count: int
    """Contador de iteraciones (para evitar bucles infinitos)"""
    
    max_iterations: int
    """Número máximo de iteraciones permitidas"""
    
    # ========================================================================
    # BITÁCORA Y AUDITORÍA
    # ========================================================================
    
    audit_trail: Annotated[List[Dict[str, Any]], operator.add]
    """Registro de todas las acciones realizadas por los agentes"""
    
    messages: Annotated[List[str], operator.add]
    """Mensajes de comunicación entre agentes"""
    
    # ========================================================================
    # CAMPOS OPCIONALES PARA EXPANSIONES
    # ========================================================================
    
    statistical_results: Optional[Dict[str, Any]]
    """Resultados de tests estadísticos (t-test, ANOVA, etc.)"""
    
    comparison_metrics: Optional[List[str]]
    """Métricas a comparar en análisis estadístico"""
    
    optimization_params: Optional[Dict[str, Any]]
    """Parámetros optimizados (para agente de optimización)"""
    
    neural_network_proposal: Optional[str]
    """Propuesta de arquitectura de red neuronal"""
    
    report_sections: Optional[Dict[str, str]]
    """Secciones de reporte generadas (para agente de documentación)"""
    
    # ========================================================================
    # CAMPOS PARA RIGOR ACADÉMICO (Feedback Director)
    # ========================================================================
    
    optimization_count: int
    """Contador de ciclos de optimización ejecutados"""
    
    simulation_seed: Optional[int]
    """Semilla aleatoria para reproducibilidad en NS-3"""
    
    confidence_intervals: Optional[Dict[str, tuple]]
    """Intervalos de confianza para métricas clave"""
    
    routing_overhead: Optional[float]
    """Overhead de enrutamiento (paquetes control/datos)"""


def create_initial_state(task: str, max_iterations: int = 5, seed: int = None) -> AgentState:
    """
    Crea un estado inicial para una nueva tarea.
    
    Args:
        task: Descripción de la tarea de investigación
        max_iterations: Número máximo de iteraciones permitidas
        seed: Semilla aleatoria para reproducibilidad (None = aleatoria)
        
    Returns:
        Estado inicial configurado
    """
    import random
    
    # Generar semilla si no se proporciona
    if seed is None:
        seed = random.randint(1, 1000000)
    
    return AgentState(
        # Tarea
        task=task,
        research_notes=[],
        papers_found=[],
        
        # Código
        code_snippet="",
        code_validated=False,
        simulation_logs="",
        simulation_status="pending",
        pcap_files=[],
        trace_analysis=None,
        trace_analysis_report=None,
        
        # Análisis
        analysis_results={},
        metrics={},
        plots_generated=[],
        
        # Control
        errors=[],
        iteration_count=0,
        max_iterations=max_iterations,
        
        # Bitácora
        audit_trail=[],
        messages=[],
        
        # Opcionales
        statistical_results=None,
        comparison_metrics=None,
        optimization_params=None,
        neural_network_proposal=None,
        report_sections=None,
        
        # Rigor académico
        optimization_count=0,
        simulation_seed=seed,
        confidence_intervals=None,
        routing_overhead=None
    )


def add_audit_entry(state: AgentState, agent_name: str, action: str, 
                    details: Dict[str, Any]) -> Dict:
    """
    Añade una entrada a la bitácora de auditoría.
    
    Args:
        state: Estado actual
        agent_name: Nombre del agente que realiza la acción
        action: Tipo de acción realizada
        details: Detalles adicionales de la acción
        
    Returns:
        Diccionario con la entrada de auditoría para actualizar el estado
    """
    import datetime
    
    entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'agent': agent_name,
        'action': action,
        'details': details
    }
    
    return {'audit_trail': [entry]}


def increment_iteration(state: AgentState) -> Dict:
    """
    Incrementa el contador de iteraciones.
    
    Args:
        state: Estado actual
        
    Returns:
        Diccionario con el contador incrementado
    """
    return {'iteration_count': state['iteration_count'] + 1}


def add_error(state: AgentState, error_message: str) -> Dict:
    """
    Añade un error al estado.
    
    Args:
        state: Estado actual
        error_message: Mensaje de error
        
    Returns:
        Diccionario con el error añadido
    """
    return {'errors': [error_message]}


def should_continue(state: AgentState) -> bool:
    """
    Determina si el sistema debe continuar iterando.
    
    Args:
        state: Estado actual
        
    Returns:
        True si debe continuar, False si debe detenerse
    """
    # Detener si se alcanzó el máximo de iteraciones
    if state['iteration_count'] >= state['max_iterations']:
        return False
    
    # Detener si la simulación se completó exitosamente
    if state['simulation_status'] == 'completed':
        return False
    
    # Continuar si hay errores y no se alcanzó el límite
    if state.get('errors') and state['iteration_count'] < state['max_iterations']:
        return True
    
    return True


if __name__ == "__main__":
    # Ejemplo de uso
    state = create_initial_state("Simular protocolo AODV con 20 nodos")
    print("Estado inicial creado:")
    print(f"  Tarea: {state['task']}")
    print(f"  Max iteraciones: {state['max_iterations']}")
    print(f"  Estado simulación: {state['simulation_status']}")


def increment_optimization_count(state: AgentState) -> Dict:
    """
    Incrementa el contador de optimizaciones
    
    Args:
        state: Estado actual
        
    Returns:
        Diccionario con el contador actualizado
    """
    return {
        'optimization_count': state.get('optimization_count', 0) + 1
    }
