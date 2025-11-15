# Creating Your First Skill

This guide walks you through creating a production-quality Claude Code skill from scratch, covering all aspects of skill development.

## Table of Contents

1. [Planning Your Skill](#planning-your-skill)
2. [File Structure](#file-structure)
3. [Writing SKILL.md](#writing-skillmd)
4. [Adding Supporting Files](#adding-supporting-files)
5. [Testing Your Skill](#testing-your-skill)
6. [Iteration and Refinement](#iteration-and-refinement)

## Planning Your Skill

Before writing any code, answer these questions:

### 1. What problem does this skill solve?

**Good**: "Help users write conventional commit messages that follow team standards"
**Bad**: "Help with git stuff"

### 2. When should Claude use this skill?

**Good**: "When the user is about to commit code, asks for help with commit messages, or mentions git commits"
**Bad**: "When working with git" (too broad)

### 3. What information does Claude need?

**Good**: Commit message format, examples, team conventions, anti-patterns
**Bad**: Entire git documentation (too much context)

### 4. Can this be automated with a script?

**When to include scripts:**
- ✅ Fragile operations (complex regex, API calls with retry logic)
- ✅ Mathematical calculations
- ✅ File format conversions
- ✅ Security-sensitive operations

**When to use plain instructions:**
- ✅ Content generation (writing, explaining)
- ✅ Analytical tasks (reviewing, suggesting)
- ✅ Creative tasks (brainstorming, designing)

## File Structure

### Minimal Skill (Single File)

```
skill-name/
└── SKILL.md              # Only required file
```

**Best for:**
- Simple instructions
- Content generation
- No external dependencies

### Standard Skill (Multi-File)

```
skill-name/
├── SKILL.md              # Core instructions
├── reference.md          # Supporting documentation
├── examples.md           # Code/content examples
└── script.py             # Optional automation
```

**Best for:**
- Moderate complexity
- Needs reference materials
- Benefits from examples

### Advanced Skill (Full Structure)

```
skill-name/
├── SKILL.md              # Core instructions
├── .gitignore           # Ignore tmp/ and cache
├── reference/           # Reference materials
│   ├── style-guide.md
│   └── glossary.md
├── scripts/             # Automation scripts
│   ├── validate.py
│   └── format.sh
├── templates/           # Reusable templates
│   └── output.md
└── tmp/                 # Temporary files (gitignored)
```

**Best for:**
- Complex workflows
- Multiple sub-tasks
- Team-shared skills requiring standards

## Writing SKILL.md

### Basic Template

```markdown
---
name: skill-name-here
description: Clear description of what this skill does and when to use it. Include both functionality and trigger conditions. Maximum 1024 characters.
---

# Skill Title

## Purpose
One-paragraph explanation of why this skill exists.

## When to Use
- Bullet points of scenarios
- When user mentions X
- When task involves Y

## Instructions

### Step 1: Gather Information
What Claude needs from the user.

### Step 2: Process
How Claude should handle the information.

### Step 3: Output
How Claude should present results.

## Examples

### Example 1: [Scenario]
**Input**: User request example
**Output**: What Claude should produce

## Edge Cases
- How to handle missing information
- Error conditions
- Alternative flows
```

### Frontmatter Deep Dive

#### name

**Requirements:**
- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags (`<`, `>`, `&`)
- No reserved words ("anthropic", "claude")

**Best Practices:**
- Use gerund form (verb + -ing): `analyzing-data`, `processing-pdfs`
- Be descriptive: `git-conventional-commits` not `git-helper`
- Use hyphens, not underscores: `code-review` not `code_review`

**Examples:**
```yaml
✅ name: generating-commit-messages
✅ name: analyzing-financial-statements
✅ name: pdf-form-filler
❌ name: GitCommitHelper (uppercase)
❌ name: git_commit (underscores)
❌ name: anthropic-skill (reserved word)
```

#### description

**Requirements:**
- Maximum 1024 characters
- Non-empty
- No XML tags

**Best Practices:**
- First sentence: What the skill does
- Second sentence: When to use it
- Include trigger keywords Claude should look for
- Be specific about scope and limitations

**Template:**
```yaml
description: [Action verb] [what] to [outcome]. Use when the user [trigger conditions]. Supports [specific capabilities]. Does not handle [limitations].
```

**Examples:**

✅ **Good**:
```yaml
description: Generate conventional commit messages following team standards (feat, fix, docs, etc.). Use when the user is about to commit code, asks for commit message help, or mentions 'git commit'. Analyzes staged changes and suggests appropriate scope and type.
```

❌ **Bad**:
```yaml
description: Helps with git
```
*Why bad: Vague, no trigger conditions, unclear scope*

✅ **Good**:
```yaml
description: Extract text and tables from PDF files, fill PDF forms programmatically, and merge multiple PDF documents. Use when user mentions PDF files, needs to process PDFs, or wants to extract data from documents. Requires PyPDF2 or pdfplumber.
```

❌ **Bad**:
```yaml
description: PDF processing tool for various PDF-related tasks and operations
```
*Why bad: Generic, no specific capabilities, missing trigger conditions*

### Writing Effective Instructions

#### Be Concise

Remember: Skills share the context window with conversation history.

**Before** (wordy):
```markdown
## Instructions

In order to help the user with their compound interest calculations, you should
first ask them to provide the following pieces of information that are necessary
for computing the compound interest formula...
```

**After** (concise):
```markdown
## Instructions

1. **Gather required inputs**:
   - Principal amount (P)
   - Annual interest rate (r)
   - Compounding frequency (n)
   - Time period in years (t)
```

#### Use Clear Structure

**Checkboxes for workflows:**
```markdown
## Workflow

- [ ] Step 1: Read the user's request
- [ ] Step 2: Identify required parameters
- [ ] Step 3: Calculate using formula
- [ ] Step 4: Present results with explanation
```

**Numbered lists for sequences:**
```markdown
## Process

1. Parse the input file
2. Extract relevant data
3. Apply transformations
4. Generate output
```

**Bullet points for options:**
```markdown
## Output Formats

- **Summary**: Brief overview (1-2 sentences)
- **Detailed**: Full analysis with examples
- **Technical**: Include formulas and calculations
```

#### Provide Examples

Examples help Claude understand expected behavior:

```markdown
## Examples

### Example 1: Basic Calculation

**User**: "Calculate compound interest on $1,000 at 5% for 2 years, compounded annually"

**Response**:
```
Principal (P) = $1,000
Rate (r) = 5% = 0.05
Compounding (n) = 1 (annually)
Time (t) = 2 years

A = 1000(1 + 0.05/1)^(1×2)
A = 1000(1.05)^2
A = $1,102.50

Interest earned: $102.50
```
```

#### Address Edge Cases

```markdown
## Edge Cases

### Missing Information
If the user doesn't provide the interest rate, ask: "What is the annual interest rate?"

### Invalid Input
If the rate is negative, explain: "Interest rates must be positive. Did you mean X%?"

### Assumptions
If compounding frequency not specified, assume annually (n=1) and inform the user.
```

## Adding Supporting Files

### When to Add Supporting Files

**Add reference files when:**
- Instructions would exceed 500 lines
- Content contains detailed examples or templates
- Information is reference material (glossaries, style guides)
- You want progressive disclosure of complex information

**Add scripts when:**
- Operations require precise execution (regex, calculations)
- External tool integration (APIs, file parsing)
- Security-sensitive operations
- Complex data transformations

### Reference File Example

**SKILL.md:**
```markdown
---
name: code-reviewer
description: Review code against team standards for style, security, and best practices. Use when user asks for code review or submits code changes.
---

# Code Review Skill

## Instructions

1. Read the code submission
2. Check against standards in `style-guide.md`
3. Review security checklist in `security-checklist.md`
4. Generate structured feedback

## Review Process

For detailed standards, refer to:
- **Style Guide**: `style-guide.md` - Formatting and naming conventions
- **Security Checklist**: `security-checklist.md` - Common vulnerabilities
- **Best Practices**: `best-practices.md` - Design patterns and anti-patterns
```

**style-guide.md** (separate file):
```markdown
# Team Code Style Guide

## Naming Conventions

### Variables
- Use camelCase for variables: `userName`, `totalCount`
- Use descriptive names: `userList` not `ul`
- Avoid single letters except loop counters

### Functions
- Use verb-noun pattern: `getUserData()`, `calculateTotal()`
- Be specific: `validateEmailFormat()` not `validate()`

## Formatting

- Indentation: 2 spaces (no tabs)
- Line length: 100 characters maximum
- Brace style: K&R (opening brace on same line)

[... more detailed guidelines ...]
```

### Script Integration Example

**SKILL.md:**
```markdown
---
name: notebook-validator
description: Validate Jupyter notebooks for security issues, code quality, and structure. Use when reviewing notebooks or checking for common issues.
---

# Notebook Validation Skill

## Instructions

1. Run automated checks: `python validate.py <notebook.ipynb>`
2. Review the validation report in `tmp/validation-report.md`
3. Manually check items not covered by automation
4. Provide structured feedback to user

## Automated Checks

The `validate.py` script checks for:
- Hardcoded API keys or secrets
- Missing documentation cells
- Code without explanations
- Deprecated patterns
```

**validate.py** (separate file with PEP 723 metadata):
```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "detect-secrets",
#     "nbformat",
#     "nbconvert",
# ]
# ///
"""
Validate Jupyter notebooks for common issues.
"""

import sys
import json
from pathlib import Path

def validate_notebook(notebook_path):
    """Run validation checks on a notebook."""
    with open(notebook_path) as f:
        nb = json.load(f)

    issues = []

    # Check for secrets
    # (implementation details)

    # Check for documentation
    # (implementation details)

    return issues

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate.py <notebook.ipynb>")
        sys.exit(1)

    issues = validate_notebook(sys.argv[1])

    # Write report to tmp/
    Path("tmp").mkdir(exist_ok=True)
    with open("tmp/validation-report.md", "w") as f:
        f.write(format_report(issues))

    print(f"Validation complete. Report: tmp/validation-report.md")
```

### .gitignore for Skills

```gitignore
# Temporary files
tmp/

# Python cache
__pycache__/
*.pyc
*.pyo

# Virtual environments (if used)
venv/
.venv/

# OS files
.DS_Store
Thumbs.db
```

## Testing Your Skill

### Testing Strategy

#### 1. Syntax Validation

```bash
# Check YAML frontmatter
python3 << 'EOF'
import yaml
with open('.claude/skills/my-skill/SKILL.md') as f:
    content = f.read()
    if content.startswith('---'):
        yaml_content = content.split('---')[1]
        try:
            metadata = yaml.safe_load(yaml_content)
            print(f"✓ Valid YAML")
            print(f"  name: {metadata.get('name')}")
            print(f"  description: {metadata.get('description')}")
        except yaml.YAMLError as e:
            print(f"✗ YAML Error: {e}")
EOF
```

#### 2. Discovery Testing

```bash
# Enable debug mode
claude --debug

# Start conversation
# You should see:
# [DEBUG] Loading skills from ~/.claude/skills/
# [DEBUG] Found skill: my-skill
```

#### 3. Activation Testing

Create test cases that should trigger your skill:

```markdown
# Test Cases for git-commit-message skill

## Should Activate
- "I need to write a commit message"
- "Can you help me commit this code?"
- "Generate a commit message for these changes"

## Should NOT Activate
- "How do I use git?"
- "Explain git branches"
- "Create a new repository"
```

Run each test case and verify Claude uses the skill.

#### 4. Functionality Testing

Test the skill's actual behavior:

```markdown
# Functionality Tests

## Test 1: Standard commit
Input: "I added a new user authentication feature"
Expected: `feat(auth): add user authentication feature`

## Test 2: Bug fix
Input: "Fixed the login redirect issue"
Expected: `fix(auth): resolve login redirect issue`

## Test 3: Missing information
Input: "I made some changes"
Expected: Claude asks for details about the changes
```

#### 5. Edge Case Testing

```markdown
# Edge Cases

## Empty description
Input: User provides no details
Expected: Claude prompts for more information

## Multiple scopes
Input: Changes span multiple areas
Expected: Claude suggests the primary scope or asks user to choose

## Non-standard changes
Input: Changes don't fit standard types
Expected: Claude uses 'chore' or asks user
```

### Testing Checklist

Before considering your skill complete:

- [ ] **YAML valid**: No syntax errors in frontmatter
- [ ] **Name valid**: Lowercase, hyphens only, under 64 chars
- [ ] **Description specific**: Includes what AND when
- [ ] **Triggers correctly**: Activates for appropriate queries
- [ ] **Doesn't over-trigger**: Stays dormant for irrelevant queries
- [ ] **Instructions clear**: Claude follows them consistently
- [ ] **Examples helpful**: Demonstrates expected behavior
- [ ] **Edge cases handled**: Graceful handling of missing/invalid input
- [ ] **Scripts work**: (if applicable) Execute without errors
- [ ] **Context-efficient**: No unnecessary verbosity
- [ ] **Multiple models**: Test with Haiku, Sonnet, and Opus

## Iteration and Refinement

### Common Issues and Solutions

#### Issue: Skill doesn't activate when expected

**Diagnosis:**
```bash
claude --debug
# Look for: [DEBUG] Evaluating skill: my-skill
# If missing, description doesn't match user query
```

**Solutions:**
1. Add more trigger keywords to description
2. Make description more specific
3. Test with exact phrases from user queries

**Before**:
```yaml
description: Help with PDF files
```

**After**:
```yaml
description: Extract text and tables from PDF files, fill PDF forms, and merge PDFs. Use when user mentions 'PDF', 'extract from PDF', 'PDF form', or 'merge PDFs'.
```

#### Issue: Skill activates too often

**Diagnosis:**
Claude uses the skill for unrelated queries.

**Solutions:**
1. Make description more specific
2. Add explicit scope limitations
3. Mention what the skill does NOT handle

**Before**:
```yaml
description: Process documents and files
```

**After**:
```yaml
description: Process PDF files only (extract text, fill forms, merge). Use when user mentions PDF files specifically. Does NOT handle Word, Excel, or other document formats.
```

#### Issue: Instructions unclear to Claude

**Diagnosis:**
Claude doesn't follow the workflow or produces inconsistent results.

**Solutions:**
1. Add explicit examples
2. Use checkboxes for workflows
3. Reduce ambiguity in language
4. Test with multiple models

**Before**:
```markdown
## Instructions
Help the user with their calculation.
```

**After**:
```markdown
## Instructions

1. Identify the calculation type (compound interest, simple interest, etc.)
2. Request missing parameters
3. Apply the formula: A = P(1 + r/n)^(nt)
4. Show step-by-step calculation
5. Present final result with explanation

Example:
[Show complete example]
```

#### Issue: Skill uses too much context

**Diagnosis:**
Long conversations fill context window, skill stops working.

**Solutions:**
1. Reduce verbosity in SKILL.md
2. Move detailed content to separate files
3. Remove unnecessary examples
4. Use progressive disclosure

**Before** (in SKILL.md):
```markdown
## Compound Interest Formula

Compound interest is the interest calculated on the initial principal and also
on the accumulated interest of previous periods. It can be thought of as
"interest on interest" and will make a sum grow faster than simple interest...

[500 more lines of explanation]
```

**After** (SKILL.md references separate file):
```markdown
## Formula

Use: A = P(1 + r/n)^(nt)

For detailed explanation, see `compound-interest-theory.md`.
```

### Refinement Process

```
1. Deploy skill
     ↓
2. Use in real conversations
     ↓
3. Identify issues
     ↓
4. Update SKILL.md or supporting files
     ↓
5. Test changes
     ↓
6. Repeat
```

**Metrics to track:**
- **Activation accuracy**: Does it activate when needed?
- **False positives**: Does it activate unnecessarily?
- **Instruction adherence**: Does Claude follow the workflow?
- **User satisfaction**: Does it solve the problem effectively?

### Versioning Your Skill

For project skills (.claude/skills/), use Git:

```bash
# Document skill changes in commits
git add .claude/skills/my-skill/
git commit -m "feat(skills): improve my-skill activation triggers

- Add more specific keywords to description
- Include examples for edge cases
- Update instructions for clarity"

# Tag stable versions
git tag -a skill-my-skill-v1.0 -m "Stable version of my-skill"
```

For API skills, use the Skills API versioning:

```python
# Create new version
new_version = client.beta.skills.versions.create(
    skill_id="your-skill-id",
    files=files_from_dir("./my-skill/"),
    betas=["skills-2025-10-02"]
)

# Use "latest" in development
# Pin to specific version in production
```

## Next Steps

You now know how to create a complete, production-ready skill!

**Continue learning:**
- **[Best Practices](03-best-practices.md)** - Advanced design patterns
- **[API Skills](04-api-skills.md)** - Upload and manage skills via API
- **[Advanced Techniques](05-advanced-techniques.md)** - Testing, deployment, multi-file skills

**Try building:**
1. A skill for a task you do frequently
2. A skill that uses a script for automation
3. A multi-file skill with progressive disclosure
4. A team-shared skill in your project repository

Remember: The best way to learn is by building! Start with a simple skill and iterate based on real usage.
