# Getting Started with Claude Code Skills

This guide will help you understand Claude Code skills and set up your first skill.

## Table of Contents

1. [What Are Skills?](#what-are-skills)
2. [Types of Skills](#types-of-skills)
3. [How Skills Work](#how-skills-work)
4. [Setup and Installation](#setup-and-installation)
5. [Your First Skill](#your-first-skill)
6. [Verifying Your Skill](#verifying-your-skill)

## What Are Skills?

**Skills** are modular capabilities that extend Claude's functionality. They consist of:

- **Instructions**: Markdown files (SKILL.md) telling Claude how to perform tasks
- **Scripts**: Optional executable code for automation
- **Resources**: Optional reference materials, templates, or data files

### Key Benefits

✅ **Reusable**: Write once, use across many conversations
✅ **Automatic**: Claude decides when to use them (no manual activation)
✅ **Shareable**: Team members can use the same skills via version control
✅ **Efficient**: Progressive loading optimizes context window usage

### Real-World Examples

- **Brand Guidelines**: Ensure all generated content follows company branding
- **Code Review**: Automated checks against team coding standards
- **Document Generation**: Create Excel reports, PowerPoint slides, or PDF forms
- **Data Analysis**: Apply domain-specific analysis techniques
- **Financial Calculations**: Compute ratios, forecasts, and benchmarks

## Types of Skills

### Claude Code Skills (Filesystem-based)

**Location**: `~/.claude/skills/` (personal) or `.claude/skills/` (project)

**Characteristics**:
- Stored as directories on your filesystem
- Automatically discovered by Claude Code
- Can include local scripts and resources
- Free to create and use
- Available in: Claude Code CLI, IDE extensions, Agent SDK

**Best for**:
- Personal productivity tools
- Team-shared project skills
- Local development workflows
- Custom automation scripts

### API Skills (Uploaded)

**Location**: Uploaded to Anthropic's platform via API

**Characteristics**:
- Managed remotely with versioning
- Run in isolated execution containers
- Available via API calls with `container` parameter
- Includes pre-built Anthropic skills (Excel, PowerPoint, PDF, Word)

**Best for**:
- Production applications
- Multi-tenant SaaS platforms
- Centralized skill management
- Leveraging pre-built document generation skills

### Comparison

| Feature | Claude Code Skills | API Skills |
|---------|-------------------|------------|
| **Storage** | Local filesystem | Anthropic platform |
| **Discovery** | Automatic (filesystem scan) | Explicit (skill_id reference) |
| **Versioning** | Git-based | API-managed |
| **Execution** | Local environment | Isolated container |
| **Cost** | Free | Included in API usage |
| **Network Access** | Yes (can run local scripts) | No (isolated) |
| **Package Install** | Yes (local) | No (pre-installed only) |
| **Sharing** | Git repository | API skill_id |

## How Skills Work

### Discovery and Loading

Claude Code uses a **progressive disclosure** strategy:

```
┌─────────────────────────────────────────────────────────┐
│ 1. STARTUP: Load Metadata (name + description)         │
│    → Minimal context usage                              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 2. ACTIVATION: Load SKILL.md Instructions               │
│    → When description matches user request              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 3. ON-DEMAND: Load Supporting Files                     │
│    → Only when explicitly referenced in instructions    │
└─────────────────────────────────────────────────────────┘
```

### Activation Triggers

Claude activates skills based on **description matching**:

**Example Skill:**
```yaml
---
name: pdf-processor
description: Extract text and tables from PDF files, fill PDF forms, and merge PDF documents. Use when the user mentions PDF files or needs to process, analyze, or manipulate PDFs.
---
```

**User requests that trigger activation:**
- ✅ "Can you extract data from this PDF?"
- ✅ "I need to fill out this PDF form"
- ✅ "Merge these three PDF documents"
- ❌ "Can you analyze this spreadsheet?" (different domain)

**Pro Tip**: The description should include both **what** the skill does AND **when** to use it.

### Context Window Sharing

Skills share Claude's context window with:
- Conversation history
- Other active skills
- System instructions
- Tool definitions

**Implication**: Keep skills concise! Every word in SKILL.md reduces available space for conversation.

## Setup and Installation

### Prerequisites

**Option 1: Claude Code CLI**
```bash
# Install Claude Code (if not already installed)
# Visit: https://docs.claude.com/en/docs/claude-code

# Verify installation
claude --version
```

**Option 2: IDE Extension**
- Install Claude Code extension for VSCode, Cursor, or other supported IDEs
- Extension automatically discovers skills in workspace

**Option 3: Agent SDK**
```bash
pip install anthropic-agent-sdk
```

### Skill Directory Setup

**Personal Skills** (available across all projects):
```bash
# Create personal skills directory
mkdir -p ~/.claude/skills

# Verify it exists
ls -la ~/.claude/skills
```

**Project Skills** (shared with team via git):
```bash
# Navigate to your project
cd /path/to/your/project

# Create project skills directory
mkdir -p .claude/skills

# Commit to version control
git add .claude/skills
git commit -m "feat: add skills directory"
```

### Choosing Personal vs. Project Skills

**Use Personal Skills (`~/.claude/skills/`) when:**
- Skill is specific to your workflow
- Not relevant to team members
- Contains personal preferences or credentials
- For experimentation and learning

**Use Project Skills (`.claude/skills/`) when:**
- Skill enforces team standards (code review, formatting)
- Multiple team members benefit
- Part of project workflow (build scripts, deployment)
- Should be version controlled

## Your First Skill

Let's create a simple skill that calculates compound interest.

### Step 1: Create the Directory

```bash
# For personal use
mkdir -p ~/.claude/skills/compound-interest

# Or for project use
mkdir -p .claude/skills/compound-interest
```

### Step 2: Create SKILL.md

Create `.claude/skills/compound-interest/SKILL.md`:

```markdown
---
name: compound-interest
description: Calculate compound interest for investments and loans. Use when the user asks about investment growth, loan calculations, compound interest, or future value of money.
---

# Compound Interest Calculator

## Purpose
Calculate compound interest to determine future value of investments or loans.

## Formula
```
A = P(1 + r/n)^(nt)

Where:
- A = Final amount
- P = Principal (initial amount)
- r = Annual interest rate (as decimal)
- n = Number of times interest compounds per year
- t = Time in years
```

## Instructions

When asked to calculate compound interest:

1. **Gather information**:
   - Principal amount (P)
   - Annual interest rate (r) - convert percentage to decimal
   - Compounding frequency (n): annually=1, semi-annually=2, quarterly=4, monthly=12, daily=365
   - Time period in years (t)

2. **Calculate**:
   - Apply the formula: A = P(1 + r/n)^(nt)
   - Calculate total interest: Interest = A - P
   - Calculate percentage gain: Gain% = (Interest / P) × 100

3. **Present results**:
   - Show the formula with values substituted
   - Display the calculation step-by-step
   - Present final amount (A)
   - Show total interest earned/paid
   - Show percentage gain/cost

## Example

**User asks**: "If I invest $10,000 at 5% annual interest compounded monthly for 10 years, how much will I have?"

**Response**:
```
Principal (P) = $10,000
Annual Rate (r) = 5% = 0.05
Compounding (n) = 12 (monthly)
Time (t) = 10 years

Using the formula: A = P(1 + r/n)^(nt)
A = 10,000(1 + 0.05/12)^(12×10)
A = 10,000(1.004167)^120
A = 10,000(1.64701)
A = $16,470.10

Results:
- Final Amount: $16,470.10
- Total Interest: $6,470.10
- Percentage Gain: 64.70%
```

## Edge Cases

- If compounding frequency not specified, assume annually (n=1)
- If time period not specified, ask user
- For continuous compounding, use formula: A = Pe^(rt)
```

### Step 3: Save and Test

Save the file, then test it with Claude Code:

```bash
# Start Claude Code
claude

# Test with a query
> "I want to invest $5,000 at 4% interest compounded quarterly for 5 years. How much will I have?"
```

Claude should automatically activate the `compound-interest` skill and provide a detailed calculation!

## Verifying Your Skill

### Method 1: Debug Mode

Enable debug mode to see skill loading:

```bash
claude --debug
```

You'll see output like:
```
[DEBUG] Loading skills from ~/.claude/skills/
[DEBUG] Found skill: compound-interest
[DEBUG] Loaded metadata: name=compound-interest, description=Calculate compound...
```

### Method 2: List Skills

Ask Claude directly:
```
> "What skills do you have available?"
```

Claude will list all discovered skills including yours.

### Method 3: Trigger Activation

Use language from your skill description:
```
> "Can you help me calculate compound interest?"
```

Claude should activate the skill and reference it in the response.

### Common Issues

**Skill not discovered:**
- ✓ Check file is named exactly `SKILL.md` (case-sensitive)
- ✓ Verify directory is in `~/.claude/skills/` or `.claude/skills/`
- ✓ Ensure YAML frontmatter is properly formatted
- ✓ Restart Claude Code to refresh skill discovery

**Skill not activating:**
- ✓ Make description more specific and include trigger words
- ✓ Use language from the description in your query
- ✓ Verify description explains WHEN to use the skill
- ✓ Check that `name` field uses only lowercase, numbers, and hyphens

**YAML errors:**
- ✓ Ensure proper syntax: `key: value`
- ✓ Use quotes for multi-line descriptions if needed
- ✓ Check for invalid characters in `name` field
- ✓ Validate with online YAML checker

## Next Steps

Now that you have a working skill:

1. **Experiment**: Modify the skill and see how Claude's behavior changes
2. **Add complexity**: Try adding a Python script for the calculation
3. **Learn best practices**: Read [Best Practices Guide](03-best-practices.md)
4. **Study examples**: Explore the [examples](examples/) directory
5. **Create more skills**: Identify tasks you do frequently and create skills for them

### Skill Ideas to Try

**For Developers:**
- `git-commit-message` - Generate conventional commit messages
- `code-review-checklist` - Apply team code review standards
- `test-case-generator` - Create unit test templates

**For Writers:**
- `blog-post-outline` - Create structured outlines
- `seo-optimizer` - Check content for SEO best practices
- `tone-checker` - Ensure content matches brand voice

**For Analysts:**
- `data-summary-stats` - Calculate statistical measures
- `chart-recommender` - Suggest appropriate chart types
- `trend-analyzer` - Identify patterns in data

**For Business:**
- `meeting-notes-formatter` - Structure meeting notes
- `email-responder` - Draft professional emails
- `project-risk-assessor` - Identify project risks

---

**Ready for more?** Continue to [Creating Your First Skill](02-creating-your-first-skill.md) for a deeper dive into skill development!
