# Release Notes v1.5.3

## Summary
This release focuses on stability, robustness, and ease of installation. It addresses critical issues with the Coder Agent, implements a structured error handling system, and provides a complete, automated installation experience for new users.

## Key Changes

### 🛠️ Fixes & Improvements
- **Coder Agent Stability**: Resolved hang issues by optimizing the default LLM configuration (`llama3.1:8b`).
- **Robust Validation**: Implemented AST-based syntax checking and compilation validation for generated code.
- **Structured Error Handling**: Introduced a comprehensive exception hierarchy (`A2AException`) for better error reporting and debugging.

### 📦 Installation & Documentation
- **New Automated Installer**: `install.sh` handles the entire setup process (System dependencies, Python, NS-3, Ollama) in one click.
- **Complete Installation Guide**: Added `docs/COMPLETE_INSTALLATION_GUIDE.md` for detailed, step-by-step instructions.
- **Documentation Updates**: Updated `README.md`, `INSTALL.md`, and `TROUBLESHOOTING.md` to reflect the latest changes.

### 🧹 Cleanup
- Consolidated installation scripts.
- Removed temporary debugging files.

## Upgrade Instructions
```bash
git pull origin main
./install.sh
```
