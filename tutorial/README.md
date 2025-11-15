# Claude Code Skills Tutorial

Welcome to the comprehensive guide for creating and using Claude Code skills! This tutorial will teach you everything you need to know about extending Claude's capabilities through custom skills.

## What You'll Learn

This tutorial covers both **Claude Code Skills** (filesystem-based) and **API Skills** (uploaded to Anthropic's platform):

1. **Understanding Skills** - What they are and when to use them
2. **Creating Your First Skill** - Hands-on walkthrough
3. **Best Practices** - Writing effective, efficient skills
4. **API Skills** - Uploading and managing skills via the Anthropic API
5. **Advanced Patterns** - Multi-file skills, progressive disclosure, and more

## What Are Claude Code Skills?

**Claude Code Skills** are modular capabilities that extend Claude's functionality through organized folders of instructions, scripts, and resources. Think of them as specialized expertise you can give to Claude.

### Key Characteristics

- **Model-invoked**: Claude automatically decides when to use them based on conversation context
- **Filesystem-based**: Stored as directories that Claude discovers automatically
- **Progressive disclosure**: Only loads what's needed, optimizing context window usage
- **Context-efficient**: Shares the conversation context, so conciseness is critical

### Skills vs. Slash Commands

| Feature | Skills | Slash Commands |
|---------|--------|----------------|
| **Invocation** | Automatic (by Claude) | Manual (by user) |
| **Discovery** | Based on description matching | Explicitly called with `/` |
| **Use Case** | Capabilities Claude should use autonomously | User-triggered workflows |
| **Example** | `analyzing-financial-statements` | `/commit`, `/review-pr` |

## Tutorial Structure

### 📚 Guides

1. **[Getting Started](01-getting-started.md)** - Setup and basic concepts
2. **[Creating Your First Skill](02-creating-your-first-skill.md)** - Step-by-step walkthrough
3. **[Best Practices](03-best-practices.md)** - Design patterns and optimization
4. **[API Skills Guide](04-api-skills.md)** - Working with the Skills API
5. **[Advanced Techniques](05-advanced-techniques.md)** - Multi-file skills, testing, deployment

### 🔧 Examples

Complete, working examples in the `examples/` directory:

- **[simple-calculator](examples/simple-calculator/)** - Minimal skill demonstrating basic structure
- **[markdown-formatter](examples/markdown-formatter/)** - Single-file skill with focused functionality
- **[code-reviewer](examples/code-reviewer/)** - Multi-file skill with progressive disclosure
- **[api-financial-analyzer](examples/api-financial-analyzer/)** - API skill with version management

Each example includes:
- Complete source code
- SKILL.md with proper frontmatter
- Supporting files (when applicable)
- Usage examples
- Best practices demonstrated

## Quick Start

### Prerequisites

- **Claude Code** installed (CLI, IDE extension, or Agent SDK)
- Basic understanding of Claude and the Messages API
- Text editor for creating SKILL.md files

### Your First Skill in 5 Minutes

```bash
# 1. Create the skill directory
mkdir -p ~/.claude/skills/hello-world

# 2. Create SKILL.md
cat > ~/.claude/skills/hello-world/SKILL.md << 'EOF'
---
name: hello-world
description: A simple demonstration skill that greets users. Use when the user asks for a greeting or mentions 'hello world'.
---

# Hello World Skill

## Purpose
Demonstrate the basic structure of a Claude Code skill.

## Instructions
When this skill is activated:
1. Greet the user warmly
2. Explain that this is a custom skill
3. Mention that skills can contain any instructions, scripts, or resources

## Example
"Hello! I'm using the 'hello-world' skill to greet you. This skill demonstrates how Claude Code can be extended with custom capabilities!"
EOF

# 3. Test it
# Open Claude Code and say: "Can you greet me?"
# Claude will automatically use the hello-world skill!
```

## Learning Path

### For Beginners
1. Start with [Getting Started](01-getting-started.md)
2. Follow [Creating Your First Skill](02-creating-your-first-skill.md)
3. Explore the [simple-calculator](examples/simple-calculator/) example
4. Read [Best Practices](03-best-practices.md)

### For Intermediate Users
1. Review [Best Practices](03-best-practices.md)
2. Study the [code-reviewer](examples/code-reviewer/) multi-file example
3. Learn [Advanced Techniques](05-advanced-techniques.md)
4. Explore the cookbook-audit skill in `.claude/skills/cookbook-audit/`

### For API Integration
1. Read [API Skills Guide](04-api-skills.md)
2. Review the [api-financial-analyzer](examples/api-financial-analyzer/) example
3. Learn versioning and deployment strategies
4. Explore pre-built Anthropic skills (Excel, PowerPoint, PDF)

## Key Concepts

### Progressive Disclosure

Skills use a three-tier loading strategy to optimize context:

1. **Metadata** (always loaded): `name` and `description` from frontmatter
2. **Instructions** (loaded when activated): Full SKILL.md content
3. **Supporting files** (loaded on-demand): Additional reference materials

### Skill Activation

Claude decides to activate a skill based on:
- **Description matching**: Does the user request match the description?
- **Context relevance**: Is this skill appropriate for the current conversation?
- **Tool requirements**: Does the skill need specific tools (bash, file operations)?

**Example:**
```yaml
---
name: pdf-processor
description: Extract text and tables from PDF files, fill PDF forms, and merge PDF documents. Use when the user mentions PDF files or needs to process, analyze, or manipulate PDFs.
---
```

User says: "Can you extract the data from this PDF?"
→ Claude recognizes "PDF" and "extract" match the description
→ Activates `pdf-processor` skill automatically

## Repository Integration

This repository (`claude-cookbooks`) already uses skills:

- **`.claude/skills/cookbook-audit/`** - Comprehensive notebook auditing
  - Multi-file structure
  - Automated validation scripts
  - Style guide reference
  - Production-ready example

Study this skill to see best practices in action!

## Official Documentation

This tutorial is based on official Anthropic documentation:

- **[Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)** - Core concepts
- **[Skills Guide](https://docs.claude.com/en/docs/build-with-claude/skills-guide)** - Comprehensive guide
- **[Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)** - Get started quickly
- **[Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)** - Official recommendations
- **[Agent SDK](https://docs.claude.com/en/docs/agent-sdk/overview)** - SDK integration

## Getting Help

- **Issues**: Open an issue in this repository
- **Discord**: [Anthropic Discord](https://www.anthropic.com/discord)
- **Documentation**: [Official Claude Docs](https://docs.claude.com/)
- **Examples**: Explore the `examples/` directory in this tutorial

## Next Steps

👉 **Start with [Getting Started](01-getting-started.md)** to learn the fundamentals!

---

## Tutorial Contents

```
tutorial/
├── README.md                          # This file - overview and index
├── 01-getting-started.md              # Setup and basic concepts
├── 02-creating-your-first-skill.md    # Step-by-step skill creation
├── 03-best-practices.md               # Design patterns and optimization
├── 04-api-skills.md                   # Skills API integration
├── 05-advanced-techniques.md          # Multi-file skills, testing, deployment
├── examples/                          # Working examples
│   ├── simple-calculator/
│   │   └── SKILL.md
│   ├── markdown-formatter/
│   │   └── SKILL.md
│   ├── code-reviewer/
│   │   ├── SKILL.md
│   │   ├── style-guide.md
│   │   └── checklist.md
│   └── api-financial-analyzer/
│       ├── SKILL.md
│       ├── calculate_ratios.py
│       └── README.md
└── assets/                            # Supporting materials
    └── skill-activation-flow.md
```

Happy learning! 🚀
