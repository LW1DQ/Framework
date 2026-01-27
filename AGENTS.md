# AGENTS.md - A2A Multi-Agent System Development Guide

This file contains essential information for agentic coding agents working in the A2A (Agent-to-Agent) multi-agent system repository.

## Build, Test, and Development Commands

### Testing
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_basic.py -v

# Run tests by marker
pytest tests/ -m unit                    # Unit tests only
pytest tests/ -m integration            # Integration tests only
pytest tests/ -m "not slow"              # Skip slow tests
pytest tests/ -m requires_ns3            # Tests requiring NS-3
pytest tests/ -m requires_ollama         # Tests requiring Ollama

# Run with coverage
pytest tests/ --cov=agents --cov=utils

# Run single test function
pytest tests/test_basic.py::TestState::test_create_initial_state -v
```

### Code Quality
```bash
# Linting (if flake8 is available)
flake8 agents/ utils/ --max-line-length=100

# Type checking (if mypy is available)
mypy agents/ utils/ --ignore-missing-imports

# Format code (if black is available)
black agents/ utils/ --line-length=100
```

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e ".[dev]"

# NS-3 bindings path (critical for simulations)
export PYTHONPATH=$PYTHONPATH:/path/to/ns3/build/bindings/python
```

## Code Style Guidelines

### File Structure and Imports
1. **Shebang and Docstring**: Every Python file starts with `#!/usr/bin/env python3` and a module docstring
2. **Path Setup**: Use sys.path.insert(0, str(Path(__file__).parent.parent)) for imports from project root
3. **Import Organization**:
   - Standard library imports first
   - Third-party imports second
   - Local imports last (agents.*, utils.*, config.*)

```python
#!/usr/bin/env python3
"""
Module description in Spanish
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, List, Optional
import pandas as pd
import numpy as np

from langchain_ollama import ChatOllama
from agents.researcher import research_node
from utils.state import AgentState
from config.settings import OLLAMA_BASE_URL
```

### Type Hints and Documentation
- **TypedDict for State**: Use TypedDict for complex state objects
- **Annotated for Lists**: Use `Annotated[List[str], operator.add]` for accumulative lists
- **Function Documentation**: Use Spanish docstrings with Args, Returns sections

```python
from typing import TypedDict, List, Annotated, Dict, Any, Optional
import operator

class AgentState(TypedDict):
    """Estado compartido entre todos los agentes del sistema."""
    
    task: str
    research_notes: Annotated[List[str], operator.add]
    papers_found: Annotated[List[Dict[str, Any]], operator.add]

def process_data(data: Dict[str, Any], option: Optional[str] = None) -> List[str]:
    """
    Procesa los datos del agente.
    
    Args:
        data: Diccionario con datos de entrada
        option: Opción opcional de procesamiento
        
    Returns:
        Lista de resultados procesados
    """
```

### Naming Conventions
- **Variables and Functions**: `snake_case` (Spanish preferred)
- **Classes**: `PascalCase` (Spanish preferred)
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `snake_case.py`

```python
# Variables
estado_agente = "pending"
resultados_simulacion = []

# Functions
def generar_codigo() -> str:
    pass

def analizar_trazas(pcap_files: List[str]) -> Dict:
    pass

# Classes
class AgenteSimulador:
    pass

class EstadoGlobal:
    pass

# Constants
MAX_ITERATIONS = 5
NS3_TEMPLATE = "template"
```

### Error Handling
- **Custom Exceptions**: Create specific exception classes in utils/errors.py
- **Try-Catch Blocks**: Use Spanish error messages
- **Logging**: Use utils.logging_utils for consistent logging

```python
from utils.errors import CodeGenerationError, SimulationError
from utils.logging_utils import log_message

try:
    result = generate_code(task)
except CodeGenerationError as e:
    log_message(f"Error en generación de código: {e}")
    raise
except Exception as e:
    log_message(f"Error inesperado: {e}")
    raise SimulationError(f"Fallo en simulación: {e}")
```

### Agent Node Pattern
All agent functions follow the LangGraph node pattern:

```python
def agent_node(state: AgentState) -> AgentState:
    """
    Agente especializado que procesa el estado.
    
    Args:
        state: Estado global del sistema
        
    Returns:
        Estado actualizado con resultados del agente
    """
    try:
        # 1. Update status
        update_agent_status("agent_name", "processing")
        
        # 2. Process using LLM
        llm = ChatOllama(model=MODEL_NAME, temperature=TEMP)
        
        # 3. Add audit entry
        add_audit_entry(state, "agent_name", "completed", "Success")
        
        return state
        
    except Exception as e:
        add_audit_entry(state, "agent_name", "failed", str(e))
        raise
```

### State Management
- **Immutable Updates**: Always return new state, don't modify in place
- **Accumulative Lists**: Use `Annotated[List[T], operator.add]` for lists that accumulate
- **Audit Trail**: Use `add_audit_entry()` for tracking operations

```python
from utils.state import add_audit_entry, increment_iteration

# Correct state update
def update_state(state: AgentState) -> AgentState:
    new_state = state.copy()
    new_state['status'] = 'completed'
    add_audit_entry(new_state, "agent_name", "completed", "Success")
    return new_state

# For accumulative lists
def add_note(state: AgentState, note: str) -> AgentState:
    state['research_notes'].append(note)  # Works with Annotated operator.add
    return state
```

### Configuration Management
- **Settings**: Import from config.settings
- **Environment Variables**: Use python-dotenv for .env files
- **Constants**: Define in config/settings.py

```python
from config.settings import (
    OLLAMA_BASE_URL,
    MODEL_CODING,
    MODEL_TEMPERATURE_CODING,
    SIMULATIONS_DIR
)
```

### Testing Patterns
- **Test Files**: Name as `test_*.py` in tests/ directory
- **Test Classes**: Use `Test*` prefix
- **Test Functions**: Use `test_*` prefix
- **Fixtures**: Use conftest.py for shared fixtures

```python
import pytest
from utils.state import create_initial_state

class TestAgent:
    """Tests para el agente especializado"""
    
    def test_agent_functionality(self):
        """Test de funcionalidad básica"""
        state = create_initial_state("Test task")
        result = agent_node(state)
        assert result['status'] == 'completed'
```

### NS-3 Integration Guidelines
- **Critical Path**: Always include NS-3 bindings path
- **Template Usage**: Use NS3_TEMPLATE for code generation
- **Error Handling**: Handle NS-3 specific errors gracefully

```python
# Critical for NS-3 simulations
sys.path.insert(0, '/home/diego/ns3/build/bindings/python')

import ns.core
import ns.network
import ns.internet
import ns.mobility
import ns.wifi
import ns.applications
```

### Memory and Learning
- **Episodic Memory**: Use utils.memory for learning from past experiments
- **Error Patterns**: Store and retrieve error solutions
- **Code Templates**: Maintain library of working code patterns

### Dashboard and Visualization
- **Streamlit**: Use for real-time dashboards
- **Plotly**: For interactive graphics
- **Matplotlib**: For publication-quality static plots (300 DPI)

### Documentation Standards
- **Spanish Comments**: Use Spanish for all user-facing comments
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all modules, classes, and public functions

## Critical Dependencies
- **Python**: 3.10+
- **LangGraph**: 0.2+ for agent orchestration
- **NS-3**: 3.36+ for network simulations
- **Ollama**: For local LLM execution
- **ChromaDB**: For vector storage
- **PyTorch**: For deep reinforcement learning

## Common Pitfalls
1. **NS-3 Path**: Always ensure PYTHONPATH includes NS-3 bindings
2. **State Mutation**: Never modify state in place, always return new state
3. **Error Handling**: Always add audit entries for both success and failure
4. **Memory Management**: Use episodic memory to avoid repeating mistakes
5. **Temperature Settings**: Use appropriate LLM temperature (coding: 0.1-0.3, creative: 0.7-0.9)

## Development Workflow
1. Create/modify agent function following node pattern
2. Add comprehensive tests with pytest
3. Update documentation in Spanish
4. Run full test suite before committing
5. Use audit trail to track agent performance