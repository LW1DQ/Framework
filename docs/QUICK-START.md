# ⚡ Quick Start Guide - A2A Framework

**Get up and running in 10 minutes**

---

## 🎯 Goal

By the end of this guide, you will:
- ✅ Have A2A installed and verified
- ✅ Run your first experiment
- ✅ Generate a scientific document
- ✅ View results in the dashboard

**Time required**: 10-15 minutes

---

## 📋 Prerequisites

- Ubuntu 20.04+ or similar Linux distribution
- Python 3.10+
- 8GB RAM
- Internet connection

---

## 🚀 Step 1: Installation (5 minutes)

```bash
# Clone repository
git clone https://github.com/LW1DQ/Framework.git
cd Framework

# Run automated installer
chmod +x install.sh
./install.sh

# Activate virtual environment
source venv/bin/activate
```

---

## ✅ Step 2: Verify Installation (1 minute)```bash
python verify-system-complete.py
```

**Expected output**:
```
✅ Python 3.10.x
✅ 16/16 Paquetes instalados
✅ 10/10 Agentes funcionales
✅ 11/11 Tests pasados
✅ 100% Verificado
```

If you see **100% Verified**, you're ready to go! 🎉

---

## 🧪 Step 3: Run First Experiment (2 minutes to start)

Let's run a simple protocol comparison:

```bash
# This will compare AODV and OLSR protocols
python experiments/experiment_runner.py --config experiments/configs/comparison.yaml
```

**What happens**:
- Generates NS-3 simulation code
- Runs 30 simulations (3 protocols × 10 repetitions)
- Analyzes results
- Generates graphics

**Time**: 3-4 hours (runs in background)

**Monitor progress**:
```bash
# In another terminal
streamlit run dashboard.py
# Open http://localhost:8501
```

---

## 📊 Step 4: View Dashboard (1 minute)

While experiment runs, explore the dashboard:

```bash
streamlit run dashboard.py
```

**Dashboard sections**:
- 🏠 **Home**: System status
- 🧪 **Experiments**: Running experiments
- 📄 **Documents**: Generated documents
- 🤖 **Agents**: Agent status
- 📈 **Results**: Graphics and data

---

## 📝 Step 5: Generate Document (1 minute)

Generate a scientific briefing:

```bash
python examples/test_scientific_writer.py
```

**Output**: 4 documents in `generated_documents/`:
- Briefing (2 pages)
- Technical report (5-10 pages)
- Thesis section
- Paper draft (IEEE format)

**Check results**:
```bash
ls generated_documents/briefing/
cat generated_documents/briefing/comparison_briefing_*.md
```

---

## 🎓 What You Just Did

Congratulations! You've:

1. ✅ Installed A2A framework
2. ✅ Verified all components work
3. ✅ Started a network simulation experiment
4. ✅ Launched the monitoring dashboard
5. ✅ Generated scientific documents

---

## 📚 Next Steps

### Learn More

1. **Read User Manual**: [MANUAL_USUARIO.md](../MANUAL_USUARIO.md)
   - Detailed guide for researchers
   - No programming knowledge required

2. **Explore Examples**: `examples/`
   - Test each agent individually
   - Learn how to customize

3. **Read Documentation**: `docs/`
   - Architecture details
   - Developer guide
   - API reference

### Try More Experiments

```bash
# Scalability analysis (8-10 hours)
python experiments/experiment_runner.py --config experiments/configs/scalability.yaml

# Mobility impact (5-6 hours)
python experiments/experiment_runner.py --config experiments/configs/mobility.yaml
```

### Customize

Edit experiment configurations in `experiments/configs/`:

```yaml
# experiments/configs/my_experiment.yaml
name: "My Custom Experiment"
simulation:
  protocol: "AODV"
  nodes: 30  # Change this
  duration: 300  # Change this
```

Run your custom experiment:
```bash
python experiments/experiment_runner.py --config experiments/configs/my_experiment.yaml
```

---

## 🐛 Troubleshooting

### Issue: Python version too old

```bash
# Install Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv
```

### Issue: Ollama not found

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
systemctl start ollama

# Pull model
ollama pull llama3.1:8b
```

### Issue: Tests fail

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run tests again
pytest tests/ -v
```

### More Help

- **Troubleshooting Guide**: [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **GitHub Issues**: [Report a problem](https://github.com/LW1DQ/Framework/issues)
- **Community**: [Ask questions](https://github.com/LW1DQ/Framework/discussions)

---

## 💡 Tips

### Performance

- **Start small**: Use 10 nodes and 2 repetitions for testing
- **Monitor resources**: Use `htop` to check CPU/RAM usage
- **Run overnight**: Large experiments take hours

### Best Practices

- **Always activate venv**: `source venv/bin/activate`
- **Check logs**: `cat logs/system.log` if something fails
- **Backup results**: Copy `experiments/results/` regularly
- **Use dashboard**: Monitor experiments in real-time

### Common Commands

```bash
# Activate environment
source venv/bin/activate

# Verify system
python verify-system-complete.py

# Run tests
pytest tests/ -v

# Launch dashboard
streamlit run dashboard.py

# Run experiment
python experiments/experiment_runner.py --config CONFIG_FILE

# Generate document
python examples/test_scientific_writer.py

# View logs
cat logs/system.log
```

---

## 🎯 Quick Reference

### File Structure

```
Framework/
├── agents/              # 10 specialized agents
├── experiments/         # Experiment framework
│   ├── configs/        # Experiment configurations
│   └── results/        # Generated results
├── docs/               # Documentation
├── examples/           # Usage examples
├── tests/              # Unit tests
├── main.py            # Main entry point
├── dashboard.py       # Streamlit dashboard
└── requirements.txt   # Dependencies
```

### Key Files

- **README.md**: Project overview
- **INSTALL.md**: Detailed installation
- **MANUAL_USUARIO.md**: User manual (no coding required)
- **docs/DEVELOPER_GUIDE.md**: For developers
- **docs/ARCHITECTURE.md**: System architecture

### Important Directories

- **experiments/results/**: All experiment outputs
- **generated_documents/**: Generated documents
- **logs/**: System logs
- **data/**: Vector database and cache

---

## ✅ Checklist

Before moving on, make sure you have:

- [ ] Installed A2A successfully
- [ ] Verified 100% system check
- [ ] Started an experiment
- [ ] Opened the dashboard
- [ ] Generated a document
- [ ] Explored the file structure
- [ ] Read the user manual

---

## 🚀 You're Ready!

You now have a working A2A installation and understand the basics.

**Next**: Read the [User Manual](../MANUAL_USUARIO.md) for detailed usage instructions.

**Questions?** Check [FAQ](FAQ.md) or ask in [Discussions](https://github.com/LW1DQ/Framework/discussions).

---

**Happy researching! 🎓**

[← Back to README](../README.md) | [User Manual →](../MANUAL_USUARIO.md) | [Installation Guide →](../INSTALL.md)
