# 📖 User Manual - A2A Framework

**Complete guide for researchers without programming experience**

---

## 👋 Welcome!

This manual is designed for researchers who want to use the A2A framework **without needing programming knowledge**. We'll guide you step by step through everything you need to know.

---

## 📋 Table of Contents

1. [What is A2A?](#what-is-a2a)
2. [Getting Started](#getting-started)
3. [Using the Dashboard](#using-the-dashboard)
4. [Running Experiments](#running-experiments)
5. [Generating Documents](#generating-documents)
6. [Understanding Results](#understanding-results)
7. [Common Tasks](#common-tasks)
8. [FAQ](#faq)

---

## 🤔 What is A2A?

A2A (Agent-to-Agent) is a system that **automates research tasks** for network protocol evaluation. Think of it as having 10 specialized assistants working for you:

### The 10 Assistants (Agents)

1. **📚 Researcher**: Searches for academic papers
2. **💻 Coder**: Writes simulation code
3. **⚙️ Simulator**: Runs network simulations
4. **📊 Analyst**: Calculates performance metrics
5. **📈 Visualizer**: Creates graphs and tables
6. **🖊️ Writer**: Generates scientific documents
7. **🧠 Optimizer**: Improves protocols using AI
8. **🔗 Integrator**: Connects different tools
9. **✅ Critic**: Checks quality
10. **📁 Manager**: Organizes results

### What Can A2A Do For You?

- ✅ Run network simulations automatically
- ✅ Analyze results with statistical rigor
- ✅ Generate publication-ready graphics
- ✅ Write scientific documents (briefings, reports, thesis chapters)
- ✅ Compare different network protocols
- ✅ Save 99% of your documentation time

---

## 🚀 Getting Started

### Step 1: Installation

Follow the [Installation Guide](INSTALL.md). The easiest way is using our automated script:

**Summary**:
```bash
# Open terminal and run these commands one by one:
git clone https://github.com/LW1DQ/Framework.git
cd Framework
chmod +x install.sh
./install.sh
source venv/bin/activate
```

### Step 2: Verify Installation

```bash
python verify-system-complete.py
```

You should see: ✅ **100% Verified**

### Step 3: Launch Dashboard

```bash
streamlit run dashboard.py
```

A web page will open in your browser at `http://localhost:8501`

---

## 📊 Using the Dashboard

The dashboard is your **control center**. Everything you need is here!

### Dashboard Sections

#### 1. **Home** 🏠
- System status
- Quick actions
- Recent experiments

#### 2. **Experiments** 🧪
- Run new experiments
- View running experiments
- Check results

#### 3. **Documents** 📄
- Generate briefings
- Create reports
- Write thesis sections

#### 4. **Agents** 🤖
- Monitor agent status
- View agent logs
- Control agent execution

#### 5. **Results** 📈
- View graphics
- Download data
- Export tables

### How to Navigate

1. **Sidebar**: Use the menu on the left to switch between sections
2. **Main Area**: Your workspace
3. **Status Bar**: Shows system status at the bottom

---

## 🧪 Running Experiments

### What is an Experiment?

An experiment is a **network simulation** that tests how protocols perform. For example:
- Compare AODV vs OLSR protocols
- Test how protocols scale with more nodes
- Evaluate impact of node mobility

### Pre-configured Experiments

A2A comes with 3 ready-to-use experiments:

#### Experiment 1: Protocol Comparison
**What it does**: Compares AODV, OLSR, and DSDV protocols

**How to run**:
```bash
python experiments/experiment_runner.py --config experiments/configs/comparison.yaml
```

**Time**: 3-4 hours  
**Output**: Comparative analysis with graphics

#### Experiment 2: Scalability Analysis
**What it does**: Tests AODV with 10 to 100 nodes

**How to run**:
```bash
python experiments/experiment_runner.py --config experiments/configs/scalability.yaml
```

**Time**: 8-10 hours  
**Output**: Scalability graphs and limits

#### Experiment 3: Mobility Impact
**What it does**: Evaluates effect of node speed

**How to run**:
```bash
python experiments/experiment_runner.py --config experiments/configs/mobility.yaml
```

**Time**: 5-6 hours  
**Output**: Mobility analysis

### Monitoring Experiments

While an experiment runs:

1. **Open Dashboard**: `streamlit run dashboard.py`
2. **Go to "Experiments"** section
3. **Watch progress** in real-time
4. **Check logs** if needed

### Understanding Experiment Output

After an experiment completes, you'll find:

```
experiments/results/comparison_YYYYMMDD_HHMMSS/
├── config.yaml              # Configuration used
├── raw_data/               # Raw simulation data
├── analysis/               # Statistical analysis
├── graphics/               # PNG/PDF graphics (300 DPI)
├── tables/                 # LaTeX tables
└── summary.md              # Results summary
```

---

## 📝 Generating Documents

### Types of Documents

A2A can generate 6 types of documents automatically:

#### 1. Briefing (2 pages)
**When to use**: Quick summary after experiment

**How to generate**:
```bash
python examples/generate_briefing.py --experiment comparison
```

**Contains**:
- Executive summary
- Configuration
- Main results
- Key observations

#### 2. Technical Report (5-10 pages)
**When to use**: Complete documentation

**How to generate**:
```bash
python examples/generate_report.py --experiment comparison
```

**Contains**:
- Introduction
- Methodology
- Results with statistical analysis
- Discussion
- Conclusions

#### 3. Thesis Section
**When to use**: Writing your thesis

**How to generate**:
```bash
python examples/generate_thesis.py --experiment comparison --section results
```

**Options for --section**:
- `methodology`: Experimental design
- `results`: Data presentation
- `discussion`: Analysis and interpretation

#### 4. Paper Draft (IEEE format)
**When to use**: Preparing publication

**How to generate**:
```bash
python examples/generate_paper.py --experiment comparison
```

**Contains**:
- Abstract
- Introduction
- Related Work
- Methodology
- Results
- Discussion
- Conclusion
- References (IEEE format)

#### 5. Presentation Slides
**When to use**: Preparing presentation

**How to generate**:
```bash
python examples/generate_slides.py --experiment comparison
```

**Output**: Markdown slides (10-15 slides)

#### 6. Comparative Analysis
**When to use**: Comparing multiple experiments

**How to generate**:
```bash
python examples/generate_comparison.py --experiments exp1 exp2 exp3
```

### Document Quality

All documents include:
- ✅ IEEE references
- ✅ Statistical validation
- ✅ Confidence intervals
- ✅ Publication-quality tables
- ✅ Professional formatting

---

## 📊 Understanding Results

### Key Metrics

#### PDR (Packet Delivery Ratio)
**What it is**: Percentage of packets successfully delivered

**Good values**: 80-95%  
**Interpretation**:
- High PDR (>90%): Reliable protocol
- Low PDR (<70%): Many packet losses

#### Delay
**What it is**: Time for packet to reach destination

**Good values**: <100 ms  
**Interpretation**:
- Low delay (<50 ms): Fast protocol
- High delay (>200 ms): Slow protocol

#### Throughput
**What it is**: Amount of data transmitted per second

**Units**: Mbps (megabits per second)  
**Interpretation**:
- High throughput: Efficient use of bandwidth
- Low throughput: Network congestion

#### Overhead
**What it is**: Extra control messages needed

**Good values**: <20%  
**Interpretation**:
- Low overhead (<15%): Efficient protocol
- High overhead (>30%): Too many control messages

### Reading Graphics

#### Bar Charts
- **Height**: Metric value
- **Error bars**: Confidence interval (95%)
- **Compare**: Taller is better (for PDR, throughput)

#### Line Charts
- **X-axis**: Usually time or number of nodes
- **Y-axis**: Metric value
- **Trend**: Shows how metric changes

#### Box Plots
- **Box**: Middle 50% of data
- **Line in box**: Median value
- **Whiskers**: Min and max values
- **Dots**: Outliers

### Statistical Significance

When comparing protocols, look for:

**p-value < 0.05**: Difference is **statistically significant**
- Example: "OLSR has significantly higher PDR than AODV (p = 0.003)"

**p-value > 0.05**: Difference is **not significant**
- Example: "No significant difference in throughput (p = 0.089)"

---

## 🔧 Common Tasks

### Task 1: Compare Two Protocols

**Goal**: Find which protocol is better

**Steps**:
1. Edit `experiments/configs/comparison.yaml`
2. Set protocols: `[AODV, OLSR]`
3. Run: `python experiments/experiment_runner.py --config experiments/configs/comparison.yaml`
4. Wait for completion (3-4 hours)
5. Generate briefing: `python examples/generate_briefing.py`
6. Review results in `experiments/results/`

### Task 2: Test Scalability

**Goal**: See how protocol performs with more nodes

**Steps**:
1. Use `experiments/configs/scalability.yaml`
2. Run: `python experiments/experiment_runner.py --config experiments/configs/scalability.yaml`
3. Wait for completion (8-10 hours)
4. Generate report: `python examples/generate_report.py`
5. Check scalability graphs

### Task 3: Write Thesis Chapter

**Goal**: Generate methodology section for thesis

**Steps**:
1. Run your experiment first
2. Generate methodology: `python examples/generate_thesis.py --section methodology`
3. Generate results: `python examples/generate_thesis.py --section results`
4. Generate discussion: `python examples/generate_thesis.py --section discussion`
5. Find documents in `generated_documents/thesis_section/`
6. Copy to your thesis LaTeX file

### Task 4: Create Presentation

**Goal**: Prepare slides for conference

**Steps**:
1. Run experiment
2. Generate slides: `python examples/generate_slides.py`
3. Open generated Markdown file
4. Convert to PowerPoint or use Marp/reveal.js
5. Add your graphics from `experiments/results/graphics/`

### Task 5: Prepare Paper

**Goal**: Write paper for publication

**Steps**:
1. Run all experiments
2. Generate paper draft: `python examples/generate_paper.py`
3. Review and edit generated paper
4. Add graphics from results
5. Check IEEE format
6. Submit to journal/conference

---

## ❓ FAQ

### General Questions

**Q: Do I need to know programming?**  
A: No! This manual is designed for non-programmers. Just follow the commands.

**Q: How long does an experiment take?**  
A: Depends on configuration:
- Small (10 nodes, 10 reps): 1-2 hours
- Medium (20 nodes, 10 reps): 3-4 hours
- Large (50+ nodes, 10 reps): 8-10 hours

**Q: Can I stop an experiment?**  
A: Yes! Press `Ctrl+C` in the terminal. Progress is saved.

**Q: How much disk space do I need?**  
A: Minimum 20 GB, recommended 50 GB for multiple experiments.

**Q: Can I run multiple experiments simultaneously?**  
A: Yes, but it will slow down your computer. Better to run one at a time.

### Technical Questions

**Q: What if an experiment fails?**  
A: Check `logs/system.log` for errors. Common issues:
- NS-3 not installed → See [INSTALL.md](INSTALL.md)
- Out of memory → Reduce number of nodes
- Configuration error → Check YAML syntax

**Q: How do I change experiment parameters?**  
A: Edit the YAML file in `experiments/configs/`. Example:
```yaml
nodes: 30  # Change from 20 to 30
duration: 300  # Change from 200 to 300 seconds
```

**Q: Where are results saved?**  
A: In `experiments/results/[experiment_name]_[timestamp]/`

**Q: Can I use my own protocols?**  
A: Yes! See [Developer Guide](docs/DEVELOPER_GUIDE.md) for instructions.

**Q: How do I cite A2A in my paper?**  
A: See [CITATION.cff](CITATION.cff) for BibTeX format.

### Document Generation Questions

**Q: Can I edit generated documents?**  
A: Yes! They are Markdown files. Edit with any text editor.

**Q: Are references included?**  
A: Yes! IEEE format references are automatically added.

**Q: Can I change document style?**  
A: Yes! Edit templates in `templates/` directory.

**Q: How do I convert Markdown to LaTeX?**  
A: Use pandoc: `pandoc input.md -o output.tex`

**Q: Can I generate documents in other languages?**  
A: Currently English only. Spanish support coming in v1.6.

---

## 🆘 Getting Help

### If Something Goes Wrong

1. **Check logs**: `cat logs/system.log`
2. **Read error message**: Usually tells you what's wrong
3. **Search documentation**: Use Ctrl+F to search this manual
4. **Check troubleshooting**: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
5. **Ask community**: [GitHub Discussions](https://github.com/LW1DQ/Framework/discussions)

### Support Channels

- **Documentation**: Read all docs in `docs/` folder
- **Examples**: Check `examples/` for working code
- **Issues**: Report bugs on GitHub
- **Email**: contact@lw1dq.com

---

## 📚 Next Steps

Now that you know the basics:

1. **Run your first experiment**: Try the comparison experiment
2. **Generate a document**: Create a briefing
3. **Explore the dashboard**: Familiarize yourself with all sections
4. **Read advanced guides**: Check `docs/` for more details
5. **Join community**: Share your experience!

---

## 💡 Tips for Success

### Best Practices

1. **Start small**: Run small experiments first (10 nodes, 2 repetitions)
2. **Monitor progress**: Use dashboard to watch experiments
3. **Save results**: Backup `experiments/results/` regularly
4. **Document everything**: Keep notes of what you try
5. **Ask for help**: Don't hesitate to ask questions

### Time Management

- **Planning**: 1 week to learn system
- **Experimentation**: 2-4 weeks for all experiments
- **Analysis**: 1-2 weeks
- **Writing**: 1 week (with A2A's help!)
- **Total**: 5-8 weeks for complete thesis chapter

### Quality Assurance

- ✅ Always run 10+ repetitions for statistical validity
- ✅ Check confidence intervals are reasonable
- ✅ Verify results make sense (compare with literature)
- ✅ Review generated documents before using
- ✅ Keep raw data for reproducibility

---

## 🎓 For Thesis Students

### Recommended Workflow

**Week 1-2: Setup and Learning**
- Install A2A
- Run example experiments
- Learn dashboard
- Read documentation

**Week 3-4: Experimentation**
- Design your experiments
- Run simulations
- Monitor and adjust
- Collect results

**Week 5-6: Analysis**
- Generate all graphics
- Calculate statistics
- Compare with literature
- Validate results

**Week 7-8: Writing**
- Generate thesis sections
- Review and edit
- Add your insights
- Finalize document

### Thesis Checklist

- [ ] All experiments completed
- [ ] Results statistically validated
- [ ] Graphics generated (300 DPI)
- [ ] Tables in LaTeX format
- [ ] Methodology section written
- [ ] Results section written
- [ ] Discussion section written
- [ ] References in IEEE format
- [ ] Raw data archived
- [ ] Code documented

---

**You're ready to start! Good luck with your research!** 🚀

[← Back to README](README.md) | [Installation Guide →](INSTALL.md) | [Troubleshooting →](docs/TROUBLESHOOTING.md)
