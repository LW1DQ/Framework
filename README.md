# 🤖 A2A: An Autonomous Framework for Reproducible Network Research

![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-1.6.0-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![NS-3](https://img.shields.io/badge/NS--3-3.45-green)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)

**A2A (Agent-to-Agent)** is a novel multi-agent system designed to function as an "Artificial Scientist" for network protocol research. By integrating Large Language Models (LLMs) with the NS-3 discrete-event simulator, A2A automates the entire scientific workflow—from hypothesis formulation and code generation to simulation execution, statistical analysis, and paper drafting.

This framework addresses the crisis of reproducibility in network research by enforcing strict version control, seed management, and standardized evaluation methodologies.

---

## 🌟 Key Innovations

### 🧠 Cognitive Architecture
- **Centralized Reasoning**: A proprietary prompt management system orchestrates 10 specialized agents.
- **Episodic Memory**: Retrieval-Augmented Generation (RAG) enables agents to learn from past simulation errors and successes.
- **Self-Correction**: Closed-loop feedback allows the system to autonomously debug compilation errors and runtime failures.

### 🔬 Advanced Simulation Capabilities
- **NS-3 AI Integration**: Native Python-C++ shared memory interface for high-performance Deep Reinforcement Learning (DRL).
- **Automated Metadata Tracking**: Every simulation generates a cryptographic manifest (`simulation_metadata.json`) ensuring data provenance.
- **Protocol Support**: Native support for MANETs (AODV, OLSR, DSDV) and IEEE 802.11s Mesh networks (HWMP).

### 📊 Rigorous Analysis
- **Statistical Validity**: Automatic calculation of 95% confidence intervals, T-tests, and ANOVA for all metrics.
- **Publication-Ready Output**: Generates 300 DPI plots and LaTeX tables formatted for IEEE/ACM conferences.
- **Full Trace Analysis**: Deep inspection of PCAP files to extract granular metrics beyond standard logs.

---

## 🚀 Quick Start

### Prerequisites
- **OS**: Ubuntu 22.04 / 24.04 LTS (Recommended)
- **NS-3**: Version 3.45 (Automatically compiled)
- **Python**: 3.10+

### One-Step Installation
We provide a comprehensive setup script that compiles NS-3, installs `ns3-ai`, and configures the Python environment.

```bash
# 1. Clone the repository
git clone https://github.com/LW1DQ/Framework.git
cd Framework

# 2. Run the setup script
chmod +x ns3_ai_setup.sh
./ns3_ai_setup.sh

# 3. Activate the environment
source .venv/bin/activate
```

### Running Your First Experiment
To run a standard comparison between AODV and OLSR protocols:

```bash
python3 experiments/experiment_runner.py --config experiments/configs/comparison.yaml
```

---

## 🧩 Agent Architecture

The framework utilizes a graph-based orchestration engine (**LangGraph**) to coordinate 10 specialized agents:

1.  **Researcher**: Queries Semantic Scholar/arXiv to ground experiments in state-of-the-art literature.
2.  **Coder**: Generates syntactically correct NS-3 scripts (C++/Python) with error-handling wrappers.
3.  **Simulator**: Manages the NS-3 runtime, enforcing timeouts and resource limits.
4.  **Trace Analyzer**: Parses raw PCAP binaries to extract packet-level insights.
5.  **Analyst**: Performs statistical hypothesis testing on simulation data.
6.  **Optimizer**: Implements DRL algorithms (PPO) via `ns3-ai` for protocol tuning.
7.  **Visualizer**: Produces vector-graphics plots for academic papers.
8.  **Scientific Writer**: Drafts technical reports and LaTeX papers following IEEE templates.
9.  **Critic**: Validates methodological soundness and code quality.
10. **Supervisor**: Managing the global state and agent hand-offs.

---

## 📂 Directory Structure

```plaintext
Framework/
├── agents/                 # Agent implementations
│   ├── coder.py           # NS-3 script generation
│   ├── ns3_ai_integration.py # Shared memory interface
│   └── ...
├── config/                 # Configuration files
│   ├── prompts.yaml       # Centralized LLM prompts
│   └── settings.py        # Global settings
├── experiments/            # Experiment definitions (YAML)
├── simulations/            # Output directory
│   ├── results/           # JSON metrics and metadata
│   └── plots/             # Generated figures
├── tests/                  # Unit and integration tests
├── utils/                  # Helper modules
└── ns3_ai_setup.sh         # Main installation script
```

---

## 📄 Citation

If you use A2A in your research, please cite our work:

```bibtex
@software{a2a_framework_2026,
  author = {Diego Quezada},
  title = {A2A: An Autonomous Framework for Reproducible Network Research},
  year = {2026},
  version = {1.6.0},
  url = {https://github.com/LW1DQ/Framework}
}
```

---

## 🤝 Contributing

We welcome contributions from the academic community. Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on submitting pull requests.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
