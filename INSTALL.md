# A2A Framework Installation Guide

This document provides detailed instructions for installing and configuring the A2A Multi-Agent Framework on Ubuntu systems.

## Prerequisites

- **Operating System**: Ubuntu 22.04 LTS or 24.04 LTS (Recommended)
- **RAM**: Minimum 8GB (16GB recommended for compilation)
- **Storage**: At least 10GB of free space

---

## 🚀 Option 1: Automated Installation (Recommended)

We provide a comprehensive setup script that handles:
1.  System dependency installation (compilers, headers).
2.  NS-3 download and compilation.
3.  `ns3-ai` integration setup.
4.  Python virtual environment creation with all dependencies.

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/LW1DQ/Framework.git
    cd Framework
    ```

2.  **Run the Setup Script**
    ```bash
    chmod +x ns3_ai_setup.sh
    ./ns3_ai_setup.sh
    ```
    *Note: This process may take 15-30 minutes depending on your hardware, as it compiles NS-3 from source.*

3.  **Activate the Environment**
    ```bash
    source .venv/bin/activate
    ```

4.  **Verify Installation**
    Run the smoke test to ensure NS-3 bindings are correctly loaded:
    ```bash
    python3 tests/smoke_test.py
    ```
    You should see: `Minimal simulation completed successfully.`

---

## 🛠️ Option 2: Manual Installation (Advanced)

If you prefer to manage your own NS-3 installation or are integrating into an existing environment.

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install build-essential python3-dev git cmake ninja-build
```

### 2. Install and Compile NS-3 (with Python bindings)
Downlad NS-3 (version 3.45 recommended):
```bash
wget https://www.nsnam.org/releases/ns-allinone-3.45.tar.bz2
tar xjf ns-allinone-3.45.tar.bz2
cd ns-allinone-3.45/ns-3.45
```

Configure and build:
```bash
./ns3 configure --enable-python-bindings --enable-examples --enable-tests
./ns3 build
```

### 3. Install ns3-ai (Optional, for DRL)
Follow the [Official ns3-ai Documentation](https://github.com/hust-diangroup/ns3-ai) to clone and build the module in the `contrib/` directory of your NS-3 installation.

### 4. Configure Python Environment
Navigate back to the Framework directory:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 5. Set Environment Variables
You must tell Python where to find the NS-3 bindings. Add this to your `.bashrc` or run it in your terminal:

```bash
export PYTHONPATH=$PYTHONPATH:/path/to/ns-3.45/build/bindings/python:/path/to/ns-3.45/build/lib
```
*(Replace `/path/to/ns-3.45` with your actual installation path)*

---

## ❓ Troubleshooting

### "ModuleNotFoundError: No module named 'ns'"
- **Cause**: Python cannot find the NS-3 bindings.
- **Fix**: accurate `PYTHONPATH`. Check it with `echo $PYTHONPATH`. Ensure it points to the `build/bindings/python` directory of your compiled NS-3.

### "cppyy" compilation errors
- **Cause**: Missing system headers.
- **Fix**: Ensure `python3-dev` and `g++` are installed (`sudo apt install python3-dev g++`).

### "Externally Managed Environment" error
- **Cause**: Trying to install pip packages globally on Ubuntu 24.04+.
- **Fix**: Always use the virtual environment (`source .venv/bin/activate`).
