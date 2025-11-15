# Getting Started with the Financial Ratio Analyzer Skill

This quick-start guide will get you up and running with the Financial Ratio Analyzer in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one free](https://console.anthropic.com/))
- 5 minutes of time

## Step 1: Install Dependencies (30 seconds)

```bash
pip install anthropic>=0.71.0
```

## Step 2: Set Your API Key (30 seconds)

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

On Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

## Step 3: Test the Skill Locally (1 minute)

Before uploading to the API, test the skill locally:

```bash
python test_skill.py
```

You should see:
```
======================================================================
Financial Ratio Analyzer - Skill Test Suite
======================================================================

Running: Basic Test
  ✓ PASSED
    - ROE: 20.0%
    - Current Ratio: 2.0
    - Debt-to-Equity: 1.0

Running: Small Company
  ✓ PASSED
    - ROE: 33.33%
    - Current Ratio: 2.0
    - Debt-to-Equity: 0.67

... (more test cases)

Test Summary
======================================================================
Passed: 4
Failed: 0
Total:  4

✓ All tests passed! Ready to upload.
```

If tests fail, check:
- Python version: `python --version` (should be 3.8+)
- API key is set correctly
- Check the error message for missing dependencies

## Step 4: Upload the Skill (1 minute)

```bash
python upload_skill.py
```

You should see:
```
============================================================
Financial Ratio Analyzer - Skill Upload
============================================================

✓ Found skill script: .../calculate_ratios.py

Testing skill locally...
✓ Local test passed!
  Sample output: {...}

✓ Read skill file (15223 bytes)

✓ Found ANTHROPIC_API_KEY

✓ Initialized Anthropic client

Uploading skill 'financial-ratio-analyzer'...
Description: Analyzes financial ratios...

✓ Skill uploaded successfully!
  Skill ID: financial-ratio-analyzer

✓ Saved skill configuration to skill_config.json

============================================================
Next Steps
...
```

## Step 5: Use the Skill (2 minutes)

Create a file `my_analysis.py`:

```python
from anthropic import Anthropic
import json

client = Anthropic()

# Your financial data
financial_data = {
    "revenue": 1000000,
    "net_income": 200000,
    "total_assets": 2000000,
    "total_equity": 1000000,
    "current_assets": 500000,
    "current_liabilities": 250000,
    "inventory": 100000,
    "total_debt": 1000000,
    "cost_of_goods_sold": 600000,
    "cash": 100000
}

response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{
        "type": "skill",
        "name": "financial-ratio-analyzer",
        "code": {
            "type": "python",
            "content": open("calculate_ratios.py").read()
        }
    }],
    messages=[{
        "role": "user",
        "content": f"""Analyze this company's financial health:

{json.dumps(financial_data, indent=2)}

Calculate key ratios and provide your assessment."""
    }]
)

print(response.content[0].text)
```

Run it:
```bash
python my_analysis.py
```

## What Each File Does

| File | Purpose |
|------|---------|
| `calculate_ratios.py` | The skill itself - calculates financial ratios |
| `upload_skill.py` | Uploads the skill to Claude via the API |
| `test_skill.py` | Tests the skill locally before uploading |
| `example_usage.py` | Shows different usage patterns |
| `SKILL.md` | Detailed skill documentation |
| `README.md` | Complete reference guide |
| `skill_config.json` | Created after upload - contains your skill_id |

## Common Issues

### "ANTHROPIC_API_KEY not found"
```bash
# Check if it's set
echo $ANTHROPIC_API_KEY

# Set it if not
export ANTHROPIC_API_KEY="your-key-here"
```

### "anthropic module not found"
```bash
pip install anthropic>=0.71.0

# If using a virtual environment, make sure it's activated
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### "Skills API not available"
- Make sure you're using `client.beta.messages.create()`
- Include `betas=["skills-2025-10-02"]` in the request
- Verify your API key has access to beta features

### "Test passes but API call fails"
- Check that you're passing the correct skill format
- Verify the skill code is being read correctly
- Enable debug logging: set `PYTHONVERBOSE=2`

## Next Steps

1. **Explore the skill**: Read `SKILL.md` for detailed capabilities
2. **Read the docs**: Check `README.md` for comprehensive reference
3. **Customize it**: Modify `calculate_ratios.py` for your needs
4. **Deploy it**: Integrate into your application

## Quick Reference

### Upload the skill once:
```bash
python upload_skill.py
```

### Then use it repeatedly:
```python
# Load saved config
with open('skill_config.json') as f:
    skill_id = json.load(f)['skill_id']

# Use in API calls
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": skill_id}],
    messages=[{
        "role": "user",
        "content": "Analyze these financial metrics..."
    }]
)
```

## Real-World Example

Analyze a real company:

```python
# Apple Inc. (example Q4 2023 data)
apple_data = {
    "revenue": 383285000000,
    "net_income": 96995000000,
    "total_assets": 352755000000,
    "total_equity": 50672000000,
    "current_assets": 135405000000,
    "current_liabilities": 120122000000,
    "total_debt": 106931000000,
    "cost_of_goods_sold": 214301000000,
}

# Pass to Claude with the skill
```

## Support

- **Issues?** Check the README.md troubleshooting section
- **Questions?** Review SKILL.md for detailed documentation
- **Want to customize?** See README.md advanced topics
- **API help?** Check [Claude docs](https://docs.claude.com/)

## You're Ready!

You now have:
- ✓ A working financial ratio analyzer
- ✓ Understanding of API skills
- ✓ Knowledge to create your own skills

Start using it or customize it for your needs!

---

**Pro Tips:**
- The skill has no external dependencies - it's pure Python
- Test locally with `test_skill.py` before uploading
- Save your `skill_config.json` for production use
- Ratios work best with complete financial data
- Consider industry context when interpreting results
