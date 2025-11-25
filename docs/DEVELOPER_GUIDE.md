# 👨‍💻 Developer Guide - A2A Framework

**Complete guide for developers who want to contribute or extend the A2A framework**

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Development Setup](#development-setup)
3. [Code Structure](#code-structure)
4. [Creating New Agents](#creating-new-agents)
5. [Adding Experiments](#adding-experiments)
6. [Extending the Framework](#extending-the-framework)
7. [Testing](#testing)
8. [Code Style](#code-style)
9. [Contributing](#contributing)

---

## 🏗️ Architecture Overview

### System Design

A2A follows a **multi-agent architecture** orchestrated by LangGraph:

```
┌─────────────────────────────────────────────────────────────┐
│                    Supervisor (LangGraph)                    │
│              - Orchestrates agent execution                  │
│              - Manages shared state                          │
│              - Handles error recovery                        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │ Agent 1 │          │ Agent 2 │          │ Agent N │
   │         │          │         │          │         │
   └────┬────┘          └────┬────┘          └────┬────┘
        │                     │                     │
        └─────────────────────▼─────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │   Shared State    │
                    │  - Experiments    │
                    │  - Results        │
                    │  - Messages       │
                    └───────────────────┘
```

### Key Components

#### 1. Agents (`agents/`)
Each agent is a specialized module that performs a specific task:
- **Input**: AgentState dictionary
- **Processing**: Uses LLM or specialized logic
- **Output**: Updated AgentState

#### 2. Supervisor (`supervisor.py`)
Orchestrates agent execution using LangGraph:
- Defines workflow graph
- Manages state transitions
- Handles errors and retries
- Provides checkpointing

#### 3. Utilities (`utils/`)
Shared functionality:
- **Memory**: Episodic memory for learning
- **Errors**: Custom exceptions
- **Logging**: Centralized logging
- **State**: State management

#### 4. Configuration (`config/`)
System-wide settings:
- Model configurations
- API endpoints
- Paths and directories

---

## 🔧 Development Setup

### Prerequisites

- Python 3.10+
- Git
- Virtual environment tool
- Code editor (VS Code recommended)

### Setup Steps

```bash
# 1. Clone repository
git clone https://github.com/LW1DQ/Framework.git
cd Framework

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Install pre-commit hooks
pre-commit install

# 5. Run tests to verify setup
pytest tests/ -v
```

### Development Dependencies

```bash
# Install additional dev tools
pip install black flake8 mypy pytest-cov ipython jupyter
```

### IDE Configuration

#### VS Code (Recommended)

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "editor.formatOnSave": true,
  "editor.rulers": [88],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    ".pytest_cache": true
  }
}
```

---

## 📁 Code Structure

### Directory Layout

```
Framework/
├── agents/                 # Agent implementations
│   ├── __init__.py        # Agent exports
│   ├── researcher.py      # Literature search
│   ├── coder.py           # Code generation
│   ├── simulator.py       # Simulation execution
│   ├── trace_analyzer.py  # PCAP analysis
│   ├── analyst.py         # KPI calculation
│   ├── visualizer.py      # Graphics generation
│   ├── optimizer.py       # DRL optimization
│   ├── ns3_ai_integration.py  # NS-3 integration
│   ├── critic.py          # Quality validation
│   └── scientific_writer.py   # Document generation
│
├── config/                # Configuration
│   ├── __init__.py
│   └── settings.py        # Global settings
│
├── utils/                 # Utilities
│   ├── __init__.py
│   ├── memory.py          # Episodic memory
│   ├── errors.py          # Custom exceptions
│   ├── logging_utils.py   # Logging system
│   ├── state.py           # State management
│   └── statistical_tests.py  # Statistical analysis
│
├── experiments/           # Experimentation framework
│   ├── experiment_runner.py  # Main runner
│   ├── statistical_analyzer.py  # Analysis
│   ├── configs/           # Experiment configurations
│   └── results/           # Generated results
│
├── ns3-integration/       # NS-3 integration
│   ├── drl-routing-agent.h   # C++ header
│   ├── drl-routing-agent.cc  # C++ implementation
│   └── verify-installation.py  # Verification
│
├── tests/                 # Unit tests
│   ├── test_agents.py     # Agent tests
│   └── test_integration.py  # Integration tests
│
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── API.md             # API reference
│   ├── TROUBLESHOOTING.md # Common issues
│   └── ...
│
├── examples/              # Usage examples
│   ├── test_scientific_writer.py
│   └── ...
│
├── main.py               # Main entry point
├── supervisor.py         # Agent orchestrator
├── dashboard.py          # Streamlit dashboard
├── requirements.txt      # Dependencies
└── README.md            # Project readme
```

### Module Dependencies

```
main.py
  └── supervisor.py
      ├── agents/
      │   ├── researcher.py
      │   ├── coder.py
      │   ├── simulator.py
      │   ├── trace_analyzer.py
      │   ├── analyst.py
      │   ├── visualizer.py
      │   ├── optimizer.py
      │   ├── ns3_ai_integration.py
      │   ├── critic.py
      │   └── scientific_writer.py
      ├── utils/
      │   ├── memory.py
      │   ├── errors.py
      │   ├── logging_utils.py
      │   └��─ state.py
      └── config/
          └── settings.py
```

---

## 🤖 Creating New Agents

### Agent Template

```python
"""
New Agent Module
Brief description of what this agent does
"""

from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from config.settings import MODEL_REASONING, OLLAMA_BASE_URL
from utils.logging_utils import log_info, log_error
from utils.errors import CustomAgentError
from utils.state import AgentState


# Initialize LLM
llm = ChatOllama(
    model=MODEL_REASONING,
    base_url=OLLAMA_BASE_URL,
    temperature=0.3
)


def new_agent_node(state: AgentState) -> AgentState:
    """
    Main agent function
    
    Args:
        state: Current agent state
        
    Returns:
        Updated agent state
        
    Raises:
        CustomAgentError: If agent execution fails
    """
    log_info("🤖 New Agent started")
    
    try:
        # 1. Extract input from state
        input_data = state.get("input_key", {})
        
        # 2. Process with LLM or custom logic
        result = process_data(input_data)
        
        # 3. Update state
        state["output_key"] = result
        state["messages"].append("✅ New Agent completed")
        
        log_info("✅ New Agent completed successfully")
        return state
        
    except Exception as e:
        log_error(f"❌ Error in New Agent: {e}")
        state["error"] = str(e)
        state["messages"].append(f"❌ Error: {e}")
        return state


def process_data(data: Dict[str, Any]) -> Any:
    """
    Process input data
    
    Args:
        data: Input data
        
    Returns:
        Processed result
    """
    # Your processing logic here
    pass


# Helper functions
def helper_function_1():
    """Helper function description"""
    pass


def helper_function_2():
    """Helper function description"""
    pass
```

### Integrating New Agent

1. **Create agent file**: `agents/new_agent.py`

2. **Export in `agents/__init__.py`**:
```python
from .new_agent import new_agent_node

__all__ = [
    # ... existing agents
    'new_agent_node'
]
```

3. **Add to supervisor** (`supervisor.py`):
```python
from agents import new_agent_node

# In __init__:
self.workflow.add_node("new_agent", new_agent_node)

# Add edges:
self.workflow.add_edge("previous_agent", "new_agent")
self.workflow.add_edge("new_agent", "next_agent")
```

4. **Add tests** (`tests/test_agents.py`):
```python
def test_new_agent():
    """Test new agent functionality"""
    state = {
        "input_key": test_data,
        "messages": []
    }
    
    result = new_agent_node(state)
    
    assert "output_key" in result
    assert result["output_key"] is not None
```

---

## 🧪 Adding Experiments

### Experiment Configuration

Create YAML file in `experiments/configs/`:

```yaml
# experiments/configs/my_experiment.yaml

name: "My Custom Experiment"
description: "Description of what this experiment does"

# Simulation parameters
simulation:
  protocol: "AODV"
  nodes: 30
  area: "1500x1500"
  duration: 300
  mobility_model: "RandomWaypoint"
  speed_range: "10-20"
  
# Traffic configuration
traffic:
  type: "CBR"
  rate: "4 pkt/s"
  packet_size: 512
  
# Experiment settings
experiment:
  repetitions: 10
  seeds: [12345, 23456, 34567, 45678, 56789, 67890, 78901, 89012, 90123, 1234]
  
# Analysis settings
analysis:
  confidence_level: 0.95
  statistical_tests: ["t-test", "anova"]
  
# Output settings
output:
  generate_graphics: true
  generate_tables: true
  generate_briefing: true
  graphics_dpi: 300
```

### Running Custom Experiment

```bash
python experiments/experiment_runner.py --config experiments/configs/my_experiment.yaml
```

### Experiment Runner Extension

To add custom experiment logic, extend `experiments/experiment_runner.py`:

```python
def run_custom_experiment(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Run custom experiment
    
    Args:
        config: Experiment configuration
        
    Returns:
        Experiment results
    """
    # Your custom experiment logic
    pass
```

---

## 🔌 Extending the Framework

### Adding New Protocols

1. **Create protocol implementation** in NS-3
2. **Add configuration** in `experiments/configs/`
3. **Update coder agent** to generate protocol code
4. **Add protocol references** in `agents/scientific_writer_enhanced.py`

### Adding New Metrics

1. **Extend analyst agent** (`agents/analyst.py`):
```python
def calculate_new_metric(trace_data: pd.DataFrame) -> Dict[str, float]:
    """Calculate new metric"""
    # Your calculation logic
    return {
        "mean": mean_value,
        "std": std_value,
        "ci": [lower, upper]
    }
```

2. **Update visualizer** to plot new metric
3. **Add to statistical analysis**

### Adding New Document Types

1. **Extend scientific writer** (`agents/scientific_writer_enhanced.py`):
```python
def generate_new_document_type(results: Dict, state: AgentState) -> str:
    """Generate new document type"""
    prompt = f"""Generate {document_type}..."""
    
    messages = [
        SystemMessage(content=create_academic_system_prompt()),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    return response.content
```

2. **Add to document type options**
3. **Create example script** in `examples/`

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_agents.py -v

# Run specific test
pytest tests/test_agents.py::test_researcher_node -v

# Run with coverage
pytest tests/ --cov=agents --cov=utils --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Writing Tests

#### Unit Test Example

```python
# tests/test_new_agent.py

import pytest
from agents.new_agent import new_agent_node


def test_new_agent_success():
    """Test successful agent execution"""
    state = {
        "input_key": {"data": "test"},
        "messages": []
    }
    
    result = new_agent_node(state)
    
    assert "output_key" in result
    assert result["output_key"] is not None
    assert len(result["messages"]) > 0


def test_new_agent_error_handling():
    """Test agent error handling"""
    state = {
        "input_key": None,  # Invalid input
        "messages": []
    }
    
    result = new_agent_node(state)
    
    assert "error" in result
    assert result["error"] is not None


@pytest.fixture
def sample_state():
    """Fixture for sample state"""
    return {
        "input_key": {"data": "test"},
        "messages": []
    }


def test_new_agent_with_fixture(sample_state):
    """Test using fixture"""
    result = new_agent_node(sample_state)
    assert result is not None
```

#### Integration Test Example

```python
# tests/test_integration.py

def test_full_workflow():
    """Test complete agent workflow"""
    from supervisor import SupervisorOrchestrator
    
    supervisor = SupervisorOrchestrator()
    
    initial_state = {
        "task": "compare_protocols",
        "protocols": ["AODV", "OLSR"],
        "messages": []
    }
    
    result = supervisor.run(initial_state)
    
    assert "experiment_results" in result
    assert "generated_document" in result
    assert len(result["messages"]) > 0
```

### Test Coverage Goals

- **Unit tests**: 80%+ coverage
- **Integration tests**: Key workflows covered
- **Edge cases**: Error handling tested
- **Performance**: No regression in speed

---

## 📝 Code Style

### Python Style Guide

We follow **PEP 8** with some modifications:

```python
# Line length: 88 characters (Black default)
# Indentation: 4 spaces
# Quotes: Double quotes for strings
# Imports: Grouped and sorted

# Good example:
from typing import Dict, Any, List, Optional

from langchain_ollama import ChatOllama

from config.settings import MODEL_REASONING
from utils.logging_utils import log_info


def process_data(
    input_data: Dict[str, Any],
    options: Optional[Dict[str, Any]] = None
) -> List[str]:
    """
    Process input data and return results.
    
    Args:
        input_data: Dictionary containing input data
        options: Optional processing options
        
    Returns:
        List of processed results
        
    Raises:
        ValueError: If input_data is invalid
    """
    if not input_data:
        raise ValueError("input_data cannot be empty")
    
    results = []
    for key, value in input_data.items():
        processed = _process_item(key, value, options)
        results.append(processed)
    
    return results


def _process_item(key: str, value: Any, options: Optional[Dict] = None) -> str:
    """Private helper function"""
    # Implementation
    pass
```

### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional, Union, Tuple

def function_name(
    param1: str,
    param2: int,
    param3: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    """Function with type hints"""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def complex_function(param1: str, param2: int) -> Dict[str, Any]:
    """
    Brief description of function.
    
    Longer description if needed. Can span multiple lines
    and include details about the function's behavior.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary containing:
            - key1: Description of key1
            - key2: Description of key2
            
    Raises:
        ValueError: If param1 is empty
        TypeError: If param2 is not an integer
        
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result["key1"])
        'value1'
    """
    pass
```

### Code Formatting

```bash
# Format code with Black
black agents/ utils/ tests/

# Check with flake8
flake8 agents/ utils/ tests/

# Type check with mypy
mypy agents/ utils/
```

### Pre-commit Hooks

`.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: ['--max-line-length=88', '--extend-ignore=E203']

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## 🤝 Contributing

### Contribution Workflow

1. **Fork repository**
2. **Create feature branch**: `git checkout -b feature/my-feature`
3. **Make changes**
4. **Add tests**
5. **Run tests**: `pytest tests/ -v`
6. **Format code**: `black .`
7. **Commit**: `git commit -m "Add my feature"`
8. **Push**: `git push origin feature/my-feature`
9. **Create Pull Request**

### Commit Messages

Follow conventional commits:

```
feat: Add new agent for X
fix: Resolve issue with Y
docs: Update developer guide
test: Add tests for Z
refactor: Improve code structure
style: Format code
chore: Update dependencies
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests passing

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings
```

---

## 📚 Additional Resources

### Documentation
- [Architecture](ARCHITECTURE.md)
- [API Reference](API.md)
- [Troubleshooting](TROUBLESHOOTING.md)

### External Resources
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [NS-3 Documentation](https://www.nsnam.org/documentation/)
- [PyTorch Documentation](https://pytorch.org/docs/)

### Community
- [GitHub Discussions](https://github.com/LW1DQ/Framework/discussions)
- [Issue Tracker](https://github.com/LW1DQ/Framework/issues)

---

**Happy coding! 🚀**

[← Back to README](../README.md) | [Architecture →](ARCHITECTURE.md) | [API Reference →](API.md)
