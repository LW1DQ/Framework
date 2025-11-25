# 📚 API Reference - A2A Framework (COMPLETE)

**Complete API documentation for developers**

**Version:** 1.5  
**Last Updated:** November 2025

---

## 📋 Table of Contents

1. [Core Components](#core-components)
2. [Agents API](#agents-api)
   - [Researcher Agent](#1-researcher-agent)
   - [Coder Agent](#2-coder-agent)
   - [Simulator Agent](#3-simulator-agent)
   - [Trace Analyzer Agent](#4-trace-analyzer-agent)
   - [Analyst Agent](#5-analyst-agent)
   - [Visualizer Agent](#6-visualizer-agent)
   - [Optimizer Agent](#7-optimizer-agent)
   - [Critic Agent](#8-critic-agent)
   - [GitHub Manager Agent](#9-github-manager-agent)
   - [NS3-AI Integration Agent](#10-ns3-ai-integration-agent)
   - [Scientific Writer Agent](#11-scientific-writer-agent)
3. [Utilities API](#utilities-api)
4. [Configuration API](#configuration-api)
5. [State Management](#state-management)
6. [Error Handling](#error-handling)

---

## 🎯 Core Components

### Supervisor

**Module**: `supervisor.py`

Main orchestrator that manages the multi-agent workflow using LangGraph.

#### SupervisorOrchestrator

```python
class SupervisorOrchestrator:
    """
    Orchestrates multi-agent workflow using LangGraph with checkpointing
    
    Attributes:
        workflow (StateGraph): LangGraph workflow definition
        app (CompiledGraph): Compiled workflow with SQLite checkpointer
    """
```

**Methods:**

```python
def __init__(self):
    """
    Initialize supervisor with all agents and workflow
    
    Creates:
        - StateGraph with all agent nodes
        - Conditional edges for decision logic
        - SQLite checkpointer for persistence
    """

def run_experiment(self, task: str, thread_id: str = None, max_iterations: int = 5) -> Dict:
    """
    Execute a complete experiment workflow
    
    Args:
        task: Description of the research task
        thread_id: Thread ID for checkpointing (optional, auto-generated if None)
        max_iterations: Maximum number of retry iterations (default: 5)
        
    Returns:
        Final state dictionary containing:
            - metrics (Dict): Performance metrics
            - plots_generated (List[str]): Paths to generated plots
            - code_filepath (str): Path to generated code
            - errors (List[str]): List of errors encountered
            - audit_trail (List[Dict]): Complete audit trail
            
    Example:
        >>> supervisor = SupervisorOrchestrator()
        >>> result = supervisor.run_experiment(
        ...     task="Simulate AODV with 20 nodes in 500x500m area",
        ...     max_iterations=3
        ... )
        >>> print(f"PDR: {result['metrics']['avg_pdr']:.2f}%")
    """
```

**Workflow Decision Functions:**

```python
def _should_retry_code(self, state: AgentState) -> Literal["critic", "retry", "end"]:
    """
    Decides whether to retry code generation based on syntax validation
    
    Logic:
        - If errors exist and iterations < max: "retry"
        - If code validated: "critic"
        - If max iterations reached: "end"
    """

def _should_approve_logic(self, state: AgentState) -> Literal["simulator", "retry_logic"]:
    """
    Decides if code passes critic's logic review
    
    Logic:
        - If critic_approved: "simulator"
        - Else: "retry_logic"
    """

def _should_retry_simulation(self, state: AgentState) -> Literal["trace_analyzer", "retry_code", "end"]:
    """
    Decides action after simulation
    
    Logic:
        - If simulation_status == 'completed': "trace_analyzer"
        - If failed and iterations < max: "retry_code"
        - If max iterations reached: "end"
    """

def _should_optimize(self, state: AgentState) -> Literal["visualizer", "optimizer"]:
    """
    Decides if optimization is needed based on KPIs
    
    Optimization criteria:
        - PDR < 85%
        - Delay > 100ms
        - Success rate < 80%
        - Optimization count < 2 (prevent infinite loop)
        
    Logic:
        - If needs optimization and count < 2: "optimizer"
        - Else: "visualizer"
    """
```

---

## 🤖 Agents API

### 1. Researcher Agent

**Module**: `agents/researcher.py`

Searches academic literature using Semantic Scholar and arXiv APIs, stores results in ChromaDB for RAG.


#### Main Functions

**research_node(state: AgentState) -> Dict**

Main node function for literature research.

**search_semantic_scholar(query: str, max_results: int = 10) -> List[Dict]**

Search papers using Semantic Scholar API with filters (year >= 2018, min citations: 5).

**synthesize_research(task: str, papers: List[Dict]) -> str**

Synthesize research findings using LLM (MODEL_REASONING).

---

### 2. Coder Agent

**Module**: `agents/coder.py`

Generates NS-3 Python code using Chain-of-Thought reasoning and auto-correction with episodic memory.

**coder_node(state: AgentState) -> Dict**

Main node function for code generation with memory-based error correction.

**generate_code(task, research_notes, previous_error, error_type, iteration) -> str**

Generate NS-3 code using Chain-of-Thought. Retrieves similar solutions from episodic memory if error exists.

---

### 3. Simulator Agent

**Module**: `agents/simulator.py`

Executes NS-3 scripts and captures results (XML + PCAP files).

**simulator_node(state: AgentState) -> Dict**

Main node function for simulation execution with pre-validation and timeout handling.

---

### 4. Trace Analyzer Agent

**Module**: `agents/trace_analyzer.py`

Analyzes PCAP files using tshark to extract detailed traffic information.

**trace_analyzer_node(state: AgentState) -> Dict**

Main node function for PCAP analysis. Requires tshark/Wireshark installed.

**analyze_pcap_routing_packets(pcap_file: str, protocol: str) -> Dict**

Analyze routing protocol packets (AODV/OLSR/DSDV) to calculate overhead.

---

### 5. Analyst Agent

**Module**: `agents/analyst.py`

Analyzes simulation results and calculates comprehensive KPIs.

**analyst_node(state: AgentState) -> Dict**

Main node function for analysis with statistical tests and confidence intervals.

**calculate_kpis(df: pd.DataFrame) -> Dict**

Calculate KPIs: PDR, Delay, Throughput, Jitter, Network Efficiency, Performance Grade.

**calculate_routing_overhead(df, trace_analysis) -> float**

Calculate routing overhead from PCAP analysis or estimate from FlowMonitor.

---

### 6. Visualizer Agent

**Module**: `agents/visualizer.py`

Generates academic-quality plots (300 DPI, publication-ready).

**visualizer_node(state: AgentState) -> Dict**

Main node function for visualization.

**create_plots(df: pd.DataFrame, kpis: Dict) -> List[str]**

Generate 4 comprehensive plots: Dashboard, Scatter, Box plots, Top/Bottom flows.

---

### 7. Optimizer Agent

**Module**: `agents/optimizer.py`

Proposes Deep Learning optimizations based on performance bottlenecks.

**optimizer_node(state: AgentState) -> Dict**

Main node function for optimization with DL architecture proposal.

**analyze_performance_bottlenecks(kpis: Dict) -> Dict**

Identify critical, moderate, and minor performance issues.

**propose_dl_architecture(bottlenecks, task) -> str**

Generate comprehensive DL architecture proposal (DQN/A3C/GNN/Transformer).

---

### 8. Critic Agent

**Module**: `agents/critic.py`

Reviews code logic before simulation (Reflection Pattern).

**critic_node(state: AgentState) -> Dict**

Evaluates code alignment with task and logic correctness using LLM.

---

### 9. GitHub Manager Agent

**Module**: `agents/github_manager.py`

Manages Git operations and GitHub integration.

**GitHubManager Class:**
- init_repo(), create_branch(), commit(), push(), merge_branch(), create_tag()

**github_manager_node(state: AgentState) -> Dict**

Creates experiment branches, commits results, and pushes to GitHub.

---

### 10. NS3-AI Integration Agent

**Module**: `agents/ns3_ai_integration.py`

Implements Deep Reinforcement Learning integration with NS-3.

**NS3AIAgent Class:**
- ActorCritic network (10 state features, 5 actions)
- run_interaction_loop() for NS-3 communication via shared memory

**Helper Functions:**
- generate_ns3_ai_code(), generate_drl_training_code(), should_use_drl()

---

### 11. Scientific Writer Agent

**Module**: `agents/scientific_writer.py`

Generates scientific papers from experimental results.

---

## 🛠️ Utilities API

### State Management (`utils/state.py`)

```python
def create_initial_state(task: str, max_iterations: int = 5) -> AgentState
def add_audit_entry(state, agent, action, details) -> Dict
def increment_iteration(state) -> Dict
def increment_optimization_count(state) -> Dict
```

### Logging (`utils/logging_utils.py`)

```python
def log_message(agent: str, message: str, level: str = "INFO")
def update_agent_status(agent: str, status: str, details: str = "")
def set_system_status(status: str, **kwargs)
```

### Memory (`utils/memory.py`)

```python
class EpisodicMemory:
    def add_experience(task, code, error, solution)
    def retrieve_experience(task, error, top_k=3) -> List[Dict]
```

### Statistical Tests (`utils/statistical_tests.py`)

```python
def t_test_two_samples(sample1, sample2, alpha=0.05) -> Dict
def calculate_confidence_interval(data, confidence=0.95) -> Tuple
def generate_statistical_report(results: Dict) -> str
```

---

## ⚙️ Configuration API

**Module**: `config/settings.py`

- Paths: PROJECT_ROOT, DATA_DIR, SIMULATIONS_DIR, LOGS_DIR, NS3_ROOT
- Ollama: MODEL_REASONING, MODEL_CODING, MODEL_EMBEDDING
- Simulation: SIMULATION_TIMEOUT, MAX_RETRIES
- Plotting: PLOT_DPI (300), PLOT_FIGSIZE (12, 8)

---

## 📊 State Management

### State Flow

```
Researcher → Coder → Critic → Simulator → Trace Analyzer → Analyst
    → [Optimize?] → Optimizer (loop to Coder) OR Visualizer → GitHub Manager → END
```

### State Persistence

- LangGraph SqliteSaver for checkpointing
- Database: `logs/langgraph_checkpoints.db`
- Thread-based: unique thread_id per experiment

---

## ⚠️ Error Handling

### Error Types

- CompilationError, SimulationError, TimeoutError, ValidationError, A2AError

### Error Recovery

1. Automatic retry (up to max_iterations)
2. Memory-based correction (episodic memory)
3. Fallback code generation
4. Graceful degradation

---

## 📝 Usage Examples

### Basic Experiment

```python
from supervisor import SupervisorOrchestrator

supervisor = SupervisorOrchestrator()
result = supervisor.run_experiment(
    task="Compare AODV and OLSR with 20 nodes",
    max_iterations=3
)
print(f"PDR: {result['metrics']['avg_pdr']:.2f}%")
```

### Memory Usage

```python
from utils.memory import memory

memory.add_experience(
    task="AODV simulation",
    code="...",
    error="ImportError: ns.aodv",
    solution="import ns.aodv"
)

experiences = memory.retrieve_experience(
    task="OLSR simulation",
    error="ImportError",
    top_k=3
)
```

---

## 🔗 Related Documentation

- [Architecture Guide](ARCHITECTURE.md)
- [Developer Guide](DEVELOPER_GUIDE.md)
- [Quick Start](QUICK-START.md)
- [Complete Thesis Guide](../TESIS-DOCTORAL-GUIA-COMPLETA.md)

---

**End of API Reference**

*For detailed function signatures and implementation details, see the source code in respective modules.*
