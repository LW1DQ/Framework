# Contributing to A2A Framework

Thank you for your interest in contributing to the A2A Framework! This document establishes the guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Bugs
If you find a bug, please open an Issue on GitHub including:
- Steps to reproduce the error.
- Expected vs actual behavior.
- Relevant logs or screenshots.
- Environment (OS, Python version, NS-3 version).

### Suggesting Improvements
Open an Issue with the `enhancement` label describing your idea and why it would be useful.

### Pull Requests
1.  **Fork** the repository.
2.  Create a branch for your feature: `git checkout -b feature/my-new-feature`.
3.  Implement your changes following the code standards.
4.  Ensure tests pass: `pytest tests/`.
5.  Commit your changes: `git commit -m 'feat: brief description'`.
6.  Push to your branch: `git push origin feature/my-new-feature`.
7.  Open a Pull Request describing your changes.

---

## 💻 Development Standards

### Code Style
- We follow **PEP 8** for Python.
- We use **Type Hints** in all new functions.
- We document classes and functions with **Docstrings** (Google format).

```python
def my_function(param: int) -> str:
    """
    Brief description.

    Args:
        param: Description of the parameter.

    Returns:
        Description of the return value.
    """
    pass
```

### Project Structure
- `agents/`: Agent logic (LangGraph nodes).
- `config/`: Global configurations.
- `utils/`: Shared utilities (logging, errors, state).
- `simulations/`: Working directory for scripts and results.
- `tests/`: Unit and integration tests.

### Tests
All new code must include unit tests.
- We use `pytest`.
- Mocks for external dependencies (NS-3, Ollama).
- Run tests before PR: `pytest tests/`.

---

## 🏗️ Architecture

The system uses a **Cognitive Agents** architecture orchestrated by **LangGraph**.
- **Shared State (`AgentState`)**: Dictionary passed between nodes.
- **Nodes**: Pure functions that receive state and return updates.
- **Memory**: SQLite for checkpoint persistence.

---

## 📜 License
By contributing, you agree that your code will be licensed under the MIT license of the project.
