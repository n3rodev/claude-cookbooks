# Best Practices for Claude Code Skills

This guide covers advanced patterns and best practices for creating production-quality Claude Code skills. Whether you're building personal productivity tools or team-shared standards, these principles will help you create skills that are reliable, maintainable, and effective.

## Table of Contents

1. [Design Principles](#design-principles)
2. [Description Best Practices](#description-best-practices)
3. [Instruction Writing](#instruction-writing)
4. [Progressive Disclosure](#progressive-disclosure)
5. [Performance Optimization](#performance-optimization)
6. [Security Considerations](#security-considerations)
7. [Multi-Model Compatibility](#multi-model-compatibility)
8. [Common Anti-Patterns](#common-anti-patterns)
9. [Skill Organization](#skill-organization)
10. [Team Collaboration](#team-collaboration)

## Design Principles

### 1. Conciseness

**Principle**: Every word in your skill consumes context window space. Be ruthlessly concise while maintaining clarity.

**Bad** (97 words):
```markdown
## Instructions

In order to help the user generate appropriate commit messages that follow
the conventional commit format that has been adopted by many open source
projects and development teams around the world, you should begin by asking
the user to describe the changes that they have made to the codebase. Once
you have received this information from the user, you should then analyze
the nature of these changes and determine which type of commit would be most
appropriate from the following list: feat, fix, docs, style, refactor, test,
or chore. After determining the appropriate type...
```

**Good** (23 words):
```markdown
## Instructions

1. Ask user to describe their changes
2. Determine commit type: feat, fix, docs, style, refactor, test, chore
3. Generate message: `<type>(<scope>): <description>`
```

**Impact**: Saved 74 words (76% reduction) while maintaining clarity.

### 2. Specificity

**Principle**: Vague instructions lead to inconsistent behavior. Be specific about what Claude should do, when, and how.

**Bad** (vague):
```markdown
---
name: code-helper
description: Helps with code review and suggestions
---

Review code and provide feedback.
```

**Good** (specific):
```markdown
---
name: python-code-reviewer
description: Review Python code for PEP 8 compliance, common anti-patterns, and security issues. Use when user submits Python code for review or asks for code quality feedback.
---

## Review Checklist

For each code submission:

1. **Style Compliance**
   - Check PEP 8 adherence (line length, naming, spacing)
   - Flag non-standard patterns

2. **Common Issues**
   - Mutable default arguments
   - Bare except clauses
   - Missing type hints on public functions

3. **Security Checks**
   - SQL injection vulnerabilities
   - Path traversal risks
   - Hardcoded credentials

4. **Output Format**
   ```
   ✅ Strengths: [List 2-3 positive aspects]
   ⚠️  Issues: [List problems with line numbers]
   💡 Suggestions: [Provide specific improvements]
   ```
```

### 3. Appropriate Constraints

**Principle**: Constraints guide Claude's behavior and prevent scope creep. Include what the skill should NOT do.

**Bad** (no constraints):
```markdown
---
description: Process PDF files for users
---
```

**Good** (with constraints):
```markdown
---
description: Extract text and tables from PDF files, fill PDF forms, and merge PDFs. Use when user mentions PDF processing. Does NOT handle image extraction, OCR, or password-protected PDFs. Maximum file size: 50MB.
---

## Scope Limitations

**Supports**:
- Text extraction from standard PDFs
- Table extraction with structure preservation
- Form filling with FDF format
- Merging multiple PDFs

**Does NOT Support**:
- Scanned documents (no OCR)
- Password-protected or encrypted PDFs
- Image/photo extraction
- PDF editing or annotation
```

## Description Best Practices

The `description` field is critical for skill activation. It's the first thing Claude sees and determines when your skill is loaded.

### What Makes a Good Description

**Formula**:
```
[Action] [what] to [outcome]. Use when [trigger conditions]. [Capabilities]. [Limitations].
```

**Components**:
1. **Action verb**: Generate, Extract, Review, Calculate, Convert, etc.
2. **What it does**: Clear statement of functionality
3. **When to use**: Trigger keywords and conditions
4. **Capabilities**: Specific features (optional)
5. **Limitations**: What it doesn't do (optional)

### Examples with Analysis

**Example 1: Financial Analysis**

❌ **Bad**:
```yaml
description: Financial calculations and analysis
```
*Problems: No trigger conditions, vague capabilities, no specifics*

✅ **Good**:
```yaml
description: Calculate financial ratios (P/E, ROE, debt-to-equity, current ratio) and perform DCF valuation. Use when user mentions financial statements, ratio analysis, stock valuation, or company financial health. Requires balance sheet and income statement data.
```
*Why better: Specific calculations listed, clear triggers, states data requirements*

**Example 2: Git Commit Messages**

❌ **Bad**:
```yaml
description: Help with git commits
```
*Problems: Too broad, no trigger words, unclear value*

✅ **Good**:
```yaml
description: Generate conventional commit messages following format: type(scope): description. Use when user is about to commit code, mentions 'commit message', or asks for git commit help. Supports types: feat, fix, docs, style, refactor, test, chore.
```
*Why better: Shows exact format, clear triggers, lists supported types*

**Example 3: Data Visualization**

❌ **Bad**:
```yaml
description: Create charts and graphs from data
```
*Problems: Generic, no technology specified, missing triggers*

✅ **Good**:
```yaml
description: Generate Python code for data visualizations using matplotlib and seaborn. Use when user has data to visualize, mentions charts/graphs/plots, or asks about data presentation. Supports: line, bar, scatter, histogram, heatmap, box plots. Does NOT generate interactive dashboards or 3D visualizations.
```
*Why better: Specific libraries, clear use cases, explicit limitations*

### Trigger Keywords

Include keywords that users naturally use when they need this skill:

**Financial Skill Triggers**:
```yaml
description: ...Use when user mentions: 'financial ratios', 'valuation', 'P/E ratio', 'DCF', 'company analysis', 'financial health', 'balance sheet analysis'...
```

**Testing Skill Triggers**:
```yaml
description: ...Use when user mentions: 'unit tests', 'test cases', 'testing', 'pytest', 'test coverage', 'TDD', 'write tests'...
```

**Documentation Skill Triggers**:
```yaml
description: ...Use when user mentions: 'docstrings', 'documentation', 'API docs', 'code comments', 'readme', 'document this'...
```

### Length Guidelines

- **Minimum**: 50 characters (be descriptive enough)
- **Target**: 150-300 characters (sweet spot)
- **Maximum**: 1024 characters (hard limit)

**Too Short** (42 chars):
```yaml
description: PDF processing and extraction
```

**Too Long** (1100+ chars):
```yaml
description: This skill provides comprehensive PDF document processing capabilities including but not limited to text extraction using multiple parsing libraries such as PyPDF2 and pdfplumber with automatic fallback mechanisms, table extraction with structure preservation using various algorithms optimized for different PDF formats, form filling capabilities supporting FDF and XFDF formats with validation, PDF merging with bookmark preservation and page range selection, metadata extraction and modification, and various other PDF manipulation tasks. Use this skill when the user mentions any PDF-related tasks... [continues]
```

**Just Right** (278 chars):
```yaml
description: Extract text and tables from PDF files, fill PDF forms programmatically, and merge multiple PDFs. Use when user mentions PDF processing, extraction, or form filling. Supports PyPDF2 and pdfplumber. Does NOT handle OCR, password-protected PDFs, or files over 50MB.
```

## Instruction Writing

### Clarity and Structure

**Bad** (unstructured):
```markdown
When the user asks you to review their code, you should look at it carefully and think about potential issues. Consider things like whether the code follows best practices, if there are any bugs, if it's readable, and whether there might be security problems. Then give them feedback about what you found.
```

**Good** (structured):
```markdown
## Code Review Process

1. **Initial Assessment**
   - Identify programming language
   - Determine code purpose and context

2. **Quality Checks**
   - [ ] Style: Follows language conventions?
   - [ ] Logic: Correct implementation?
   - [ ] Readability: Clear naming and structure?
   - [ ] Performance: Obvious inefficiencies?

3. **Security Scan**
   - [ ] Input validation present?
   - [ ] SQL/Command injection risks?
   - [ ] Secrets exposure?

4. **Provide Feedback**
   ```
   ✅ Strengths: [2-3 points]
   ⚠️  Issues: [List with line numbers]
   💡 Suggestions: [Specific improvements]
   ```
```

### Use Action-Oriented Language

**Bad** (passive):
```markdown
The user should be asked to provide the principal amount and interest rate,
which will then be used in the calculation that needs to be performed.
```

**Good** (active):
```markdown
1. Ask user for:
   - Principal amount (P)
   - Interest rate (r)
2. Calculate using: A = P(1 + r/n)^(nt)
```

### Provide Complete Examples

Examples are powerful teaching tools. Include realistic, complete examples.

**Bad** (incomplete):
```markdown
## Example

User: "Calculate interest"
Response: [Show calculation]
```

**Good** (complete):
```markdown
## Example: Basic Compound Interest

**User Input**:
"If I invest $10,000 at 5% annual interest compounded monthly for 10 years, how much will I have?"

**Response**:
```
Given Information:
- Principal (P): $10,000
- Annual Rate (r): 5% = 0.05
- Compounding (n): 12 (monthly)
- Time (t): 10 years

Formula: A = P(1 + r/n)^(nt)

Calculation:
A = 10,000(1 + 0.05/12)^(12×10)
A = 10,000(1.004167)^120
A = 10,000(1.64701)
A = $16,470.10

Results:
- Final Amount: $16,470.10
- Interest Earned: $6,470.10
- Total Return: 64.70%
```
```

### Handle Edge Cases Explicitly

**Bad** (ignores edge cases):
```markdown
Calculate the compound interest and show the result.
```

**Good** (handles edge cases):
```markdown
## Edge Cases

### Missing Information
If user doesn't specify compounding frequency:
- **Ask**: "How often is the interest compounded? (annually, quarterly, monthly, daily)"
- **Default**: If user unsure, assume annually (n=1) and state assumption

### Invalid Input
If negative values provided:
- **Rate < 0**: "Interest rates must be positive. Did you mean +X%?"
- **Principal ≤ 0**: "Principal must be greater than zero."
- **Time ≤ 0**: "Time period must be positive."

### Zero Interest Rate
If r = 0:
- Return principal unchanged
- Note: "With 0% interest, your investment remains at $P"

### Continuous Compounding
If user mentions "continuous" or "infinite" compounding:
- Use formula: A = Pe^(rt)
- Explain difference from discrete compounding
```

## Progressive Disclosure

Progressive disclosure means loading information only when needed, saving context window space.

### When to Use Multiple Files

**Single File (SKILL.md only)**:
- Skill fits in < 500 lines
- No complex reference material
- Instructions are straightforward

**Multiple Files**:
- Total content > 500 lines
- Contains reference tables, examples, or documentation
- Needs progressive complexity
- Benefits from separation of concerns

### File Organization Strategies

**Strategy 1: By Complexity**

```
git-commit-helper/
├── SKILL.md              # Core instructions (always loaded)
├── examples.md           # Load when: "show me examples"
└── advanced.md           # Load when: "explain conventional commits"
```

**SKILL.md**:
```markdown
## Instructions

Generate conventional commit messages: `type(scope): description`

**Types**: feat, fix, docs, style, refactor, test, chore

For examples, see `examples.md`
For detailed explanation, see `advanced.md`
```

**Strategy 2: By Topic**

```
code-reviewer/
├── SKILL.md              # Main workflow
├── style-guide.md        # Coding standards
├── security-checklist.md # Security patterns
└── anti-patterns.md      # Common mistakes
```

**SKILL.md**:
```markdown
## Review Process

1. Check code against `style-guide.md`
2. Scan for issues in `security-checklist.md`
3. Compare against `anti-patterns.md`
4. Generate structured feedback
```

**Strategy 3: By Function**

```
data-analyzer/
├── SKILL.md              # Main instructions
├── statistical-methods.md # Reference formulas
├── visualization-guide.md # Chart recommendations
└── scripts/
    └── analyze.py        # Automation
```

### Reference Patterns

**Pattern 1: Explicit Loading**
```markdown
For detailed Python style rules, read `style-guide.md` then apply those rules.
```

**Pattern 2: Conditional Loading**
```markdown
If user asks for examples, consult `examples.md`
If user asks "why", explain using concepts from `theory.md`
```

**Pattern 3: Script Integration**
```markdown
1. Run: `python validate.py <file>`
2. Read the report: `tmp/validation-report.md`
3. Present findings to user
```

## Performance Optimization

### Context Management

**Problem**: Skills consume context window space, reducing conversation capacity.

**Solution**: Minimize skill size while maintaining effectiveness.

**Before** (350 words):
```markdown
## Compound Interest Calculator

This skill helps users calculate compound interest, which is a fundamental
concept in finance and investing. Compound interest is the interest calculated
on the initial principal and also on the accumulated interest from previous
periods. This differs from simple interest, where interest is only calculated
on the principal amount.

The formula for compound interest is: A = P(1 + r/n)^(nt)

Where:
- A represents the final amount after interest
- P represents the principal, or initial amount invested or borrowed
- r represents the annual interest rate expressed as a decimal
- n represents the number of times interest is compounded per year
- t represents the time period in years

When helping users with compound interest calculations, you should first
gather all necessary information including the principal amount, the annual
interest rate (making sure to convert from percentage to decimal), the
compounding frequency (such as annually, semi-annually, quarterly, monthly,
or daily), and the time period in years.

[continues...]
```

**After** (62 words):
```markdown
## Instructions

Calculate compound interest: A = P(1 + r/n)^(nt)

1. **Gather**: Principal (P), rate (r), frequency (n), time (t)
2. **Calculate**: Apply formula
3. **Present**:
   ```
   Principal: $P
   Rate: r% = 0.r
   Compounding: n times/year
   Time: t years
   Final Amount: $A
   Interest Earned: $(A-P)
   ```
```

**Savings**: 82% reduction in word count

### Skill Size Guidelines

| Size | Total Lines | When to Use |
|------|------------|-------------|
| **Micro** | < 50 | Simple instructions, no reference material |
| **Small** | 50-200 | Standard skill with basic examples |
| **Medium** | 200-500 | Multiple workflows, extensive examples |
| **Large** | 500-1000 | Complex domain knowledge, multiple files |
| **Extra Large** | 1000+ | Comprehensive systems, use progressive disclosure |

**Optimization Checklist**:
- [ ] Remove redundant explanations
- [ ] Use bullet points over paragraphs
- [ ] Move examples to separate files
- [ ] Use tables over prose
- [ ] Reference external docs instead of duplicating
- [ ] Remove obvious statements
- [ ] Combine related instructions

### Caching Strategies

For skills with static reference material:

```markdown
## Reference Data

<!-- This section is static and benefits from caching -->

### Financial Ratios

| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| Current Ratio | Current Assets / Current Liabilities | 1.5 - 3.0 |
| Debt-to-Equity | Total Debt / Shareholders' Equity | < 2.0 |
| ROE | Net Income / Shareholders' Equity | > 15% |
| P/E Ratio | Price per Share / EPS | 15 - 25 |
```

Claude's caching helps reduce costs for frequently-used static content.

## Security Considerations

### Script Safety

When skills include executable scripts:

**1. Input Validation**

**Bad** (no validation):
```python
#!/usr/bin/env python3
import sys
import os

filename = sys.argv[1]
os.system(f"cat {filename}")  # Command injection risk!
```

**Good** (validated):
```python
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

def safe_read(filename):
    # Validate input
    path = Path(filename).resolve()

    # Ensure path exists and is a file
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filename}")

    if not path.is_file():
        raise ValueError(f"Not a file: {filename}")

    # Prevent path traversal
    if ".." in str(path):
        raise ValueError("Path traversal not allowed")

    # Use safe file reading
    with open(path, 'r') as f:
        return f.read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)

    try:
        content = safe_read(sys.argv[1])
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
```

**2. Dependency Management with PEP 723**

Always use inline script metadata for dependency declaration:

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "requests>=2.31.0",
#     "pydantic>=2.0.0",
# ]
# ///
"""
Secure API interaction script with validated dependencies.
"""

import requests
from pydantic import BaseModel, ValidationError

# Script implementation...
```

**3. Secrets Management**

**Bad** (hardcoded secrets):
```python
API_KEY = "sk-ant-api03-abcd..."  # NEVER DO THIS
```

**Good** (environment variables):
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")
```

### File Handling

**Bad** (unsafe):
```python
def process_file(user_path):
    with open(user_path) as f:  # Risk: arbitrary file access
        return f.read()
```

**Good** (safe):
```python
from pathlib import Path

ALLOWED_EXTENSIONS = {'.txt', '.md', '.csv', '.json'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def process_file(user_path, allowed_dir=None):
    path = Path(user_path).resolve()

    # Validate extension
    if path.suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix}")

    # Validate directory (if specified)
    if allowed_dir:
        allowed = Path(allowed_dir).resolve()
        if not path.is_relative_to(allowed):
            raise ValueError("File outside allowed directory")

    # Validate size
    if path.stat().st_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large (max {MAX_FILE_SIZE} bytes)")

    # Safe read
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
```

### Temporary File Management

**Bad** (security risk):
```python
def create_report():
    with open("/tmp/report.txt", "w") as f:  # Predictable path
        f.write(sensitive_data)
```

**Good** (secure):
```python
import tempfile
from pathlib import Path

def create_report():
    # Create secure temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        report_path = Path(tmpdir) / "report.txt"

        # Restrictive permissions (owner only)
        report_path.touch(mode=0o600)

        with open(report_path, "w") as f:
            f.write(sensitive_data)

        # Process report...

    # Automatically cleaned up when context exits
```

**In SKILL.md**:
```markdown
## Security Notes

Scripts in this skill:
- ✅ Validate all user inputs
- ✅ Use environment variables for secrets
- ✅ Restrict file access to specific directories
- ✅ Create temporary files securely
- ✅ Clean up resources automatically
```

## Multi-Model Compatibility

Different Claude models have different capabilities and behaviors. Test skills across models.

### Model Differences

| Aspect | Haiku 4.5 | Sonnet 4.5 | Opus 4.1 |
|--------|-----------|------------|----------|
| **Speed** | Fastest | Medium | Slowest |
| **Cost** | Lowest | Medium | Highest |
| **Reasoning** | Good | Excellent | Best |
| **Instruction Following** | Good | Excellent | Excellent |
| **Context Understanding** | Good | Excellent | Best |
| **Best For** | Simple tasks | General purpose | Complex analysis |

### Writing Model-Agnostic Skills

**Bad** (assumes advanced reasoning):
```markdown
## Instructions

Analyze the code deeply, considering subtle architectural implications,
potential future maintenance challenges, scalability concerns in distributed
systems, and the philosophical alignment with domain-driven design principles.
```
*Haiku may struggle with this level of abstraction*

**Good** (explicit and structured):
```markdown
## Instructions

Review the code for:

1. **Architecture**
   - [ ] Separation of concerns maintained?
   - [ ] Dependencies flow in one direction?
   - [ ] Single Responsibility Principle followed?

2. **Maintainability**
   - [ ] Functions under 50 lines?
   - [ ] Clear naming conventions?
   - [ ] Adequate comments for complex logic?

3. **Scalability**
   - [ ] Stateless design where possible?
   - [ ] Database queries optimized?
   - [ ] Caching opportunities identified?
```
*Works well across all models*

### Testing Across Models

Create a test suite for your skill:

**test-cases.md**:
```markdown
# Skill Test Cases

## Test 1: Basic Functionality
**Input**: "Calculate compound interest: $1000, 5%, 2 years, annually"
**Expected Output**: Clear calculation showing $1,102.50

**Haiku**: ✅ Pass
**Sonnet**: ✅ Pass
**Opus**: ✅ Pass

## Test 2: Missing Information
**Input**: "Calculate compound interest for $1000"
**Expected Output**: Prompt for missing: rate, time, frequency

**Haiku**: ⚠️ Sometimes assumes defaults
**Sonnet**: ✅ Consistently asks
**Opus**: ✅ Consistently asks

**Fix**: Make required parameters explicit in instructions

## Test 3: Edge Case - Zero Interest
**Input**: "Calculate compound interest: $1000, 0%, 5 years, monthly"
**Expected Output**: Recognize special case, explain no growth

**Haiku**: ✅ Pass
**Sonnet**: ✅ Pass (with explanation)
**Opus**: ✅ Pass (with detailed explanation)
```

### Adjusting for Model Capabilities

**For Haiku Compatibility**:
- ✅ Use explicit step-by-step instructions
- ✅ Provide clear examples
- ✅ Use structured formats (checklists, tables)
- ❌ Avoid complex abstractions
- ❌ Avoid implicit context requirements

**For Sonnet/Opus**:
- ✅ Can handle more nuanced instructions
- ✅ Better at inferring context
- ✅ Can work with more complex reasoning chains
- ✅ Understands subtle distinctions

**Universal Principles**:
- ✅ Explicit is always better than implicit
- ✅ Examples improve consistency across models
- ✅ Structure beats prose for reliability
- ✅ Clear success criteria help all models

## Common Anti-Patterns

### Anti-Pattern 1: Over-Engineering

**Bad** (too complex):
```markdown
---
name: ultimate-code-assistant
description: Comprehensive code analysis, review, generation, refactoring, testing, documentation, optimization, security scanning, and team collaboration tool
---

# Ultimate Code Assistant

This skill provides complete software development lifecycle support...
[2000 lines of instructions covering everything]
```

**Good** (focused):
```markdown
---
name: python-security-scanner
description: Scan Python code for common security vulnerabilities (SQL injection, XSS, hardcoded secrets, path traversal). Use when reviewing Python code for security issues.
---

# Python Security Scanner

## Vulnerability Checks

1. **SQL Injection**: String concatenation in queries
2. **XSS**: Unescaped user input in HTML
3. **Secrets**: Hardcoded API keys, passwords, tokens
4. **Path Traversal**: Unsanitized file paths

[Focused, specific instructions]
```

**Why**: Focused skills are more reliable, easier to maintain, and use less context.

### Anti-Pattern 2: Vague Descriptions

**Bad**:
```yaml
description: Helps with data
```

**Bad**:
```yaml
description: Assists users with various data-related tasks and operations
```

**Good**:
```yaml
description: Calculate statistical measures (mean, median, mode, std dev, percentiles) for numerical datasets. Use when user mentions statistics, data analysis, or asks to summarize numbers. Handles lists, CSV data, and pandas DataFrames.
```

### Anti-Pattern 3: Missing Examples

**Bad**:
```markdown
## Instructions

When user provides financial data, calculate key ratios and provide analysis.
```

**Good**:
```markdown
## Instructions

When user provides financial data, calculate key ratios.

## Example

**User Input**:
```
Revenue: $100M
Net Income: $15M
Total Assets: $200M
Total Equity: $80M
```

**Response**:
```
Financial Ratios:
- Profit Margin: 15% (Net Income / Revenue)
- ROA: 7.5% (Net Income / Total Assets)
- ROE: 18.75% (Net Income / Equity)

Analysis:
✅ Strong profitability (15% margin)
✅ Excellent ROE (>15% target)
⚠️  ROA below industry average (typical: 10%)
```
```

### Anti-Pattern 4: Ignoring Error Cases

**Bad**:
```markdown
## Instructions

1. Parse the JSON file
2. Extract the data
3. Generate report
```

**Good**:
```markdown
## Instructions

1. **Parse JSON file**
   - If invalid JSON: "Error: File contains invalid JSON. Check syntax."
   - If file not found: "Error: File not found. Check path."

2. **Extract data**
   - If required field missing: "Error: Missing required field: {field}"
   - If unexpected format: Attempt graceful degradation, note issues

3. **Generate report**
   - If no data: "Warning: No data found. Check input criteria."
   - If partial success: Report completed items, note failures
```

### Anti-Pattern 5: Duplicating Documentation

**Bad**:
```markdown
## Python Style Guide

PEP 8 states that you should use 4 spaces for indentation, not tabs.
Lines should be no longer than 79 characters for code and 72 for comments.
Use snake_case for function names and UPPER_CASE for constants.
[Copies entire PEP 8 specification - 2000+ lines]
```

**Good**:
```markdown
## Python Style Guide

Apply PEP 8 standards:
- Indentation: 4 spaces
- Line length: 79 characters (code), 72 (comments)
- Naming: snake_case (functions), UPPER_CASE (constants)

Full reference: https://pep8.org/
```

### Anti-Pattern 6: Ambiguous Scope

**Bad**:
```yaml
description: Process documents
```

**Good**:
```yaml
description: Extract text from PDF and DOCX files only. Use when user needs to read document contents. Does NOT handle images, spreadsheets, or presentations. Maximum file size: 25MB.
```

### Anti-Pattern 7: No Version Control

**Bad**:
```markdown
<!-- No indication of what changed or when -->
```

**Good**:
```markdown
<!--
Version: 2.1.0
Last Updated: 2025-01-15
Changes:
- Added support for quarterly compounding
- Fixed edge case with zero interest rate
- Improved error messages for negative values
-->
```

### Anti-Pattern 8: Hardcoding Paths

**Bad**:
```markdown
## Instructions

Run: `python /Users/alice/scripts/validate.py <file>`
```

**Good**:
```markdown
## Instructions

Run: `python scripts/validate.py <file>`

*Note: Script is in the same directory as this skill file*
```

## Skill Organization

### Naming Conventions

**Skill Directory Names**:
- ✅ Use lowercase with hyphens: `financial-calculator`
- ❌ Not underscores: `financial_calculator`
- ❌ Not camelCase: `financialCalculator`
- ❌ Not spaces: `financial calculator`

**File Names**:
- `SKILL.md` - Main instructions (required, case-sensitive)
- `README.md` - Human-readable documentation (optional)
- `reference.md`, `examples.md`, `style-guide.md` - Supporting docs
- `scripts/` - Directory for executable scripts
- `templates/` - Directory for output templates
- `tmp/` - Directory for temporary files (should be gitignored)

### Directory Structure Examples

**Simple Skill**:
```
compound-interest/
├── SKILL.md
└── README.md
```

**Standard Skill**:
```
git-commit-helper/
├── SKILL.md
├── README.md
├── examples.md
└── .gitignore
```

**Complex Skill**:
```
code-reviewer/
├── SKILL.md
├── README.md
├── .gitignore
├── reference/
│   ├── style-guide.md
│   ├── security-checklist.md
│   └── anti-patterns.md
├── scripts/
│   ├── lint.py
│   └── security-scan.py
├── templates/
│   └── review-report.md
└── tmp/              # Gitignored
```

### Documentation Standards

**README.md Template**:
```markdown
# Skill Name

Brief description of what this skill does.

## Purpose

Why this skill exists and what problems it solves.

## Usage

How Claude activates and uses this skill.

### Example Interactions

**User**: "Example query that triggers skill"
**Claude**: [Shows typical response]

## Features

- Feature 1
- Feature 2
- Feature 3

## Limitations

- Does NOT handle X
- Maximum Y
- Requires Z

## Files

- `SKILL.md` - Main instructions
- `reference.md` - Detailed reference material
- `scripts/validate.py` - Validation automation

## Version History

### v1.1.0 (2025-01-15)
- Added feature X
- Fixed issue Y

### v1.0.0 (2025-01-01)
- Initial release

## Maintainers

- Alice (@alice) - Creator
- Bob (@bob) - Contributor
```

### .gitignore for Skills

```gitignore
# Temporary files
tmp/
*.tmp
*.cache

# Python
__pycache__/
*.py[cod]
*.so
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Test outputs
test-output/
*.test.md

# Credentials (extra safety)
.env
*.key
*.pem
credentials.*
```

## Team Collaboration

### Sharing Skills via Git

**Project Skills** (shared with team):

```bash
# Create project skill
mkdir -p .claude/skills/team-code-standards
cd .claude/skills/team-code-standards

# Create skill files
cat > SKILL.md << 'EOF'
---
name: team-code-standards
description: Enforce team coding standards for Python projects. Use when reviewing code or providing feedback.
---
[Instructions]
EOF

# Commit to repository
git add .claude/skills/team-code-standards
git commit -m "feat(skills): add team code standards skill"
git push

# Team members automatically get the skill when they pull
```

**Personal Skills** (not shared):

```bash
# Create personal skill
mkdir -p ~/.claude/skills/my-preferences
cd ~/.claude/skills/my-preferences

# This stays local, not committed to project repo
```

### Versioning Skills

**Semantic Versioning for Skills**:
- **Major** (v2.0.0): Breaking changes to behavior
- **Minor** (v1.1.0): New features, backward compatible
- **Patch** (v1.0.1): Bug fixes, minor improvements

**In SKILL.md**:
```markdown
<!--
version: 1.2.0
-->
```

**Changelog Approach**:
```markdown
## Changelog

### v1.2.0 (2025-01-15)
**Added**:
- Support for async/await validation
- New security check for async race conditions

**Fixed**:
- False positive for list comprehensions

**Changed**:
- Improved error messages for validation failures

### v1.1.0 (2025-01-01)
**Added**:
- Type hint validation
- Docstring completeness check
```

### Pull Request Template for Skills

```markdown
## Skill Change Summary

**Skill Name**: `skill-name`
**Change Type**: [Feature / Bug Fix / Breaking Change]
**Version**: v1.2.0 → v1.3.0

## Description

Brief description of what changed and why.

## Changes

- [ ] Updated `SKILL.md` with new instructions
- [ ] Added examples to `examples.md`
- [ ] Updated `README.md` documentation
- [ ] Tested across Haiku, Sonnet, Opus

## Testing

### Test Case 1: [Description]
**Input**: [Example input]
**Expected**: [Expected behavior]
**Result**: ✅ Pass / ❌ Fail

### Test Case 2: [Description]
**Input**: [Example input]
**Expected**: [Expected behavior]
**Result**: ✅ Pass / ❌ Fail

## Breaking Changes

[ ] Yes - Describe what breaks and migration path
[X] No

## Checklist

- [ ] Skill description updated if behavior changed
- [ ] Examples reflect new behavior
- [ ] Documentation complete
- [ ] Tested with all three models
- [ ] No hardcoded secrets or credentials
- [ ] Scripts follow security best practices
- [ ] Temporary files properly gitignored
```

### Code Review Guidelines for Skills

When reviewing skill changes:

**Check Description**:
- [ ] Clear and specific?
- [ ] Includes trigger conditions?
- [ ] States limitations?
- [ ] Under 1024 characters?

**Check Instructions**:
- [ ] Concise and clear?
- [ ] Includes examples?
- [ ] Handles edge cases?
- [ ] Error scenarios covered?

**Check Security** (if scripts included):
- [ ] Input validation present?
- [ ] No hardcoded secrets?
- [ ] Safe file handling?
- [ ] Dependencies specified (PEP 723)?

**Check Organization**:
- [ ] Files properly named?
- [ ] .gitignore includes tmp/?
- [ ] README.md up to date?
- [ ] Version documented?

### Skill Ownership Models

**Model 1: Centralized** (one maintainer):
```markdown
## Maintainer

- Alice (@alice) - Primary maintainer
- Contact for questions: alice@company.com

## Contributing

Submit PRs to @alice for review. Please include test cases.
```

**Model 2: Distributed** (team owned):
```markdown
## Maintainers

- Team: Platform Engineering (@platform-eng)
- CODEOWNERS: .claude/skills/code-standards/

## Contributing

Any team member can update. PRs require 1 approval.
```

**Model 3: Community** (open collaboration):
```markdown
## Maintainers

Open to contributions from all developers.

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit PR with test cases
4. Minimum 2 approvals required
```

### Skill Discovery Documentation

Help team members discover available skills:

**In repository root** (`SKILLS.md`):
```markdown
# Available Skills

## Code Quality

### `python-code-reviewer`
**Location**: `.claude/skills/python-code-reviewer/`
**Purpose**: Review Python code for PEP 8, security, and best practices
**Triggers**: "review code", "code quality", "security scan"
**Maintainer**: @alice

### `team-code-standards`
**Location**: `.claude/skills/team-code-standards/`
**Purpose**: Enforce team-specific coding conventions
**Triggers**: "code review", "standards check"
**Maintainer**: @platform-eng

## Documentation

### `api-doc-generator`
**Location**: `.claude/skills/api-doc-generator/`
**Purpose**: Generate OpenAPI/Swagger documentation
**Triggers**: "API docs", "generate swagger", "OpenAPI"
**Maintainer**: @bob

## Testing

### `test-generator`
**Location**: `.claude/skills/test-generator/`
**Purpose**: Generate pytest unit tests
**Triggers**: "write tests", "unit tests", "test coverage"
**Maintainer**: @charlie
```

### Migration Guides for Breaking Changes

When making breaking changes to skills:

```markdown
# Migration Guide: team-code-standards v1.x → v2.0

## Breaking Changes

### 1. Description Format Changed

**Old Behavior** (v1.x):
```yaml
description: Review code for team standards
```

**New Behavior** (v2.0):
```yaml
description: Review Python code for team PEP 8 standards, security patterns, and project conventions. Use when reviewing Python code or checking code quality.
```

**Migration**: No action needed. New version has more specific triggers.

### 2. Output Format Changed

**Old Format**:
```
Issues found:
- Line 10: Use snake_case
- Line 25: Missing docstring
```

**New Format**:
```
✅ Strengths:
  - Good use of type hints
  - Clear function names

⚠️  Issues:
  - Line 10: Use snake_case for variable names
  - Line 25: Missing docstring on public function

💡 Suggestions:
  - Consider extracting lines 15-30 into separate function
```

**Migration**: Update any scripts that parse output to handle new format.

### 3. Script Location Changed

**Old**: `validate.py` in skill root
**New**: `scripts/validate.py` in subdirectory

**Migration**: Update SKILL.md references from:
```markdown
Run: `python validate.py <file>`
```

To:
```markdown
Run: `python scripts/validate.py <file>`
```

## Upgrade Path

1. Pull latest changes: `git pull origin main`
2. Skills automatically updated (no manual steps)
3. Verify new behavior with test case:
   ```
   Ask Claude: "Review this Python code: [sample code]"
   Expect: New structured format with ✅ ⚠️ 💡 sections
   ```

## Rollback

If issues arise:
```bash
git checkout v1.9.0 -- .claude/skills/team-code-standards
```

## Questions

Contact @alice or post in #engineering-tools
```

## Summary

Effective Claude Code skills follow these principles:

**Design**:
- ✅ Concise (every word counts)
- ✅ Specific (clear behaviors and constraints)
- ✅ Focused (one skill, one purpose)

**Descriptions**:
- ✅ Action-oriented (what it does)
- ✅ Trigger-rich (when to use it)
- ✅ Bounded (what it doesn't do)

**Instructions**:
- ✅ Structured (checklists, tables, steps)
- ✅ Example-driven (show, don't just tell)
- ✅ Complete (handle edge cases and errors)

**Organization**:
- ✅ Progressive disclosure (load only what's needed)
- ✅ Clear file structure (logical organization)
- ✅ Proper versioning (track changes)

**Security**:
- ✅ Input validation (never trust user input)
- ✅ Safe file handling (prevent path traversal)
- ✅ Secrets management (environment variables)

**Collaboration**:
- ✅ Clear ownership (who maintains it)
- ✅ Good documentation (README.md, changelog)
- ✅ Version control (Git-based workflow)

**Testing**:
- ✅ Multi-model compatibility (Haiku, Sonnet, Opus)
- ✅ Test cases documented (expected behavior)
- ✅ Regression prevention (version testing)

## Next Steps

- **Practice**: Create a skill using these principles
- **Refactor**: Improve an existing skill with these patterns
- **Review**: Use the anti-patterns list to audit your skills
- **Share**: Collaborate with your team on shared skills

**Further Reading**:
- [Getting Started](01-getting-started.md) - Fundamentals
- [Creating Your First Skill](02-creating-your-first-skill.md) - Step-by-step guide
- [Official Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) - Skills API reference
