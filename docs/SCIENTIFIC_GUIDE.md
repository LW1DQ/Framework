# 🔬 Scientific Features Guide

**A2A Framework v1.5**

---

## 📋 Table of Contents

1. [Reproducibility with Seeds](#1-reproducibility-with-seeds)
2. [PCAP Trace Capture & Analysis](#2-pcap-trace-capture--analysis)
3. [Routing Overhead Calculation](#3-routing-overhead-calculation)
4. [Statistical Tests](#4-statistical-tests)
5. [Confidence Intervals](#5-confidence-intervals)
6. [Automated Reporting](#6-automated-reporting)
7. [Practical Examples](#7-practical-examples)

---

## 1. Reproducibility with Seeds

### What is it?
Total control over simulation randomness to guarantee reproducible results.

### How it works
The system automatically configures the random seed in NS-3 before creating nodes.

### Basic Usage

```python
# The system automatically generates code with seed
# No special action needed

# Example of generated code:
ns.core.RngSeedManager.SetSeed(12345)
ns.core.RngSeedManager.SetRun(1)
```

### Advanced Usage: Multiple Seeds

For robust statistical validation, run the same simulation with different seeds:

```python
# Custom script
seeds = [12345, 23456, 34567, 45678, 56789]

for seed in seeds:
    print(f"Running with seed: {seed}")
    # Modify generated code to use this seed
    # Or pass as parameter to the system
```

### Benefits
- ✅ 100% Reproducible results
- ✅ Peer validation
- ✅ Easier debugging
- ✅ Meets scientific standards

---

## 2. PCAP Trace Capture & Analysis

### What is it?
Capture of all packets transmitted during simulation for detailed analysis.

### How it works
The system automatically enables PCAP capture in the generated code.

### Generated Files

```
simulations/results/
├── simulacion-0-0_20251124_143022.pcap  # Node 0, interface 0
├── simulacion-0-1_20251124_143022.pcap  # Node 0, interface 1
├── simulacion-1-0_20251124_143022.pcap  # Node 1, interface 0
└── ...
```

### Automated Analysis

The **Trace Analyzer** agent automatically analyzes PCAP files and generates:

- Basic statistics (packets, bytes, duration)
- Protocol distribution (IP, UDP, TCP, ICMP, etc.)
- Routing protocol detection (AODV, OLSR, DSDV, DSR)
- Routing overhead calculation
- Latency analysis

### Manual Analysis with Wireshark

```bash
# Open PCAP file in Wireshark
wireshark simulations/results/simulacion-0-0_*.pcap

# Useful filters:
# - AODV packets: aodv
# - UDP packets: udp
# - Specific node packets: ip.src == 10.1.1.1
```

---

## 3. Routing Overhead Calculation

### What is it?
Ratio between control bytes (routing) and data bytes.

```
Overhead = Control_Bytes / Data_Bytes
```

### How is it calculated?

#### Method 1: From PCAP (Precise)
The Trace Analyzer analyzes PCAP files and counts:
- Routing packet bytes (AODV, OLSR, etc.)
- Data packet bytes (UDP, TCP)

#### Method 2: Estimation (Fallback)
If no PCAP is available, it estimates based on literature:
- AODV: ~15%
- OLSR: ~35%
- DSDV: ~45%
- DSR: ~20%

### Interpretation

```
Overhead < 20%  → Excellent (efficient protocol)
Overhead 20-30% → Good (acceptable)
Overhead 30-40% → Regular (proactive protocol)
Overhead > 40%  → High (consider optimization)
```

---

## 4. Statistical Tests

### What are they?
Tests to determine if observed differences are statistically significant.

### Available Tests

#### T-Test (Two Samples)
Compares two groups to see if their means are different.

**Example**: Compare PDR of successful vs failed flows.

```python
# The system automatically executes:
t_test_result = t_test_two_samples(
    successful_flows['pdr'].values,
    failed_flows['pdr'].values
)

# Result:
{
    't_statistic': 5.234,
    'p_value': 0.0001,
    'significant': True,
    'interpretation': 'Statistically significant difference (p < 0.05)'
}
```

#### ANOVA (Multiple Groups)
Compares three or more groups.

**Example**: Compare PDR among different protocols.

### p-value Interpretation

```
p < 0.001  → Highly significant (***)
p < 0.01   → Very significant (**)
p < 0.05   → Significant (*)
p ≥ 0.05   → Not significant (ns)
```

---

## 5. Confidence Intervals

### What are they?
Range of values where the true value is expected to be with a certain probability (95%).

### Format

```
Metric: [Lower Limit, Upper Limit]
```

### Output Example

```
📊 Calculating confidence intervals (95% CI)...
  ✓ Intervals calculated for 3 metrics
     pdr: [94.234, 96.876]
     avg_delay_ms: [45.321, 52.789]
     throughput_mbps: [2.123, 2.567]
```

### Interpretation

```
PDR: [94.2%, 96.9%]
→ We are 95% confident that the true PDR is between 94.2% and 96.9%
→ Narrow range = high precision
→ Wide range = low precision (needs more data)
```

---

## 6. Automated Reporting

### Statistical Report

The system automatically generates a Markdown report:

```
simulations/analysis/statistical_report_20251124_143022.md
```

### Report Content

```markdown
# Statistical Report - NS-3 Simulation

## Date: 2025-11-24 14:30:22

## Statistical Tests

### T-Test: Successful vs Failed Flows
- **t-statistic**: 5.234
- **p-value**: 0.0001
- **Significant**: Yes (p < 0.05)
- **Interpretation**: Statistically significant difference

## Confidence Intervals (95%)

| Metric | Lower Limit | Upper Limit | Range |
|--------|-------------|-------------|-------|
| PDR | 94.234% | 96.876% | 2.642% |
| Delay | 45.321 ms | 52.789 ms | 7.468 ms |
| Throughput | 2.123 Mbps | 2.567 Mbps | 0.444 Mbps |
```

---

## 7. Practical Examples

### Example 1: Basic Simulation with All Features

```bash
# 1. Run simulation
python main.py

# 2. Check generated files
ls -l simulations/results

# You should see:
# - sim_*.xml (FlowMonitor)
# - simulacion-*.pcap (PCAP Captures)
# - sim_*_stdout.txt (Logs)

# 3. Check analysis
ls -l simulations/analysis

# You should see:
# - statistical_report_*.md (Statistical report)
```

### Example 2: Compare Two Protocols

```python
# Run simulation with AODV
# Task: "Simulate MANET with AODV, 20 nodes"
python main.py

# Save results
cp simulations/results/sim_*.xml results_aodv.xml
cp simulations/analysis/statistical_report_*.md report_aodv.md

# Run simulation with OLSR
# Task: "Simulate MANET with OLSR, 20 nodes"
python main.py

# Save results
cp simulations/results/sim_*.xml results_olsr.xml
cp simulations/analysis/statistical_report_*.md report_olsr.md

# Compare reports
diff report_aodv.md report_olsr.md
```

---

## 📚 References

### Relevant Papers

1. **AODV**: Perkins et al., "Ad hoc On-Demand Distance Vector Routing", RFC 3561, 2003
2. **OLSR**: Clausen et al., "Optimized Link State Routing Protocol", RFC 3626, 2003
3. **Statistical Analysis**: Montgomery, "Design and Analysis of Experiments", 2017

### Tools

- **NS-3**: https://www.nsnam.org/
- **Scapy**: https://scapy.net/
- **Wireshark**: https://www.wireshark.org/
- **SciPy**: https://scipy.org/

---
