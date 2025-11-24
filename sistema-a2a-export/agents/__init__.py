"""
Módulo de Agentes del Sistema A2A

Contiene todos los agentes especializados que componen el sistema.
"""

from .researcher import research_node
from .coder import coder_node
from .simulator import simulator_node
from .analyst import analyst_node
from .visualizer import visualizer_node
from .github_manager import github_manager_node
from .optimizer import optimizer_node
from .trace_analyzer import trace_analyzer_node

__all__ = [
    'research_node',
    'coder_node',
    'simulator_node',
    'analyst_node',
    'visualizer_node',
    'github_manager_node',
    'optimizer_node',
    'trace_analyzer_node'
]
