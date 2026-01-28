# Testing the A2A Framework

This directory contains tests to verify the functionality of the A2A Framework and its integration with NS-3.

## Prerequisites

Before running tests, ensure you have set up the environment using `ns3_ai_setup.sh`:

```bash
./ns3_ai_setup.sh
source .venv/bin/activate
```

## Smoke Test

The smoke test verifies that:
1. NS-3 Python bindings are importable.
2. A minimal simulation can be configured and run.
3. Logical components (Nodes, WiFi, Internet Stack) work as expected.

### Running the Smoke Test

```bash
python3 tests/smoke_test.py
```

If successful, you should see:
```
NS-3 Version: 3.45 (or similar)
Running minimal simulation...
Minimal simulation completed successfully.
```

If it fails with `ImportError: No module named 'ns'`, ensure your `PYTHONPATH` includes the NS-3 bindings (handled by `ns3_ai_setup.sh` activation).

## End-to-End Tests

(To be implemented: running full agent workflows using `tests/test_end_to_end.py`)
