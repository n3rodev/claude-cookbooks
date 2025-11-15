#!/usr/bin/env python3
"""
Test script for the Financial Ratio Analyzer skill.

This demonstrates how to test the skill locally before uploading it
to the Claude API.

Usage:
    python test_skill.py
"""

import json
import subprocess
import sys
from pathlib import Path


def test_skill_with_data(test_data: dict) -> bool:
    """
    Test the skill with a specific dataset.

    Args:
        test_data: Dictionary with financial data

    Returns:
        True if test passes, False otherwise
    """
    script_path = Path(__file__).parent / "calculate_ratios.py"

    try:
        result = subprocess.run(
            ['python3', str(script_path)],
            input=json.dumps(test_data),
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print("Error running skill:")
            print(result.stderr)
            return False

        # Parse and validate output
        output = json.loads(result.stdout)

        # Check for required keys
        required_keys = ['profitability', 'liquidity', 'leverage', 'efficiency']
        for key in required_keys:
            if key not in output:
                print(f"Missing required key: {key}")
                return False

        return True, output

    except Exception as e:
        print(f"Error: {e}")
        return False, None


def main():
    """Run tests."""
    print("=" * 70)
    print("Financial Ratio Analyzer - Skill Test Suite")
    print("=" * 70)
    print()

    test_cases = {
        "Basic Test": {
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
        },
        "Small Company": {
            "revenue": 100000,
            "net_income": 10000,
            "total_assets": 50000,
            "total_equity": 30000,
            "current_assets": 20000,
            "current_liabilities": 10000,
            "total_debt": 20000,
            "cost_of_goods_sold": 60000
        },
        "High Growth Company": {
            "revenue": 5000000,
            "net_income": 1000000,
            "total_assets": 2000000,
            "total_equity": 1500000,
            "current_assets": 1000000,
            "current_liabilities": 200000,
            "inventory": 200000,
            "total_debt": 500000,
            "cost_of_goods_sold": 2500000,
            "cash": 300000
        },
        "High Leverage Company": {
            "revenue": 1000000,
            "net_income": 100000,
            "total_assets": 1000000,
            "total_equity": 200000,
            "current_assets": 300000,
            "current_liabilities": 200000,
            "total_debt": 800000,
            "cost_of_goods_sold": 600000
        }
    }

    passed = 0
    failed = 0

    for test_name, test_data in test_cases.items():
        print(f"Running: {test_name}")
        result = test_skill_with_data(test_data)

        if result[0] if isinstance(result, tuple) else result:
            if isinstance(result, tuple):
                output = result[1]
                print(f"  ✓ PASSED")
                print(f"    - ROE: {output['profitability'].get('roe_percentage', 'N/A')}%")
                print(f"    - Current Ratio: {output['liquidity'].get('current_ratio', 'N/A')}")
                print(f"    - Debt-to-Equity: {output['leverage'].get('debt_to_equity_ratio', 'N/A')}")
            passed += 1
        else:
            print(f"  ✗ FAILED")
            failed += 1

        print()

    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total:  {passed + failed}")
    print()

    if failed == 0:
        print("✓ All tests passed! Ready to upload.")
        return 0
    else:
        print("✗ Some tests failed. Fix issues before uploading.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
