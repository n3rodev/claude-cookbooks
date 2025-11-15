# API Financial Analyzer - Complete Skill Example

A comprehensive example demonstrating how to create, upload, and use custom API skills with Claude. This example implements a financial ratio analyzer that calculates key financial metrics for company analysis.

## Overview

This project shows the complete lifecycle of API skills:

1. **Create** - Write a Python skill using PEP 723 format
2. **Upload** - Upload to Claude via the Skills API
3. **Use** - Call the skill from your application
4. **Deploy** - Integrate into production systems

## What You'll Learn

- Creating Python skills with PEP 723 metadata format
- Uploading skills via the Claude Skills API
- Integrating skills into Claude API calls
- Best practices for skill design and error handling
- Testing and validating skills

## Project Structure

```
api-financial-analyzer/
├── SKILL.md                    # Skill documentation and specifications
├── calculate_ratios.py         # Main skill implementation (PEP 723 format)
├── upload_skill.py             # Script to upload skill to API
├── README.md                   # This file
├── skill_config.json           # Generated after upload (skill metadata)
└── example_financial_data.json # Sample data for testing
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([get one](https://console.anthropic.com/))
- Anthropic Python SDK 0.71.0 or later

### Installation

1. **Clone or navigate to this directory**

```bash
cd tutorial/examples/api-financial-analyzer
```

2. **Install dependencies**

```bash
pip install anthropic>=0.71.0
```

3. **Set API key**

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### Upload the Skill

```bash
python upload_skill.py
```

This will:
- Validate the skill locally
- Upload to Claude
- Save the skill_id for future use
- Display configuration instructions

### Use the Skill

Once uploaded, use in your code:

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": "your-skill-id"}],
    messages=[{
        "role": "user",
        "content": """Analyze the financial health of this company:
        - Revenue: $1,000,000
        - Net Income: $200,000
        - Total Assets: $2,000,000
        - Total Equity: $1,000,000
        - Current Assets: $500,000
        - Current Liabilities: $250,000
        - Total Debt: $1,000,000"""
    }]
)

print(response.content[0].text)
```

## File Descriptions

### SKILL.md

Complete skill documentation including:
- Skill overview and capabilities
- How to use the skill
- Input/output formats
- Example usage scenarios
- Limitations and best practices

### calculate_ratios.py

The main skill implementation featuring:

**PEP 723 Metadata**:
```python
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
```

**FinancialRatioCalculator Class**:
- `calculate_profitability_ratios()` - ROE, ROA, profit margins
- `calculate_liquidity_ratios()` - Current, quick, cash ratios
- `calculate_leverage_ratios()` - Debt-to-equity, debt-to-assets
- `calculate_efficiency_ratios()` - Asset turnover, inventory turnover
- `calculate_all_ratios()` - Comprehensive analysis

**Helper Functions**:
- Interpretation methods for each ratio
- Data validation
- Flexible input parsing (JSON, text)
- Error handling

**Key Features**:
- No external dependencies (pure Python)
- ~400 lines of well-documented code
- Comprehensive ratio analysis
- Detailed interpretations
- Robust error handling

### upload_skill.py

Script for uploading and managing skills:

**Main Functions**:
- `read_skill_file()` - Load skill code
- `upload_skill()` - Upload via Skills API
- `save_skill_config()` - Save configuration locally
- `test_skill_locally()` - Validate before upload

**Features**:
- Local testing before upload
- API key management
- Configuration persistence
- Helpful error messages
- Step-by-step output

**Usage**:
```bash
python upload_skill.py
```

## API Integration Guide

### 1. Basic Usage

```python
from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": "financial-ratio-analyzer"}],
    messages=[{
        "role": "user",
        "content": "Calculate ratios for: revenue=$1M, net_income=$200K, ..."
    }]
)
```

### 2. With Multiple Skills

```python
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[
        {"skill_id": "financial-ratio-analyzer"},
        {"skill_id": "other-skill-id"}
    ],
    messages=[...]
)
```

### 3. Error Handling

```python
from anthropic import APIError

try:
    response = client.beta.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1024,
        betas=["skills-2025-10-02"],
        skills=[{"skill_id": "financial-ratio-analyzer"}],
        messages=[{
            "role": "user",
            "content": "Analyze financial data"
        }]
    )
except APIError as e:
    print(f"API Error: {e.message}")
    print(f"Status: {e.status_code}")
```

### 4. Processing Results

```python
response = client.beta.messages.create(...)

# Access the response
if response.stop_reason == "end_turn":
    result_text = response.content[0].text
    print("Analysis:", result_text)
else:
    print("Unexpected stop reason:", response.stop_reason)
```

## Input Data Formats

### JSON Format

```json
{
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
```

### CSV Format

```csv
metric,value
revenue,1000000
net_income,200000
total_assets,2000000
total_equity,1000000
```

### Natural Language

```
Company has:
- Revenue: $1 million
- Net income: $200K
- Assets: $2M
- Equity: $1M
```

## Output Format

The skill returns:

```json
{
    "profitability": {
        "roe": 0.20,
        "roe_percentage": 20.0,
        "roe_interpretation": "Excellent - Above 20% is outstanding return on equity",
        "roa": 0.10,
        "roa_percentage": 10.0,
        "roa_interpretation": "Excellent - Above 10% shows strong asset efficiency"
    },
    "liquidity": {
        "current_ratio": 2.0,
        "current_ratio_interpretation": "Good - 1.5-3.0 indicates healthy liquidity position",
        "quick_ratio": 1.5,
        "quick_ratio_interpretation": "Good - Above 1.0 indicates strong immediate liquidity",
        "cash_ratio": 1.0,
        "cash_ratio_interpretation": "Strong - Above 0.5 indicates excellent cash position"
    },
    "leverage": {
        "debt_to_equity_ratio": 1.0,
        "debt_to_equity_interpretation": "Moderate - Balanced capital structure",
        "debt_to_assets_ratio": 0.5,
        "debt_to_assets_interpretation": "Moderate - Reasonable debt level",
        "equity_ratio": 0.5
    },
    "efficiency": {
        "asset_turnover": 0.5,
        "asset_turnover_interpretation": "Moderate - Reasonable asset efficiency",
        "inventory_turnover": 6.0,
        "inventory_turnover_interpretation": "Good - Healthy inventory management"
    },
    "validation_errors": null,
    "summary": "Overall financial health: strong profitability, strong liquidity, moderate leverage"
}
```

## Testing

### Local Testing

Test the skill before uploading:

```bash
# Using upload_skill.py (included)
python upload_skill.py

# Or manually test the calculator
python calculate_ratios.py '{"revenue": 1000000, "net_income": 200000, ...}'
```

### API Testing

After upload, test with API:

```python
from anthropic import Anthropic

client = Anthropic()

response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": "financial-ratio-analyzer"}],
    messages=[{
        "role": "user",
        "content": """Please analyze these financial metrics:
        {
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
        }"""
    }]
)

print(response.content[0].text)
```

## Common Use Cases

### 1. Quick Financial Assessment

```python
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": "financial-ratio-analyzer"}],
    messages=[{
        "role": "user",
        "content": """I'm considering investing in Company X.
        Please analyze their financial health based on these metrics: [data]"""
    }]
)
```

### 2. Comparative Analysis

```python
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=2048,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": "financial-ratio-analyzer"}],
    messages=[{
        "role": "user",
        "content": """Compare the financial health of these two companies:
        Company A: [metrics]
        Company B: [metrics]"""
    }]
)
```

### 3. Trend Analysis

```python
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=2048,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": "financial-ratio-analyzer"}],
    messages=[{
        "role": "user",
        "content": """Analyze the financial trend for our company over the past 3 years:
        2022: [metrics]
        2023: [metrics]
        2024: [metrics]"""
    }]
)
```

## Best Practices

### Skill Design
- Keep skills focused on a single capability
- Use clear, descriptive function names
- Include comprehensive error handling
- Provide detailed interpretations
- Document input/output formats
- Use PEP 723 for metadata

### API Integration
- Always use the `betas` parameter per-request
- Include appropriate error handling
- Validate user input before passing to API
- Cache skill_id for production use
- Monitor token usage
- Log API calls for debugging

### Data Handling
- Validate financial data completeness
- Handle missing values gracefully
- Provide meaningful error messages
- Never expose sensitive data in logs
- Use HTTPS for all communications

### Performance
- Keep skill calculations lightweight
- Design for concurrent requests
- Cache frequently used calculations
- Monitor API latency
- Optimize token usage

## Troubleshooting

### "ANTHROPIC_API_KEY not found"

```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### "Module not found: anthropic"

```bash
pip install anthropic>=0.71.0
```

### "Skills API not available"

- Check you're using `client.beta.messages.create()`
- Verify `betas` parameter includes `"skills-2025-10-02"`
- Ensure API key has access to beta features

### "skill_id not found"

- Run `python upload_skill.py` to upload first
- Check `skill_config.json` for saved skill_id
- Verify the skill_id in your API call

### Unexpected results

- Validate input data in `skill_config.json`
- Check calculation logic in `calculate_ratios.py`
- Run local tests: `python calculate_ratios.py < test.json`
- Enable debug logging for API calls

## Advanced Topics

### Creating Your Own Skill

1. **Create a Python script** with your logic
2. **Add PEP 723 metadata** at the top
3. **Implement main()** function
4. **Handle input/output** as JSON
5. **Test locally** before upload
6. **Use upload_skill.py** as template

### Skill Lifecycle

```
Development → Testing → Upload → Integration → Deployment → Monitoring
```

### Integrating Multiple Skills

Skills can work together:

```python
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=2048,
    betas=["skills-2025-10-02"],
    skills=[
        {"skill_id": "financial-ratio-analyzer"},
        {"skill_id": "chart-generator"},
        {"skill_id": "report-writer"}
    ],
    messages=[{
        "role": "user",
        "content": "Create a financial report with analysis and charts"
    }]
)
```

## Files Reference

### calculate_ratios.py

**Classes**:
- `FinancialRatioCalculator` - Main calculator class

**Methods**:
- `__init__(financial_data)` - Initialize with data
- `calculate_profitability_ratios()` - ROE, ROA, margins
- `calculate_liquidity_ratios()` - Current, quick, cash ratios
- `calculate_leverage_ratios()` - Debt ratios
- `calculate_efficiency_ratios()` - Turnover ratios
- `calculate_all_ratios()` - Complete analysis

**Input**:
- JSON string or text format

**Output**:
- Dictionary with calculated ratios and interpretations

### upload_skill.py

**Functions**:
- `read_skill_file()` - Load skill code
- `upload_skill()` - Upload to API
- `save_skill_config()` - Save locally
- `test_skill_locally()` - Validate
- `main()` - Entry point

**Output**:
- Uploaded skill_id
- skill_config.json file

## Resources

- [Claude API Documentation](https://docs.claude.com/)
- [Skills API Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Files API Reference](https://docs.claude.com/en/api/files-content)
- [PEP 723 Specification](https://peps.python.org/pep-0723/)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)

## License

MIT License - See LICENSE file in root directory

## Contributing

Contributions welcome! Please:
1. Test locally before submitting
2. Follow the existing code style
3. Update documentation
4. Include usage examples
5. Test with the upload script

## Support

For issues or questions:
1. Check this README for common issues
2. Review SKILL.md for skill-specific docs
3. Check Anthropic documentation
4. Enable debug logging in upload_skill.py

## Next Steps

1. Run `python upload_skill.py` to upload the skill
2. Save the skill_id from the output
3. Integrate into your application
4. Customize for your use case
5. Deploy to production

Happy building!
