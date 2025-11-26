# Changelog

All notable changes to the A2A Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.5.1] - 2025-11-25

### Added
- **HWMP Protocol Support** - IEEE 802.11s mesh networking
  - Automatic code generation with MeshHelper
  - Hybrid routing (reactive + proactive)
  - Ideal for smart city mesh infrastructure
- **Experiment Configurations**
  - `hwmp_comparison.yaml` - Compare HWMP vs AODV vs OLSR (30 simulations)
  - `hwmp_mesh_scalability.yaml` - Scalability analysis 10-75 nodes (50 simulations)
- **Documentation**
  - `docs/HWMP_GUIDE.md` - Complete HWMP usage guide (300+ lines)
- **Testing**
  - `tests/test_hwmp_support.py` - Automated validation tests

### Improved
- **Coder Agent** - Enhanced protocol detection for HWMP
  - Detects HWMP in user requests
  - Generates mesh-specific code with MeshHelper
  - Automatically adds `import ns.mesh`
- **Researcher Agent** - Updated knowledge base with mesh protocols
  - Distinguishes between MANET and Mesh protocols
  - Provides mesh-specific configuration guidance
- **README** - Updated supported protocols list
  - Now includes: AODV, OLSR, DSDV, DSR, HWMP (IEEE 802.11s mesh), and custom

---

## [1.5.0] - 2025-11-25

### 🎉 Major Release - Complete Research Automation System

This release represents a complete overhaul of the A2A framework with production-ready features for academic research.
