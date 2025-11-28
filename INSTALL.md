# 📦 Installation Guide - A2A Framework

Complete installation instructions for Ubuntu/Linux systems.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Installation](#quick-installation)
3. [Detailed Installation](#detailed-installation)
4. [NS-3 Installation](#ns-3-installation)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04+ / Debian 11+ / Other Linux distributions
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Storage**: 20 GB free space
- **Python**: 3.10 or higher

### Recommended Requirements
- **OS**: Ubuntu 22.04 LTS
- **CPU**: 8+ cores
- **RAM**: 16 GB

### One-Click Installation (Recommended)

The easiest way to install the A2A Framework is using the automated script:

```bash
# 1. Clone the repository
git clone https://github.com/LW1DQ/Framework.git
cd Framework

# 2. Run the installer
./install.sh
```

This script will automatically:
- Install system dependencies
- Set up Python 3.10+ and virtual environment
- Install and configure NS-3 with 5G-LENA and ns3-ai
- Install and configure Ollama
- Verify the installation

### Manual Installation
If you prefer to install manually, follow the [Detailed Installation](#detailed-installation) section below.

**Detailed NS-3 installation guide**: See [ns3-integration/INSTALL-NS3-AI.md](ns3-integration/INSTALL-NS3-AI.md)

---

## ✅ Verification

### Verify System Installation

```bash
# Activate virtual environment
source venv/bin/activate

# Run verification script
python verify-system-complete.py
```

**Expected output**:
```
======================================================================
              VERIFICACIÓN COMPLETA DEL SISTEMA A2A v1.5
======================================================================

✅ Python 3.10.x
✅ 16/16 Paquetes instalados
✅ 10/10 Agentes funcionales
✅ 11/11 Tests pasados
✅ 100% Verificado
```

### Run Unit Tests

```bash
pytest tests/ -v
```

**Expected**: All 11 tests should pass.

### Test Dashboard

```bash
streamlit run dashboard.py
```

**Expected**: Dashboard opens in browser at `http://localhost:8501`

### Test Scientific Writer

```bash
python examples/test_scientific_writer.py
```

**Expected**: 4 documents generated in `generated_documents/`

---

## 🐛 Troubleshooting

### Issue: Python version too old

**Error**: `Python 3.10+ required`

**Solution**:
```bash
# Install Python 3.10
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.10 python3.10-venv python3.10-dev

# Use Python 3.10 explicitly
python3.10 -m venv venv
source venv/bin/activate
```

### Issue: pip install fails

**Error**: `Failed building wheel for X`

**Solution**:
```bash
# Install build dependencies
sudo apt install -y python3-dev build-essential

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Try again
pip install -r requirements.txt
```

### Issue: Ollama not found

**Error**: `ollama: command not found`

**Solution**:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
systemctl start ollama

# Pull model
ollama pull llama3.1:8b
```

### Issue: ChromaDB fails to install

**Error**: `Failed to build chromadb`

**Solution**:
```bash
# Install additional dependencies
sudo apt install -y libsqlite3-dev

# Install ChromaDB separately
pip install chromadb==0.5.5
```

### Issue: NS-3 build fails

**Error**: `Build failed`

**Solution**:
```bash
# Install missing dependencies
sudo apt install -y gcc g++ python3-dev cmake

# Clean and rebuild
./ns3 clean
./ns3 configure --enable-examples
./ns3 build
```

### Issue: Tests fail

**Error**: `ImportError: No module named X`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Run tests again
pytest tests/ -v
```

### Issue: Dashboard doesn't start

**Error**: `streamlit: command not found`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Install streamlit
pip install streamlit

# Run dashboard
streamlit run dashboard.py
```

---

## 🔄 Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Verify installation
python verify-system-complete.py
```

---

## 🗑️ Uninstallation

To completely remove the A2A framework:

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf Framework

# Optional: Remove Ollama
sudo systemctl stop ollama
sudo rm /usr/local/bin/ollama
sudo rm -rf ~/.ollama

# Optional: Remove NS-3
rm -rf ~/ns3
```

---

## 📚 Next Steps

After successful installation:

1. **Read the User Manual**: [MANUAL_USUARIO.md](MANUAL_USUARIO.md)
2. **Try Quick Start**: [docs/QUICK-START.md](docs/QUICK-START.md)
3. **Run First Experiment**: [experiments/README.md](experiments/README.md)
4. **Explore Examples**: [examples/](examples/)

---

## 💡 Tips

### Performance Optimization

```bash
# Use faster package installer
pip install uv
uv pip install -r requirements.txt

# Enable parallel builds for NS-3
./ns3 configure --enable-examples -j$(nproc)
./ns3 build -j$(nproc)
```

### Development Setup

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run code quality checks
flake8 agents/ utils/
mypy agents/ utils/
black agents/ utils/
```

### Resource Management

```bash
# Monitor system resources
htop

# Check disk space
df -h

# Monitor GPU (if available)
nvidia-smi
```

---

## 🆘 Getting Help

If you encounter issues not covered here:

1. **Check Troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
2. **Search Issues**: [GitHub Issues](https://github.com/LW1DQ/Framework/issues)
3. **Ask Community**: [GitHub Discussions](https://github.com/LW1DQ/Framework/discussions)
4. **Contact Support**: contact@lw1dq.com

---

## ✅ Installation Checklist

- [ ] System dependencies installed
- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Python dependencies installed
- [ ] Ollama installed and model pulled
- [ ] Verification script passed (100%)
- [ ] Unit tests passed (11/11)
- [ ] Dashboard launches successfully
- [ ] NS-3 installed (optional)
- [ ] ns3-ai installed (optional)

---

**Installation complete! You're ready to start using A2A.** 🎉

[← Back to README](README.md) | [User Manual →](MANUAL_USUARIO.md)
