"""
Módulo de manejo de errores estructurados para el sistema A2A.
Define la jerarquía de excepciones para clasificar fallos en simulación, compilación y validación.
"""

class A2AError(Exception):
    """Clase base para todas las excepciones del sistema A2A"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

class SimulationError(A2AError):
    """Error durante la ejecución de la simulación NS-3 (Runtime Error)"""
    pass

class CompilationError(A2AError):
    """Error de sintaxis o compilación en el script generado"""
    pass

class TimeoutError(A2AError):
    """La simulación excedió el tiempo límite asignado"""
    pass

class ValidationError(A2AError):
    """El código no pasó la validación del Crítico o las métricas son inválidas"""
    pass

def format_error_for_agent(error: A2AError) -> str:
    """Formatea el error para que sea consumible por el LLM"""
    error_type = type(error).__name__
    details_str = "\n".join([f"- {k}: {v}" for k, v in error.details.items()])
    return f"ERROR TIPO: {error_type}\nMENSAJE: {error.message}\nDETALLES:\n{details_str}"
