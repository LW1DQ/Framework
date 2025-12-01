"""
Excepciones personalizadas para el Sistema A2A

Proporciona jerarquía de errores específicos para mejor manejo y debugging.
"""


class A2AError(Exception):
    """Excepción base del sistema A2A"""
    pass


class ConfigurationError(A2AError):
    """Error en la configuración del sistema"""
    pass


class AgentError(A2AError):
    """Error base para errores de agentes"""
    pass


class ResearchError(AgentError):
    """Error en el agente de investigación"""
    pass


class CodeGenerationError(AgentError):
    """Error generando código NS-3"""
    pass


class CompilationError(AgentError):
    """Error de compilación o sintaxis en código generado"""
    pass


class SimulationError(AgentError):
    """Error durante la ejecución de simulación NS-3"""
    pass


class TimeoutError(SimulationError):
    """Simulación excedió el tiempo límite"""
    pass


class AnalysisError(AgentError):
    """Error analizando resultados"""
    pass


class OptimizationError(AgentError):
    """Error en optimización"""
    pass


class DocumentGenerationError(AgentError):
    """Error generando documentos científicos"""
    pass


class ValidationError(A2AError):
    """Error de validación de datos o código"""
    pass


class ExternalDependencyError(A2AError):
    """Error con dependencia externa (Ollama, NS-3, etc.)"""
    pass


class MemoryError(A2AError):
    """Error en memoria episódica"""
    pass


# Mapeo de tipos de error a clases
ERROR_TYPE_MAP = {
    'CompilationError': CompilationError,
    'SimulationError': SimulationError,
    'TimeoutError': TimeoutError,
    'AnalysisError': AnalysisError,
    'OptimizationError': OptimizationError,
    'ValidationError': ValidationError,
    'DocumentGenerationError': DocumentGenerationError,
    'A2AError': A2AError
}


def get_error_class(error_type: str) -> type:
    """
    Obtiene la clase de error correspondiente al tipo
    
    Args:
        error_type: Tipo de error como string
        
    Returns:
        Clase de excepción correspondiente
    """
    return ERROR_TYPE_MAP.get(error_type, A2AError)


if __name__ == "__main__":
    # Ejemplos de uso
    print("Ejemplos de excepciones personalizadas:\n")
    
    try:
        raise CompilationError("Error de sintaxis en línea 42")
    except CompilationError as e:
        print(f"✓ CompilationError capturado: {e}")
    
    try:
        raise TimeoutError("Simulación excedió 900 segundos")
    except SimulationError as e:  # TimeoutError es subclase de SimulationError
        print(f"✓ TimeoutError capturado como SimulationError: {e}")
    
    try:
        raise OptimizationError("No se pudo mejorar PDR")
    except AgentError as e:  # OptimizationError es subclase de AgentError
        print(f"✓ OptimizationError capturado como AgentError: {e}")
    
    print("\n✅ Sistema de excepciones funcionando correctamente")
