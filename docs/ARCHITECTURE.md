# 🏗️ System Architecture - A2A Framework

**Detailed technical architecture documentation**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Agent Architecture](#agent-architecture)
4. [Data Flow](#data-flow)
5. [State Management](#state-management)
6. [Communication Patterns](#communication-patterns)
7. [Error Handling](#error-handling)
8. [Performance Considerations](#performance-considerations)

---

## 🎯 Overview

A2A is a **multi-agent system** built on LangGraph that orchestrates specialized agents to automate network protocol research. The architecture follows these principles:

### Design Principles

1. **Modularity**: Each agent is independent and replaceable
2. **Scalability**: Can handle multiple concurrent experiments
3. **Extensibility**: Easy to add new agents or capabilities
4. **Reliability**: Robust error handling and recovery
5. **Reproducibility**: Deterministic execution with controlled randomness

### Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │  Main    │  │Examples  │  │  Tests   │   │
│  │(Streamlit│  │  CLI     │  │          │  │          │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    Orchestration Layer                     │
│  ┌────────────────────────────────────────────────────┐   │
│  │         Supervisor (LangGraph)                     │   │
│  │  - Workflow definition                             │   │
│  │  - State management                                │   │
│  │  - Agent coordination                              │   │
│  └────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                      Agent Layer                           │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐  │
│  │Agent1│ │Agent2│ │Agent3│ │Agent4│ │Agent5│ │Agent6│  │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘  │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                    │
│  │Agent7│ │Agent8│ │Agent9│ │Agent10│                   │
│  └──────┘ └──────┘ └──────┘ └──────┘                    │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────▼─────────────────────────────┐
│                    Infrastructure Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
│  │  LLM     │  │  NS-3    │  │ChromaDB  │  │ SQLite   │ │
│  │(Ollama)  │  │Simulator │  │(Vectors) │  │(Memory)  │ │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🧩 System Components

### 1. Supervisor (Orchestrator)

**Location**: `supervisor.py`

**Responsibilities**:
- Define agent workflow graph
- Manage state transitions
- Handle agent execution
- Provide checkpointing
- Error recovery

**Implementation**:
```python
class SupervisorOrchestrator:
    def __init__(self):
        self.workflow = StateGraph(AgentState)
        self._setup_agents()
        self._setup_edges()
        self.app = self.workflow.compile(checkpointer=SqliteSaver(...))
    
    def run(self, initial_state: AgentState) -> AgentState:
        return self.app.invoke(initial_state)
```

### 2. Agents

**Location**: `agents/`

Each agent is a Python module with a main function:

```python
def agent_node(state: AgentState) -> AgentState:
    """
    Agent implementation
    
    Args:
        state: Current system state
        
    Returns:
        Updated system state
    """
    # Process input
    # Execute agent logic
    # Update state
    # Return state
```

#### Agent Types

| Agent | Type | Primary Tool | Output |
|-------|------|--------------|--------|
| Researcher | Information Retrieval | Semantic Scholar API | Papers, References |
| Coder | Code Generation | LLM | NS-3 Scripts |
| Simulator | Execution | NS-3 | Trace Files |
| Trace Analyzer | Data Processing | Scapy/PyShark | Metrics Data |
| Analyst | Statistical Analysis | Pandas/SciPy | KPIs, Statistics |
| Visualizer | Data Visualization | Matplotlib/Plotly | Graphics, Tables |
| Optimizer | Machine Learning | PyTorch | Optimized Policies |
| NS3-AI Integration | System Integration | ns3-ai | DRL Training |
| Critic | Quality Assurance | LLM | Validation Report |
| Scientific Writer | Document Generation | LLM | Academic Documents |

### 3. Utilities

**Location**: `utils/`

#### Memory System (`utils/memory.py`)

```python
class EpisodicMemory:
    """
    Stores and retrieves past experiences
    
    Features:
    - Similarity-based retrieval
    - Error pattern learning
    - Success case storage
    """
    
    def store_experience(self, experience: Dict) -> None:
        """Store new experience"""
        
    def retrieve_similar(self, query: str, k: int = 5) -> List[Dict]:
        """Retrieve similar experiences"""
```

#### Error Handling (`utils/errors.py`)

```python
class A2AError(Exception):
    """Base exception for A2A"""

class CompilationError(A2AError):
    """NS-3 compilation failed"""

class SimulationError(A2AError):
    """Simulation execution failed"""

class AnalysisError(A2AError):
    """Data analysis failed"""
```

#### Logging (`utils/logging_utils.py`)

```python
def log_info(message: str) -> None:
    """Log info message"""

def log_error(message: str) -> None:
    """Log error message"""

def update_agent_status(agent: str, status: str) -> None:
    """Update agent status in dashboard"""
```

### 4. Configuration

**Location**: `config/settings.py`

```python
# LLM Configuration
MODEL_REASONING = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
RESULTS_DIR = BASE_DIR / "experiments" / "results"

# Simulation Settings
DEFAULT_NODES = 20
DEFAULT_DURATION = 200
DEFAULT_REPETITIONS = 10

# Analysis Settings
CONFIDENCE_LEVEL = 0.95
SIGNIFICANCE_LEVEL = 0.05
```

---

## 🤖 Agent Architecture

### Agent Lifecycle

```
┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Receive     │
│ State       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validate    │
│ Input       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Execute     │
│ Logic       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Update      │
│ State       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Return      │
│ State       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   End       │
└─────────────┘
```

### Agent Communication

Agents communicate through **shared state**:

```python
AgentState = TypedDict('AgentState', {
    # Input data
    'task': str,
    'protocols': List[str],
    'configuration': Dict[str, Any],
    
    # Intermediate results
    'papers': List[Dict],
    'code': str,
    'simulation_output': str,
    'trace_data': pd.DataFrame,
    'metrics': Dict[str, Any],
    
    # Final outputs
    'experiment_results': Dict[str, Any],
    'generated_document': str,
    
    # Metadata
    'messages': List[str],
    'error': Optional[str],
    'timestamp': str
})
```

### Agent Patterns

#### 1. LLM-Based Agent

```python
def llm_agent_node(state: AgentState) -> AgentState:
    """Agent that uses LLM for processing"""
    
    # Create prompt
    prompt = create_prompt(state)
    
    # Call LLM
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]
    response = llm.invoke(messages)
    
    # Process response
    result = parse_response(response.content)
    
    # Update state
    state["output"] = result
    return state
```

#### 2. Tool-Based Agent

```python
def tool_agent_node(state: AgentState) -> AgentState:
    """Agent that uses external tools"""
    
    # Extract input
    input_data = state["input"]
    
    # Use tool
    result = external_tool.process(input_data)
    
    # Update state
    state["output"] = result
    return state
```

#### 3. Hybrid Agent

```python
def hybrid_agent_node(state: AgentState) -> AgentState:
    """Agent that combines LLM and tools"""
    
    # Use tool for data processing
    processed_data = tool.process(state["input"])
    
    # Use LLM for analysis
    analysis = llm.analyze(processed_data)
    
    # Combine results
    state["output"] = {
        "data": processed_data,
        "analysis": analysis
    }
    return state
```

---

## 🔄 Data Flow

### Complete Workflow

```
User Request
     │
     ▼
┌─────────────────────────────────────────────────────────┐
│                    Supervisor                            │
└─────────────────────────────────────────────────────────┘
     │
     ├──► Researcher ──► papers ──┐
     │                             │
     ├──► Coder ──────► code ─────┤
     │                             │
     ├──► Simulator ──► traces ───┤
     │                             ├──► Shared State
     ├──► Trace Analyzer ► data ──┤
     │                             │
     ├──► Analyst ────► metrics ──┤
     │                             │
     ├──► Visualizer ─► graphics ─┤
     │                             │
     └──► Scientific Writer ► doc ┘
                │
                ▼
           Final Results
```

### State Evolution

```python
# Initial State
state = {
    "task": "compare_protocols",
    "protocols": ["AODV", "OLSR"],
    "messages": []
}

# After Researcher
state = {
    ...
    "papers": [
        {"title": "...", "authors": "...", "year": 2020},
        ...
    ]
}

# After Coder
state = {
    ...
    "code": "/* NS-3 simulation code */"
}

# After Simulator
state = {
    ...
    "simulation_output": "Simulation completed",
    "trace_files": ["trace1.pcap", "trace2.pcap"]
}

# After Analyst
state = {
    ...
    "metrics": {
        "AODV": {"pdr": 0.87, "delay": 45.2, ...},
        "OLSR": {"pdr": 0.91, "delay": 38.7, ...}
    }
}

# After Scientific Writer
state = {
    ...
    "generated_document": "# Technical Report\n\n..."
}
```

---

## 💾 State Management

### State Structure

```python
from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict, total=False):
    # Task definition
    task: str
    protocols: List[str]
    configuration: Dict[str, Any]
    
    # Research phase
    papers: List[Dict[str, Any]]
    references: List[str]
    
    # Code generation phase
    code: str
    compilation_output: str
    
    # Simulation phase
    simulation_output: str
    trace_files: List[str]
    
    # Analysis phase
    trace_data: Any  # pandas DataFrame
    metrics: Dict[str, Any]
    statistical_analysis: Dict[str, Any]
    
    # Visualization phase
    graphics: List[str]
    tables: List[str]
    
    # Documentation phase
    generated_document: str
    document_path: str
    
    # Metadata
    messages: List[str]
    error: Optional[str]
    timestamp: str
    agent_status: Dict[str, str]
```

### State Persistence

```python
# Checkpointing with SQLite
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

app = workflow.compile(checkpointer=checkpointer)

# Run with checkpointing
config = {"configurable": {"thread_id": "experiment_1"}}
result = app.invoke(initial_state, config=config)

# Resume from checkpoint
result = app.invoke(None, config=config)
```

---

## 📡 Communication Patterns

### 1. Sequential Execution

```python
workflow.add_edge("agent1", "agent2")
workflow.add_edge("agent2", "agent3")
workflow.add_edge("agent3", END)
```

```
Agent1 ──► Agent2 ──► Agent3 ──► END
```

### 2. Conditional Routing

```python
def router(state: AgentState) -> str:
    if state.get("error"):
        return "error_handler"
    elif state.get("needs_optimization"):
        return "optimizer"
    else:
        return "next_agent"

workflow.add_conditional_edges(
    "current_agent",
    router,
    {
        "error_handler": "error_handler",
        "optimizer": "optimizer",
        "next_agent": "next_agent"
    }
)
```

```
                    ┌──► Error Handler
                    │
Current Agent ──────┼──► Optimizer
                    │
                    └──► Next Agent
```

### 3. Parallel Execution

```python
# Not directly supported in LangGraph
# Workaround: Use async execution

async def parallel_agents(state: AgentState) -> AgentState:
    results = await asyncio.gather(
        agent1_async(state),
        agent2_async(state),
        agent3_async(state)
    )
    
    # Merge results
    state["combined_results"] = merge_results(results)
    return state
```

---

## ⚠️ Error Handling

### Error Hierarchy

```
A2AError (Base)
├── CompilationError
├── SimulationError
├── TraceAnalysisError
├── AnalysisError
├── VisualizationError
├── OptimizationError
├── DocumentGenerationError
└── GitHubError
```

### Error Handling Strategy

```python
def agent_with_error_handling(state: AgentState) -> AgentState:
    """Agent with comprehensive error handling"""
    
    try:
        # Main logic
        result = process_data(state)
        state["output"] = result
        
    except SpecificError as e:
        # Handle specific error
        log_error(f"Specific error: {e}")
        state["error"] = str(e)
        
        # Try recovery
        if can_recover(e):
            result = recover_from_error(state, e)
            state["output"] = result
            state["error"] = None
        
    except Exception as e:
        # Handle unexpected error
        log_error(f"Unexpected error: {e}")
        state["error"] = str(e)
        
        # Store in episodic memory
        memory.store_experience({
            "type": "error",
            "agent": "agent_name",
            "error": str(e),
            "state": state
        })
    
    finally:
        # Cleanup
        cleanup_resources()
    
    return state
```

### Retry Mechanism

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def agent_with_retry(state: AgentState) -> AgentState:
    """Agent with automatic retry"""
    # Logic that might fail
    pass
```

---

## ⚡ Performance Considerations

### Optimization Strategies

#### 1. Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(input_data: str) -> str:
    """Cache expensive computations"""
    # Expensive operation
    pass
```

#### 2. Lazy Loading

```python
class LazyAgent:
    def __init__(self):
        self._llm = None
    
    @property
    def llm(self):
        if self._llm is None:
            self._llm = ChatOllama(...)
        return self._llm
```

#### 3. Batch Processing

```python
def process_batch(items: List[Any]) -> List[Any]:
    """Process items in batches"""
    batch_size = 10
    results = []
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        batch_results = process_items(batch)
        results.extend(batch_results)
    
    return results
```

#### 4. Resource Management

```python
import psutil

def check_resources():
    """Check system resources"""
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    
    if cpu_percent > 90 or memory_percent > 90:
        log_warning("High resource usage")
        # Throttle or pause execution
```

### Performance Metrics

| Component | Typical Time | Optimization |
|-----------|-------------|--------------|
| Researcher | 30-60s | Cache results |
| Coder | 10-30s | Template reuse |
| Simulator | 5-30min | Parallel runs |
| Trace Analyzer | 1-5min | Batch processing |
| Analyst | 10-30s | Vectorization |
| Visualizer | 5-15s | Lazy rendering |
| Scientific Writer | 30-120s | Prompt optimization |

---

## 🔐 Security Considerations

### Input Validation

```python
def validate_input(state: AgentState) -> bool:
    """Validate input state"""
    required_keys = ["task", "protocols"]
    
    for key in required_keys:
        if key not in state:
            raise ValueError(f"Missing required key: {key}")
    
    # Validate protocols
    valid_protocols = ["AODV", "OLSR", "DSDV", "DSR"]
    for protocol in state["protocols"]:
        if protocol not in valid_protocols:
            raise ValueError(f"Invalid protocol: {protocol}")
    
    return True
```

### Sandboxing

```python
import subprocess

def run_simulation_sandboxed(script: str) -> str:
    """Run simulation in sandboxed environment"""
    # Use subprocess with timeout
    result = subprocess.run(
        ["ns3", "run", script],
        timeout=3600,  # 1 hour max
        capture_output=True,
        text=True
    )
    
    return result.stdout
```

---

**For more details, see:**
- [Developer Guide](DEVELOPER_GUIDE.md)
- [API Reference](API.md)
- [Contributing Guide](../CONTRIBUTING.md)

[← Back to README](../README.md)
