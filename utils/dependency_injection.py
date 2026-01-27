"""
Sistema de Inyección de Dependencias para el Proyecto A2A

Elimina hardcoded dependencies y permite configuración flexible
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, Optional, Protocol
from enum import Enum

import requests
from langchain_ollama import ChatOllama


class Environment(Enum):
    """Ambientes de ejecución"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


@dataclass
class NS3Config:
    """Configuración de NS-3"""
    root_path: Path
    version: str
    python_bindings_path: Optional[Path] = None
    executable_path: Optional[Path] = None
    
    def __post_init__(self):
        """Valida y completa paths"""
        if self.python_bindings_path is None:
            self.python_bindings_path = self.root_path / "build" / "bindings" / "python"
        
        if self.executable_path is None:
            self.executable_path = self.root_path / "ns3"
        
        # Validar que existan
        if not self.root_path.exists():
            raise ValueError(f"NS-3 root path does not exist: {self.root_path}")
        
        if not self.python_bindings_path.exists():
            raise ValueError(f"NS-3 Python bindings not found: {self.python_bindings_path}")


@dataclass
class OllamaConfig:
    """Configuración de Ollama"""
    base_url: str
    reasoning_model: str
    coding_model: str
    embedding_model: str
    timeout: int = 120
    
    def __post_init__(self):
        """Valida configuración"""
        # Validar URL
        if not self.base_url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid Ollama URL: {self.base_url}")


@dataclass
class DatabaseConfig:
    """Configuración de base de datos"""
    chroma_path: Path
    sqlite_path: Path
    collection_name: str = "thesis_papers"
    
    def __post_init__(self):
        """Asegura que los directorios existan"""
        self.chroma_path.mkdir(parents=True, exist_ok=True)
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)


@dataclass
class LoggingConfig:
    """Configuración de logging"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[Path] = None
    
    def __post_init__(self):
        """Crea directorio de logs si es necesario"""
        if self.file_path:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)


class ConfigProvider(ABC):
    """Interfaz abstracta para proveedores de configuración"""
    
    @abstractmethod
    def get_ns3_config(self) -> NS3Config:
        """Obtiene configuración de NS-3"""
        pass
    
    @abstractmethod
    def get_ollama_config(self) -> OllamaConfig:
        """Obtiene configuración de Ollama"""
        pass
    
    @abstractmethod
    def get_database_config(self) -> DatabaseConfig:
        """Obtiene configuración de base de datos"""
        pass
    
    @abstractmethod
    def get_logging_config(self) -> LoggingConfig:
        """Obtiene configuración de logging"""
        pass


class EnvironmentConfigProvider(ConfigProvider):
    """Proveedor de configuración basado en variables de entorno"""
    
    def __init__(self, environment: Environment = Environment.DEVELOPMENT):
        self.environment = environment
        self.project_root = self._get_project_root()
    
    def _get_project_root(self) -> Path:
        """Obtiene el directorio raíz del proyecto"""
        # Intentar desde variable de entorno
        if 'PROJECT_ROOT' in os.environ:
            return Path(os.environ['PROJECT_ROOT'])
        
        # Intentar desde el archivo actual
        current_file = Path(__file__).resolve()
        return current_file.parent.parent
    
    def get_ns3_config(self) -> NS3Config:
        """Obtiene configuración de NS-3 desde variables de entorno"""
        ns3_path = os.getenv('NS3_ROOT')
        if not ns3_path:
            # Default basado en el directorio home
            ns3_path = Path.home() / "ns-3.45"
        else:
            ns3_path = Path(ns3_path)
        
        return NS3Config(
            root_path=ns3_path,
            version=os.getenv('NS3_VERSION', '3.45')
        )
    
    def get_ollama_config(self) -> OllamaConfig:
        """Obtiene configuración de Ollama desde variables de entorno"""
        return OllamaConfig(
            base_url=os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434'),
            reasoning_model=os.getenv('MODEL_REASONING', 'llama3.1:8b'),
            coding_model=os.getenv('MODEL_CODING', 'llama3.1:8b'),
            embedding_model=os.getenv('MODEL_EMBEDDING', 'nomic-embed-text'),
            timeout=int(os.getenv('LLM_TIMEOUT', '120'))
        )
    
    def get_database_config(self) -> DatabaseConfig:
        """Obtiene configuración de base de datos desde variables de entorno"""
        data_dir = self.project_root / "data"
        logs_dir = self.project_root / "logs"
        
        return DatabaseConfig(
            chroma_path=data_dir / "vector_db",
            sqlite_path=logs_dir / "langgraph_checkpoints.db",
            collection_name=os.getenv('CHROMA_COLLECTION', 'thesis_papers')
        )
    
    def get_logging_config(self) -> LoggingConfig:
        """Obtiene configuración de logging desde variables de entorno"""
        logs_dir = self.project_root / "logs"
        
        return LoggingConfig(
            level=os.getenv('LOG_LEVEL', 'INFO'),
            format=os.getenv('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            file_path=logs_dir / "sistema_a2a.log"
        )


class ServiceContainer:
    """
    Contenedor de inyección de dependencias
    """
    
    def __init__(self, config_provider: ConfigProvider):
        self.config_provider = config_provider
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register(self, name: str, factory, singleton: bool = False):
        """Registra un servicio"""
        self._services[name] = {
            'factory': factory,
            'singleton': singleton
        }
    
    def get(self, name: str):
        """Obtiene un servicio del contenedor"""
        if name not in self._services:
            raise ValueError(f"Service '{name}' not registered")
        
        service_config = self._services[name]
        
        if service_config['singleton']:
            if name not in self._singletons:
                self._singletons[name] = service_config['factory'](self)
            return self._singletons[name]
        else:
            return service_config['factory'](self)
    
    def get_config(self) -> ConfigProvider:
        """Obtiene el proveedor de configuración"""
        return self.config_provider


# Factories para servicios
def create_ollama_client(container: ServiceContainer) -> ChatOllama:
    """Factory para cliente Ollama"""
    config = container.get_config().get_ollama_config()
    return ChatOllama(
        base_url=config.base_url,
        model=config.reasoning_model,
        timeout=config.timeout
    )


def create_coding_llm(container: ServiceContainer) -> ChatOllama:
    """Factory para LLM de coding"""
    config = container.get_config().get_ollama_config()
    return ChatOllama(
        base_url=config.base_url,
        model=config.coding_model,
        temperature=0.05,
        timeout=config.timeout
    )


def create_reasoning_llm(container: ServiceContainer) -> ChatOllama:
    """Factory para LLM de razonamiento"""
    config = container.get_config().get_ollama_config()
    return ChatOllama(
        base_url=config.base_url,
        model=config.reasoning_model,
        temperature=0.1,
        timeout=config.timeout
    )


def create_requests_session(container: ServiceContainer) -> requests.Session:
    """Factory para sesión de requests con retry"""
    session = requests.Session()
    
    # Configurar retry strategy
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


class DIContainer:
    """
    Contenedor principal de inyección de dependencias
    """
    
    def __init__(self, environment: Environment = Environment.DEVELOPMENT):
        self.environment = environment
        self.config_provider = EnvironmentConfigProvider(environment)
        self.container = ServiceContainer(self.config_provider)
        self._register_services()
    
    def _register_services(self):
        """Registra todos los servicios en el contenedor"""
        # LLMs
        self.container.register('ollama_client', create_ollama_client, singleton=True)
        self.container.register('coding_llm', create_coding_llm, singleton=True)
        self.container.register('reasoning_llm', create_reasoning_llm, singleton=True)
        
        # HTTP Client
        self.container.register('requests_session', create_requests_session, singleton=True)
    
    def get_ollama_client(self) -> ChatOllama:
        """Obtiene cliente Ollama"""
        return self.container.get('ollama_client')
    
    def get_coding_llm(self) -> ChatOllama:
        """Obtiene LLM para coding"""
        return self.container.get('coding_llm')
    
    def get_reasoning_llm(self) -> ChatOllama:
        """Obtiene LLM para razonamiento"""
        return self.container.get('reasoning_llm')
    
    def get_requests_session(self) -> requests.Session:
        """Obtiene sesión HTTP"""
        return self.container.get('requests_session')
    
    def get_ns3_config(self) -> NS3Config:
        """Obtiene configuración de NS-3"""
        return self.config_provider.get_ns3_config()
    
    def get_database_config(self) -> DatabaseConfig:
        """Obtiene configuración de base de datos"""
        return self.config_provider.get_database_config()
    
    def get_logging_config(self) -> LoggingConfig:
        """Obtiene configuración de logging"""
        return self.config_provider.get_logging_config()
    
    def validate_configuration(self) -> List[str]:
        """Valida toda la configuración"""
        errors = []
        
        try:
            ns3_config = self.get_ns3_config()
            # Validar NS-3
            if not ns3_config.root_path.exists():
                errors.append(f"NS-3 no encontrado en: {ns3_config.root_path}")
            
            if not ns3_config.python_bindings_path.exists():
                errors.append(f"Bindings de Python NS-3 no encontrados en: {ns3_config.python_bindings_path}")
                
        except Exception as e:
            errors.append(f"Error en configuración NS-3: {e}")
        
        try:
            ollama_config = self.config_provider.get_ollama_config()
            # Validar Ollama
            session = self.get_requests_session()
            response = session.get(f"{ollama_config.base_url}/api/tags", timeout=5)
            if response.status_code != 200:
                errors.append(f"Ollama no responde en: {ollama_config.base_url}")
                
        except Exception as e:
            errors.append(f"Error en configuración Ollama: {e}")
        
        return errors


# Instancia global del contenedor
_di_container: Optional[DIContainer] = None


def get_di_container() -> DIContainer:
    """Obtiene la instancia global del contenedor de DI"""
    global _di_container
    
    if _di_container is None:
        # Determinar ambiente
        env_name = os.getenv('ENVIRONMENT', 'development').lower()
        environment = Environment(env_name) if env_name in [e.value for e in Environment] else Environment.DEVELOPMENT
        
        _di_container = DIContainer(environment)
    
    return _di_container


def initialize_di(environment: Environment = Environment.DEVELOPMENT) -> DIContainer:
    """Inicializa el contenedor de DI con un ambiente específico"""
    global _di_container
    _di_container = DIContainer(environment)
    return _di_container


# Funciones de conveniencia para obtener servicios
def get_ollama_client() -> ChatOllama:
    """Obtiene cliente Ollama desde DI container"""
    return get_di_container().get_ollama_client()


def get_coding_llm() -> ChatOllama:
    """Obtiene LLM para coding desde DI container"""
    return get_di_container().get_coding_llm()


def get_reasoning_llm() -> ChatOllama:
    """Obtiene LLM para razonamiento desde DI container"""
    return get_di_container().get_reasoning_llm()


def get_ns3_config() -> NS3Config:
    """Obtiene configuración NS-3 desde DI container"""
    return get_di_container().get_ns3_config()


def validate_system_configuration() -> List[str]:
    """Valida configuración del sistema usando DI"""
    return get_di_container().validate_configuration()