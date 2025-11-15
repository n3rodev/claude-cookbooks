# API Skills: Complete Guide

This comprehensive guide covers creating, uploading, and managing skills through the Anthropic API. Learn how to build production-ready custom skills and leverage pre-built Anthropic skills for document generation.

## Table of Contents

1. [API Skills Overview](#api-skills-overview)
2. [Prerequisites and Setup](#prerequisites-and-setup)
3. [Creating and Uploading Skills](#creating-and-uploading-skills)
4. [Using Pre-built Anthropic Skills](#using-pre-built-anthropic-skills)
5. [Version Management](#version-management)
6. [Container Management](#container-management)
7. [Skills API Reference](#skills-api-reference)
8. [File Handling](#file-handling)
9. [Beta Headers and Parameters](#beta-headers-and-parameters)
10. [Production Best Practices](#production-best-practices)
11. [Limitations](#limitations)
12. [Complete Working Examples](#complete-working-examples)

## API Skills Overview

### What are API Skills?

**API Skills** are specialized capabilities that you can upload to and manage via the Anthropic platform. They give Claude access to instructions, code, and resources for specific tasks, allowing you to build production-ready applications with domain expertise.

### API Skills vs Filesystem Skills

| Feature | **API Skills** | **Filesystem Skills** |
|---------|---------------|----------------------|
| **Storage** | Anthropic's platform (cloud) | Local filesystem |
| **Access Method** | API with `skill_id` reference | Automatic discovery from `~/.claude/skills/` |
| **Execution Environment** | Isolated containers | Local environment |
| **Versioning** | API-managed with epochs | Git-based |
| **Network Access** | ❌ No (isolated sandbox) | ✅ Yes |
| **Package Installation** | ❌ No (pre-installed only) | ✅ Yes (local) |
| **Use Case** | Production apps, SaaS platforms | Personal productivity, local dev |
| **Cost** | Included in API usage | Free (local only) |
| **Sharing** | API `skill_id` | Git repository |
| **Pre-built Skills** | ✅ Anthropic-managed (Excel, PowerPoint, PDF, Word) | ❌ Build your own |
| **Best For** | Multi-tenant apps, production, document generation | Personal tools, local automation |

### When to Use API Skills

**Choose API Skills when:**
- Building production applications or SaaS platforms
- Need centralized skill management
- Want to use pre-built document generation skills (Excel, PowerPoint, PDF, Word)
- Require versioned, auditable skill deployments
- Building multi-tenant applications where each customer has custom skills
- Need isolated execution for security

**Choose Filesystem Skills when:**
- Working locally with Claude Code CLI or IDE extensions
- Building personal productivity tools
- Sharing skills via Git with your team
- Need network access or custom package installation
- Developing and testing skills before uploading

### Key Features

- **Pre-built Anthropic Skills**: Excel, PowerPoint, PDF, Word document generation
- **Custom Skills**: Upload your own instructions and code
- **Version Control**: Create, list, update, and delete skill versions
- **Container Reuse**: Load skills once, reuse across conversations
- **Isolated Execution**: Skills run in sandboxed environments
- **Progressive Disclosure**: Skills load incrementally to optimize token usage

## Prerequisites and Setup

### Requirements

- **Python 3.8+** (3.11 or 3.12 recommended)
- **Anthropic SDK 0.71.0+** (Skills support)
- **Anthropic API Key** from [console.anthropic.com](https://console.anthropic.com/)

### Installation

```bash
# Install the Anthropic SDK
pip install anthropic>=0.71.0

# For development with file handling
pip install anthropic python-dotenv
```

### API Key Configuration

**Option 1: Environment Variable**
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

**Option 2: .env File (Recommended)**
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." > .env
```

```python
# Load in Python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
```

**Option 3: Direct in Code (Not Recommended)**
```python
from anthropic import Anthropic

# ⚠️ Never commit API keys to version control
client = Anthropic(api_key="sk-ant-api03-...")
```

### Basic Client Setup

```python
from anthropic import Anthropic
import os

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# For Skills API, add the skills beta header
client_with_skills = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    default_headers={"anthropic-beta": "skills-2025-10-02"}
)

print("✓ Client initialized successfully")
```

### Verify Setup

```python
# Test API connection
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=100,
    messages=[{
        "role": "user",
        "content": "Say 'Setup successful!' if you can read this."
    }]
)

print(response.content[0].text)
# Output: Setup successful!
```

## Creating and Uploading Skills

### Skill Directory Structure

Before uploading, organize your skill files:

```
my-financial-analyzer/
├── SKILL.md              # Required: Core instructions
├── examples.md           # Optional: Usage examples
├── calculations.py       # Optional: Helper scripts
└── templates/            # Optional: Resources
    └── report.md
```

### SKILL.md Format

```markdown
---
name: financial-analyzer
description: Analyze financial statements to calculate key ratios (ROI, ROE, debt-to-equity, current ratio). Use when user provides financial data or asks for ratio analysis.
---

# Financial Statement Analyzer

## Purpose
Calculate and interpret key financial ratios from balance sheet and income statement data.

## Instructions

When the user provides financial data:

1. **Identify available metrics**:
   - Total Assets, Total Equity, Total Debt
   - Net Income, Revenue
   - Current Assets, Current Liabilities

2. **Calculate relevant ratios**:
   - **ROI** = (Net Income / Total Assets) × 100
   - **ROE** = (Net Income / Total Equity) × 100
   - **Debt-to-Equity** = Total Debt / Total Equity
   - **Current Ratio** = Current Assets / Current Liabilities

3. **Interpret results**:
   - Compare to industry benchmarks
   - Flag unusual values
   - Provide context

## Example

**Input**: "Analyze this company: Assets $1M, Equity $600K, Debt $400K, Net Income $80K"

**Output**:
```
Financial Analysis:

Ratios Calculated:
- ROI: 8.0% (Net Income $80K / Total Assets $1M)
- ROE: 13.3% (Net Income $80K / Total Equity $600K)
- Debt-to-Equity: 0.67 (Total Debt $400K / Total Equity $600K)

Interpretation:
- ROE of 13.3% shows healthy returns for shareholders
- Debt-to-Equity of 0.67 indicates moderate leverage
- Company appears financially stable
```

## Edge Cases
- Missing data: Ask user for required metrics
- Negative values: Flag as unusual, provide cautious analysis
- Division by zero: Handle gracefully with error message
```

### Creating a Skill from Directory

```python
from anthropic import Anthropic
from pathlib import Path
import os

client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    default_headers={"anthropic-beta": "skills-2025-10-02"}
)

def files_from_dir(directory_path: str) -> list:
    """Convert directory contents to API-compatible file list."""
    files = []
    skill_dir = Path(directory_path)

    for file_path in skill_dir.rglob("*"):
        if file_path.is_file():
            # Get relative path from skill directory
            relative_path = file_path.relative_to(skill_dir)

            with open(file_path, "rb") as f:
                files.append({
                    "name": str(relative_path),
                    "content": f.read()
                })

    return files

# Create skill from directory
skill_directory = "./my-financial-analyzer"
files = files_from_dir(skill_directory)

# Upload skill
skill = client.beta.skills.create(
    files=files,
    betas=["skills-2025-10-02"]
)

print(f"✓ Skill created!")
print(f"  Skill ID: {skill.id}")
print(f"  Name: {skill.name}")
print(f"  Version: {skill.version}")
print(f"  Description: {skill.description}")
```

### Creating a Skill from Individual Files

```python
# Create skill by manually specifying files
skill = client.beta.skills.create(
    files=[
        {
            "name": "SKILL.md",
            "content": b"""---
name: tax-calculator
description: Calculate income tax for different brackets. Use when user asks about tax calculations.
---

# Tax Calculator

## Instructions
Calculate federal income tax based on 2025 tax brackets:
- $0 - $11,000: 10%
- $11,001 - $44,725: 12%
- $44,726 - $95,375: 22%
- Over $95,375: 24%

Calculate tax by applying rates to each bracket.
"""
        },
        {
            "name": "examples.md",
            "content": b"""# Examples

## Example 1: Basic Calculation
Income: $50,000
Tax: $6,307
"""
        }
    ],
    betas=["skills-2025-10-02"]
)

print(f"Tax calculator skill created: {skill.id}")
```

### Response Structure

```python
# Skill creation response
{
    "id": "skill_01ABC123...",          # Unique skill ID
    "type": "skill",
    "source": "user",                    # "user" or "anthropic"
    "display_title": "Financial Analyzer",
    "latest_version": "1737849600000",   # Epoch timestamp
    "created_at": "2025-01-25T12:00:00Z"
}

# Version details (when retrieved)
{
    "id": "skill_01ABC123...",
    "version": "1737849600000",
    "name": "financial-analyzer",
    "description": "Analyze financial statements...",
    "files": [
        {"name": "SKILL.md", "size": 1234},
        {"name": "examples.md", "size": 567}
    ]
}
```

## Using Pre-built Anthropic Skills

Anthropic provides professionally-maintained skills for document generation:

| Skill ID | Purpose | Capabilities |
|----------|---------|--------------|
| `xlsx` | Excel workbooks | Spreadsheets, formulas, charts, formatting |
| `pptx` | PowerPoint presentations | Slides, charts, images, transitions |
| `pdf` | PDF documents | Text, tables, images, formatting |
| `docx` | Word documents | Rich text, tables, images, styles |

### Basic Usage Pattern

```python
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Use an Anthropic skill
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Create an Excel budget spreadsheet with income and expenses"
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Response includes file_id for created document
print(response.content[0].text)
```

### Excel Skill Example

```python
# Create an Excel file with formulas and charts
excel_response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": """Create a Q1 2025 sales report Excel file:

Data:
- January: $45,000
- February: $52,000
- March: $48,000

Include:
1. Monthly sales data with proper headers
2. Total sales formula
3. Average sales formula
4. A column chart showing monthly trends
5. Professional formatting
"""
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Extract and download file (covered in File Handling section)
```

### PowerPoint Skill Example

```python
# Create a presentation
ppt_response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": """Create a 3-slide PowerPoint presentation:

Slide 1: Title
- Title: "Product Launch Plan"
- Subtitle: "Q2 2025 Strategy"

Slide 2: Market Analysis
- Title: "Target Market"
- Bullet points:
  - Primary: Tech professionals 25-40
  - Secondary: Enterprise decision makers
  - Geographic focus: North America

Slide 3: Timeline
- Title: "Launch Schedule"
- Table with:
  - Month | Activity
  - April | Beta testing
  - May | Marketing campaign
  - June | Official launch

Use professional design and consistent formatting.
"""
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

### PDF Skill Example

```python
# Create a PDF document
pdf_response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "pdf", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": """Create a professional invoice PDF:

INVOICE

Acme Corporation
123 Business St, Suite 100
New York, NY 10001

Bill To:
John Smith
456 Client Ave
Boston, MA 02101

Invoice #: INV-2025-001
Date: January 25, 2025
Due Date: February 25, 2025

Services:
- Consulting Services (40 hours @ $150/hr): $6,000.00
- Project Management (20 hours @ $120/hr): $2,400.00
- Documentation: $500.00

Subtotal: $8,900.00
Tax (8%): $712.00
Total Due: $9,612.00

Payment Terms: Net 30 days
"""
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

### Word Skill Example

```python
# Create a Word document
docx_response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "docx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": """Create a Word document for a project proposal:

PROJECT PROPOSAL

Executive Summary
This proposal outlines the development of a customer analytics platform.

Project Scope
- Data collection and integration
- Real-time analytics dashboard
- Custom reporting tools

Timeline
Phase 1 (Months 1-3): Requirements and design
Phase 2 (Months 4-6): Development
Phase 3 (Months 7-8): Testing and deployment

Budget
Development: $150,000
Infrastructure: $30,000
Total: $180,000

Use professional formatting with headers and proper spacing.
"""
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

### Combining Multiple Skills

```python
# Use multiple skills in one request
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=8192,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": """Create a financial report package:

1. Excel file with quarterly revenue data and formulas
2. PowerPoint presentation summarizing the Excel data with charts

Data: Q1=$100K, Q2=$120K, Q3=$135K, Q4=$150K
"""
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Response will include file_ids for both Excel and PowerPoint files
```

## Version Management

### Understanding Skill Versions

Skills use **epoch timestamps** as version identifiers:
- Each skill upload creates a new version
- Versions are immutable (cannot be modified)
- Use `"latest"` to always get the most recent version
- Pin to specific versions for production stability

```python
# Version format: milliseconds since Unix epoch
"version": "1737849600000"  # Represents: 2025-01-25 12:00:00 UTC
```

### Creating a New Version

```python
# Create new version of existing skill
new_version = client.beta.skills.versions.create(
    skill_id="skill_01ABC123...",
    files=files_from_dir("./my-financial-analyzer-v2"),
    betas=["skills-2025-10-02"]
)

print(f"New version created: {new_version.version}")
print(f"Previous version: {skill.latest_version}")
```

### Listing All Versions

```python
# List all versions of a skill
versions = client.beta.skills.versions.list(
    skill_id="skill_01ABC123...",
    betas=["skills-2025-10-02"]
)

print(f"Found {len(versions.data)} versions:")
for version in versions.data:
    print(f"  - {version.version} (created: {version.created_at})")

# Output:
# Found 3 versions:
#   - 1737849600000 (created: 2025-01-25T12:00:00Z)
#   - 1737763200000 (created: 2025-01-24T12:00:00Z)
#   - 1737676800000 (created: 2025-01-23T12:00:00Z)
```

### Retrieving a Specific Version

```python
# Get details of a specific version
version_info = client.beta.skills.versions.retrieve(
    skill_id="skill_01ABC123...",
    version="1737849600000",  # Specific version
    betas=["skills-2025-10-02"]
)

print(f"Name: {version_info.name}")
print(f"Description: {version_info.description}")
print(f"Files: {[f.name for f in version_info.files]}")
```

### Using Specific Versions

```python
# Use a specific version (production)
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [{
            "type": "user",
            "skill_id": "skill_01ABC123...",
            "version": "1737849600000"  # Pin to specific version
        }]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Analyze this financial data..."}],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Use latest version (development)
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [{
            "type": "user",
            "skill_id": "skill_01ABC123...",
            "version": "latest"  # Always use most recent version
        }]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Analyze this financial data..."}],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

### Deleting a Version

```python
# Delete a specific version
client.beta.skills.versions.delete(
    skill_id="skill_01ABC123...",
    version="1737676800000",  # Old version to remove
    betas=["skills-2025-10-02"]
)

print("✓ Version deleted")

# Note: Cannot delete the only remaining version
# To remove a skill entirely, delete all versions or the skill itself
```

### Version Management Best Practices

```python
class SkillVersionManager:
    """Manage skill versions with semantic versioning metadata."""

    def __init__(self, client, skill_id):
        self.client = client
        self.skill_id = skill_id
        self.versions = {}  # version_epoch -> metadata

    def create_version(self, files, semantic_version=None, notes=None):
        """Create new version with metadata."""
        # Create version
        version = self.client.beta.skills.versions.create(
            skill_id=self.skill_id,
            files=files,
            betas=["skills-2025-10-02"]
        )

        # Store metadata (in your own database)
        metadata = {
            "epoch": version.version,
            "semantic": semantic_version,  # e.g., "2.1.0"
            "notes": notes,
            "created_at": version.created_at
        }
        self.versions[version.version] = metadata

        return version

    def list_versions_with_metadata(self):
        """List versions with semantic version info."""
        versions = self.client.beta.skills.versions.list(
            skill_id=self.skill_id,
            betas=["skills-2025-10-02"]
        )

        for v in versions.data:
            metadata = self.versions.get(v.version, {})
            print(f"Version {metadata.get('semantic', 'unknown')}")
            print(f"  Epoch: {v.version}")
            print(f"  Created: {v.created_at}")
            print(f"  Notes: {metadata.get('notes', 'N/A')}")
            print()

# Usage
manager = SkillVersionManager(client, "skill_01ABC123...")

# Create versioned release
manager.create_version(
    files=files_from_dir("./financial-analyzer-v2"),
    semantic_version="2.0.0",
    notes="Major update: Added ROA calculation and industry benchmarks"
)
```

## Container Management

### What are Containers?

**Containers** are isolated execution environments where skills run. They persist across messages in a conversation, allowing you to:
- Reuse loaded skills without reloading
- Maintain state between messages
- Reduce token usage by avoiding skill reloading

### Container Lifecycle

```python
# First message: Create container
response1 = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Create a budget spreadsheet"
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Extract container ID from response
container_id = response1.container.id
print(f"Container created: {container_id}")

# Second message: Reuse container
response2 = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "id": container_id  # Reuse existing container
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Now add a chart showing the budget data"
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Excel skill is still loaded, no need to reload!
```

### Container State Persistence

```python
# Multi-turn conversation with container reuse
def create_financial_report(client):
    """Create report with multiple interactions."""

    # Turn 1: Create initial spreadsheet
    response1 = client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        container={
            "skills": [
                {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
            ]
        },
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{
            "role": "user",
            "content": "Create a revenue spreadsheet for Q1-Q4: $100K, $120K, $135K, $150K"
        }],
        betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
    )

    container_id = response1.container.id
    print(f"Step 1: Spreadsheet created (container: {container_id})")

    # Turn 2: Add formulas (reuse container)
    response2 = client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        container={"id": container_id},
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{
            "role": "user",
            "content": "Add total revenue and average formulas"
        }],
        betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
    )

    print("Step 2: Formulas added")

    # Turn 3: Add visualization (reuse container)
    response3 = client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        container={"id": container_id},
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{
            "role": "user",
            "content": "Add a column chart showing quarterly growth"
        }],
        betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
    )

    print("Step 3: Chart added")

    return response3, container_id

# Skills loaded once, reused three times!
final_response, container_id = create_financial_report(client)
```

### Adding Skills to Existing Container

```python
# Start with Excel skill
response1 = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{"role": "user", "content": "Create revenue data spreadsheet"}],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

container_id = response1.container.id

# Add PowerPoint skill to same container
response2 = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "id": container_id,
        "skills": [
            {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": "Create a presentation summarizing the spreadsheet data"
    }],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)

# Container now has both xlsx and pptx skills loaded
```

### Container Cleanup

Containers have automatic cleanup, but you can manage them explicitly:

```python
class ContainerManager:
    """Manage container lifecycle."""

    def __init__(self, client):
        self.client = client
        self.active_containers = {}

    def create_container(self, skills, name=None):
        """Create new container and track it."""
        response = self.client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={"skills": skills},
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{"role": "user", "content": "Initialize container"}],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        container_id = response.container.id
        self.active_containers[container_id] = {
            "name": name,
            "created_at": response.container.created_at,
            "skills": skills
        }

        return container_id

    def get_container(self, container_id):
        """Get container info."""
        return self.active_containers.get(container_id)

    def list_containers(self):
        """List all active containers."""
        for cid, info in self.active_containers.items():
            print(f"Container: {cid}")
            print(f"  Name: {info['name']}")
            print(f"  Skills: {[s['skill_id'] for s in info['skills']]}")
            print()

# Usage
manager = ContainerManager(client)

# Create named containers for different workflows
excel_container = manager.create_container(
    skills=[{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}],
    name="excel-workflow"
)

ppt_container = manager.create_container(
    skills=[{"type": "anthropic", "skill_id": "pptx", "version": "latest"}],
    name="presentation-workflow"
)

manager.list_containers()
```

## Skills API Reference

### Skills Endpoints

#### List All Skills

```python
# List all available skills
response = client.beta.skills.list(
    betas=["skills-2025-10-02"]
)

# Filter by source
anthropic_skills = client.beta.skills.list(
    source="anthropic",
    betas=["skills-2025-10-02"]
)

user_skills = client.beta.skills.list(
    source="user",
    betas=["skills-2025-10-02"]
)

for skill in response.data:
    print(f"Skill: {skill.id}")
    print(f"  Display Title: {skill.display_title}")
    print(f"  Source: {skill.source}")
    print(f"  Latest Version: {skill.latest_version}")
```

#### Create Skill

```python
# Create new skill
skill = client.beta.skills.create(
    files=[
        {
            "name": "SKILL.md",
            "content": b"# Skill content..."
        }
    ],
    betas=["skills-2025-10-02"]
)

# Response
{
    "id": "skill_01ABC...",
    "type": "skill",
    "source": "user",
    "display_title": "Skill Name",
    "latest_version": "1737849600000",
    "created_at": "2025-01-25T12:00:00Z"
}
```

#### Retrieve Skill

```python
# Get skill metadata
skill = client.beta.skills.retrieve(
    skill_id="skill_01ABC...",
    betas=["skills-2025-10-02"]
)

print(f"Skill: {skill.display_title}")
print(f"Latest Version: {skill.latest_version}")
```

#### Delete Skill

```python
# Delete entire skill (all versions)
client.beta.skills.delete(
    skill_id="skill_01ABC...",
    betas=["skills-2025-10-02"]
)

print("✓ Skill deleted")
```

### Skill Versions Endpoints

#### List Versions

```python
# List all versions of a skill
versions = client.beta.skills.versions.list(
    skill_id="skill_01ABC...",
    betas=["skills-2025-10-02"]
)

for version in versions.data:
    print(f"Version: {version.version}")
    print(f"  Created: {version.created_at}")
```

#### Create Version

```python
# Create new version
version = client.beta.skills.versions.create(
    skill_id="skill_01ABC...",
    files=[
        {"name": "SKILL.md", "content": b"..."}
    ],
    betas=["skills-2025-10-02"]
)

print(f"New version: {version.version}")
```

#### Retrieve Version

```python
# Get specific version details
version = client.beta.skills.versions.retrieve(
    skill_id="skill_01ABC...",
    version="1737849600000",
    betas=["skills-2025-10-02"]
)

print(f"Name: {version.name}")
print(f"Description: {version.description}")
print(f"Files: {[f.name for f in version.files]}")
```

#### Delete Version

```python
# Delete specific version
client.beta.skills.versions.delete(
    skill_id="skill_01ABC...",
    version="1737849600000",
    betas=["skills-2025-10-02"]
)

print("✓ Version deleted")
```

### Complete API Reference

```python
# Full Skills API interface
class SkillsAPI:
    """Complete Skills API reference."""

    # Skills Management
    client.beta.skills.list(source=None, betas=[...])
    client.beta.skills.create(files=[...], betas=[...])
    client.beta.skills.retrieve(skill_id="...", betas=[...])
    client.beta.skills.delete(skill_id="...", betas=[...])

    # Version Management
    client.beta.skills.versions.list(skill_id="...", betas=[...])
    client.beta.skills.versions.create(skill_id="...", files=[...], betas=[...])
    client.beta.skills.versions.retrieve(skill_id="...", version="...", betas=[...])
    client.beta.skills.versions.delete(skill_id="...", version="...", betas=[...])

    # Using Skills in Messages
    client.beta.messages.create(
        model="...",
        max_tokens=...,
        container={
            "id": "...",  # Optional: reuse container
            "skills": [
                {
                    "type": "anthropic" | "user",
                    "skill_id": "...",
                    "version": "latest" | "1737849600000"
                }
            ]
        },
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[...],
        betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
    )
```

## File Handling

### Understanding File Generation

When skills create files (Excel, PowerPoint, PDF, Word), they:
1. Generate files in the code execution environment
2. Return `file_id` attributes in the response
3. Require the Files API to download actual file content

### Extracting File IDs from Response

```python
def extract_file_ids(response) -> list:
    """Extract all file_ids from a Skills API response."""
    file_ids = []

    for block in response.content:
        # Skills responses use tool_result blocks
        if block.type == "tool_result":
            # File IDs are in the content
            if hasattr(block, 'content'):
                for content_item in block.content:
                    if hasattr(content_item, 'file_id'):
                        file_ids.append(content_item.file_id)

    return file_ids

# Usage
response = client.beta.messages.create(...)  # Skills request
file_ids = extract_file_ids(response)
print(f"Found {len(file_ids)} files: {file_ids}")
```

### Downloading Files

```python
# Download a file using Files API
def download_file(client, file_id: str, output_path: str):
    """Download file from Files API."""

    # Download file content
    file_content = client.beta.files.download(file_id=file_id)

    # Save to disk
    with open(output_path, "wb") as f:
        f.write(file_content.read())  # Use .read(), not .content

    # Get file metadata
    metadata = client.beta.files.retrieve_metadata(file_id=file_id)

    return {
        "file_id": file_id,
        "filename": metadata.filename,
        "size": metadata.size_bytes,  # Use size_bytes, not size
        "mime_type": metadata.mime_type,
        "output_path": output_path
    }

# Example
file_info = download_file(client, "file_abc123...", "output/budget.xlsx")
print(f"Downloaded: {file_info['filename']} ({file_info['size']} bytes)")
```

### Files API Methods

```python
# 1. Download file content
content = client.beta.files.download(file_id="file_abc123...")
with open("output.xlsx", "wb") as f:
    f.write(content.read())  # IMPORTANT: Use .read(), not .content

# 2. Get file metadata
metadata = client.beta.files.retrieve_metadata(file_id="file_abc123...")
print(f"Filename: {metadata.filename}")
print(f"Size: {metadata.size_bytes} bytes")  # IMPORTANT: size_bytes, not size
print(f"MIME Type: {metadata.mime_type}")
print(f"Created: {metadata.created_at}")

# 3. List all files
files = client.beta.files.list()
for file in files.data:
    print(f"{file.filename} - {file.created_at}")

# 4. Delete a file
client.beta.files.delete(file_id="file_abc123...")
```

### Complete File Handling Workflow

```python
def create_and_download_excel(client, prompt: str, output_dir: str):
    """Complete workflow: create Excel file and download it."""
    from pathlib import Path

    # 1. Create file using Skills
    print("Creating Excel file...")
    response = client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        container={
            "skills": [
                {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
            ]
        },
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{"role": "user", "content": prompt}],
        betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
    )

    # 2. Extract file IDs
    file_ids = extract_file_ids(response)
    if not file_ids:
        raise ValueError("No files created in response")

    print(f"✓ Found {len(file_ids)} file(s)")

    # 3. Download each file
    downloaded_files = []
    for file_id in file_ids:
        # Get metadata for filename
        metadata = client.beta.files.retrieve_metadata(file_id=file_id)

        # Download content
        content = client.beta.files.download(file_id=file_id)

        # Save to output directory
        output_path = Path(output_dir) / metadata.filename
        with open(output_path, "wb") as f:
            f.write(content.read())

        downloaded_files.append({
            "file_id": file_id,
            "filename": metadata.filename,
            "size": metadata.size_bytes,
            "path": str(output_path)
        })

        print(f"✓ Downloaded: {metadata.filename} ({metadata.size_bytes / 1024:.1f} KB)")

    return downloaded_files

# Usage
files = create_and_download_excel(
    client,
    prompt="Create a sales report with Q1-Q4 data and a chart",
    output_dir="./outputs"
)

for file in files:
    print(f"Saved: {file['path']}")
```

### Batch File Downloads

```python
def download_all_files(client, response, output_dir: str, prefix: str = ""):
    """Download all files from a Skills response."""
    from pathlib import Path
    import time

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    file_ids = extract_file_ids(response)
    results = []

    for i, file_id in enumerate(file_ids):
        try:
            # Get metadata
            metadata = client.beta.files.retrieve_metadata(file_id=file_id)

            # Generate output filename with prefix
            filename = f"{prefix}{metadata.filename}" if prefix else metadata.filename
            output_path = Path(output_dir) / filename

            # Check if file exists
            overwritten = output_path.exists()

            # Download content
            content = client.beta.files.download(file_id=file_id)

            # Save file
            with open(output_path, "wb") as f:
                f.write(content.read())

            results.append({
                "success": True,
                "file_id": file_id,
                "filename": metadata.filename,
                "output_path": str(output_path),
                "size": metadata.size_bytes,
                "overwritten": overwritten
            })

        except Exception as e:
            results.append({
                "success": False,
                "file_id": file_id,
                "error": str(e)
            })

    return results

# Usage
response = client.beta.messages.create(...)  # Skills request
results = download_all_files(client, response, output_dir="./outputs", prefix="report_")

# Print summary
for result in results:
    if result["success"]:
        status = "[overwritten]" if result["overwritten"] else "[new]"
        print(f"✓ {status} {result['filename']} -> {result['output_path']}")
    else:
        print(f"✗ Failed: {result['file_id']} - {result['error']}")
```

## Beta Headers and Parameters

### Required Beta Features

Skills functionality requires three beta features:

1. **code-execution-2025-08-25**: Enables code execution (required for Skills)
2. **files-api-2025-04-14**: Enables file download/upload
3. **skills-2025-10-02**: Enables Skills feature

### Using Beta Headers

```python
# Method 1: Per-request (Recommended)
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={...},
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[...],
    betas=[
        "code-execution-2025-08-25",
        "files-api-2025-04-14",
        "skills-2025-10-02"
    ]
)

# Method 2: Default headers (for Skills API endpoints only)
client_with_skills = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    default_headers={"anthropic-beta": "skills-2025-10-02"}
)

# Use for Skills API calls
skills = client_with_skills.beta.skills.list()
```

### Beta API Namespace

All Skills functionality uses the `beta` namespace:

```python
# ✅ Correct: Use beta namespace
response = client.beta.messages.create(...)
client.beta.skills.list()
client.beta.files.download(file_id=...)

# ❌ Wrong: Regular namespace doesn't support Skills
response = client.messages.create(container={...})  # Error!
```

### Complete Beta Configuration

```python
from anthropic import Anthropic
import os

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Use Skills with all required beta features
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,

    # Container with skills
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
        ]
    },

    # Code execution tool (REQUIRED)
    tools=[
        {"type": "code_execution_20250825", "name": "code_execution"}
    ],

    # Messages
    messages=[
        {"role": "user", "content": "Create a spreadsheet"}
    ],

    # Beta features (REQUIRED)
    betas=[
        "code-execution-2025-08-25",  # Enable code execution
        "files-api-2025-04-14",       # Enable file operations
        "skills-2025-10-02"            # Enable Skills
    ]
)
```

### Common Beta Header Issues

```python
# ❌ Issue 1: Missing code execution tool
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    container={"skills": [...]},
    messages=[...],
    betas=["skills-2025-10-02"]  # Error: Skills requires code_execution tool
)

# ✅ Fix: Include code execution tool
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    container={"skills": [...]},
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[...],
    betas=["code-execution-2025-08-25", "skills-2025-10-02"]
)

# ❌ Issue 2: Using default_headers for all requests
client = Anthropic(
    api_key="...",
    default_headers={"anthropic-beta": "code-execution-2025-08-25,skills-2025-10-02"}
)
# This applies to ALL requests, not ideal

# ✅ Fix: Use betas parameter per-request
response = client.beta.messages.create(
    ...,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"]
)

# ❌ Issue 3: Forgetting beta namespace
response = client.messages.create(container={...})  # Error!

# ✅ Fix: Use beta namespace
response = client.beta.messages.create(container={...})
```

## Production Best Practices

### 1. Version Pinning

```python
# ❌ Development: Use "latest"
development_config = {
    "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
    ]
}

# ✅ Production: Pin to specific version
production_config = {
    "skills": [
        {"type": "anthropic", "skill_id": "xlsx", "version": "1737849600000"}
    ]
}

# Best Practice: Environment-based configuration
import os

def get_skill_version(skill_id: str) -> str:
    """Get skill version based on environment."""
    if os.getenv("ENV") == "production":
        # Pin to tested version in production
        PRODUCTION_VERSIONS = {
            "xlsx": "1737849600000",
            "pptx": "1737849600000",
            "pdf": "1737849600000"
        }
        return PRODUCTION_VERSIONS.get(skill_id, "latest")
    else:
        # Use latest in development
        return "latest"

# Usage
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [
            {
                "type": "anthropic",
                "skill_id": "xlsx",
                "version": get_skill_version("xlsx")
            }
        ]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[...],
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
)
```

### 2. Error Handling

```python
from anthropic import Anthropic, APIError, APIConnectionError
import time

def create_with_retry(client, max_retries=3, backoff_factor=2):
    """Create skill with exponential backoff retry."""

    for attempt in range(max_retries):
        try:
            response = client.beta.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=4096,
                container={
                    "skills": [
                        {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
                    ]
                },
                tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
                messages=[{"role": "user", "content": "Create spreadsheet"}],
                betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
            )
            return response

        except APIConnectionError as e:
            # Network error - retry
            if attempt < max_retries - 1:
                wait_time = backoff_factor ** attempt
                print(f"Connection error, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

        except APIError as e:
            # API error - check if retryable
            if e.status_code == 429:  # Rate limit
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    print(f"Rate limited, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    raise
            else:
                # Non-retryable error
                raise

# Usage
try:
    response = create_with_retry(client)
    print("✓ Request successful")
except Exception as e:
    print(f"✗ Failed after retries: {e}")
```

### 3. Container Reuse Strategy

```python
class SkillsSession:
    """Manage Skills sessions with container reuse."""

    def __init__(self, client, skills):
        self.client = client
        self.skills = skills
        self.container_id = None
        self.message_count = 0

    def send_message(self, content: str):
        """Send message, reusing container after first request."""

        # Build container config
        if self.container_id:
            # Reuse existing container
            container = {"id": self.container_id}
        else:
            # Create new container with skills
            container = {"skills": self.skills}

        # Send request
        response = self.client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container=container,
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{"role": "user", "content": content}],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        # Store container ID from first response
        if not self.container_id:
            self.container_id = response.container.id

        self.message_count += 1
        return response

    def reset(self):
        """Reset session (creates new container on next message)."""
        self.container_id = None
        self.message_count = 0

# Usage
session = SkillsSession(
    client,
    skills=[{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]
)

# First message: Creates container
response1 = session.send_message("Create a budget spreadsheet")

# Subsequent messages: Reuse container
response2 = session.send_message("Add formulas for totals")
response3 = session.send_message("Add a chart")

print(f"✓ Completed {session.message_count} messages using 1 container")
```

### 4. Monitoring and Logging

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SkillsMonitor:
    """Monitor Skills usage with logging and metrics."""

    def __init__(self, client):
        self.client = client
        self.metrics = {
            "requests": 0,
            "tokens_used": 0,
            "files_created": 0,
            "errors": 0
        }

    def create_with_monitoring(self, container, messages):
        """Create with full monitoring."""
        start_time = datetime.now()

        try:
            # Log request
            logger.info(f"Skills request started: {len(messages)} messages")

            # Make request
            response = self.client.beta.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=4096,
                container=container,
                tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
                messages=messages,
                betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
            )

            # Update metrics
            self.metrics["requests"] += 1
            self.metrics["tokens_used"] += (
                response.usage.input_tokens + response.usage.output_tokens
            )

            # Count files created
            file_ids = extract_file_ids(response)
            self.metrics["files_created"] += len(file_ids)

            # Log success
            duration = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Skills request completed in {duration:.2f}s: "
                f"{len(file_ids)} files, "
                f"{response.usage.input_tokens + response.usage.output_tokens} tokens"
            )

            return response

        except Exception as e:
            # Log error
            self.metrics["errors"] += 1
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"Skills request failed after {duration:.2f}s: {e}")
            raise

    def get_metrics(self):
        """Get usage metrics."""
        return self.metrics.copy()

# Usage
monitor = SkillsMonitor(client)

response = monitor.create_with_monitoring(
    container={"skills": [{"type": "anthropic", "skill_id": "xlsx", "version": "latest"}]},
    messages=[{"role": "user", "content": "Create spreadsheet"}]
)

# View metrics
print(monitor.get_metrics())
# Output: {'requests': 1, 'tokens_used': 15234, 'files_created': 1, 'errors': 0}
```

### 5. Testing Skills

```python
import pytest
from anthropic import Anthropic

class TestSkills:
    """Test Skills functionality."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    def test_excel_creation(self, client):
        """Test Excel file creation."""
        response = client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={
                "skills": [
                    {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
                ]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{"role": "user", "content": "Create simple budget spreadsheet"}],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        # Verify response
        assert response.stop_reason == "end_turn"

        # Verify file created
        file_ids = extract_file_ids(response)
        assert len(file_ids) > 0

        # Verify file downloadable
        metadata = client.beta.files.retrieve_metadata(file_id=file_ids[0])
        assert metadata.filename.endswith(".xlsx")
        assert metadata.size_bytes > 0

    def test_custom_skill(self, client):
        """Test custom skill upload and usage."""
        # Create skill
        skill = client.beta.skills.create(
            files=[{
                "name": "SKILL.md",
                "content": b"""---
name: test-skill
description: Test skill for pytest
---

# Test Skill
Always respond with "Test successful!"
"""
            }],
            betas=["skills-2025-10-02"]
        )

        # Use skill
        response = client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={
                "skills": [
                    {"type": "user", "skill_id": skill.id, "version": "latest"}
                ]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{"role": "user", "content": "Run test"}],
            betas=["code-execution-2025-08-25", "skills-2025-10-02"]
        )

        # Verify response
        assert "Test successful!" in response.content[0].text

        # Cleanup
        client.beta.skills.delete(skill_id=skill.id, betas=["skills-2025-10-02"])

# Run tests
# pytest test_skills.py -v
```

## Limitations

### Execution Environment Constraints

Skills run in **isolated sandbox environments** with specific limitations:

#### 1. No Network Access

```python
# ❌ These will FAIL in Skills:
# - HTTP requests
# - API calls
# - Database connections
# - External service integrations

# Skills CANNOT do this:
import requests
response = requests.get("https://api.example.com/data")  # Error!

# ✅ Instead: Provide data in the prompt
messages = [{
    "role": "user",
    "content": """Create spreadsheet with this data:

    Data from API:
    - Revenue: $100,000
    - Expenses: $75,000
    - Profit: $25,000
    """
}]
```

#### 2. No Package Installation

```python
# ❌ Cannot install packages during execution:
# Skills CANNOT do this:
!pip install custom-library  # Error!

# ✅ Pre-installed packages only
# Available packages vary by skill
# Common ones: pandas, numpy, openpyxl, python-pptx, reportlab
```

#### 3. File Size Limits

```python
# Limits (approximate):
# - Individual files: ~10 MB
# - Skill directory total: ~20 MB
# - Response size: Limited by token limits

# ✅ Best Practice: Keep files focused and minimal
# - Split large skills into multiple smaller skills
# - Remove unnecessary content from SKILL.md
# - Compress resources when possible
```

#### 4. Execution Time Limits

```python
# Skills have execution time limits:
# - Typical operations: Complete in 1-2 minutes
# - Complex document generation: May take longer
# - Timeout: Varies by operation complexity

# ✅ Best Practice: Keep operations focused
# - Generate one document at a time when possible
# - Break complex workflows into steps
# - Use container reuse for multi-step processes
```

### Skills-Specific Limitations

#### 1. SKILL.md Requirements

```python
# ❌ These will be REJECTED:
# - SKILL.md missing required YAML frontmatter
# - name contains uppercase or underscores
# - name uses reserved words ("anthropic", "claude")
# - description exceeds 1024 characters
# - name exceeds 64 characters

# ✅ Valid SKILL.md:
"""
---
name: my-skill-name
description: Clear description under 1024 chars
---

# Rest of skill content
"""
```

#### 2. Progressive Disclosure Caveats

```python
# Initially, only metadata is loaded:
# - name: 64 char max
# - description: 1024 char max

# Full SKILL.md loaded only when skill is activated
# - Recommended: Keep under 5,000 tokens
# - Supporting files loaded only when referenced

# ✅ Implication:
# - Skills don't bloat context until used
# - Description must clearly indicate when to use skill
# - Activations are based on description matching
```

### Workarounds and Alternatives

```python
# Limitation: No network access
# Workaround: Fetch data in your application, pass to Claude

def create_report_with_external_data(client):
    """Fetch data externally, then use Skills."""

    # 1. Fetch data in your application (has network access)
    import requests
    data = requests.get("https://api.example.com/financial-data").json()

    # 2. Pass data to Claude in prompt
    response = client.beta.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        container={
            "skills": [
                {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
            ]
        },
        tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
        messages=[{
            "role": "user",
            "content": f"""Create Excel report with this data:

            {data}
            """
        }],
        betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
    )

    return response

# Limitation: No custom packages
# Workaround: Use pre-built Anthropic skills or include code in SKILL.md

# Limitation: Large skill directories
# Workaround: Split into multiple focused skills
```

## Complete Working Examples

### Example 1: Financial Ratio Analyzer

A complete custom skill for financial analysis:

```python
from anthropic import Anthropic
from pathlib import Path
import os

# Initialize client
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# 1. Create skill directory
skill_dir = Path("./financial-ratio-analyzer")
skill_dir.mkdir(exist_ok=True)

# 2. Create SKILL.md
skill_content = """---
name: financial-ratio-analyzer
description: Calculate and interpret financial ratios (ROI, ROE, debt-to-equity, current ratio, profit margin) from financial statements. Use when user provides balance sheet or income statement data.
---

# Financial Ratio Analyzer

## Purpose
Analyze financial statements and calculate key performance ratios for business health assessment.

## Ratios Calculated

### Profitability Ratios
- **ROI (Return on Investment)**: (Net Income / Total Assets) × 100
- **ROE (Return on Equity)**: (Net Income / Total Equity) × 100
- **Profit Margin**: (Net Income / Revenue) × 100

### Liquidity Ratios
- **Current Ratio**: Current Assets / Current Liabilities
- **Quick Ratio**: (Current Assets - Inventory) / Current Liabilities

### Leverage Ratios
- **Debt-to-Equity**: Total Debt / Total Equity
- **Debt Ratio**: Total Debt / Total Assets

## Instructions

When user provides financial data:

1. **Identify available metrics** from the data provided
2. **Calculate applicable ratios** using the formulas above
3. **Interpret results**:
   - Compare to industry benchmarks when relevant
   - Flag unusual or concerning values
   - Provide context and recommendations
4. **Format output**:
   - Show formula with values
   - Display calculated result
   - Add interpretation

## Example

**Input**: "Analyze: Total Assets $1M, Equity $600K, Debt $400K, Net Income $80K, Revenue $500K"

**Output**:
```
Financial Ratio Analysis

Profitability:
- ROI = ($80K / $1M) × 100 = 8.0%
  ↳ Solid return on assets deployed

- ROE = ($80K / $600K) × 100 = 13.3%
  ↳ Strong returns for shareholders

- Profit Margin = ($80K / $500K) × 100 = 16.0%
  ↳ Healthy profit margin

Leverage:
- Debt-to-Equity = $400K / $600K = 0.67
  ↳ Moderate leverage, within healthy range

- Debt Ratio = $400K / $1M = 0.40
  ↳ 40% of assets financed by debt

Overall Assessment: Company shows strong profitability with conservative leverage.
ROE of 13.3% indicates efficient use of shareholder capital.
```

## Edge Cases
- Missing metrics: Ask user for required data
- Negative values: Flag as unusual, investigate further
- Zero values: Handle division by zero gracefully
- Unusual ratios: Highlight and request verification
"""

(skill_dir / "SKILL.md").write_text(skill_content)

# 3. Upload skill
def files_from_dir(directory_path: str) -> list:
    """Convert directory to file list."""
    files = []
    for file_path in Path(directory_path).rglob("*"):
        if file_path.is_file():
            relative_path = file_path.relative_to(directory_path)
            with open(file_path, "rb") as f:
                files.append({
                    "name": str(relative_path),
                    "content": f.read()
                })
    return files

skill = client.beta.skills.create(
    files=files_from_dir(str(skill_dir)),
    betas=["skills-2025-10-02"]
)

print(f"✓ Skill created: {skill.id}")
print(f"  Name: {skill.name}")
print(f"  Version: {skill.version}")

# 4. Use the skill
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    container={
        "skills": [{
            "type": "user",
            "skill_id": skill.id,
            "version": "latest"
        }]
    },
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
    messages=[{
        "role": "user",
        "content": """Analyze this company's financials:

        Balance Sheet:
        - Total Assets: $2,500,000
        - Current Assets: $800,000
        - Total Equity: $1,500,000
        - Total Debt: $1,000,000
        - Current Liabilities: $300,000

        Income Statement:
        - Revenue: $3,000,000
        - Net Income: $180,000
        """
    }],
    betas=["code-execution-2025-08-25", "skills-2025-10-02"]
)

# 5. Display results
print("\n" + "="*80)
print("FINANCIAL ANALYSIS RESULTS")
print("="*80)
for block in response.content:
    if block.type == "text":
        print(block.text)

print(f"\nToken usage: {response.usage.input_tokens} in, {response.usage.output_tokens} out")
```

### Example 2: Automated Document Generator

Complete workflow for multi-format document generation:

```python
from anthropic import Anthropic
from pathlib import Path
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def extract_file_ids(response):
    """Extract file IDs from response."""
    file_ids = []
    for block in response.content:
        if block.type == "tool_result" and hasattr(block, 'content'):
            for item in block.content:
                if hasattr(item, 'file_id'):
                    file_ids.append(item.file_id)
    return file_ids

def download_file(client, file_id, output_dir):
    """Download file from Files API."""
    metadata = client.beta.files.retrieve_metadata(file_id=file_id)
    content = client.beta.files.download(file_id=file_id)

    output_path = Path(output_dir) / metadata.filename
    with open(output_path, "wb") as f:
        f.write(content.read())

    return {
        "filename": metadata.filename,
        "size": metadata.size_bytes,
        "path": str(output_path)
    }

class DocumentGenerator:
    """Generate comprehensive business reports in multiple formats."""

    def __init__(self, client):
        self.client = client
        self.container_id = None

    def create_quarterly_report(self, quarter_data, output_dir="./outputs"):
        """Generate complete quarterly report package."""

        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = {}

        # Step 1: Create Excel analysis
        print("Step 1: Creating Excel financial analysis...")
        excel_response = self.client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={
                "skills": [
                    {"type": "anthropic", "skill_id": "xlsx", "version": "latest"}
                ]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{
                "role": "user",
                "content": f"""Create a detailed quarterly financial analysis Excel file:

                {quarter_data}

                Include:
                1. Revenue breakdown by month with totals
                2. Expense tracking with categories
                3. Profit/loss calculations with formulas
                4. Year-over-year comparison
                5. Column chart showing revenue vs expenses
                6. Pie chart showing expense breakdown
                """
            }],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        self.container_id = excel_response.container.id

        # Download Excel file
        for file_id in extract_file_ids(excel_response):
            results["excel"] = download_file(self.client, file_id, output_dir)

        print(f"  ✓ Excel created: {results['excel']['filename']}")

        # Step 2: Create PowerPoint presentation
        print("\nStep 2: Creating PowerPoint executive summary...")
        ppt_response = self.client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={
                "id": self.container_id,  # Reuse container
                "skills": [
                    {"type": "anthropic", "skill_id": "pptx", "version": "latest"}
                ]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{
                "role": "user",
                "content": f"""Create an executive summary PowerPoint presentation based on this data:

                {quarter_data}

                Include 4 slides:
                1. Title slide with quarter and year
                2. Revenue highlights with key metrics
                3. Expense overview with breakdown
                4. Key takeaways and recommendations
                """
            }],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        # Download PowerPoint
        for file_id in extract_file_ids(ppt_response):
            results["powerpoint"] = download_file(self.client, file_id, output_dir)

        print(f"  ✓ PowerPoint created: {results['powerpoint']['filename']}")

        # Step 3: Create PDF report
        print("\nStep 3: Creating PDF formal report...")
        pdf_response = self.client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={
                "id": self.container_id,  # Reuse container
                "skills": [
                    {"type": "anthropic", "skill_id": "pdf", "version": "latest"}
                ]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{
                "role": "user",
                "content": f"""Create a formal quarterly report PDF:

                {quarter_data}

                Structure:
                - Cover page with company name and quarter
                - Executive summary (1 paragraph)
                - Financial overview with key metrics in table
                - Detailed analysis by category
                - Recommendations section
                """
            }],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        # Download PDF
        for file_id in extract_file_ids(pdf_response):
            results["pdf"] = download_file(self.client, file_id, output_dir)

        print(f"  ✓ PDF created: {results['pdf']['filename']}")

        return results

# Usage
generator = DocumentGenerator(client)

quarter_data = """
Q1 2025 Financial Data:

Revenue:
- January: $145,000
- February: $158,000
- March: $162,000
- Total Q1: $465,000

Expenses:
- Salaries: $180,000
- Marketing: $45,000
- Operations: $75,000
- Technology: $35,000
- Total: $335,000

Net Profit: $130,000
YoY Growth: +15%
"""

print("="*80)
print("GENERATING QUARTERLY REPORT PACKAGE")
print("="*80 + "\n")

results = generator.create_quarterly_report(quarter_data, output_dir="./q1_2025_reports")

print("\n" + "="*80)
print("REPORT GENERATION COMPLETE")
print("="*80)
print(f"\nGenerated {len(results)} documents:")
for doc_type, info in results.items():
    print(f"\n{doc_type.upper()}:")
    print(f"  File: {info['filename']}")
    print(f"  Size: {info['size'] / 1024:.1f} KB")
    print(f"  Path: {info['path']}")
```

### Example 3: Multi-Tenant SaaS Application

Skills for a multi-tenant platform with custom branding:

```python
from anthropic import Anthropic
import os

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

class TenantSkillManager:
    """Manage custom skills for each tenant."""

    def __init__(self, client):
        self.client = client
        self.tenant_skills = {}  # tenant_id -> skill_id mapping

    def create_tenant_brand_skill(self, tenant_id, brand_config):
        """Create custom branding skill for tenant."""

        skill_content = f"""---
name: {tenant_id}-branding
description: Apply {brand_config['company_name']} brand guidelines to all documents. Use for any document generation for this tenant.
---

# {brand_config['company_name']} Brand Guidelines

## Color Palette
- Primary: {brand_config['primary_color']}
- Secondary: {brand_config['secondary_color']}
- Accent: {brand_config['accent_color']}

## Typography
- Headings: {brand_config['heading_font']}
- Body: {brand_config['body_font']}

## Logo Usage
- Company: {brand_config['company_name']}
- Tagline: {brand_config['tagline']}

## Document Templates

### Excel
- Use primary color for headers
- Company logo in top-left
- Footer with company name and page numbers

### PowerPoint
- Title slide: Primary color background, white text
- Content slides: White background, primary color headers
- Company tagline on every slide footer

### PDF
- Header: Company logo and name
- Footer: Page numbers and tagline
- Section dividers: Primary color

## Instructions

When generating documents:
1. Always apply color scheme
2. Include company branding elements
3. Follow typography guidelines
4. Maintain professional appearance
5. Ensure accessibility (contrast ratios)
"""

        # Create skill
        skill = self.client.beta.skills.create(
            files=[{
                "name": "SKILL.md",
                "content": skill_content.encode()
            }],
            betas=["skills-2025-10-02"]
        )

        # Store mapping
        self.tenant_skills[tenant_id] = skill.id

        return skill.id

    def generate_tenant_document(self, tenant_id, document_type, content):
        """Generate document with tenant branding."""

        # Get tenant's brand skill
        brand_skill_id = self.tenant_skills.get(tenant_id)
        if not brand_skill_id:
            raise ValueError(f"No brand skill found for tenant {tenant_id}")

        # Map document type to Anthropic skill
        skill_map = {
            "excel": "xlsx",
            "powerpoint": "pptx",
            "pdf": "pdf",
            "word": "docx"
        }

        doc_skill = skill_map.get(document_type)
        if not doc_skill:
            raise ValueError(f"Unknown document type: {document_type}")

        # Generate document with both skills
        response = self.client.beta.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            container={
                "skills": [
                    # Tenant brand skill
                    {"type": "user", "skill_id": brand_skill_id, "version": "latest"},
                    # Document generation skill
                    {"type": "anthropic", "skill_id": doc_skill, "version": "latest"}
                ]
            },
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
            messages=[{
                "role": "user",
                "content": f"Create a {document_type} document with our branding:\n\n{content}"
            }],
            betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"]
        )

        return response

# Usage Example
manager = TenantSkillManager(client)

# Onboard new tenant
tenant_id = "acme-corp"
brand_config = {
    "company_name": "Acme Corporation",
    "tagline": "Innovation Through Excellence",
    "primary_color": "#0066CC",
    "secondary_color": "#FF6600",
    "accent_color": "#00CC66",
    "heading_font": "Montserrat Bold",
    "body_font": "Open Sans"
}

skill_id = manager.create_tenant_brand_skill(tenant_id, brand_config)
print(f"✓ Brand skill created for {tenant_id}: {skill_id}")

# Generate branded document
response = manager.generate_tenant_document(
    tenant_id="acme-corp",
    document_type="powerpoint",
    content="""
    Create a 3-slide product launch presentation:

    Slide 1: New Product Announcement
    Slide 2: Key Features (AI-powered, Cloud-based, Scalable)
    Slide 3: Launch Timeline (Beta: March, Release: April)
    """
)

# Extract and download files
file_ids = extract_file_ids(response)
print(f"\n✓ Generated {len(file_ids)} branded documents")

# Cleanup (optional)
# client.beta.skills.delete(skill_id=skill_id, betas=["skills-2025-10-02"])
```

---

## Next Steps

### Continue Learning

- **[Best Practices Guide](03-best-practices.md)** - Advanced skill design patterns
- **[Skills Notebooks](../skills/notebooks/)** - Interactive examples with Jupyter

### Official Resources

- [Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- [Files API Documentation](https://docs.claude.com/en/api/files-content)
- [API Reference](https://docs.claude.com/en/api/messages)

### Support

- [Claude Support](https://support.claude.com)
- [GitHub Issues](https://github.com/anthropics/claude-cookbooks/issues)
- [Discord Community](https://www.anthropic.com/discord)

---

**Ready to build?** Start with the [Complete Working Examples](#complete-working-examples) section and adapt the code for your use case!
