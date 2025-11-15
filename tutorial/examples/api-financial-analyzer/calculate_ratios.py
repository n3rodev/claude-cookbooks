# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
Financial Ratio Calculator - PEP 723 Compliant Skill

This module calculates comprehensive financial ratios from financial statement data.
It's designed to be uploaded as an API skill via the Claude Skills API.

PEP 723 Format: Metadata at the top allows this script to be executed directly
and also parsed by tools that understand the PEP 723 inline script metadata format.
"""

import json
import sys
from typing import Dict, Any


class FinancialRatioCalculator:
    """
    Comprehensive financial ratio calculator for analyzing company financial health.

    Attributes:
        data: Dictionary containing financial statement data
        ratios: Dictionary storing calculated ratios
        errors: List of validation errors or missing data warnings
    """

    def __init__(self, financial_data: Dict[str, float]):
        """
        Initialize the calculator with financial data.

        Args:
            financial_data: Dictionary with keys like 'revenue', 'net_income', etc.
        """
        self.data = financial_data
        self.ratios = {}
        self.errors = []
        self._validate_data()

    def _validate_data(self) -> None:
        """Validate that required fields are present and valid."""
        required_fields = ['net_income', 'total_equity', 'total_assets']
        for field in required_fields:
            if field not in self.data or self.data[field] is None:
                self.errors.append(f"Missing required field: {field}")

        # Check for negative values in inappropriate fields
        for field, value in self.data.items():
            if value is not None and value < 0 and 'liabilities' not in field:
                self.errors.append(f"Negative value for {field}: {value}")

    def calculate_profitability_ratios(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate profitability ratios: ROE and ROA.

        Returns:
            Dictionary with profitability metrics and interpretations
        """
        profitability = {}

        # Return on Equity (ROE)
        if 'total_equity' in self.data and self.data['total_equity'] != 0:
            roe = self.data.get('net_income', 0) / self.data['total_equity']
            profitability['roe'] = round(roe, 4)
            profitability['roe_percentage'] = round(roe * 100, 2)
            profitability['roe_interpretation'] = self._interpret_roe(roe)
        else:
            profitability['roe_error'] = "Cannot calculate ROE: missing or zero total equity"

        # Return on Assets (ROA)
        if 'total_assets' in self.data and self.data['total_assets'] != 0:
            roa = self.data.get('net_income', 0) / self.data['total_assets']
            profitability['roa'] = round(roa, 4)
            profitability['roa_percentage'] = round(roa * 100, 2)
            profitability['roa_interpretation'] = self._interpret_roa(roa)
        else:
            profitability['roa_error'] = "Cannot calculate ROA: missing or zero total assets"

        # Profit Margin (if revenue available)
        if 'revenue' in self.data and self.data['revenue'] != 0:
            net_margin = self.data.get('net_income', 0) / self.data['revenue']
            profitability['net_profit_margin'] = round(net_margin, 4)
            profitability['net_profit_margin_percentage'] = round(net_margin * 100, 2)

        return profitability

    def calculate_liquidity_ratios(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate liquidity ratios: Current, Quick, and Cash ratios.

        Returns:
            Dictionary with liquidity metrics and interpretations
        """
        liquidity = {}

        # Current Ratio
        if 'current_assets' in self.data and 'current_liabilities' in self.data:
            if self.data.get('current_liabilities', 0) != 0:
                current_ratio = self.data['current_assets'] / self.data['current_liabilities']
                liquidity['current_ratio'] = round(current_ratio, 2)
                liquidity['current_ratio_interpretation'] = self._interpret_current_ratio(current_ratio)

        # Quick Ratio (Current Assets - Inventory) / Current Liabilities
        if 'current_assets' in self.data and 'current_liabilities' in self.data:
            if self.data.get('current_liabilities', 0) != 0:
                inventory = self.data.get('inventory', 0)
                quick_assets = self.data['current_assets'] - inventory
                quick_ratio = quick_assets / self.data['current_liabilities']
                liquidity['quick_ratio'] = round(quick_ratio, 2)
                liquidity['quick_ratio_interpretation'] = self._interpret_quick_ratio(quick_ratio)

        # Cash Ratio (Cash + Equivalents) / Current Liabilities
        if 'cash' in self.data and 'current_liabilities' in self.data:
            if self.data.get('current_liabilities', 0) != 0:
                cash_ratio = self.data['cash'] / self.data['current_liabilities']
                liquidity['cash_ratio'] = round(cash_ratio, 2)
                liquidity['cash_ratio_interpretation'] = self._interpret_cash_ratio(cash_ratio)

        return liquidity

    def calculate_leverage_ratios(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate leverage ratios: Debt-to-Equity and Debt-to-Assets.

        Returns:
            Dictionary with leverage metrics and interpretations
        """
        leverage = {}

        # Debt-to-Equity Ratio
        if 'total_debt' in self.data and 'total_equity' in self.data:
            if self.data.get('total_equity', 0) != 0:
                d_to_e = self.data['total_debt'] / self.data['total_equity']
                leverage['debt_to_equity_ratio'] = round(d_to_e, 2)
                leverage['debt_to_equity_interpretation'] = self._interpret_debt_to_equity(d_to_e)

        # Debt-to-Assets Ratio
        if 'total_debt' in self.data and 'total_assets' in self.data:
            if self.data.get('total_assets', 0) != 0:
                d_to_a = self.data['total_debt'] / self.data['total_assets']
                leverage['debt_to_assets_ratio'] = round(d_to_a, 2)
                leverage['debt_to_assets_interpretation'] = self._interpret_debt_to_assets(d_to_a)

        # Equity Ratio (inverse of debt-to-assets)
        if 'total_equity' in self.data and 'total_assets' in self.data:
            if self.data.get('total_assets', 0) != 0:
                equity_ratio = self.data['total_equity'] / self.data['total_assets']
                leverage['equity_ratio'] = round(equity_ratio, 2)

        return leverage

    def calculate_efficiency_ratios(self) -> Dict[str, Dict[str, Any]]:
        """
        Calculate efficiency ratios: Asset Turnover and Inventory Turnover.

        Returns:
            Dictionary with efficiency metrics and interpretations
        """
        efficiency = {}

        # Asset Turnover Ratio
        if 'revenue' in self.data and 'total_assets' in self.data:
            if self.data.get('total_assets', 0) != 0:
                asset_turnover = self.data['revenue'] / self.data['total_assets']
                efficiency['asset_turnover'] = round(asset_turnover, 2)
                efficiency['asset_turnover_interpretation'] = self._interpret_asset_turnover(asset_turnover)

        # Inventory Turnover Ratio
        if 'cost_of_goods_sold' in self.data and 'inventory' in self.data:
            if self.data.get('inventory', 0) != 0:
                inventory_turnover = self.data['cost_of_goods_sold'] / self.data['inventory']
                efficiency['inventory_turnover'] = round(inventory_turnover, 2)
                efficiency['inventory_turnover_interpretation'] = self._interpret_inventory_turnover(inventory_turnover)

        return efficiency

    def calculate_all_ratios(self) -> Dict[str, Any]:
        """
        Calculate all available financial ratios and compile a comprehensive report.

        Returns:
            Comprehensive dictionary with all calculated ratios and interpretations
        """
        profitability = self.calculate_profitability_ratios()
        liquidity = self.calculate_liquidity_ratios()
        leverage = self.calculate_leverage_ratios()
        efficiency = self.calculate_efficiency_ratios()

        return {
            'profitability': profitability,
            'liquidity': liquidity,
            'leverage': leverage,
            'efficiency': efficiency,
            'validation_errors': self.errors if self.errors else None,
            'summary': self._generate_summary(profitability, liquidity, leverage)
        }

    def _interpret_roe(self, roe: float) -> str:
        """Interpret Return on Equity value."""
        if roe < 0.05:
            return "Poor - Below 5% indicates weak profitability"
        elif roe < 0.10:
            return "Fair - 5-10% is below average performance"
        elif roe < 0.15:
            return "Good - 10-15% is healthy return on equity"
        elif roe < 0.20:
            return "Very Good - 15-20% indicates strong performance"
        else:
            return "Excellent - Above 20% is outstanding return on equity"

    def _interpret_roa(self, roa: float) -> str:
        """Interpret Return on Assets value."""
        if roa < 0.02:
            return "Poor - Below 2% indicates inefficient asset use"
        elif roa < 0.05:
            return "Fair - 2-5% is average asset efficiency"
        elif roa < 0.10:
            return "Good - 5-10% indicates healthy asset efficiency"
        else:
            return "Excellent - Above 10% shows strong asset efficiency"

    def _interpret_current_ratio(self, ratio: float) -> str:
        """Interpret Current Ratio."""
        if ratio < 1.0:
            return "Weak - Below 1.0 indicates potential liquidity problems"
        elif ratio < 1.5:
            return "Fair - 1.0-1.5 indicates adequate short-term liquidity"
        elif ratio < 3.0:
            return "Good - 1.5-3.0 indicates healthy liquidity position"
        else:
            return "Excellent - Above 3.0 indicates very strong liquidity"

    def _interpret_quick_ratio(self, ratio: float) -> str:
        """Interpret Quick Ratio (more conservative liquidity measure)."""
        if ratio < 0.5:
            return "Weak - Below 0.5 indicates potential liquidity stress"
        elif ratio < 1.0:
            return "Fair - 0.5-1.0 indicates adequate immediate liquidity"
        else:
            return "Good - Above 1.0 indicates strong immediate liquidity"

    def _interpret_cash_ratio(self, ratio: float) -> str:
        """Interpret Cash Ratio (most conservative liquidity measure)."""
        if ratio < 0.2:
            return "Low - Below 0.2 is typical for most companies"
        elif ratio < 0.5:
            return "Adequate - 0.2-0.5 indicates good cash reserves"
        else:
            return "Strong - Above 0.5 indicates excellent cash position"

    def _interpret_debt_to_equity(self, ratio: float) -> str:
        """Interpret Debt-to-Equity Ratio."""
        if ratio < 0.5:
            return "Conservative - Low leverage with good equity cushion"
        elif ratio < 1.0:
            return "Moderate - Balanced capital structure"
        elif ratio < 2.0:
            return "Elevated - Higher leverage requires monitoring"
        else:
            return "High - Significant financial risk from high leverage"

    def _interpret_debt_to_assets(self, ratio: float) -> str:
        """Interpret Debt-to-Assets Ratio."""
        if ratio < 0.3:
            return "Conservative - Low proportion of debt financing"
        elif ratio < 0.5:
            return "Moderate - Reasonable debt level"
        elif ratio < 0.7:
            return "Elevated - Higher proportion financed by debt"
        else:
            return "High - Majority of assets financed by debt"

    def _interpret_asset_turnover(self, ratio: float) -> str:
        """Interpret Asset Turnover Ratio."""
        if ratio < 0.5:
            return "Low - Assets are underutilized; consider optimization"
        elif ratio < 1.0:
            return "Moderate - Reasonable asset efficiency"
        elif ratio < 2.0:
            return "Good - Efficient use of assets to generate revenue"
        else:
            return "Excellent - Very efficient asset utilization"

    def _interpret_inventory_turnover(self, ratio: float) -> str:
        """Interpret Inventory Turnover Ratio."""
        if ratio < 2:
            return "Low - Slow inventory movement; consider clearance"
        elif ratio < 5:
            return "Moderate - Reasonable inventory turnover"
        elif ratio < 10:
            return "Good - Healthy inventory management"
        else:
            return "Excellent - Very efficient inventory turnover"

    def _generate_summary(self, profitability: Dict[str, Any], liquidity: Dict[str, Any],
                          leverage: Dict[str, Any]) -> str:
        """
        Generate a one-line summary of overall financial health.

        Args:
            profitability: Calculated profitability ratios
            liquidity: Calculated liquidity ratios
            leverage: Calculated leverage ratios

        Returns:
            Summary string describing overall financial health
        """
        if self.errors:
            return "Analysis incomplete due to missing data"

        roe_health = 'strong' if profitability.get('roe', 0) > 0.10 else 'moderate'
        liquidity_health = 'strong' if liquidity.get('current_ratio', 0) > 1.5 else 'weak'
        leverage_health = 'strong' if leverage.get('debt_to_equity_ratio', 0) < 1.0 else 'elevated'

        return f"Overall financial health: {roe_health} profitability, {liquidity_health} liquidity, {leverage_health} leverage"


def parse_financial_data(input_data: str) -> Dict[str, float]:
    """
    Parse financial data from various formats.

    Args:
        input_data: JSON string or raw text with financial data

    Returns:
        Dictionary with parsed financial data
    """
    try:
        return json.loads(input_data)
    except json.JSONDecodeError:
        # If not valid JSON, attempt to extract numbers from text
        import re
        data = {}
        lines = input_data.split('\n')
        for line in lines:
            # Look for patterns like "key: value" or "key = value"
            match = re.search(r'(\w+)[:\s=]+(\d+\.?\d*)', line)
            if match:
                key = match.group(1).lower().replace(' ', '_')
                data[key] = float(match.group(2))
        return data


def main():
    """Main entry point for the skill."""
    if len(sys.argv) > 1:
        input_data = sys.argv[1]
    else:
        input_data = sys.stdin.read()

    try:
        financial_data = parse_financial_data(input_data)
        calculator = FinancialRatioCalculator(financial_data)
        results = calculator.calculate_all_ratios()

        print(json.dumps(results, indent=2))
        return 0
    except Exception as e:
        error_response = {
            'error': str(e),
            'message': 'Failed to calculate financial ratios',
            'input_received': input_data[:100] + ('...' if len(input_data) > 100 else '')
        }
        print(json.dumps(error_response, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
