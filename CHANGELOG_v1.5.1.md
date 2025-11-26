# Changelog

All notable changes to the A2A Framework will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### Technical Details

**Files Modified**:
- `agents/coder.py` - Lines 177, 204, 230, 376-379
- `agents/researcher.py` - Lines 443-449
- `README.md` - Line 415

**Files Created**:
- `experiments/configs/hwmp_comparison.yaml`
- `experiments/configs/hwmp_mesh_scalability.yaml`
- `docs/HWMP_GUIDE.md`
- `tests/test_hwmp_support.py`

**Total Changes**: 3 files modified, 4 files created

### Use Cases

#### Smart City Applications
- **Intelligent Lighting**: 50-100 streetlight mesh network
- **Environmental Monitoring**: 30-50 air quality sensor network
- **Video Surveillance**: 20-30 distributed camera network
- **Public WiFi**: Urban mesh access points

#### Research Applications
- Protocol comparison (HWMP vs AODV vs OLSR)
- Scalability analysis (10-75+ nodes)
- Deep Learning optimization of mesh routing
- Urban IoT network design

### Expected Performance

| Metric | HWMP | AODV | OLSR |
|--------|------|------|------|
| PDR | 90-98% | 85-95% | 88-95% |
| Delay | 30-60 ms | 40-80 ms | 50-100 ms |
| Overhead | 15-25% | 10-20% | 30-40% |
| Scalability | 100+ nodes | 50 nodes | 30 nodes |

### Usage Examples

```bash
# Basic HWMP simulation
python main.py --task "Simular red mesh con HWMP, 20 nodos, 200 segundos"

# Comparison experiment
python experiments/experiment_runner.py --config experiments/configs/hwmp_comparison.yaml

# Scalability analysis
python experiments/experiment_runner.py --config experiments/configs/hwmp_mesh_scalability.yaml
```

### Breaking Changes

None. This release is fully backward compatible.

### Migration Guide

No migration needed. HWMP support is additive and does not affect existing functionality.

---
