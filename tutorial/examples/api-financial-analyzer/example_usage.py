#!/usr/bin/env python3
"""
Example usage of the Financial Ratio Analyzer skill via Claude API.

This demonstrates how to:
1. Initialize the Anthropic client
2. Upload and use the financial ratio analyzer skill
3. Process the results

Prerequisites:
    - ANTHROPIC_API_KEY environment variable set
    - Anthropic Python SDK installed: pip install anthropic>=0.71.0
    - Financial Ratio Analyzer skill uploaded (run upload_skill.py first)

Usage:
    python example_usage.py
"""

import os
import json
import sys
from pathlib import Path

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install with: pip install anthropic>=0.71.0")
    sys.exit(1)


def example_1_basic_analysis():
    """Example 1: Basic financial analysis."""
    print("\n" + "=" * 70)
    print("Example 1: Basic Financial Analysis")
    print("=" * 70)

    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

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

    print("\nFinancial Data:")
    for key, value in financial_data.items():
        print(f"  {key}: ${value:,}")

    print("\nSending to Claude for analysis...")

    # Note: This example shows the structure. For actual use with an uploaded skill,
    # you would need the skill_id from your upload_skill.py output
    try:
        response = client.beta.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1024,
            betas=["skills-2025-10-02"],
            # Note: Replace with your actual skill_id from upload_skill.py
            skills=[{
                "type": "skill",
                "name": "financial-ratio-analyzer",
                "description": "Analyzes financial ratios",
                "code": {
                    "type": "python",
                    "content": _read_skill_code()
                }
            }],
            messages=[{
                "role": "user",
                "content": f"""Please analyze the financial health of this company:

{json.dumps(financial_data, indent=2)}

Calculate key ratios including ROE, ROA, current ratio, and debt-to-equity.
Provide your interpretation of what these ratios mean for the company's financial health."""
            }]
        )

        print("\nClaud's Analysis:")
        print(response.content[0].text)

    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: This example requires the skill to be properly configured.")


def example_2_comparative_analysis():
    """Example 2: Comparing two companies."""
    print("\n" + "=" * 70)
    print("Example 2: Comparative Analysis")
    print("=" * 70)

    company_a = {
        "name": "Tech Corp A",
        "revenue": 5000000,
        "net_income": 1000000,
        "total_assets": 3000000,
        "total_equity": 2000000,
        "current_assets": 1500000,
        "current_liabilities": 500000,
        "inventory": 200000,
        "total_debt": 1000000,
        "cost_of_goods_sold": 2500000,
        "cash": 500000
    }

    company_b = {
        "name": "Retail Corp B",
        "revenue": 3000000,
        "net_income": 300000,
        "total_assets": 2000000,
        "total_equity": 1000000,
        "current_assets": 800000,
        "current_liabilities": 400000,
        "inventory": 500000,
        "total_debt": 1000000,
        "cost_of_goods_sold": 1800000,
        "cash": 100000
    }

    print(f"\nComparing: {company_a['name']} vs {company_b['name']}")
    print(f"Company A Revenue: ${company_a['revenue']:,}")
    print(f"Company B Revenue: ${company_b['revenue']:,}")

    print("\nFor comparative analysis, you would:")
    print("1. Calculate ratios for both companies")
    print("2. Compare ROE, liquidity, leverage across companies")
    print("3. Identify strengths and weaknesses")
    print("4. Provide investment recommendations")


def example_3_with_uploaded_skill():
    """Example 3: Using an uploaded skill via skill_id."""
    print("\n" + "=" * 70)
    print("Example 3: Using an Uploaded Skill")
    print("=" * 70)

    print("\nAfter uploading with upload_skill.py, use the skill_id:")
    print("""
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Load the skill_id from skill_config.json
with open('skill_config.json') as f:
    config = json.load(f)
    skill_id = config['skill_id']

response = client.beta.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    betas=["skills-2025-10-02"],
    skills=[{"skill_id": skill_id}],
    messages=[{
        "role": "user",
        "content": "Analyze the financial ratios for [financial data]"
    }]
)

print(response.content[0].text)
    """)


def example_4_error_handling():
    """Example 4: Proper error handling."""
    print("\n" + "=" * 70)
    print("Example 4: Error Handling")
    print("=" * 70)

    print("\nProper error handling:")
    print("""
from anthropic import APIError, Anthropic

client = Anthropic(api_key="your-api-key")

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

    # Process response
    if response.stop_reason == "end_turn":
        print("Analysis:", response.content[0].text)
    else:
        print(f"Unexpected completion: {response.stop_reason}")

except APIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
except Exception as e:
    print(f"Error: {e}")
    """)


def _read_skill_code() -> str:
    """Read the skill code from calculate_ratios.py."""
    try:
        skill_path = Path(__file__).parent / "calculate_ratios.py"
        with open(skill_path, 'r') as f:
            return f.read()
    except (FileNotFoundError, IOError, OSError) as e:
        print(f"Warning: Could not read skill file: {e}")
        return ""


def main():
    """Run examples."""
    print("\n" + "=" * 70)
    print("Financial Ratio Analyzer - API Usage Examples")
    print("=" * 70)

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nWarning: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("\nShowing example structures (won't execute API calls)...")
    else:
        print("\n✓ Found API key, examples will execute")

    # Run examples
    example_1_basic_analysis()
    example_2_comparative_analysis()
    example_3_with_uploaded_skill()
    example_4_error_handling()

    # Summary
    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print("""
To use the Financial Ratio Analyzer skill:

1. Upload the skill:
   python upload_skill.py

2. Use in your code:
   - Inline: Include the skill code in your API request
   - Via ID: Use the skill_id from skill_config.json

3. Integrate with Claude:
   - Pass financial data as part of user message
   - Claude will use the skill to analyze ratios
   - Results include interpretations and insights

See README.md for detailed documentation.
    """)


if __name__ == "__main__":
    main()
