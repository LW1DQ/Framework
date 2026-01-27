# Changelog

All notable changes to the A2A Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.6.0] - 2026-01-27

### Added
- **Dependency Injection System**: Complete DI container for flexible configuration (`utils/dependency_injection.py`)
- **Retry Patterns**: Comprehensive retry mechanism with exponential backoff (`utils/retry_patterns.py`)
- **Agent Refactoring**: 
  - Refactored analyst agent with modular architecture (`agents/analyst_refactored.py`)
  - Refactored optimizer agent with enhanced capabilities (`agents/optimizer_refactored.py`)
- **Analysis Subsystem**: 
  - Metrics analyzer for performance tracking (`agents/analysis/metrics_analyzer.py`)
  - Report generator with multiple output formats (`agents/analysis/report_generator.py`)
- **Optimization Subsystem**:
  - Code generator with template support (`agents/optimization/code_generator.py`)
  - Optimization proposer with ML-based suggestions (`agents/optimization/optimization_proposer.py`)
  - Performance analyzer for bottleneck detection (`agents/optimization/performance_analyzer.py`)
- **Integration Testing**: Comprehensive integration test suite (`tests/test_integration.py`)
- **Validation Script**: Automated validation for all improvements (`scripts/validate_improvements.py`)
- **Agent Documentation**: Complete AGENTS.md guide for agentic coding

### Enhanced
- **Configuration Management**: Updated settings with DI support and environment-specific configs
- **Error Handling**: Improved error patterns across all agents
- **Code Architecture**: Modular design with clear separation of concerns
- **Testing**: Better test coverage with mocking and fixtures

### Fixed
- **State Management**: Immutable state updates with proper audit trails
- **Resource Management**: Better handling of NS-3 resources and cleanup
- **Memory Usage**: Optimized memory patterns for long-running simulations

### Technical Details
- **Lines of Code**: +4,244 additions across 15 files
- **Architecture**: Moved from monolithic agents to modular subsystems
- **Testing**: Added comprehensive integration test coverage
- **Documentation**: Complete developer onboarding guide

---

## [1.5.4] - 2025-12-09

### Fixed
- **Critical Recursion Bug** - Fixed infinite loop between Coder and Critic agents by improving Coder's prompt with valid NS-3 examples.
- **NS-3 Bindings Path** - Fixed `ModuleNotFoundError` by explicitly injecting `PYTHONPATH` in generated scripts.
- **Graph Connectivity** - Fixed `supervisor.py` workflow where `Scientific Writer` was unreachable.
- **Data Flow** - Fixed `Analyst` agent to correctly pass `experiment_results` to `Scientific Writer`.
- **Logging** - Fixed `TypeError` in `Scientific Writer` logging calls.
- **Researcher Agent** - Improved search query generation using LLM to avoid poor results.

### Added
- **Dependency** - Added `cppyy>=3.0.0` to `requirements.txt` for robust NS-3 Python bindings support.
- **Documentation** - Added "Troubleshooting" section to `README.md` covering `PYTHONPATH` and `cppyy` issues.

---

## [1.5.3] - 2025-11-28

### Fixed
- **Coder Agent Hang** - Resolved hang during code generation by switching default model to `llama3.1:8b`.
- **Validation** - Implemented robust code validation using AST and compilation checks in `utils/validation.py`.
- **Error Handling** - Implemented structured exception hierarchy in `utils/errors.py` and updated agents to use it.

### Improved
- **Coder Agent** - Added detailed logging and fallback mechanisms.
- **Simulator Agent** - Enhanced error reporting with specific exception types (`SimulationError`, `TimeoutError`, `CompilationError`).

---

## [1.5.2] - 2025-11-26

### Documentation
- **Standardization** - Updated all documentation to be professional and consistent (English).
- **Installation** - Prioritized `install.sh` automated installation in `README.md`, `INSTALL.md`, and `MANUAL_USUARIO.md`.
- **New Guides**
  - `docs/SCIENTIFIC_GUIDE.md` - Comprehensive guide on reproducibility, PCAP analysis, and statistical reporting.
- **Cleanup** - Removed outdated files (`INSTALACION-COMPLETA.md`, `GUIA-USO-NUEVAS-FUNCIONALIDADES.md`, `COMMIT_GUIDE.md`).

---

## [1.5.1] - 2025-11-25

### 🎉 Feature Release - HWMP (IEEE 802.11s) Mesh Protocol Support

This release adds complete support for HWMP (Hybrid Wireless Mesh Protocol), the default routing protocol for IEEE 802.11s mesh networks, enabling simulation and optimization of WiFi mesh networks for smart cities.

### Added

#### Protocol Support
- **HWMP Protocol** - IEEE 802.11s mesh networking support
  - Automatic code generation with `MeshHelper`
  - IEEE 802.11s WiFi standard configuration
  - Hybrid routing (reactive + proactive)
  - Ideal for urban mesh networks and smart city infrastructure

#### Experiment Configurations
- **`hwmp_comparison.yaml`** - Compare HWMP vs AODV vs OLSR
  - 3 protocols × 10 repetitions = 30 simulations
  - Static topology (typical for mesh infrastructure)
  - Statistical comparison (T-test, ANOVA)
  
- **`hwmp_mesh_scalability.yaml`** - HWMP scalability analysis
  - 5 network sizes: 10, 20, 30, 50, 75 nodes
  - 10 repetitions per size = 50 simulations
  - Regression analysis and correlation tests

#### Documentation
- **`docs/HWMP_GUIDE.md`** - Complete HWMP usage guide (300+ lines)
  - Introduction to HWMP and IEEE 802.11s
  - Comparison with MANET protocols
  - Usage instructions in the framework
  - Smart city applications
  - Expected metrics and performance
  - Troubleshooting guide
  - Best practices

#### Testing
- **`tests/test_hwmp_support.py`** - Automated validation tests
  - Code generation verification
  - YAML configuration validation
  - Import detection testing

### Improved

#### Agents
- **Coder Agent** - Enhanced protocol detection
  - Detects HWMP in user requests
  - Generates mesh-specific code with `MeshHelper`
  - Automatically adds `import ns.mesh`
  - Configures IEEE 802.11s WiFi standard
  
- **Researcher Agent** - Updated knowledge base
  - Includes HWMP in protocol recommendations
  - Distinguishes between MANET and Mesh protocols
  - Provides mesh-specific configuration guidance

#### Documentation
- **README.md** - Updated supported protocols list
  - Now includes: AODV, OLSR, DSDV, DSR, HWMP (IEEE 802.11s mesh), and custom

---

## [1.5.0] - 2025-11-25

### 🎉 Major Release - Complete Research Automation System

This release represents a complete overhaul of the A2A framework with production-ready features for academic research.

### Added

#### New Agents
- **Scientific Writer Agent v2.0** - Automatic generation of academic documents
  - 6 document types: Briefings, Reports, Thesis Sections, Papers, Slides, Comparative Analysis
  - IEEE-format references (14+ standard references included)
  - Formal academic style (third person, passive voice)
  - Statistical validation in all documents
  - Publication-quality output

#### Documentation
- **README.md** - Complete project presentation with badges and statistics
- **INSTALL.md** - Detailed installation guide for Ubuntu/Linux
- **MANUAL_USUARIO.md** - User manual for researchers without programming experience
- **docs/DEVELOPER_GUIDE.md** - Complete guide for developers and contributors
- **docs/ARCHITECTURE.md** - Detailed system architecture documentation
- **docs/QUICK-START.md** - 10-minute quick start guide
- **docs/FAQ.md** - Comprehensive FAQ with 50+ questions
- **GITHUB-RELEASE-GUIDE.md** - Guide for publishing releases
- **TESIS-DOCTORAL-GUIA-COMPLETA.md** - Complete PhD thesis guide

#### Features
- **Episodic Memory System** - Learns from past experiments and errors
- **Real-time Dashboard** - Streamlit-based monitoring interface
- **Experimentation Framework** - Automated experiment execution with statistical analysis
- **Statistical Analysis** - Confidence intervals, significance tests, effect sizes
- **Publication-Quality Graphics** - 300 DPI PNG/PDF output
- **LaTeX Table Generation** - Ready for thesis and papers
- **Reproducibility Framework** - Controlled seeds, versioned configs, raw data storage

#### Experiments
- **Protocol Comparison** - Compare AODV, OLSR, DSDV (30 simulations)
- **Scalability Analysis** - Test with 10-100 nodes (70 simulations)
- **Mobility Impact** - Evaluate different node speeds (50 simulations)

#### Testing
- **11 Unit Tests** - Complete test coverage for all agents
- **Integration Tests** - End-to-end workflow validation
- **System Verification Script** - `verify-system-complete.py`

### Improved

#### Agents
- **Researcher Agent** - Better literature search with ChromaDB integration
- **Coder Agent** - Improved NS-3 code generation
- **Simulator Agent** - Enhanced process management and monitoring
- **Trace Analyzer Agent** - Real PCAP detection and analysis
- **Analyst Agent** - Statistical rigor with confidence intervals
- **Visualizer Agent** - Publication-quality graphics (300 DPI)
- **Optimizer Agent** - Actor-Critic implementation for DRL
- **Critic Agent** - Enhanced code validation

#### System
- **Error Handling** - Custom exceptions for each agent
- **Logging System** - Centralized logging with rotation
- **State Management** - Robust shared state with type hints
- **Memory Management** - Episodic memory with similarity search
- **Performance** - Optimized for large-scale experiments

#### Documentation
- **Code Documentation** - Complete docstrings (Google style)
- **Type Hints** - Full type annotation coverage
- **Examples** - Working examples for all features
- **Guides** - Multi-level documentation (users, researchers, developers)

### Changed

- **Project Structure** - Reorganized for better maintainability
- **Configuration** - Centralized in `config/settings.py`
- **Dependencies** - Updated to latest stable versions
- **Python Version** - Minimum Python 3.10+ (was 3.8+)
- **LLM Integration** - Migrated to Ollama for local execution

### Fixed

- **NS-3 Integration** - Resolved compilation issues
- **PCAP Analysis** - Fixed trace file detection
- **Statistical Tests** - Corrected confidence interval calculations
- **Memory Leaks** - Fixed in long-running experiments
- **Dashboard** - Resolved real-time update issues

### Removed

- **Temporary Files** - Removed 15 session/checkpoint files
- **Internal Communications** - Cleaned up development artifacts
- **Obsolete Code** - Removed deprecated functions
- **Test Data** - Removed large test files from repository

### Security

- **Input Validation** - Added validation for all user inputs
- **Sandboxing** - Simulation execution in controlled environment
- **Dependencies** - Updated all packages to secure versions

### Performance

- **Caching** - Added LRU cache for expensive computations
- **Batch Processing** - Optimized trace analysis
- **Lazy Loading** - Reduced memory footprint
- **Parallel Execution** - Support for concurrent simulations

### Documentation Statistics

- **Total Documentation**: 16,000+ lines
- **Guides Created**: 9 comprehensive guides
- **Code Documentation**: 100% coverage
- **Examples**: 10+ working examples
- **Languages**: English (Spanish planned for v1.6)

---

## [1.4.0] - 2025-11-20

### Added
- NS-3 AI integration module
- Deep Reinforcement Learning optimizer
- Actor-Critic implementation
- Python-C++ communication bridge

### Improved
- Simulation execution speed
- Memory usage optimization
- Error recovery mechanisms

### Fixed
- NS-3 compilation issues on Ubuntu 22.04
- ChromaDB persistence problems
- Dashboard refresh rate

---

## [1.3.0] - 2025-11-15

### Added
- Real-time dashboard with Streamlit
- Experiment monitoring interface
- Agent status visualization
- Interactive graphics with Plotly

### Improved
- Logging system with rotation
- State management
- Agent coordination

### Fixed
- Memory leaks in long experiments
- Dashboard connection issues

---

## [1.2.0] - 2025-11-10

### Added
- Episodic memory system
- Experience storage and retrieval
- Error pattern learning
- Success case storage

### Improved
- Agent error handling
- Recovery mechanisms
- Learning from past experiments

---

## [1.1.0] - 2025-11-05

### Added
- Trace Analyzer agent
- PCAP file analysis
- Network metrics extraction
- Statistical analysis framework

### Improved
- Analyst agent with confidence intervals
- Visualizer with publication-quality output
- Experiment reproducibility

---

## [1.0.0] - 2025-11-01

### Initial Release

#### Core Features
- Multi-agent system with LangGraph
- 8 specialized agents
- NS-3 integration
- Basic experimentation framework

#### Agents
- Researcher - Literature search
- Coder - NS-3 code generation
- Simulator - Simulation execution
- Analyst - KPI calculation
- Visualizer - Graphics generation
- Optimizer - Basic optimization
- GitHub Manager - Results management
- Critic - Code validation

#### Documentation
- Basic README
- Installation instructions
- Usage examples

---

## [0.9.0] - 2025-10-25 (Beta)

### Added
- Initial multi-agent architecture
- LangGraph integration
- Basic agent implementations
- Proof of concept

---

## Version Comparison

| Feature | v1.0 | v1.3 | v1.5 |
|---------|------|------|------|
| Agents | 8 | 9 | 10 |
| Documentation | Basic | Good | Excellent |
| Tests | 5 | 8 | 11 |
| Dashboard | ❌ | ✅ | ✅ |
| Episodic Memory | ❌ | ✅ | ✅ |
| Scientific Writer | ❌ | ❌ | ✅ |
| IEEE References | ❌ | ❌ | ✅ |
| Thesis Guide | ❌ | ❌ | ✅ |
| Test Coverage | 40% | 70% | 85%+ |

---

## Upgrade Guide

### From v1.4 to v1.5

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Run verification
python verify-system-complete.py

# Update configurations (if needed)
# Check config/settings.py for new options
```

**Breaking Changes**: None

**New Features**:
- Scientific Writer agent available
- New documentation in `docs/`
- Enhanced experiment framework

### From v1.3 to v1.4

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Install NS-3 AI (if using DRL)
# See ns3-integration/INSTALL-NS3-AI.md
```

**Breaking Changes**: None

**New Features**:
- DRL optimization available
- NS-3 AI integration

### From v1.0 to v1.3

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Install new dashboard dependencies
pip install streamlit plotly

# Run dashboard
streamlit run dashboard.py
```

**Breaking Changes**:
- Configuration file format changed
- State structure updated

**Migration**:
- Update config files to new format
- Re-run experiments to generate new state format

---

## Roadmap

### v1.6 (Q1 2026)
- [ ] Multi-language support (Spanish, French, German)
- [ ] Web-based GUI
- [ ] Integration with Zotero/Mendeley
- [ ] Automatic plagiarism detection
- [ ] Enhanced DRL algorithms (PPO, SAC, TD3)

### v2.0 (Q2 2026)
- [ ] Cloud deployment support
- [ ] Collaborative experiments
- [ ] Real-time collaboration
- [ ] Mobile app for monitoring
- [ ] Advanced visualization

### Future
- [ ] Support for other simulators (OMNeT++, OPNET)
- [ ] Integration with academic databases
- [ ] Automated peer review assistance
- [ ] AI-powered research suggestions

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Citation

If you use A2A in your research, please cite:

```bibtex
@software{a2a_framework_2025,
  title = {A2A: Multi-Agent System for Network Protocol Research},
  author = {Your Name},
  year = {2025},
  version = {1.5.0},
  url = {https://github.com/LW1DQ/Framework}
}
```

---

## Acknowledgments

- NS-3 Team for the excellent network simulator
- LangChain/LangGraph for the agent orchestration framework
- Ollama for local LLM execution
- Research community for feedback and contributions

---

## Support

- **Issues**: [GitHub Issues](https://github.com/LW1DQ/Framework/issues)
- **Discussions**: [GitHub Discussions](https://github.com/LW1DQ/Framework/discussions)
- **Documentation**: [Full Documentation](https://github.com/LW1DQ/Framework/tree/main/docs)

---

**Last Updated**: 2026-01-27
