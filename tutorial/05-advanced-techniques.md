# Advanced Techniques for Claude Code Skills

This guide covers sophisticated patterns and best practices for building production-quality Claude Code skills. We'll explore architecture patterns, optimization strategies, and advanced workflows using real examples from the Claude Cookbooks repository.

## Table of Contents

1. [Multi-File Skills Architecture](#1-multi-file-skills-architecture)
2. [Progressive Disclosure Strategies](#2-progressive-disclosure-strategies)
3. [Script Integration Patterns](#3-script-integration-patterns)
4. [Testing Strategies](#4-testing-strategies)
5. [Debugging Techniques](#5-debugging-techniques)
6. [Deployment Workflows](#6-deployment-workflows)
7. [Skill Composition](#7-skill-composition)
8. [Performance Optimization](#8-performance-optimization)
9. [Security Hardening](#9-security-hardening)
10. [Advanced Examples](#10-advanced-examples)

---

## 1. Multi-File Skills Architecture

### When to Use Multi-File Skills

**Single File (SKILL.md only):**
- Simple instructions under 500 words
- Pure LLM reasoning tasks (no scripts)
- Self-contained knowledge
- Example: Math formula calculator, writing style guide

**Multi-File Structure:**
- Complex workflows requiring reference materials
- Scripts for automation or validation
- Large reference data (style guides, glossaries)
- Team skills needing documentation
- Example: Code review skill, document generation

### Architecture Patterns

#### Pattern 1: Core + Reference

**Use when**: You have comprehensive reference material that's only sometimes needed

```
skill-name/
├── SKILL.md              # Core instructions (always loaded when activated)
├── style_guide.md        # Reference material (loaded on-demand)
└── glossary.md          # Additional reference (loaded on-demand)
```

**Example - cookbook-audit skill**:
```markdown
<!-- SKILL.md -->
---
name: cookbook-audit
description: Audit an Anthropic Cookbook notebook based on a rubric.
---

# Cookbook Audit

## Instructions
Review the requested Cookbook notebook using the guidelines and
rubrics in `style_guide.md`.

**IMPORTANT**: Always read `style_guide.md` first before conducting
an audit. The style guide contains canonical templates and examples.

## Workflow
1. **Read the style guide**: First review `style_guide.md`
2. **Run automated checks**: Use `python3 validate_notebook.py <path>`
3. **Manual review**: Evaluate against rubric
4. **Generate report**: Follow audit report format
```

**Benefits**:
- Keeps SKILL.md concise (reduces base context usage)
- Claude loads style_guide.md only when needed
- Easy to update reference materials independently

#### Pattern 2: Core + Script + Template

**Use when**: Automation + structured output required

```
skill-name/
├── SKILL.md              # Instructions
├── validate.py           # Automation script
├── template.md           # Output template
└── .gitignore           # Ignore tmp/ directory
```

**Example Structure**:
```markdown
<!-- SKILL.md -->
## Workflow
1. Run validation: `python3 validate.py <input>`
2. Review automated findings
3. Perform manual checks
4. Generate report using `template.md`
```

#### Pattern 3: Modular Architecture

**Use when**: Complex skills with multiple sub-capabilities

```
skill-name/
├── SKILL.md              # Main instructions + orchestration
├── reference/
│   ├── style-guide.md    # Writing standards
│   ├── api-spec.md       # Technical reference
│   └── examples.md       # Code examples
├── scripts/
│   ├── validate.py       # Validation
│   ├── format.py         # Formatting
│   └── utils.py          # Shared utilities
├── templates/
│   └── report.md         # Output templates
└── tmp/                  # Temporary files (gitignored)
```

**SKILL.md Orchestration Pattern**:
```markdown
## Instructions

This skill provides code review capabilities across multiple dimensions.

### Workflow

1. **Automated Validation**
   - Run `python3 scripts/validate.py <file>` for technical checks
   - Review output for syntax errors, security issues, deprecated patterns

2. **Style Review**
   - Reference `reference/style-guide.md` for team standards
   - Check formatting, naming conventions, documentation

3. **Architecture Review**
   - Use `reference/api-spec.md` to verify API usage
   - Consult `reference/examples.md` for best practices

4. **Report Generation**
   - Follow structure in `templates/report.md`
   - Include specific line references and examples
```

### Directory Organization Best Practices

**Naming Conventions**:
- Skill directory: `lowercase-with-hyphens`
- Core file: Always `SKILL.md` (case-sensitive)
- Scripts: `lowercase_with_underscores.py`
- Reference: `descriptive-name.md`

**What to Include**:
- ✅ SKILL.md (required)
- ✅ Scripts with clear purposes
- ✅ Reference materials frequently needed
- ✅ Templates for structured output
- ✅ .gitignore to exclude tmp/ and cache/

**What to Exclude**:
- ❌ Binary files or large datasets (use URLs instead)
- ❌ Redundant documentation (link to official docs)
- ❌ Environment-specific configurations
- ❌ Temporary or generated files

---

## 2. Progressive Disclosure Strategies

Progressive disclosure minimizes context window usage by loading information only when needed.

### Three-Tier Loading Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ TIER 1: Metadata (Startup)                                 │
│ - Loaded: Always (for all skills)                          │
│ - Size: ~50-100 tokens                                      │
│ - Contents: name + description from YAML frontmatter       │
│ - Purpose: Activation decision                             │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ TIER 2: Core Instructions (Activation)                     │
│ - Loaded: When description matches user request            │
│ - Size: 500-2000 tokens (keep concise!)                    │
│ - Contents: SKILL.md main instructions                     │
│ - Purpose: Execute core skill logic                        │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ TIER 3: Supporting Files (On-Demand)                       │
│ - Loaded: Only when explicitly referenced                  │
│ - Size: Variable (can be large)                            │
│ - Contents: style_guide.md, templates, etc.                │
│ - Purpose: Detailed reference and automation               │
└─────────────────────────────────────────────────────────────┘
```

### Lazy Loading Patterns

#### Pattern 1: Explicit References

**SKILL.md instructs Claude when to load supporting files**:

```markdown
## Instructions

When user requests code review:

1. **First, load the style guide**: Read `style_guide.md` for current standards
2. Then review the code against those standards
3. Generate report using examples from style guide
```

**Why this works**:
- Claude only loads style_guide.md when activated
- Clear directive ensures consistency
- Prevents unnecessary context usage when skill not needed

#### Pattern 2: Conditional Loading

**Load different files based on task type**:

```markdown
## Instructions

Determine the review type first:

- **Security Review**: Read `security-checklist.md` and run `security_scan.py`
- **Performance Review**: Read `performance-guide.md` and check against benchmarks
- **Style Review**: Read `style-guide.md` and verify formatting

Then proceed with review for that specific dimension.
```

#### Pattern 3: Staged Loading

**Load incrementally as needed**:

```markdown
## Instructions

### Phase 1: Quick Check
Run `python3 quick_validate.py <file>` for immediate issues.
If critical issues found, stop here and report.

### Phase 2: Detailed Review
If Phase 1 passes, read `detailed-guidelines.md` for comprehensive review.

### Phase 3: Advanced Analysis
If needed for complex cases, consult `advanced-patterns.md`.
```

### Context Budget Management

**Estimating Token Usage**:

```bash
# Quick estimation (rough approximation)
# 1 token ≈ 4 characters for English text

# Check file sizes
wc -c skill-name/*.md

# Example output:
#  2500 SKILL.md          (~625 tokens)
# 12000 style_guide.md    (~3000 tokens)
#  4000 examples.md       (~1000 tokens)
```

**Optimization Strategies**:

1. **Keep SKILL.md under 2000 tokens** (8000 characters)
   - Use bullet points instead of paragraphs
   - Link to external docs instead of duplicating
   - Move examples to separate files

2. **Use code instead of prose** for complex logic
   ```markdown
   <!-- Instead of explaining complex regex in prose -->
   Run `python3 extract_data.py` which handles:
   - Email extraction with validation
   - URL normalization
   - Special character escaping
   ```

3. **Leverage Claude's knowledge**
   ```markdown
   <!-- Don't include -->
   Python follows PEP 8 style guide. Variables should be snake_case...

   <!-- Instead -->
   Follow PEP 8 conventions. Check against official guide if unsure.
   ```

---

## 3. Script Integration Patterns

Scripts extend skills with automation, validation, and complex operations.

### PEP 723 Inline Dependencies

**PEP 723** allows declaring dependencies directly in Python scripts, enabling self-contained executables.

#### Basic PEP 723 Script

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "anthropic>=0.71.0",
#     "python-dotenv>=1.0.0",
# ]
# ///
"""
Script description here.

Usage:
    python script.py <arguments>
"""
import sys
from anthropic import Anthropic
from dotenv import load_dotenv

def main():
    # Your code here
    pass

if __name__ == "__main__":
    main()
```

**Running with uv**:
```bash
# uv automatically installs dependencies in isolated environment
uv run script.py arguments
```

#### Production Example: validate_notebook.py

From the **cookbook-audit skill**:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "nbconvert",
# ]
# ///
"""
Automated validation checks for Anthropic Cookbook notebooks.

Usage:
    python validate_notebook.py <notebook.ipynb>

Exit codes:
    0 - No issues found
    1 - Critical issues found (must fix)
"""
import json
import sys
from pathlib import Path

class NotebookValidator:
    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        self.issues: list[str] = []
        self.warnings: list[str] = []

        # Load and parse notebook
        with open(self.notebook_path) as f:
            self.nb = json.load(f)

    def check_hardcoded_secrets(self):
        """Check for API keys in code."""
        # Implementation here
        pass

    def run_all_checks(self):
        """Run all validation checks."""
        self.check_hardcoded_secrets()
        # Other checks...

    def get_exit_code(self) -> int:
        """Return 0 for success, 1 for failures."""
        return 1 if self.issues else 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_notebook.py <notebook.ipynb>")
        sys.exit(1)

    validator = NotebookValidator(sys.argv[1])
    validator.run_all_checks()
    sys.exit(validator.get_exit_code())

if __name__ == "__main__":
    main()
```

**Integration in SKILL.md**:
```markdown
## Workflow

1. **Run automated checks**:
   ```bash
   python3 validate_notebook.py path/to/notebook.ipynb
   ```
2. **Review findings**: Script outputs issues and warnings
3. **Manual review**: Check aspects scripts can't validate
```

### Error Handling Patterns

#### Pattern 1: Graceful Degradation

**Handle missing tools gracefully**:

```python
def check_with_external_tool(self):
    """Use external tool if available, fallback otherwise."""
    try:
        # Try using external tool
        result = subprocess.run(
            ["external-tool", "check"],
            capture_output=True,
            text=True,
            check=True
        )
        self._parse_tool_output(result.stdout)

    except FileNotFoundError:
        # Tool not installed - use fallback
        self.warnings.append(
            "external-tool not found - using basic checks. "
            "Install with: pip install external-tool"
        )
        self._fallback_check()

    except subprocess.CalledProcessError as e:
        # Tool failed - report but continue
        self.warnings.append(f"external-tool error: {e}")
        self._fallback_check()
```

**From cookbook-audit's validate_notebook.py**:
```python
def check_hardcoded_secrets(self):
    """Check for secrets using detect-secrets."""
    try:
        # Try using detect-secrets
        result = subprocess.run(["detect-secrets", "scan"], ...)
        # Process results

    except FileNotFoundError:
        # Fallback to basic pattern matching
        self.warnings.append(
            "detect-secrets not found - using basic detection"
        )
        self._check_hardcoded_secrets_fallback()
```

#### Pattern 2: Informative Exit Codes

**Use standard exit codes**:

```python
# Exit codes
SUCCESS = 0
GENERAL_ERROR = 1
INVALID_INPUT = 2
MISSING_DEPENDENCY = 3

def main():
    try:
        # Validate input
        if not validate_input(sys.argv):
            print("Error: Invalid input format", file=sys.stderr)
            sys.exit(INVALID_INPUT)

        # Run checks
        result = run_checks()

        # Return appropriate code
        sys.exit(SUCCESS if result.ok else GENERAL_ERROR)

    except ImportError as e:
        print(f"Missing dependency: {e}", file=sys.stderr)
        sys.exit(MISSING_DEPENDENCY)
```

**In SKILL.md**:
```markdown
## Script Exit Codes

- `0`: Success, no issues found
- `1`: Issues found, see output for details
- `2`: Invalid input provided
- `3`: Missing required dependency
```

#### Pattern 3: Structured Output

**Machine-readable + human-readable**:

```python
import json
from dataclasses import dataclass, asdict

@dataclass
class ValidationResult:
    file_path: str
    issues: list[str]
    warnings: list[str]
    passed: bool

def print_results(result: ValidationResult, format: str = "human"):
    """Print results in specified format."""
    if format == "json":
        print(json.dumps(asdict(result), indent=2))

    elif format == "human":
        print(f"\n{'='*60}")
        print(f"Validation: {result.file_path}")
        print(f"{'='*60}\n")

        if result.issues:
            print("ISSUES:")
            for issue in result.issues:
                print(f"  ❌ {issue}")

        if result.warnings:
            print("\nWARNINGS:")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")

        status = "✅ PASSED" if result.passed else "❌ FAILED"
        print(f"\n{status}")
```

### Integration Best Practices

**1. Clear Usage Documentation**:

```python
"""
Script description and purpose.

Usage:
    python script.py <input> [options]

    Options:
        --format json    Output as JSON
        --verbose        Show detailed logs

Examples:
    python script.py file.ipynb
    python script.py file.ipynb --format json

Exit Codes:
    0 - Success
    1 - Validation failed
    2 - Invalid arguments
"""
```

**2. Progress Feedback**:

```python
def process_large_file(file_path: Path):
    """Process file with progress updates."""
    print(f"Processing {file_path}...")

    # Long-running operation
    print("  → Analyzing structure...")
    analyze_structure()

    print("  → Checking content...")
    check_content()

    print("  → Running validation...")
    validate()

    print("✓ Complete!")
```

**3. Helpful Error Messages**:

```python
try:
    data = parse_input(file_path)
except json.JSONDecodeError as e:
    print(
        f"Error: {file_path} is not valid JSON\n"
        f"  Line {e.lineno}, Column {e.colno}\n"
        f"  {e.msg}",
        file=sys.stderr
    )
    sys.exit(1)
```

---

## 4. Testing Strategies

### Unit Testing Scripts

**Test Structure**:

```
skill-name/
├── SKILL.md
├── validate.py
└── tests/
    ├── __init__.py
    ├── test_validate.py
    ├── fixtures/
    │   ├── valid_notebook.ipynb
    │   └── invalid_notebook.ipynb
    └── conftest.py
```

**Example Unit Test**:

```python
# tests/test_validate.py
import pytest
from pathlib import Path
from validate import NotebookValidator

class TestNotebookValidator:

    @pytest.fixture
    def valid_notebook(self):
        """Path to valid test notebook."""
        return Path(__file__).parent / "fixtures" / "valid_notebook.ipynb"

    @pytest.fixture
    def invalid_notebook(self):
        """Path to invalid test notebook."""
        return Path(__file__).parent / "fixtures" / "invalid_notebook.ipynb"

    def test_valid_notebook_passes(self, valid_notebook):
        """Valid notebooks should pass validation."""
        validator = NotebookValidator(str(valid_notebook))
        validator.run_all_checks()

        assert len(validator.issues) == 0
        assert validator.get_exit_code() == 0

    def test_hardcoded_secrets_detected(self, invalid_notebook):
        """Notebooks with secrets should fail."""
        validator = NotebookValidator(str(invalid_notebook))
        validator.check_hardcoded_secrets()

        assert len(validator.issues) > 0
        assert any("secret" in issue.lower() for issue in validator.issues)

    def test_missing_file_raises_error(self):
        """Missing files should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            NotebookValidator("nonexistent.ipynb")
```

**Running Tests**:

```bash
# Using pytest
uv run --with pytest pytest tests/

# With coverage
uv run --with pytest --with pytest-cov \
    pytest tests/ --cov=validate --cov-report=html
```

### Integration Testing Skills

**Test Complete Skill Workflow**:

```python
# tests/test_skill_integration.py
import subprocess
from pathlib import Path

def test_skill_end_to_end(tmp_path):
    """Test complete skill workflow."""

    # 1. Create test input
    test_file = tmp_path / "test.ipynb"
    test_file.write_text('{"cells": []}')

    # 2. Run script as skill would
    result = subprocess.run(
        ["python3", "validate.py", str(test_file)],
        capture_output=True,
        text=True
    )

    # 3. Verify output
    assert result.returncode == 0
    assert "validation" in result.stdout.lower()
```

### Activation Testing

**Verify Skill Activates Correctly**:

Create a test script that simulates user requests:

```python
# tests/test_activation.py
"""
Test that skill activates on appropriate user requests.

Note: These are manual tests - run with Claude Code CLI
"""

activation_tests = [
    {
        "name": "Direct request",
        "query": "Can you audit this notebook for me?",
        "should_activate": True,
    },
    {
        "name": "Implicit request",
        "query": "Is this notebook following best practices?",
        "should_activate": True,
    },
    {
        "name": "Unrelated request",
        "query": "What's the weather like?",
        "should_activate": False,
    },
]

def print_activation_tests():
    """Print test cases for manual verification."""
    print("Activation Test Cases")
    print("=" * 60)
    print("\nTest these queries with Claude Code and verify activation:\n")

    for i, test in enumerate(activation_tests, 1):
        should = "SHOULD" if test["should_activate"] else "SHOULD NOT"
        print(f"{i}. {test['name']}")
        print(f"   Query: \"{test['query']}\"")
        print(f"   Expected: {should} activate skill")
        print()

if __name__ == "__main__":
    print_activation_tests()
```

**Run and verify manually**:

```bash
python tests/test_activation.py

# Then test each query with Claude Code:
claude
> "Can you audit this notebook for me?"
# Check if skill activates in debug output
```

### Description Quality Testing

**Test Description Effectiveness**:

```markdown
<!-- tests/description_tests.md -->

# Skill Description Testing

## Current Description
"Audit an Anthropic Cookbook notebook based on a rubric. Use whenever
a notebook review or audit is requested."

## Test Cases

### Should Activate

- [x] "Can you review this notebook?"
- [x] "Audit this cookbook for quality"
- [x] "Is this notebook up to standards?"
- [x] "Check this notebook against the rubric"

### Should Not Activate

- [x] "What's in this notebook?" (information request, not review)
- [x] "Run this notebook" (execution, not review)
- [x] "Create a new notebook" (creation, not audit)

## Refinement Notes

If skill activates incorrectly:
- Add negative examples to description: "...audit is requested (not for
  notebook creation or execution)"

If skill doesn't activate when it should:
- Add more trigger keywords: "review, audit, check quality, verify standards"
```

### Continuous Testing in CI

**GitHub Actions Workflow**:

```yaml
# .github/workflows/test-skills.yml
name: Test Skills

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v1

      - name: Run script tests
        working-directory: .claude/skills/cookbook-audit
        run: |
          uv run --with pytest pytest tests/

      - name: Validate skill structure
        run: |
          # Check SKILL.md exists
          test -f .claude/skills/cookbook-audit/SKILL.md

          # Check scripts are executable
          test -x .claude/skills/cookbook-audit/validate_notebook.py

      - name: Test script execution
        run: |
          # Test script with sample notebook
          uv run .claude/skills/cookbook-audit/validate_notebook.py \
            capabilities/classification/guide.ipynb
```

---

## 5. Debugging Techniques

### Debug Mode

**Enable Debug Logging**:

```bash
# Claude Code CLI
claude --debug

# You'll see:
[DEBUG] Loading skills from ~/.claude/skills/
[DEBUG] Found skill: cookbook-audit
[DEBUG] Loaded metadata: name=cookbook-audit, description=Audit...
[DEBUG] Skill activated: cookbook-audit
[DEBUG] Reading file: style_guide.md
```

### Logging in Scripts

**Structured Logging**:

```python
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('skill_debug.log'),
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

def validate_notebook(path: str):
    """Validate notebook with debug logging."""
    logger.info(f"Starting validation: {path}")

    try:
        logger.debug("Loading notebook file")
        with open(path) as f:
            data = json.load(f)

        logger.debug(f"Found {len(data.get('cells', []))} cells")

        # Validation logic
        issues = check_issues(data)

        logger.info(f"Validation complete: {len(issues)} issues found")
        return issues

    except Exception as e:
        logger.error(f"Validation failed: {e}", exc_info=True)
        raise
```

**Environment Variable Control**:

```python
import os

DEBUG = os.getenv("SKILL_DEBUG", "false").lower() == "true"

def debug_print(message: str):
    """Print debug message if debug mode enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}", file=sys.stderr)

# Usage
debug_print("Loading configuration...")
```

**Run with debug**:
```bash
SKILL_DEBUG=true python validate.py notebook.ipynb
```

### Troubleshooting Common Issues

#### Issue 1: Skill Not Discovered

**Symptoms**:
- Skill doesn't appear in Claude's skill list
- Not activating even with direct requests

**Debug Checklist**:

```bash
# 1. Verify file location
ls ~/.claude/skills/skill-name/SKILL.md
# or
ls .claude/skills/skill-name/SKILL.md

# 2. Check filename (case-sensitive!)
# Must be exactly: SKILL.md (not skill.md or Skill.md)

# 3. Validate YAML frontmatter
head -n 5 ~/.claude/skills/skill-name/SKILL.md
```

**Expected output**:
```yaml
---
name: skill-name
description: Clear description of what skill does
---
```

**Common Fixes**:
- Rename file to `SKILL.md` exactly
- Fix YAML syntax (use online validator)
- Ensure `name` uses only lowercase, numbers, hyphens
- Restart Claude Code to refresh skill cache

#### Issue 2: Skill Not Activating

**Symptoms**:
- Skill is discovered but doesn't activate
- Claude doesn't reference the skill

**Debug Steps**:

```markdown
<!-- Add temporary debug section to SKILL.md -->

## Debug Info

This skill should activate when user:
- Mentions "audit" or "review"
- Asks about notebook quality
- Requests rubric-based evaluation

Test activation with: "Can you audit this notebook?"
```

**Fixes**:
- Make description more specific with trigger keywords
- Add "Use when..." clause to description
- Include domain-specific terms users will actually say

**Before**:
```yaml
description: Notebook quality checker
```

**After**:
```yaml
description: Audit an Anthropic Cookbook notebook based on a rubric. Use whenever a notebook review or audit is requested.
```

#### Issue 3: Script Fails When Called

**Debug Script Execution**:

```python
# Add debug wrapper
def main():
    """Main entry point with debug info."""
    try:
        print(f"Script: {__file__}", file=sys.stderr)
        print(f"Args: {sys.argv}", file=sys.stderr)
        print(f"CWD: {os.getcwd()}", file=sys.stderr)
        print(f"Python: {sys.version}", file=sys.stderr)

        # Actual logic
        result = run_validation()
        sys.exit(result.exit_code)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

**Test Script Independently**:

```bash
# Run script directly (outside of skill)
cd ~/.claude/skills/skill-name/
python3 script.py test_input.txt

# Check dependencies
uv run --with dep1 --with dep2 script.py test_input.txt

# Verify PEP 723 header
head -n 10 script.py
```

#### Issue 4: High Context Usage

**Measure Context Usage**:

```bash
# Estimate token usage of skill files
wc -w ~/.claude/skills/skill-name/*.md

# Output shows word count (approximate tokens)
#   625 SKILL.md
#  3000 style_guide.md
#  1000 examples.md
```

**Optimization**:

1. **Split large files**:
   ```markdown
   <!-- Instead of one 5000-word SKILL.md -->

   <!-- SKILL.md (500 words) -->
   Main instructions. For detailed examples, see examples.md.

   <!-- examples.md (4500 words) -->
   Loaded only when examples needed
   ```

2. **Use external links**:
   ```markdown
   <!-- Instead of duplicating docs -->
   Follows PEP 8 style guide: https://pep8.org/

   <!-- Not this -->
   PEP 8 requires: [5 pages of style rules copied here]
   ```

3. **Compress instructions**:
   ```markdown
   <!-- Before (wordy) -->
   When the user asks you to review their code, you should first
   read through the code carefully. Then, you should check for
   any issues or problems. After that, you should provide feedback.

   <!-- After (concise) -->
   Review workflow:
   1. Read code
   2. Identify issues
   3. Provide feedback
   ```

### Interactive Debugging

**Add Debug Commands to SKILL.md**:

```markdown
## Debug Commands

When user says "debug skill":
1. Print loaded files: List all files currently loaded
2. Show configuration: Display YAML frontmatter values
3. Test activation: Confirm description matching logic
4. Measure context: Estimate total token usage
```

---

## 6. Deployment Workflows

### Personal vs. Project vs. API Skills

#### Personal Skills (`~/.claude/skills/`)

**Best for**:
- Individual productivity tools
- Personal preferences and workflows
- Experimental skills
- Learning and prototyping

**Setup**:
```bash
# Create personal skill
mkdir -p ~/.claude/skills/my-workflow
cat > ~/.claude/skills/my-workflow/SKILL.md << 'EOF'
---
name: my-workflow
description: Personal workflow automation
---

# My Workflow

[Your personal instructions]
EOF
```

**Advantages**:
- Immediately available across all projects
- Private to your machine
- Quick to create and modify
- No team coordination needed

**Limitations**:
- Not shared with team
- Not version controlled
- Machine-specific

#### Project Skills (`.claude/skills/`)

**Best for**:
- Team coding standards
- Project-specific workflows
- Shared best practices
- CI/CD integration

**Setup**:
```bash
# In your project repo
mkdir -p .claude/skills/code-review
cat > .claude/skills/code-review/SKILL.md << 'EOF'
---
name: code-review
description: Review code against team standards
---

# Code Review

[Team-shared instructions]
EOF

# Commit to version control
git add .claude/skills/
git commit -m "feat: add code review skill"
git push
```

**Team Onboarding**:
```bash
# New team member clones repo
git clone https://github.com/team/project.git
cd project

# Skills automatically available!
claude
> "Review this code"  # Skill auto-activates
```

**Advantages**:
- Version controlled with code
- Shared across team
- Evolves with project
- Works in CI/CD

**Best Practices**:
- Document skills in project README
- Include activation examples
- Keep skills project-specific
- Update with code changes

#### API Skills (Anthropic Platform)

**Best for**:
- Production applications
- Multi-tenant SaaS
- Centralized management
- Pre-built Anthropic skills (Excel, PowerPoint, PDF)

**Upload Skill via API**:
```python
import anthropic

client = anthropic.Anthropic()

# Create skill
skill = client.beta.skills.create(
    name="data-analyzer",
    instructions="""
    Analyze datasets and generate insights.

    ## Workflow
    1. Load data
    2. Compute statistics
    3. Generate visualizations
    4. Provide recommendations
    """,
    betas=["skills-2025-10-02"]
)

print(f"Skill ID: {skill.id}")
```

**Use in API Calls**:
```python
# Reference skill in message
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    skills=[skill.id],  # Activate this skill
    messages=[{
        "role": "user",
        "content": "Analyze this dataset: [data]"
    }],
    betas=["skills-2025-10-02"]
)
```

**Advantages**:
- Managed by Anthropic (versioning, isolation)
- Available via API globally
- Pre-built skills (Excel, etc.) ready to use
- Execution in isolated containers

**Limitations**:
- No local file system access
- No arbitrary package installation
- Requires API key and internet
- Usage billed through API

### CI/CD Integration

#### Pattern 1: Skill-Powered CI Checks

**Use skills in GitHub Actions**:

```yaml
# .github/workflows/code-review.yml
name: Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: |
          # Install Claude Code CLI
          curl -fsSL https://install.claude.com | sh

      - name: Review Changes
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Get changed files
          FILES=$(git diff --name-only origin/main...HEAD)

          # Run code review skill on each file
          for file in $FILES; do
            echo "Reviewing $file"
            claude --skill code-review "Review $file"
          done
```

#### Pattern 2: Slash Commands in CI

**Example from cookbook repository**:

```yaml
# .github/workflows/notebook-review.yml
name: Notebook Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Review Notebooks
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Get changed notebooks
          NOTEBOOKS=$(git diff --name-only origin/main...HEAD | grep '.ipynb$')

          # Run slash command (uses project skill)
          for nb in $NOTEBOOKS; do
            claude /notebook-review "$nb"
          done
```

**Slash command definition** (`.claude/commands/notebook-review.md`):
```markdown
---
description: Comprehensive review of Jupyter notebooks
---

Review the specified Jupyter notebooks using the cookbook-audit skill.

Provide a clear summary with:
- ✅ What looks good
- ⚠️ Suggestions for improvement
- ❌ Critical issues that must be fixed
```

#### Pattern 3: Automated Skill Testing

**Test skills before merging**:

```yaml
# .github/workflows/test-skills.yml
name: Test Skills

on: [pull_request]

jobs:
  test-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate Skill Structure
        run: |
          # Check all skills have required files
          for skill in .claude/skills/*/; do
            if [ ! -f "$skill/SKILL.md" ]; then
              echo "Error: $skill missing SKILL.md"
              exit 1
            fi
          done

      - name: Test Skill Scripts
        run: |
          # Run unit tests for skill scripts
          for skill in .claude/skills/*/; do
            if [ -d "$skill/tests" ]; then
              echo "Testing $skill"
              uv run --with pytest pytest "$skill/tests/"
            fi
          done

      - name: Validate YAML Frontmatter
        run: |
          # Check YAML syntax in all SKILL.md files
          uv run --with pyyaml python3 << 'EOF'
          import yaml
          from pathlib import Path

          for skill_md in Path(".claude/skills").glob("*/SKILL.md"):
              print(f"Validating {skill_md}")

              # Extract frontmatter
              content = skill_md.read_text()
              if content.startswith("---"):
                  parts = content.split("---", 2)
                  frontmatter = parts[1]

                  # Validate YAML
                  yaml.safe_load(frontmatter)

          print("✓ All YAML frontmatter valid")
          EOF
```

### Versioning and Updates

**Semantic Versioning for Skills**:

```markdown
<!-- SKILL.md -->
---
name: code-review
description: Review code against team standards (v2.1.0)
version: 2.1.0
---

# Code Review Skill

## Changelog

### v2.1.0 (2025-11-15)
- Added security scanning integration
- Improved performance check patterns

### v2.0.0 (2025-10-01)
- BREAKING: Changed output format to JSON
- Added TypeScript support

### v1.0.0 (2025-08-15)
- Initial release
```

**Version in Git Tags**:
```bash
# Tag skill versions
git tag skill/code-review/v2.1.0
git push origin skill/code-review/v2.1.0

# Team can pin to specific version
git checkout skill/code-review/v2.0.0
```

---

## 7. Skill Composition

### Combining Multiple Skills

Skills can reference and complement each other:

#### Pattern 1: Skill Chains

**Workflow across multiple skills**:

```markdown
<!-- .claude/skills/security-review/SKILL.md -->
---
name: security-review
description: Review code for security vulnerabilities
---

# Security Review

## Instructions

1. Run security checks
2. If issues found in code style, suggest running `code-review` skill
3. If issues found in dependencies, suggest running `dependency-audit` skill
```

**Usage**:
```
User: "Review this code for security issues"
Claude: [Activates security-review skill]
        "Found several security issues. I also notice some style
         inconsistencies - would you like me to run a code review as well?"
User: "Yes please"
Claude: [Activates code-review skill]
```

#### Pattern 2: Skill Orchestration

**Meta-skill that coordinates others**:

```markdown
<!-- .claude/skills/full-review/SKILL.md -->
---
name: full-review
description: Comprehensive code review including security, style, and performance
---

# Full Review

## Instructions

When user requests full review:

1. **Security**: Activate `security-review` skill
   - Review for vulnerabilities
   - Check dependency safety

2. **Code Quality**: Activate `code-review` skill
   - Verify style compliance
   - Check best practices

3. **Performance**: Activate `performance-audit` skill
   - Identify bottlenecks
   - Suggest optimizations

4. **Generate Report**: Combine findings from all skills
   - Prioritize critical issues
   - Group by category
   - Provide actionable recommendations
```

#### Pattern 3: Skill Dependencies

**Skills that build on each other**:

```markdown
<!-- .claude/skills/api-client/SKILL.md -->
---
name: api-client
description: Generate HTTP API client code
---

# API Client Generator

## Instructions

1. Generate client code based on OpenAPI spec
2. After generation, automatically run `code-review` skill to ensure quality
3. Run `security-review` to check for common API security issues
4. Suggest running `test-generator` skill to create tests for the client

## Output

Generated client will be reviewed and tested automatically.
```

### Cross-Skill Communication

**Share context between skills**:

```markdown
<!-- .claude/skills/data-loader/SKILL.md -->
---
name: data-loader
description: Load and validate datasets
---

# Data Loader

## Instructions

1. Load dataset from provided source
2. Validate schema and data types
3. **Save metadata** for other skills:
   - Dataset schema
   - Row count
   - Column names
   - Data types
4. Suggest running `data-analyzer` skill for analysis

## Output Format

Save findings in structured format for `data-analyzer`:
```json
{
  "schema": {...},
  "rows": 1000,
  "validated": true
}
```
```

```markdown
<!-- .claude/skills/data-analyzer/SKILL.md -->
---
name: data-analyzer
description: Analyze datasets and generate insights
---

# Data Analyzer

## Prerequisites

For best results, run `data-loader` skill first to validate data.

## Instructions

1. Check if data was loaded by `data-loader` skill
2. If yes, use the metadata to inform analysis
3. If no, load data first then analyze
```

### Skill Libraries

**Organize related skills**:

```
.claude/skills/
├── testing/
│   ├── test-generator/
│   │   └── SKILL.md
│   ├── test-runner/
│   │   └── SKILL.md
│   └── coverage-analyzer/
│       └── SKILL.md
├── review/
│   ├── code-review/
│   │   └── SKILL.md
│   ├── security-review/
│   │   └── SKILL.md
│   └── performance-review/
│       └── SKILL.md
└── documentation/
    ├── docstring-generator/
    │   └── SKILL.md
    └── readme-generator/
        └── SKILL.md
```

**Index skill for discovery**:

```markdown
<!-- .claude/skills/README.md -->

# Project Skills

## Testing Suite

- **test-generator**: Create unit tests from code
- **test-runner**: Execute tests and report results
- **coverage-analyzer**: Analyze test coverage

## Code Review

- **code-review**: Style and best practices
- **security-review**: Security vulnerabilities
- **performance-review**: Performance optimizations

## Documentation

- **docstring-generator**: Generate Python docstrings
- **readme-generator**: Create project documentation
```

---

## 8. Performance Optimization

### Measuring Token Usage

**Estimate Context Consumption**:

```python
#!/usr/bin/env python3
"""
Estimate token usage of a skill.

Usage:
    python measure_tokens.py ~/.claude/skills/skill-name
"""

import sys
from pathlib import Path

def estimate_tokens(text: str) -> int:
    """Rough estimation: 1 token ≈ 4 characters."""
    return len(text) // 4

def analyze_skill(skill_dir: Path):
    """Analyze token usage of all files in skill."""

    results = {}
    total = 0

    for file in skill_dir.glob("**/*.md"):
        if file.name.startswith('.'):
            continue

        text = file.read_text()
        tokens = estimate_tokens(text)

        results[file.name] = tokens
        total += tokens

    print(f"\nSkill: {skill_dir.name}")
    print("=" * 60)

    for filename, tokens in sorted(results.items(), key=lambda x: -x[1]):
        print(f"{filename:30} {tokens:6,} tokens")

    print("-" * 60)
    print(f"{'TOTAL':30} {total:6,} tokens")
    print("=" * 60)

    # Recommendations
    if total > 3000:
        print("\n⚠️  High context usage! Consider:")
        print("  - Split large files into reference materials")
        print("  - Move examples to separate files")
        print("  - Use external links instead of duplicating docs")
    elif total > 1500:
        print("\n✓ Moderate context usage")
    else:
        print("\n✓ Low context usage - well optimized!")

if __name__ == "__main__":
    skill_path = Path(sys.argv[1])
    analyze_skill(skill_path)
```

**Example Output**:
```
Skill: cookbook-audit
============================================================
style_guide.md                  3,245 tokens
SKILL.md                          687 tokens
------------------------------------------------------------
TOTAL                           3,932 tokens
============================================================

⚠️  High context usage! Consider:
  - Split large files into reference materials
  - Move examples to separate files
  - Use external links instead of duplicating docs
```

### Optimization Strategies

#### Strategy 1: Lazy Loading

**Before** (loads everything):
```markdown
---
name: style-checker
description: Check code style
---

# Style Checker

## Rules

[3000 words of detailed style rules included inline]
```

**After** (loads on-demand):
```markdown
---
name: style-checker
description: Check code style
---

# Style Checker

## Instructions

1. Check code against rules in `style_rules.md`
2. Report violations with line numbers

For detailed rule explanations, reference `style_rules.md`.
```

**Savings**: ~3000 tokens when skill not activated, ~0 tokens when activated (file loaded anyway)

#### Strategy 2: External References

**Before**:
```markdown
Python follows PEP 8 style guide:

- Indentation: 4 spaces
- Line length: 79 characters for code, 72 for docstrings
- Naming: snake_case for functions, PascalCase for classes
- Imports: standard library, third-party, local
[... 2000 more words of PEP 8 content]
```

**After**:
```markdown
Python follows PEP 8 style guide (https://pep8.org/).

Key points for review:
- Indentation and line length
- Naming conventions
- Import organization

For full details, reference PEP 8 documentation.
```

**Savings**: ~2000+ tokens

#### Strategy 3: Code Over Prose

**Before**:
```markdown
To validate emails, you should check that the string contains an @ symbol,
and that there is at least one character before the @ and at least one
character after it. You should also verify that the domain part contains
a period and has characters after the period. Additionally, you should
check for invalid characters...
[500 words of email validation logic]
```

**After**:
```markdown
Validate emails using `validate_email.py`:

```bash
python3 validate_email.py <email>
```

The script handles all validation rules including format, domain checks,
and character restrictions.
```

**Savings**: ~400 tokens + more reliable validation

#### Strategy 4: Compression

**Before**:
```markdown
When the user asks you to review their code, you should carefully read
through the entire codebase. After you have finished reading the code,
you should analyze it for potential issues. Once you have completed your
analysis, you should prepare a detailed report of your findings.
```

**After**:
```markdown
Code review process:
1. Read code
2. Analyze for issues
3. Generate report
```

**Savings**: ~30 tokens for this example, scales with content size

### Caching Strategies

**File-Level Caching** (Claude's automatic caching):

```markdown
<!-- Large reference file that rarely changes -->
<!-- .claude/skills/skill-name/reference.md -->

# Comprehensive Reference

[10,000 words of reference material]
```

Claude may cache large files automatically, reducing token usage on subsequent requests.

**Version Pinning for Cache Stability**:

```markdown
<!-- SKILL.md -->
---
name: api-client
description: Generate API clients
version: 1.2.0
---

# API Client Generator

**Version**: 1.2.0 (last updated: 2025-11-15)

Reference materials:
- `openapi_spec_v3.md` (v3.0.0)
- `examples.md` (v1.2.0)
```

Stable versions improve cache hit rates.

### Performance Monitoring

**Add metrics to scripts**:

```python
import time
from functools import wraps

def timing_decorator(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start

        print(f"[TIMING] {func.__name__}: {elapsed:.2f}s", file=sys.stderr)
        return result
    return wrapper

@timing_decorator
def validate_notebook(path: str):
    """Validate notebook."""
    # Validation logic
    pass
```

**Output**:
```
[TIMING] validate_notebook: 1.23s
[TIMING] check_secrets: 0.45s
[TIMING] generate_report: 0.12s
```

---

## 9. Security Hardening

### Input Validation

**Validate All Inputs**:

```python
from pathlib import Path

def validate_file_path(path: str) -> Path:
    """Validate and sanitize file path."""

    # Convert to Path object
    file_path = Path(path).resolve()

    # Check exists
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    # Check is file (not directory)
    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    # Check extension
    allowed_extensions = {'.ipynb', '.py', '.md'}
    if file_path.suffix not in allowed_extensions:
        raise ValueError(
            f"Invalid file type: {file_path.suffix}. "
            f"Allowed: {', '.join(allowed_extensions)}"
        )

    # Prevent directory traversal
    # Ensure file is within expected directory
    expected_base = Path.cwd()
    if not file_path.is_relative_to(expected_base):
        raise ValueError(f"File outside allowed directory: {path}")

    return file_path

# Usage
try:
    validated_path = validate_file_path(sys.argv[1])
    process_file(validated_path)
except (FileNotFoundError, ValueError) as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
```

### Secrets Detection

**From cookbook-audit's validate_notebook.py**:

```python
import subprocess

def check_hardcoded_secrets(self):
    """Check for API keys using detect-secrets."""
    try:
        # Use detect-secrets tool
        cmd = [
            "uvx",
            "--from", "detect-secrets",
            "detect-secrets-hook",
            "--baseline", ".secrets.baseline",
            str(self.notebook_path)
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            # Secrets detected
            self.issues.append(
                "Contains potential hardcoded secrets"
            )
            # Print details for review
            print(result.stdout)

    except FileNotFoundError:
        # Fallback to basic pattern matching
        self._check_secrets_fallback()

def _check_secrets_fallback(self):
    """Basic secret detection patterns."""
    patterns = {
        "Anthropic API key": r"sk-ant-[a-zA-Z0-9-]+",
        "OpenAI API key": r"sk-[a-zA-Z0-9]{32,}",
        "AWS key": r"AKIA[0-9A-Z]{16}",
        "Generic secret": r'(secret|password|token)\s*=\s*["\'][^"\']{20,}["\']',
    }

    for cell in self.cells:
        source = self.get_cell_source(cell)
        for secret_type, pattern in patterns.items():
            if re.search(pattern, source, re.IGNORECASE):
                self.issues.append(f"Hardcoded {secret_type} detected")
```

### Sandboxing

**Limit Script Capabilities**:

```python
import os
import sys
from pathlib import Path

# Restrict to specific directory
ALLOWED_DIR = Path("/workspace/data")

def secure_read_file(path: str) -> str:
    """Read file with security restrictions."""

    # Resolve to absolute path
    abs_path = Path(path).resolve()

    # Ensure within allowed directory
    if not abs_path.is_relative_to(ALLOWED_DIR):
        raise PermissionError(
            f"Access denied: {path} is outside allowed directory"
        )

    # Prevent reading sensitive files
    sensitive_patterns = ['.env', 'credentials', 'secret', 'private']
    if any(pattern in abs_path.name.lower() for pattern in sensitive_patterns):
        raise PermissionError(f"Cannot read sensitive file: {path}")

    # Read with size limit (prevent DoS)
    MAX_SIZE = 10 * 1024 * 1024  # 10 MB
    if abs_path.stat().st_size > MAX_SIZE:
        raise ValueError(f"File too large: {path}")

    return abs_path.read_text()
```

### Subprocess Safety

**Secure subprocess execution**:

```python
import subprocess
import shlex

def run_command_safely(command: list[str]) -> str:
    """Run command with security measures."""

    # Whitelist allowed commands
    ALLOWED_COMMANDS = {'python3', 'jupyter', 'git', 'uv'}

    if command[0] not in ALLOWED_COMMANDS:
        raise ValueError(f"Command not allowed: {command[0]}")

    # Never use shell=True (prevents injection)
    # Always pass command as list
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,  # Prevent hanging
            check=True,
            # Security: no shell, no user environment
            shell=False,
            env={  # Minimal environment
                'PATH': '/usr/bin:/bin',
                'HOME': os.environ.get('HOME', '/tmp'),
            }
        )
        return result.stdout

    except subprocess.TimeoutExpired:
        raise RuntimeError(f"Command timed out: {command}")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e}")

# Usage
# ❌ NEVER do this (vulnerable to injection):
# subprocess.run(f"git log {user_input}", shell=True)

# ✅ DO this:
safe_args = ['git', 'log', '--oneline', '--max-count=10']
output = run_command_safely(safe_args)
```

### Secret Management

**Environment Variables for Secrets**:

```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Get secrets from environment
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError(
        "ANTHROPIC_API_KEY not found in environment. "
        "Create .env file with: ANTHROPIC_API_KEY=your-key"
    )

# ❌ NEVER hardcode secrets:
# API_KEY = "sk-ant-abc123"

# ❌ NEVER log secrets:
# print(f"Using API key: {API_KEY}")

# ✅ DO mask in logs:
print(f"Using API key: {API_KEY[:10]}...")
```

**Skill Instructions**:

```markdown
<!-- SKILL.md -->

## Security Requirements

### API Keys

NEVER hardcode API keys. Always use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

### Secrets in Notebooks

Before committing, verify no secrets:
```bash
python3 validate_notebook.py notebook.ipynb
```

The validator automatically scans for:
- API keys (Anthropic, OpenAI, AWS)
- Hardcoded passwords
- Access tokens
```

---

## 10. Advanced Examples

### Example 1: Multi-Stage Processing Pipeline

**Real-world scenario**: Document generation with quality checks

```
.claude/skills/doc-pipeline/
├── SKILL.md
├── stages/
│   ├── 01_analyze.py
│   ├── 02_generate.py
│   ├── 03_validate.py
│   └── 04_finalize.py
├── templates/
│   └── report.md
└── config.yaml
```

**SKILL.md**:

```markdown
---
name: doc-pipeline
description: Generate technical documentation with automated quality checks
---

# Documentation Pipeline

## Workflow

### Stage 1: Analysis
```bash
python3 stages/01_analyze.py <source_code>
```
- Extracts structure
- Identifies components
- Generates outline

### Stage 2: Generation
```bash
python3 stages/02_generate.py <outline.json>
```
- Writes documentation
- Includes code examples
- Applies templates

### Stage 3: Validation
```bash
python3 stages/03_validate.py <draft.md>
```
- Checks completeness
- Validates links
- Runs spell check

### Stage 4: Finalization
```bash
python3 stages/04_finalize.py <validated.md>
```
- Formats output
- Generates table of contents
- Creates final deliverable

## Quality Gates

Each stage must pass before proceeding:
- Stage 1: Valid JSON output
- Stage 2: All sections present
- Stage 3: No broken links, no spelling errors
- Stage 4: Proper formatting

## Output

Final document saved to: `output/documentation.md`
```

**Stage Script Example** (stages/03_validate.py):

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "markdown-it-py",
#     "linkchecker",
# ]
# ///
"""
Validate generated documentation.

Exit codes:
    0 - Validation passed
    1 - Validation failed
"""

import sys
import json
from pathlib import Path
from markdown_it import MarkdownIt

def validate_document(doc_path: Path) -> dict:
    """Run all validation checks."""

    content = doc_path.read_text()
    md = MarkdownIt()
    tokens = md.parse(content)

    results = {
        "completeness": check_completeness(tokens),
        "links": check_links(tokens),
        "spelling": check_spelling(content),
    }

    return results

def check_completeness(tokens) -> dict:
    """Verify all required sections present."""
    required_sections = [
        "Introduction",
        "Prerequisites",
        "Usage",
        "Examples",
        "Troubleshooting"
    ]

    found_sections = [
        token.content
        for token in tokens
        if token.type == "heading_open"
    ]

    missing = [
        section
        for section in required_sections
        if section not in found_sections
    ]

    return {
        "passed": len(missing) == 0,
        "missing_sections": missing
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python 03_validate.py <document.md>")
        sys.exit(1)

    doc_path = Path(sys.argv[1])
    results = validate_document(doc_path)

    # Print results
    print(json.dumps(results, indent=2))

    # Determine pass/fail
    all_passed = all(
        check.get("passed", False)
        for check in results.values()
    )

    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    main()
```

### Example 2: Adaptive Skill with Context Awareness

**Skill that adapts based on project context**:

```markdown
---
name: test-generator
description: Generate unit tests based on project type and conventions
---

# Test Generator

## Instructions

### Step 1: Detect Project Type

Check for framework indicators:
```bash
python3 detect_framework.py
```

Supported frameworks:
- **pytest**: pytest.ini or conftest.py present
- **unittest**: Uses unittest in existing tests
- **jest**: package.json with jest dependency
- **go test**: *_test.go files present

### Step 2: Load Framework Templates

Based on detected framework:
- pytest → `templates/pytest_template.py`
- unittest → `templates/unittest_template.py`
- jest → `templates/jest_template.js`
- go test → `templates/gotest_template.go`

### Step 3: Analyze Code Structure

Extract:
- Function signatures
- Class methods
- Dependencies
- Edge cases

### Step 4: Generate Tests

Use framework-specific template to generate:
- Happy path tests
- Edge case tests
- Error handling tests
- Mock/stub setup if needed

### Step 5: Validate Generated Tests

Run generated tests:
```bash
python3 run_tests.py <test_file>
```

Ensure:
- Tests are syntactically valid
- Tests can run (even if they fail)
- No import errors

## Output Format

```python
# Generated for pytest framework
# File: test_calculator.py

import pytest
from calculator import Calculator

class TestCalculator:
    @pytest.fixture
    def calc(self):
        return Calculator()

    def test_add_positive_numbers(self, calc):
        assert calc.add(2, 3) == 5

    def test_add_negative_numbers(self, calc):
        assert calc.add(-2, -3) == -5

    # ... more tests
```
```

**Framework Detection Script**:

```python
#!/usr/bin/env python3
"""Detect test framework used in project."""

import json
from pathlib import Path

def detect_framework() -> dict:
    """Detect which test framework to use."""

    cwd = Path.cwd()

    # Check for pytest
    if (cwd / "pytest.ini").exists() or (cwd / "conftest.py").exists():
        return {
            "framework": "pytest",
            "template": "templates/pytest_template.py",
            "run_command": "pytest"
        }

    # Check for jest (JavaScript)
    package_json = cwd / "package.json"
    if package_json.exists():
        content = json.loads(package_json.read_text())
        if "jest" in content.get("devDependencies", {}):
            return {
                "framework": "jest",
                "template": "templates/jest_template.js",
                "run_command": "npm test"
            }

    # Check for Go
    if list(cwd.glob("**/*_test.go")):
        return {
            "framework": "go test",
            "template": "templates/gotest_template.go",
            "run_command": "go test ./..."
        }

    # Default to unittest (Python standard library)
    return {
        "framework": "unittest",
        "template": "templates/unittest_template.py",
        "run_command": "python -m unittest"
    }

if __name__ == "__main__":
    result = detect_framework()
    print(json.dumps(result, indent=2))
```

### Example 3: Skill with External API Integration

**Skill that fetches live data**:

```markdown
---
name: api-validator
description: Validate API endpoints and generate integration tests
---

# API Validator

## Instructions

### Phase 1: Endpoint Discovery

Scan for API definitions:
- OpenAPI/Swagger specs
- Code annotations
- Route definitions

Run:
```bash
python3 discover_endpoints.py <source_dir>
```

### Phase 2: Live Testing

For each endpoint, run:
```bash
python3 test_endpoint.py <endpoint_url> <method>
```

Tests:
- Response status codes
- Response schema
- Response times
- Error handling

### Phase 3: Generate Integration Tests

Based on live results, generate test suite:
```bash
python3 generate_tests.py endpoints.json
```

Output: Test file with realistic test data from actual responses

## Security

- Use read-only API keys
- Never test against production
- Respect rate limits
- Handle authentication securely
```

**test_endpoint.py**:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx",
#     "python-dotenv",
# ]
# ///
"""
Test API endpoint and generate validation report.
"""

import sys
import json
import httpx
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

def test_endpoint(url: str, method: str = "GET") -> Dict[str, Any]:
    """Test single API endpoint."""

    # Get API key from environment
    api_key = os.getenv("API_KEY")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        # Make request with timeout
        with httpx.Client(timeout=10.0) as client:
            response = client.request(
                method=method,
                url=url,
                headers=headers
            )

        # Collect metrics
        result = {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "response_time_ms": response.elapsed.total_seconds() * 1000,
            "headers": dict(response.headers),
            "success": 200 <= response.status_code < 300,
        }

        # Try to parse JSON response
        try:
            result["body"] = response.json()
            result["content_type"] = "application/json"
        except json.JSONDecodeError:
            result["body"] = response.text[:500]  # Truncate
            result["content_type"] = "text/plain"

        return result

    except httpx.TimeoutException:
        return {
            "url": url,
            "method": method,
            "error": "Request timed out",
            "success": False
        }

    except Exception as e:
        return {
            "url": url,
            "method": method,
            "error": str(e),
            "success": False
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_endpoint.py <url> [method]")
        sys.exit(1)

    url = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else "GET"

    result = test_endpoint(url, method)

    # Print results
    print(json.dumps(result, indent=2))

    # Exit based on success
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
```

---

## Conclusion

This guide covered advanced techniques for building production-quality Claude Code skills:

1. **Multi-File Architecture**: Organizing complex skills with reference materials and scripts
2. **Progressive Disclosure**: Optimizing context usage through lazy loading
3. **Script Integration**: Using PEP 723 for self-contained automation
4. **Testing**: Unit tests, integration tests, and activation verification
5. **Debugging**: Tools and techniques for troubleshooting skills
6. **Deployment**: Personal, project, and API deployment patterns
7. **Composition**: Combining skills and building skill libraries
8. **Performance**: Measuring and optimizing token usage
9. **Security**: Input validation, secrets detection, and sandboxing
10. **Advanced Patterns**: Real-world examples of complex skill workflows

### Key Takeaways

**Design Principles**:
- Keep SKILL.md concise (under 2000 tokens)
- Load reference materials on-demand
- Use scripts for complex or fragile operations
- Optimize for team collaboration and CI/CD

**Production Checklist**:
- [ ] Clear, specific description with trigger keywords
- [ ] Progressive loading strategy for large skills
- [ ] Scripts with PEP 723 dependencies
- [ ] Comprehensive error handling
- [ ] Security validation (secrets, input sanitization)
- [ ] Testing (unit, integration, activation)
- [ ] Documentation and examples
- [ ] Version control and CI integration

### Learning from cookbook-audit

The **cookbook-audit skill** in this repository demonstrates many advanced techniques:

- **Multi-file structure**: SKILL.md + style_guide.md + validate_notebook.py
- **Progressive disclosure**: References style_guide.md only when needed
- **PEP 723 script**: Self-contained with nbconvert dependency
- **External tool integration**: Uses detect-secrets for security scanning
- **Graceful degradation**: Fallback when tools unavailable
- **Structured output**: Generates markdown files in tmp/ for review
- **Comprehensive validation**: Multiple check methods with clear reporting

Study this skill for patterns to apply in your own skills.

### Next Steps

**To deepen your skills**:

1. **Explore existing skills**: Study `.claude/skills/` in repositories
2. **Build a skill library**: Create a collection for your domain
3. **Contribute**: Share skills with the community
4. **Integrate with CI/CD**: Automate quality checks
5. **Compose workflows**: Build meta-skills that orchestrate others

**Resources**:
- [Claude Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [PEP 723 Specification](https://peps.python.org/pep-0723/)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [cookbook-audit skill](../.claude/skills/cookbook-audit/)

---

**Ready to build?** Apply these advanced techniques to create powerful, production-ready skills that enhance your workflow and your team's productivity!
