# ❓ Frequently Asked Questions (FAQ)

**Common questions and answers about the A2A framework**

---

## 📋 Table of Contents

1. [General Questions](#general-questions)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Experiments](#experiments)
5. [Document Generation](#document-generation)
6. [Troubleshooting](#troubleshooting)
7. [Development](#development)
8. [Performance](#performance)

---

## 🌟 General Questions

### What is A2A?

A2A (Agent-to-Agent) is a multi-agent framework that automates the complete research cycle for network protocol evaluation. It uses 10 specialized agents to handle everything from literature search to scientific document generation.

### Who should use A2A?

- **PhD students** working on network protocols
- **Researchers** evaluating MANET/IoT protocols
- **Network engineers** testing protocol performance
- **Educators** teaching network simulation

### Do I need programming knowledge?

No! A2A is designed for researchers without programming experience. The [User Manual](../MANUAL_USUARIO.md) provides step-by-step instructions for all tasks.

### Is A2A free?

Yes! A2A is open-source under the MIT License. You can use, modify, and distribute it freely.

### What protocols does A2A support?

Currently: AODV, OLSR, DSDV, DSR. You can add custom protocols by following the [Developer Guide](DEVELOPER_GUIDE.md).

### Can I use A2A for my thesis?

Absolutely! A2A includes a complete [Thesis Guide](../TESIS-DOCTORAL-GUIA-COMPLETA.md) with:
- Experiment design
- Statistical analysis
- Document generation
- Publication preparation

---

## 💻 Installation

### What are the system requirements?

**Minimum**:
- Ubuntu 20.04+ or similar Linux
- Python 3.10+
- 8GB RAM
- 20GB disk space

**Recommended**:
- Ubuntu 22.04 LTS
- Python 3.11+
- 16GB RAM
- 50GB SSD

### Can I use A2A on Windows?

Yes, but with limitations. NS-3 works better on Linux. We recommend:
- Use WSL2 (Windows Subsystem for Linux)
- Or use a Linux virtual machine
- Or dual-boot with Ubuntu

### Can I use A2A on macOS?

Yes! Follow the same installation steps as Linux. NS-3 works well on macOS.

### How long does installation take?

- **Basic installation**: 10-15 minutes
- **With NS-3**: 45-60 minutes (includes compilation)
- **Full setup with tests**: 60-90 minutes

### Do I need a GPU?

No, GPU is optional. It's only useful for:
- Deep Reinforcement Learning training (faster)
- Large-scale experiments (parallel processing)

### What if I don't have Ollama?

Ollama is required for the LLM-based agents. Install it with:
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
```

Alternative: Use OpenAI API (requires API key and modification of config).

---

## 🚀 Usage

### How do I start using A2A?

1. Follow [Quick Start](QUICK-START.md) (10 minutes)
2. Read [User Manual](../MANUAL_USUARIO.md)
3. Run your first experiment
4. Generate documents

### What's the typical workflow?

```
1. Design experiment → Edit YAML config
2. Run experiment → python experiments/experiment_runner.py
3. Monitor progress → streamlit run dashboard.py
4. Analyze results → Automatic
5. Generate documents → python examples/generate_briefing.py
6. Review and edit → Manual refinement
```

### Can I run multiple experiments simultaneously?

Yes, but it will slow down your system. Better to run one at a time unless you have a powerful machine (16+ cores, 32+ GB RAM).

### How do I stop an experiment?

Press `Ctrl+C` in the terminal. Progress is saved and you can resume later.

### Where are results saved?

In `experiments/results/[experiment_name]_[timestamp]/`:
- `config.yaml`: Configuration used
- `raw_data/`: Raw simulation data
- `analysis/`: Statistical analysis
- `graphics/`: PNG/PDF graphics
- `tables/`: LaTeX tables
- `summary.md`: Results summary

---

## 🧪 Experiments

### How long does an experiment take?

Depends on configuration:
- **Small** (10 nodes, 2 reps): 30-60 minutes
- **Medium** (20 nodes, 10 reps): 3-4 hours
- **Large** (50 nodes, 10 reps): 8-10 hours
- **Very large** (100 nodes, 10 reps): 20-30 hours

### How many repetitions should I use?

- **Testing**: 2-3 repetitions
- **Research**: 10+ repetitions (for statistical validity)
- **Publication**: 30+ repetitions (for high confidence)

### Can I customize experiment parameters?

Yes! Edit the YAML file in `experiments/configs/`:

```yaml
simulation:
  nodes: 30  # Change number of nodes
  duration: 300  # Change simulation time
  mobility_model: "RandomWaypoint"  # Change mobility
  speed_range: "10-20"  # Change speed
```

### What metrics are calculated?

- **PDR** (Packet Delivery Ratio): % of packets delivered
- **Delay**: Average end-to-end delay
- **Throughput**: Data transmission rate
- **Overhead**: Routing control messages
- **Jitter**: Delay variation
- **Success Rate**: Successful transmissions

### How do I compare protocols?

Use the comparison experiment:
```bash
python experiments/experiment_runner.py --config experiments/configs/comparison.yaml
```

Edit `comparison.yaml` to select protocols:
```yaml
protocols: ["AODV", "OLSR", "DSDV"]
```

### Can I add my own protocol?

Yes! See [Developer Guide](DEVELOPER_GUIDE.md) section "Adding New Protocols".

---

## 📝 Document Generation

### What documents can A2A generate?

1. **Briefing** (2 pages): Quick summary
2. **Technical Report** (5-10 pages): Complete documentation
3. **Thesis Section**: Methodology, Results, Discussion
4. **Paper Draft** (IEEE format): Ready for submission
5. **Presentation Slides**: 10-15 slides
6. **Comparative Analysis**: Multi-experiment comparison

### Are documents ready to use?

Documents are **high-quality drafts** that need:
- ✅ Review and validation
- ✅ Addition of your insights
- ✅ Verification of data
- ✅ Minor formatting adjustments

They save 99% of writing time but still need human review.

### Do documents include references?

Yes! All documents include:
- IEEE-format references
- Automatic citation of protocols
- References to NS-3, metrics, and methodology
- 14+ standard references included

### Can I customize document style?

Yes! Edit templates in `agents/scientific_writer_enhanced.py`:
- Change formality level
- Modify prompts
- Add custom references
- Adjust structure

### How do I convert Markdown to LaTeX?

```bash
pandoc input.md -o output.tex --template=thesis_template.tex
```

Or use online converters like Overleaf.

### Can I generate documents in Spanish?

Currently English only. Spanish support planned for v1.6.

---

## 🐛 Troubleshooting

### Experiment fails with "NS-3 not found"

**Solution**: Install NS-3 following [ns3-integration/INSTALL-NS3-AI.md](../ns3-integration/INSTALL-NS3-AI.md)

### "Out of memory" error

**Solutions**:
- Reduce number of nodes
- Reduce simulation duration
- Close other applications
- Add swap space

### Tests fail

**Solutions**:
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Clear cache
rm -rf __pycache__ .pytest_cache

# Run tests again
pytest tests/ -v
```

### Dashboard doesn't start

**Solutions**:
```bash
# Ensure venv is activated
source venv/bin/activate

# Install streamlit
pip install streamlit

# Run dashboard
streamlit run dashboard.py
```

### Ollama model not found

**Solutions**:
```bash
# Check Ollama is running
ollama list

# Pull model
ollama pull llama3.1:8b

# Restart Ollama
systemctl restart ollama
```

### Simulation hangs

**Solutions**:
- Check logs: `cat logs/system.log`
- Kill process: `pkill -f ns3`
- Reduce simulation complexity
- Check NS-3 installation

### More issues?

See [Troubleshooting Guide](TROUBLESHOOTING.md) for detailed solutions.

---

## 👨‍💻 Development

### How do I contribute?

1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

See [Contributing Guide](../CONTRIBUTING.md) for details.

### How do I add a new agent?

Follow the template in [Developer Guide](DEVELOPER_GUIDE.md) section "Creating New Agents".

### Can I use a different LLM?

Yes! Modify `config/settings.py`:

```python
# Use OpenAI
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4", api_key="your-key")

# Use Anthropic
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3", api_key="your-key")
```

### How do I add new metrics?

Extend `agents/analyst.py`:

```python
def calculate_new_metric(trace_data):
    # Your calculation
    return {"mean": value, "std": std, "ci": [lower, upper]}
```

### Where is the documentation for developers?

- [Developer Guide](DEVELOPER_GUIDE.md)
- [Architecture](ARCHITECTURE.md)
- [API Reference](API.md)
- Code comments and docstrings

---

## ⚡ Performance

### How can I speed up experiments?

1. **Reduce repetitions** (for testing)
2. **Use fewer nodes** (start small)
3. **Shorter duration** (100s instead of 200s)
4. **Parallel execution** (if you have resources)
5. **Use SSD** (faster I/O)

### How much disk space do I need?

- **Installation**: 5GB
- **Per experiment**: 100MB - 1GB
- **Recommended**: 50GB free space

### Can I run A2A on a cluster?

Yes! A2A can be deployed on:
- University clusters
- Cloud instances (AWS, GCP, Azure)
- HPC systems

Contact us for deployment assistance.

### What's the bottleneck?

Usually:
1. **NS-3 simulation** (CPU-intensive)
2. **LLM inference** (if using large models)
3. **Trace analysis** (I/O-intensive)

### Can I use multiple GPUs?

Yes, for DRL training. Configure PyTorch to use multiple GPUs:

```python
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

---

## 📊 Research & Publications

### Can I publish results from A2A?

Yes! A2A is designed for academic research. Please cite:

```bibtex
@software{a2a_framework_2025,
  title = {A2A: Multi-Agent System for Network Protocol Research},
  author = {LW1DQ},
  year = {2025},
  url = {https://github.com/LW1DQ/Framework}
}
```

### Are results reproducible?

Yes! A2A ensures reproducibility through:
- Controlled random seeds
- Versioned configurations
- Raw data storage
- Documented methodology

### What statistical tests are used?

- **t-tests**: Compare two protocols
- **ANOVA**: Compare multiple protocols
- **Regression**: Scalability analysis
- **Confidence intervals**: 95% by default

### How do I validate results?

1. Compare with literature values
2. Check confidence intervals are reasonable
3. Verify statistical significance (p < 0.05)
4. Run multiple repetitions
5. Cross-validate with different seeds

### Can I use A2A for my paper?

Yes! A2A generates:
- Publication-quality graphics (300 DPI)
- LaTeX tables
- IEEE-format papers
- Statistical validation

---

## 🆘 Getting More Help

### Where can I find more information?

- **Documentation**: `docs/` folder
- **Examples**: `examples/` folder
- **User Manual**: [MANUAL_USUARIO.md](../MANUAL_USUARIO.md)
- **Developer Guide**: [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)

### How do I report a bug?

1. Check if it's a known issue: [GitHub Issues](https://github.com/LW1DQ/Framework/issues)
2. If not, create a new issue with:
   - Description of problem
   - Steps to reproduce
   - Error messages
   - System information

### How do I request a feature?

Open a feature request on [GitHub Discussions](https://github.com/LW1DQ/Framework/discussions) with:
- Description of feature
- Use case
- Why it's useful

### Is there a community?

Yes!
- **GitHub Discussions**: Ask questions, share experiences
- **Issues**: Report bugs, request features
- **Email**: contact@lw1dq.com

### Can I get commercial support?

Contact us at contact@lw1dq.com for:
- Custom development
- Training workshops
- Deployment assistance
- Consulting services

---

## 📚 Additional Resources

### Tutorials

- [Quick Start](QUICK-START.md) - 10 minutes
- [User Manual](../MANUAL_USUARIO.md) - Complete guide
- [Developer Guide](DEVELOPER_GUIDE.md) - For contributors

### Documentation

- [Architecture](ARCHITECTURE.md) - System design
- [API Reference](API.md) - Complete API
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues

### External Resources

- [NS-3 Documentation](https://www.nsnam.org/documentation/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [PyTorch Documentation](https://pytorch.org/docs/)

---

**Still have questions?** Ask in [GitHub Discussions](https://github.com/LW1DQ/Framework/discussions)!

[← Back to README](../README.md) | [Quick Start →](QUICK-START.md) | [User Manual →](../MANUAL_USUARIO.md)
