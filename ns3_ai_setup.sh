#!/bin/bash

# ns3_ai_setup.sh
# Script to set up the A2A Framework environment and install ns3-ai

set -e  # Exit on error

# Configuration
FRAMEWORK_DIR=$(pwd)
NS3_DIR="$HOME/ns3"
VENV_DIR=".venv"

echo "=================================================="
echo "🚀 A2A Framework & NS-3 AI Setup"
echo "=================================================="

# 1. Check NS-3 Installation
if [ ! -d "$NS3_DIR" ]; then
    echo "❌ NS-3 not found at $NS3_DIR"
    echo "   Please install NS-3 first or update NS3_DIR in this script."
    exit 1
fi
echo "✅ NS-3 found at $NS3_DIR"

# 2. Python Virtual Environment Setup
echo "--------------------------------------------------"
echo "🐍 Setting up Python Virtual Environment..."

if [ ! -d "$VENV_DIR" ]; then
    echo "   Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
else
    echo "   Virtual environment already exists."
fi

# Activate venv
source "$VENV_DIR/bin/activate"
echo "   Virtual environment activated."

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "   Installing Python dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found!"
fi

# Install cppyy separately if needed (often tricky)
if ! python3 -c "import cppyy" &> /dev/null; then
    echo "   Installing cppyy..."
    pip install cppyy
fi

echo "✅ Python environment ready."

# 3. Install ns3-ai
echo "--------------------------------------------------"
echo "🤖 Setting up ns3-ai..."

NS3_AI_DIR="$NS3_DIR/contrib/ns3-ai"

if [ ! -d "$NS3_AI_DIR" ]; then
    echo "   Cloning ns3-ai repository..."
    git clone https://github.com/hust-diangroup/ns3-ai.git "$NS3_AI_DIR"
else
    echo "   ns3-ai repository already exists in contrib."
    # Optional: git pull to update
fi

# 4. Build NS-3 with ns3-ai and Python bindings
echo "--------------------------------------------------"
echo "🏗️  Building NS-3 with Python bindings..."

cd "$NS3_DIR"

# Configure NS-3
# Ensure python is enabled. Using the venv python.
./ns3 configure --enable-python-bindings --enable-examples --enable-tests

# Build
./ns3 build

echo "✅ NS-3 Build completed."

# 5. Install ns3-ai python package
echo "--------------------------------------------------"
echo "📦 Installing ns3-ai Python package..."

if [ -d "$NS3_AI_DIR/python" ]; then
    cd "$NS3_AI_DIR/python"
    pip install .
    echo "✅ ns3-ai Python package installed."
else
    echo "⚠️  Could not find ns3-ai/python directory. Check clone."
fi

# 6. Final verification
echo "--------------------------------------------------"
echo "🔍 Verifying Installation..."
cd "$FRAMEWORK_DIR"

# Create a small verification script
cat <<EOF > verify_install.py
import sys
import ns.core
import ns.ai
print(f"✅ NS-3 Version: {ns.core.Version()}")
print("✅ ns3-ai imported successfully")
EOF

# Run test
export PYTHONPATH=$NS3_DIR/build/bindings/python:$NS3_DIR/build/lib
python3 verify_install.py

echo "=================================================="
echo "🎉 Setup Complete!"
echo "   To start working, run: source .venv/bin/activate"
echo "   Ensure PYTHONPATH is set correctly."
echo "=================================================="
