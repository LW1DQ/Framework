# Cost Estimation Guide

## Overview
This document outlines the operational costs associated with running the A2A Framework using various LLM backends.

## 💰 Cost Considerations

### Using Local Models (FREE)

The framework works out-of-the-box with Ollama (FREE):
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model
ollama pull llama3.1:8b

# Total cost: $0
```

**Advantages:**
- ✅ Zero operational cost
- ✅ Data privacy (runs locally)
- ✅ No internet required after download
- ✅ Unlimited experiments

**Limitations:**
- ⚠️ Lower code quality than commercial models
- ⚠️ Requires powerful GPU (8GB+ VRAM recommended)
- ⚠️ Slower than API calls

### Using Commercial APIs

For **production research** requiring **publication-quality** results:

#### Cost Estimation (Full Experiment Cycle)

**Scenario: Protocol Comparison (AODV vs OLSR vs DSDV)**
- Literature Review: ~5K tokens → $0.015
- Code Generation: ~20K tokens → $0.06
- Code Review (3 iterations): ~15K tokens → $0.045
- Analysis: ~10K tokens → $0.03
- Document Generation: ~30K tokens → $0.09
**Total per experiment: ~$0.24 (with Claude 3.5 Sonnet)**

**Monthly Research Budget Examples:**
- **Light usage** (10 experiments/month): ~$2.40/month
- **Medium usage** (50 experiments/month): ~$12/month
- **Heavy usage** (200 experiments/month): ~$48/month

#### Cost Comparison

| Model | Input ($) | Output ($) | Avg. Experiment Cost |
|-------|-----------|------------|----------------------|
| **Claude 3.5 Sonnet** | $3/1M | $15/1M | $0.24 |
| GPT-4 Turbo | $10/1M | $30/1M | $0.80 |
| GPT-4o | $2.50/1M | $10/1M | $0.35 |
| Gemini Pro | $0.50/1M | $1.50/1M | $0.12 |
| **Ollama (Local)** | FREE | FREE | $0.00 |

**Recommended Strategy:**
1. **Development/Testing**: Use Ollama (FREE)
2. **Final Experiments**: Use Claude 3.5 Sonnet ($0.24/experiment)
3. **Budget Option**: Use Gemini Pro ($0.12/experiment)

**Cost Control Tips:**
- Use local models for development and debugging
- Switch to API only for final production runs
- Set API rate limits in config
- Enable caching to reduce redundant calls
- Use smaller context windows when possible

### API Key Management

```yaml
# config/api_keys.yaml (DO NOT COMMIT TO GIT)
anthropic:
  api_key: "sk-ant-..."
  rate_limit: 100  # requests per minute
  monthly_budget: 50  # USD

openai:
  api_key: "sk-..."
  rate_limit: 60
  monthly_budget: 100
```
