"""
Patrones de Retry con Tenacity para Mayor Resiliencia

Implementa estrategias de reintento robustas para operaciones externas
"""

import time
import logging
from functools import wraps
from typing import Any, Callable, Optional, Dict, Union, Type, List
from enum import Enum

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    wait_random_exponential,
    wait_fixed,
    retry_if_exception_type,
    retry_if_exception_message,
    before_sleep_log,
    after_log,
    RetryError
)


class RetryStrategy(Enum):
    """Estrategias de retry predefinidas"""
    AGGRESSIVE = "aggressive"
    STANDARD = "standard"
    CONSERVATIVE = "conservative"
    NETWORK = "network"
    LLM = "llm"


class RetryConfig:
    """
    Configuración de retry con parámetros predefinidos
    """
    
    # Configuraciones predefinidas
    STRATEGIES = {
        RetryStrategy.AGGRESSIVE: {
            'stop': stop_after_attempt(3),
            'wait': wait_exponential(multiplier=1, min=1, max=10),
            'reraise': True
        },
        RetryStrategy.STANDARD: {
            'stop': stop_after_attempt(5),
            'wait': wait_exponential(multiplier=1, min=2, max=30),
            'reraise': True
        },
        RetryStrategy.CONSERVATIVE: {
            'stop': stop_after_attempt(10),
            'wait': wait_exponential(multiplier=2, min=5, max=60),
            'reraise': True
        },
        RetryStrategy.NETWORK: {
            'stop': stop_after_attempt(5),
            'wait': wait_random_exponential(multiplier=1, max=30),
            'retry': retry_if_exception_type((ConnectionError, TimeoutError)),
            'reraise': True
        },
        RetryStrategy.LLM: {
            'stop': stop_after_attempt(3),
            'wait': wait_exponential(multiplier=2, min=1, max=20),
            'retry': retry_if_exception_message(
                contains=["timeout", "connection", "rate limit", "overloaded"]
            ),
            'reraise': True
        }
    }
    
    @classmethod
    def get_config(cls, strategy: RetryStrategy, **overrides) -> Dict[str, Any]:
        """Obtiene configuración para una estrategia con overrides"""
        config = cls.STRATEGIES[strategy].copy()
        config.update(overrides)
        return config


def with_retry(
    strategy: Union[RetryStrategy, Dict] = RetryStrategy.STANDARD,
    exceptions: Optional[List[Type[Exception]]] = None,
    logger: Optional[logging.Logger] = None,
    on_retry: Optional[Callable] = None,
    **kwargs
):
    """
    Decorador genérico de retry con múltiples estrategias
    
    Args:
        strategy: Estrategia de retry predefinida o config personalizada
        exceptions: Lista de excepciones para retry (si no se especifica en strategy)
        logger: Logger para logging de reintentos
        on_retry: Función a ejecutar en cada reintento
        **kwargs: Parámetros adicionales para tenacity
    """
    def decorator(func: Callable) -> Callable:
        # Determinar configuración
        if isinstance(strategy, RetryStrategy):
            config = RetryConfig.get_config(strategy, **kwargs)
        else:
            config = strategy
        
        # Añadir manejo de excepciones si se especifica
        if exceptions and 'retry' not in config:
            config['retry'] = retry_if_exception_type(tuple(exceptions))
        
        # Añadir logging si se proporciona logger
        if logger:
            config['before_sleep'] = before_sleep_log(logger, logging.WARNING)
            config['after'] = after_log(logger, logging.INFO)
        
        # Crear decorador de retry
        retry_decorator = retry(**config)
        
        # Aplicar decorador
        decorated_func = retry_decorator(func)
        
        # Añadir callback on_retry si se proporciona
        if on_retry:
            @wraps(decorated_func)
            def wrapper(*args, **kwargs):
                try:
                    return decorated_func(*args, **kwargs)
                except Exception as e:
                    if hasattr(e, '__retry__'):
                        on_retry(e, args, kwargs)
                    raise
            
            return wrapper
        
        return decorated_func
    
    return decorator


def network_retry(max_attempts: int = 5, backoff_factor: float = 1.0):
    """
    Decorador especializado para operaciones de red
    
    Args:
        max_attempts: Número máximo de intentos
        backoff_factor: Factor para backoff exponencial
    """
    return with_retry(
        strategy=RetryStrategy.NETWORK,
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=backoff_factor, min=1, max=30),
        retry=retry_if_exception_type((
            ConnectionError,
            TimeoutError,
            OSError,
            ConnectionResetError,
            ConnectionRefusedError
        ))
    )


def llm_retry(max_attempts: int = 3, temperature: float = 0.1):
    """
    Decorador especializado para llamadas a LLM
    
    Args:
        max_attempts: Número máximo de intentos
        temperature: Temperatura para retries (decreciente)
    """
    def decorator(func: Callable) -> Callable:
        call_count = 0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_count
            original_temperature = kwargs.get('temperature', temperature)
            
            try:
                call_count += 1
                
                # Reducir temperatura en reintentos
                if call_count > 1:
                    kwargs['temperature'] = original_temperature * 0.8
                    logging.warning(f"Reduciendo LLM temperature a {kwargs['temperature']} (intento {call_count})")
                
                return func(*args, **kwargs)
                
            except Exception as e:
                if call_count >= max_attempts:
                    raise RetryError(f"LLM call failed after {max_attempts} attempts: {str(e)}") from e
                else:
                    logging.warning(f"LLM call attempt {call_count} failed: {str(e)}. Retrying...")
                    time.sleep(2 ** call_count)  # Exponential backoff
                    return wrapper(*args, **kwargs)
        
        return wrapper
    
    return decorator


def file_operation_retry(max_attempts: int = 3):
    """
    Decorador especializado para operaciones de archivos
    
    Args:
        max_attempts: Número máximo de intentos
    """
    return with_retry(
        strategy=RetryStrategy.CONSERVATIVE,
        stop=stop_after_attempt(max_attempts),
        wait=wait_fixed(0.1),
        retry=retry_if_exception_type((
            FileNotFoundError,
            PermissionError,
            OSError,
            IOError
        ))
    )


def database_retry(max_attempts: int = 5):
    """
    Decorador especializado para operaciones de base de datos
    
    Args:
        max_attempts: Número máximo de intentos
    """
    return with_retry(
        strategy=RetryStrategy.STANDARD,
        stop=stop_after_attempt(max_attempts),
        retry=retry_if_exception_type((
            ConnectionError,
            TimeoutError,
            OSError
        ))
    )


class CircuitBreaker:
    """
    Implementa el patrón Circuit Breaker para protección contra fallos repetidos
    """
    
    def __init__(self, 
                 failure_threshold: int = 5,
                 recovery_timeout: float = 60.0,
                 expected_exception: Type[Exception] = Exception):
        """
        Inicializa circuit breaker
        
        Args:
            failure_threshold: Número de fallos antes de abrir el circuito
            recovery_timeout: Tiempo de espera antes de intentar recuperación
            expected_exception: Tipo de excepción esperada
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        
    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == 'OPEN':
                if time.time() - self.last_failure_time > self.recovery_timeout:
                    self.state = 'HALF_OPEN'
                    logging.info("Circuit breaker transitioning to HALF_OPEN")
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            try:
                result = func(*args, **kwargs)
                
                # Reset en caso de éxito
                self.failure_count = 0
                if self.state == 'HALF_OPEN':
                    self.state = 'CLOSED'
                    logging.info("Circuit breaker reset to CLOSED")
                
                return result
                
            except self.expected_exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()
                
                if self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                    logging.warning(f"Circuit breaker OPENED after {self.failure_count} failures")
                
                raise e
        
        return wrapper


def resilient_llm_call(
    max_retries: int = 3,
    temperature: float = 0.1,
    circuit_breaker: bool = True,
    timeout: Optional[float] = None
):
    """
    Decorador combinado para llamadas LLM resilientes
    
    Args:
        max_retries: Número máximo de reintentos
        temperature: Temperatura inicial del LLM
        circuit_breaker: Si usar circuit breaker
        timeout: Timeout para la llamada
    """
    def decorator(func: Callable) -> Callable:
        decorated_func = func
        
        # Aplicar timeout si se especifica
        if timeout:
            @wraps(decorated_func)
            def with_timeout(*args, **kwargs):
                import signal
                
                def timeout_handler(signum, frame):
                    raise TimeoutError(f"Function call timed out after {timeout} seconds")
                
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(int(timeout))
                
                try:
                    result = decorated_func(*args, **kwargs)
                    return result
                finally:
                    signal.alarm(0)
            
            decorated_func = with_timeout
        
        # Aplicar circuit breaker
        if circuit_breaker:
            decorated_func = CircuitBreaker(failure_threshold=3)(decorated_func)
        
        # Aplicar retry de LLM
        decorated_func = llm_retry(max_attempts=max_retries, temperature=temperature)(decorated_func)
        
        return decorated_func
    
    return decorator


# Clase para manejo de reintentos con contexto
class RetryContext:
    """
    Context manager para operaciones con retry
    """
    
    def __init__(self, strategy: RetryStrategy = RetryStrategy.STANDARD, **config):
        self.strategy = strategy
        self.config = config
        self.attempts = 0
        self.max_attempts = config.get('stop', stop_after_attempt(5)).stop
        
    def __enter__(self):
        self.attempts = 0
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.attempts += 1
            if self.attempts < self.max_attempts:
                # Calcular tiempo de espera
                wait_time = 2 ** self.attempts  # Exponential backoff
                logging.warning(f"Attempt {self.attempts}/{self.max_attempts} failed. Waiting {wait_time}s...")
                time.sleep(wait_time)
                return True  # Suprimir excepción para reintento
        return False
    
    @property
    def should_retry(self) -> bool:
        """Indica si se debe reintentar"""
        return self.attempts < self.max_attempts


# Funciones de conveniencia
def retry_with_backoff(max_attempts: int = 3, backoff_factor: float = 1.0):
    """Retry con backoff exponencial simple"""
    return with_retry(
        strategy={
            'stop': stop_after_attempt(max_attempts),
            'wait': wait_exponential(multiplier=backoff_factor, min=1, max=30)
        }
    )


def retry_with_jitter(max_attempts: int = 5):
    """Retry con jitter aleatorio para evitar thundering herd"""
    return with_retry(
        strategy={
            'stop': stop_after_attempt(max_attempts),
            'wait': wait_random_exponential(multiplier=1, max=30)
        }
    )


if __name__ == "__main__":
    # Ejemplos de uso
    
    @network_retry(max_attempts=3)
    def test_network_call(url: str):
        """Simula llamada de red"""
        import random
        if random.random() < 0.7:  # 70% probabilidad de fallo
            raise ConnectionError("Network error")
        return f"Response from {url}"
    
    @llm_retry(max_attempts=2)
    def test_llm_call(prompt: str):
        """Simula llamada a LLM"""
        import random
        if random.random() < 0.5:  # 50% probabilidad de fallo
            raise TimeoutError("LLM timeout")
        return f"LLM response for: {prompt[:50]}..."
    
    @CircuitBreaker(failure_threshold=3)
    def test_circuit_breaker():
        """Simula servicio que falla"""
        import random
        if random.random() < 0.8:  # 80% probabilidad de fallo
            raise Exception("Service unavailable")
        return "Service response"
    
    print("Testing retry patterns...")
    
    # Test network retry
    try:
        result = test_network_call("https://api.example.com")
        print(f"Network call success: {result}")
    except Exception as e:
        print(f"Network call failed: {e}")
    
    # Test LLM retry
    try:
        result = test_llm_call("Test prompt")
        print(f"LLM call success: {result}")
    except Exception as e:
        print(f"LLM call failed: {e}")
    
    # Test circuit breaker
    for i in range(5):
        try:
            result = test_circuit_breaker()
            print(f"Circuit breaker test {i}: {result}")
        except Exception as e:
            print(f"Circuit breaker test {i}: {e}")
    
    print("Retry patterns test completed")