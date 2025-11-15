---
name: financial-ratio-analyzer
description: API Skill for comprehensive financial ratio analysis and performance metrics
---

# Financial Ratio Analyzer API Skill

This is an API-based skill that demonstrates how to upload and manage custom skills via the Claude API. It provides comprehensive financial ratio analysis for evaluating company financial health, profitability, liquidity, and leverage.

## Overview

The Financial Ratio Analyzer is designed to be uploaded to Claude via the Skills API, enabling Claude to perform financial analysis without users needing to handle the calculations directly. This example demonstrates the full lifecycle of creating, uploading, and using a custom API skill.

## Capabilities

This skill calculates and interprets:

### Profitability Ratios
- **Return on Equity (ROE)**: Measures how effectively the company generates profit from shareholder equity
- **Return on Assets (ROA)**: Indicates how efficiently assets are used to generate profit

### Liquidity Ratios
- **Current Ratio**: Assesses the company's ability to pay short-term obligations
- **Quick Ratio**: Similar to current ratio but excludes inventory
- **Cash Ratio**: Measures immediate liquidity using only cash and equivalents

### Leverage Ratios
- **Debt-to-Equity Ratio**: Evaluates financial risk and capital structure
- **Debt-to-Assets Ratio**: Shows the proportion of assets financed by debt

### Efficiency Ratios
- **Asset Turnover**: Measures how efficiently assets generate revenue
- **Inventory Turnover**: Shows how quickly inventory is converted to sales

## How to Use This Skill

### 1. Upload the Skill

Use the `upload_skill.py` script to upload this skill to Claude:

```bash
python upload_skill.py
```

This will:
- Read the `calculate_ratios.py` file
- Package it with metadata
- Upload to Claude via the Skills API
- Return a `skill_id` for use in API calls

### 2. Use the Skill in Your Application

Once uploaded, reference the skill in your Claude API calls:

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Use the uploaded skill
response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["files-api-2025-04-14", "skills-2025-10-02"],
    skills=[{"skill_id": "your-skill-id-from-upload"}],
    messages=[{
        "role": "user",
        "content": "Analyze the financial health of a company with these metrics: revenue of $1M, net income of $200K, current assets of $500K, current liabilities of $250K, total assets of $2M, and total equity of $1M"
    }]
)

print(response.content[0].text)
```

### 3. Input Format

Provide financial data in any of these formats:

**JSON Format**:
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
    "cost_of_goods_sold": 600000
}
```

**CSV Format**:
```csv
metric,value
revenue,1000000
net_income,200000
total_assets,2000000
```

**Natural Language**:
> "Our company has revenue of $1M, net income of $200K, current assets of $500K, and current liabilities of $250K"

### 4. Output Format

The skill returns:

```json
{
    "profitability": {
        "roe": 0.20,
        "roe_interpretation": "Strong return on equity",
        "roa": 0.10,
        "roa_interpretation": "Good asset efficiency"
    },
    "liquidity": {
        "current_ratio": 2.0,
        "current_ratio_interpretation": "Healthy liquidity position",
        "quick_ratio": 1.5,
        "cash_ratio": 1.0
    },
    "leverage": {
        "debt_to_equity": 1.0,
        "debt_to_equity_interpretation": "Moderate leverage",
        "debt_to_assets": 0.5
    },
    "efficiency": {
        "asset_turnover": 0.5,
        "inventory_turnover": 6.0
    }
}
```

## File Structure

```
api-financial-analyzer/
├── SKILL.md                    # This file - skill documentation
├── calculate_ratios.py         # Main skill code (PEP 723 format)
├── upload_skill.py             # Script to upload skill to API
├── README.md                   # Detailed usage guide
└── example_financial_data.json # Sample data for testing
```

## Best Practices

### Data Validation
- Always validate that required fields are present before calculation
- Handle missing or zero values appropriately
- Flag potential data quality issues

### Industry Context
- Ratios should be compared against industry benchmarks
- Same ratio can mean different things in different industries
- Always provide context and caveats

### Error Handling
- Return meaningful error messages when data is invalid
- Suggest what data might be missing
- Don't return partial results without noting limitations

### Performance Considerations
- Calculations are lightweight and fast
- Suitable for real-time analysis
- Can be called multiple times in a single conversation

## Example Usage Scenarios

### Scenario 1: Quick Company Assessment
```
"I have these financial figures for Company X. What's their financial health?"
[User provides financials]
→ Skill calculates all ratios and provides interpretation
```

### Scenario 2: Comparison Analysis
```
"Compare the financial ratios of Company A and Company B"
[User provides financials for both]
→ Skill calculates ratios for each and highlights differences
```

### Scenario 3: Trend Analysis
```
"How have our financial ratios changed over the last 3 years?"
[User provides historical data]
→ Skill calculates trends and flags concerning changes
```

## Limitations

- Requires complete or near-complete financial data
- Ratios are calculated from provided figures; accuracy depends on input accuracy
- Industry benchmarks are general guidelines
- Does not account for accounting method differences (GAAP vs IFRS)
- Historical analysis doesn't guarantee future performance

## Technical Requirements

- Python 3.8 or higher
- Anthropic Python SDK (0.71.0+)
- API key with access to Skills API
- No external dependencies for skill calculations

## Deployment Considerations

### Security
- Never expose financial data in logs
- Use HTTPS for all API calls
- Validate input to prevent injection attacks
- Consider rate limiting for production use

### Scalability
- Skill is stateless and can handle concurrent requests
- Suitable for cloud deployment
- No database dependencies

### Monitoring
- Log skill invocations for audit purposes
- Monitor calculation accuracy with random sampling
- Track performance metrics and API latency

## Support and Updates

For issues or improvements:
1. Check the README.md for common issues
2. Review error messages and validation logs
3. Test with the provided sample data
4. Update the skill using the same upload process with modified code

## Resources

- [Claude API Documentation](https://docs.claude.com/)
- [Skills API Guide](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Files API Reference](https://docs.claude.com/en/api/files-content)
- [Financial Ratio Analysis Guide](https://www.investopedia.com/financial-ratios-4689817)

