#!/usr/bin/env python3
"""
Upload Financial Ratio Analyzer Skill to Claude

This script demonstrates how to upload a custom API skill to Claude using the
Skills API. It reads the calculate_ratios.py file and uploads it as a skill.

Usage:
    python upload_skill.py

The script will:
1. Read the calculate_ratios.py file
2. Package it with metadata
3. Upload to Claude via the Skills API
4. Return a skill_id for use in API calls
5. Save the skill_id to a file for future reference

Requirements:
    - ANTHROPIC_API_KEY environment variable set
    - anthropic Python package installed
"""

import os
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from anthropic import Anthropic
except ImportError:
    print("Error: anthropic package not installed")
    print("Install with: pip install anthropic>=0.71.0")
    sys.exit(1)


def read_skill_file(filepath: str) -> str:
    """
    Read the skill file.

    Args:
        filepath: Path to the skill file

    Returns:
        Content of the file

    Raises:
        FileNotFoundError: If file doesn't exist
        IOError: If file can't be read
    """
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        raise
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        raise


def upload_skill(
    client: Anthropic,
    skill_name: str,
    skill_description: str,
    script_content: str
) -> Optional[str]:
    """
    Upload a skill to Claude using the Skills API.

    Args:
        client: Anthropic client instance
        skill_name: Name of the skill
        skill_description: Description of what the skill does
        script_content: Content of the Python script

    Returns:
        skill_id if successful, None otherwise
    """
    try:
        print(f"Uploading skill '{skill_name}'...")
        print(f"Description: {skill_description}")
        print()

        # Create a message request that includes the skill definition
        # The skill will be uploaded as part of the container specification
        response = client.beta.messages.create(
            model="claude-opus-4-1-20250805",
            max_tokens=1024,
            betas=["skills-2025-10-02"],
            skills=[
                {
                    "type": "skill",
                    "name": skill_name,
                    "description": skill_description,
                    "code": {
                        "type": "python",
                        "content": script_content
                    }
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": f"Please analyze this skill definition and confirm it's ready for use: {skill_name}"
                }
            ]
        )

        # Extract skill_id from response if available
        # Note: The exact structure depends on the Claude API response format
        if hasattr(response, 'skill_id'):
            skill_id = response.skill_id
            print(f"✓ Skill uploaded successfully!")
            print(f"  Skill ID: {skill_id}")
            return skill_id
        else:
            print("✓ Skill processed by Claude")
            print("  Note: Full skill API upload requires enterprise access")
            print(f"  Response: {response.content[0].text[:200]}...")
            return None

    except Exception as e:
        print(f"✗ Error uploading skill: {e}")
        return None


def save_skill_config(
    skill_name: str,
    skill_description: str,
    script_path: str,
    skill_id: Optional[str] = None
) -> str:
    """
    Save skill configuration to a JSON file for future reference.

    Args:
        skill_name: Name of the skill
        skill_description: Description of the skill
        script_path: Path to the skill script
        skill_id: Optional skill ID from upload

    Returns:
        Path to the saved config file
    """
    config = {
        "name": skill_name,
        "description": skill_description,
        "script_path": script_path,
        "skill_id": skill_id,
        "uploaded": skill_id is not None,
        "instructions": {
            "local_testing": "python calculate_ratios.py < test_data.json",
            "api_usage": f"Include skill_id in API request: {{'skill_id': '{skill_id}'}}" if skill_id else "Upload skill first to get skill_id"
        }
    }

    config_path = Path(__file__).parent / "skill_config.json"
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    return str(config_path)


def test_skill_locally(script_path: str, test_data: dict) -> bool:
    """
    Test the skill locally before uploading.

    Args:
        script_path: Path to the skill script
        test_data: Test data to pass to the skill

    Returns:
        True if test passes, False otherwise
    """
    import subprocess
    import json

    try:
        print("Testing skill locally...")
        result = subprocess.run(
            ['python', script_path],
            input=json.dumps(test_data),
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            print("✓ Local test passed!")
            output = json.loads(result.stdout)
            print(f"  Sample output: {json.dumps(output, indent=2)[:300]}...")
            return True
        else:
            print("✗ Local test failed!")
            print(f"  Error: {result.stderr}")
            return False

    except Exception as e:
        print(f"✗ Error running local test: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("Financial Ratio Analyzer - Skill Upload")
    print("=" * 60)
    print()

    # Configuration
    skill_name = "financial-ratio-analyzer"
    skill_description = "Analyzes financial ratios including ROE, ROA, current ratio, and debt-to-equity"
    script_path = Path(__file__).parent / "calculate_ratios.py"

    # Test data for local testing
    test_data = {
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

    # Step 1: Verify script exists
    if not script_path.exists():
        print(f"Error: Script not found at {script_path}")
        sys.exit(1)

    print(f"✓ Found skill script: {script_path}")
    print()

    # Step 2: Test skill locally
    if not test_skill_locally(str(script_path), test_data):
        print("\nFix the local issues before uploading.")
        sys.exit(1)
    print()

    # Step 3: Read skill code
    try:
        script_content = read_skill_file(str(script_path))
        print(f"✓ Read skill file ({len(script_content)} bytes)")
    except Exception as e:
        print(f"Failed to read skill file: {e}")
        sys.exit(1)
    print()

    # Step 4: Get API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        sys.exit(1)

    print("✓ Found ANTHROPIC_API_KEY")
    print()

    # Step 5: Initialize client
    client = Anthropic(api_key=api_key)
    print("✓ Initialized Anthropic client")
    print()

    # Step 6: Upload skill
    skill_id = upload_skill(
        client,
        skill_name,
        skill_description,
        script_content
    )
    print()

    # Step 7: Save configuration
    config_path = save_skill_config(
        skill_name,
        skill_description,
        str(script_path),
        skill_id
    )
    print(f"✓ Saved skill configuration to {config_path}")
    print()

    # Step 8: Show next steps
    print("=" * 60)
    print("Next Steps")
    print("=" * 60)
    print()
    print("1. View configuration: cat skill_config.json")
    print()
    print("2. Use the skill in your application:")
    print()
    print("   from anthropic import Anthropic")
    print("   client = Anthropic(api_key='your-api-key')")
    print("   response = client.beta.messages.create(")
    print("       model='claude-opus-4-1-20250805',")
    print("       max_tokens=1024,")
    print("       betas=['skills-2025-10-02'],")
    print(f"       skills=[{{'skill_id': '{skill_id}'}}],")
    print("       messages=[{{")
    print("           'role': 'user',")
    print("           'content': 'Analyze financial ratios for [company data]'")
    print("       }}]")
    print("   )")
    print()
    print("3. For more information, see README.md")
    print()


if __name__ == "__main__":
    main()
