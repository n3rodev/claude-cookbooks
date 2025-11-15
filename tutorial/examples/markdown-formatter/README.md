# Markdown Formatter Skill Example

This directory contains a **single-file skill** example demonstrating focused functionality for formatting and improving markdown documents.

## What This Example Demonstrates

The markdown formatter skill is a **minimal skill** that showcases:

1. **Single-File Structure** - All skill instructions in one `SKILL.md` file
2. **Focused Functionality** - Single, well-defined purpose (markdown formatting)
3. **Comprehensive Examples** - Good vs. bad formatting patterns
4. **Best Practices** - Clear guidelines for consistent markdown
5. **Practical Learning** - A skill you can use immediately

This is an ideal example if you're:
- Learning to create your first skill
- Want a skill with focused, single-purpose functionality
- Need a reference for markdown best practices
- Building a skill that doesn't require external scripts or files

## File Structure

```
markdown-formatter/
├── SKILL.md      # Complete skill definition and instructions
└── README.md     # This file - explains the example
```

## How It Works

### Frontmatter

The `SKILL.md` file starts with YAML frontmatter that helps Claude discover and understand the skill:

```yaml
---
name: markdown-formatter
description: Format and improve markdown documents by standardizing headers, lists, code blocks, tables, links, and overall structure. Use when the user asks to improve, format, or clean up markdown content.
---
```

**Key elements:**
- `name` - Unique identifier for the skill (used in selection)
- `description` - Helps Claude decide when to activate this skill
  - Should be specific about what the skill does
  - Include keywords users might use
  - Explain the skill's purpose clearly

### Skill Content

Everything after the frontmatter is the skill's instructions. This skill provides:

- **Capability Overview** - What the skill can do
- **Usage Instructions** - How to use the skill
- **Input/Output Formats** - What to expect
- **Formatting Guidelines** - Detailed examples of good vs. bad markdown
- **Best Practices** - Principles to follow
- **Common Mistakes** - What to avoid

## Key Learning Points

### 1. Good vs. Bad Examples

This skill demonstrates a pattern used throughout the tutorial: showing problematic code/markup alongside corrections.

**Pattern:**

```
**Good:**
[correct example]

**Bad:**
[incorrect example]

**Fix:** [explanation]
```

This makes it clear what improvements should be made.

### 2. Comprehensive Coverage

The skill covers all major markdown elements:
- Headers (H1-H6)
- Lists (ordered and unordered)
- Code blocks (with language identifiers)
- Tables (alignment and structure)
- Links (inline and reference style)
- Emphasis (bold, italic, code)
- Whitespace and structure

### 3. Practical Actionability

When activated, this skill guides Claude to:
1. **Analyze** the current markdown structure
2. **Identify** formatting issues
3. **Apply** corrections
4. **Explain** changes made

### 4. Single Responsibility

The skill focuses exclusively on markdown formatting. It doesn't try to:
- Rewrite content
- Change meaning
- Add new sections
- Validate spelling

This focused approach makes it easier to use and understand.

## Using This Skill

### In Claude Code

When you save `SKILL.md` in the appropriate skills directory, Claude will automatically discover it:

```bash
# Place in your Claude Code skills directory
cp -r markdown-formatter ~/.claude/skills/
```

Then ask Claude to format markdown:

```
"Can you improve the formatting of this markdown document?"

[paste your markdown]
```

Claude will automatically activate the markdown-formatter skill.

### In the Tutorial

This example serves as reference material for:
- Learning the structure of a complete, single-file skill
- Understanding how to organize formatting guidelines
- Seeing examples of good documentation
- Understanding skill activation and capability descriptions

## Comparing to Other Examples

| Example | Files | Complexity | Use Case |
|---------|-------|-----------|----------|
| **simple-calculator** | 1 | Minimal | Basic skill structure |
| **markdown-formatter** | 1 | Moderate | Single-purpose skill with guidelines |
| **code-reviewer** | 3+ | Advanced | Multi-file skill with progressive disclosure |
| **api-financial-analyzer** | 3+ | Advanced | API skill with external scripts |

The markdown formatter sits in the "moderate" category - it's more comprehensive than simple-calculator but maintains a single-file structure.

## Best Practices Demonstrated

1. **Clear Metadata** - Description helps Claude understand when to use the skill
2. **Organized Content** - Logical sections with clear headers
3. **Concrete Examples** - Good and bad patterns for each concept
4. **Actionable Guidelines** - Users understand what to do
5. **Comprehensive Coverage** - Addresses all major markdown elements
6. **Whitespace Usage** - Good spacing between sections for readability

## Extending This Skill

To modify or extend this skill, consider:

1. **Add HTML Support** - Include guidelines for embedded HTML
2. **Add Front Matter** - Show Jekyll/Hugo frontmatter examples
3. **Add Diagram Support** - Include mermaid diagram formatting
4. **Add Writing Tips** - Suggest tone and voice improvements
5. **Add Link Validation** - Provide script for checking links

However, these additions would likely require multiple files and should use the code-reviewer pattern instead.

## Common Use Cases

This skill helps with:

- Cleaning up poorly formatted markdown
- Converting documentation to standard format
- Ensuring consistency across multiple documents
- Teaching markdown best practices
- Auditing markdown quality
- Creating documentation templates

## Testing This Skill

To test the markdown formatter skill:

1. **Copy to your skills directory**
   ```bash
   mkdir -p ~/.claude/skills/markdown-formatter
   cp SKILL.md ~/.claude/skills/markdown-formatter/
   ```

2. **Start Claude Code**
   ```bash
   claude
   ```

3. **Test with examples**
   ```
   "Fix the formatting in this markdown:

   #My Document
   This is messy.
   ##Section
   - item1
   * item2
   ```

4. **Verify activation** - Claude should mention using the markdown-formatter skill

## Next Steps

After understanding this example:

1. Read [simple-calculator](../simple-calculator/) for the minimal structure
2. Study [code-reviewer](../code-reviewer/) for multi-file patterns
3. Review [api-financial-analyzer](../api-financial-analyzer/) for API integration
4. Check out the [cookbook-audit](../../.claude/skills/cookbook-audit/) skill in the repository for a production example

## Key Takeaways

- Single-file skills work well for focused, well-defined functionality
- Clear examples (good vs. bad) help guide Claude's behavior
- Comprehensive documentation makes skills more useful
- Proper frontmatter helps Claude discover and activate skills
- Skills don't need external scripts or dependencies to be valuable

## Questions?

For more information:
- See [Creating Your First Skill](../../02-creating-your-first-skill.md)
- Read [Best Practices](../../03-best-practices.md)
- Check the [main tutorial README](../../README.md)
- Refer to [official Agent Skills documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

---

Happy formatting! This skill demonstrates how simple, focused instructions can create powerful and reusable capabilities.
