---
name: markdown-formatter
description: Format and improve markdown documents by standardizing headers, lists, code blocks, tables, links, and overall structure. Use when the user asks to improve, format, or clean up markdown content.
---

# Markdown Formatter Skill

This skill provides comprehensive markdown formatting and improvement capabilities. It helps users create clean, well-structured, and consistent markdown documents following best practices.

## Capabilities

The markdown formatter skill can:

- **Standardize Headers** - Ensure proper heading hierarchy (H1 → H6)
- **Format Lists** - Convert between ordered/unordered lists and fix inconsistencies
- **Improve Code Blocks** - Add language identifiers and proper indentation
- **Organize Tables** - Format and align markdown tables correctly
- **Validate Links** - Check link syntax and identify broken references
- **Fix Whitespace** - Normalize spacing, indentation, and blank lines
- **Improve Structure** - Organize content with proper sections and hierarchy
- **Add Metadata** - Insert frontmatter (YAML) for Jekyll, Hugo, or documentation sites

## How to Use

When this skill is activated, provide markdown content that needs formatting. The formatter will:

1. **Analyze** the current markdown structure
2. **Identify** formatting issues and inconsistencies
3. **Apply** corrections following markdown best practices
4. **Return** improved markdown with explanations of changes

## Input Formats

Accept markdown content in multiple forms:
- Raw markdown text (paste directly)
- Markdown files (describe content)
- Markdown fragments (partial documents)
- Multi-section documents
- Markdown with existing mixed formatting

## Output Format

Return improved markdown with:
- Clear before/after comparison (when helpful)
- Explanation of changes made
- Best practices applied
- Preserved content (only formatting changed)
- Suggestions for further improvements

## Formatting Guidelines

### Headers

**Good:**
```markdown
# Main Title

## Section One

### Subsection

## Section Two
```

**Bad:**
```markdown
#Main Title
##Section One
###Subsection
##Section Two
```

**Bad (inconsistent hierarchy):**
```markdown
# Main Title

### Subsection

## Section Two
```

**Fix:** Ensure proper hierarchy without skipping levels.

### Lists

**Good - Unordered:**
```markdown
- Item one
- Item two
  - Nested item
  - Another nested
- Item three
```

**Good - Ordered:**
```markdown
1. First step
2. Second step
   1. Sub-step A
   2. Sub-step B
3. Third step
```

**Bad (inconsistent markers):**
```markdown
- Item one
* Item two
+ Item three
```

**Bad (improper nesting):**
```markdown
- Item one
  - Nested
- Item two
   - Wrong indentation (extra space)
```

**Fix:** Use consistent markers and proper indentation (2 or 4 spaces).

### Code Blocks

**Good:**
```markdown
Here's a Python example:

\`\`\`python
def hello_world():
    print("Hello, World!")
\`\`\`

And JavaScript:

\`\`\`javascript
function helloWorld() {
    console.log("Hello, World!");
}
\`\`\`
```

**Bad (no language identifier):**
```markdown
\`\`\`
def hello_world():
    print("Hello, World!")
\`\`\`
```

**Bad (inline code for multi-line):**
```markdown
`def hello_world():
    print("Hello, World!")`
```

**Bad (inconsistent indentation):**
```markdown
\`\`\`python
def hello_world():
  print("Hello, World!")  # 2 spaces
    other_code()          # 4 spaces
\`\`\`
```

**Fix:** Use triple backticks with language identifiers and proper indentation.

### Tables

**Good:**
```markdown
| Header One | Header Two | Header Three |
|-----------|-----------|-------------|
| Cell 1    | Cell 2    | Cell 3      |
| Cell 4    | Cell 5    | Cell 6      |
| Cell 7    | Cell 8    | Cell 9      |
```

**Good (with alignment):**
```markdown
| Left      | Center    | Right       |
|:----------|:---------:|------------|
| Left      | Centered  | Right       |
| Aligned   | Aligned   | Aligned     |
```

**Bad (misaligned):**
```markdown
| Header One | Header Two | Header Three |
|---|---|---|
| Cell 1 | Cell 2 | Cell 3 |
| Cell 4 | Cell 5 | Cell 6 |
```

**Bad (inconsistent column count):**
```markdown
| Header One | Header Two |
|---|---|
| Cell 1 | Cell 2 | Cell 3 |
| Cell 4 | Cell 5 |
```

**Bad (no pipe characters):**
```markdown
Header One | Header Two | Header Three
Cell 1 | Cell 2 | Cell 3
```

**Fix:** Use consistent pipe characters, proper spacing, and aligned separator rows.

### Links

**Good (inline):**
```markdown
Check out [the documentation](https://example.com/docs) for more info.
```

**Good (reference style):**
```markdown
Check out [the documentation][docs] for more info.

[docs]: https://example.com/docs
```

**Good (with title attribute):**
```markdown
Visit [the homepage](https://example.com "Example Site Homepage").
```

**Bad (missing brackets):**
```markdown
Check out the documentation https://example.com/docs for more info.
```

**Bad (broken link text):**
```markdown
Check out [the documentation](https://example.com/docs) [for more info].
```

**Bad (invalid URL):**
```markdown
Visit [the homepage](example.com) instead of "https://example.com".
```

**Fix:** Use proper markdown link syntax: `[text](url)` or reference-style links.

### Emphasis and Formatting

**Good:**
```markdown
This is **bold text** for emphasis.

This is *italic text* for emphasis.

This is ***bold and italic***.

`inline code` for code references.
```

**Bad (inconsistent emphasis markers):**
```markdown
This is __bold text__ but also **this**.

This is _italic text_ and also *this*.
```

**Bad (nested emphasis):**
```markdown
**This is *bold and italic* text** - confusing.
```

**Fix:** Use consistent markers: `**bold**`, `*italic*`, `` `code` ``.

### Whitespace and Structure

**Good:**
```markdown
# Title

Introduction paragraph.

## Section One

Content for section one.

### Subsection

More content.

## Section Two

Content for section two.
```

**Bad (no spacing):**
```markdown
# Title
Introduction paragraph.
## Section One
Content for section one.
### Subsection
More content.
## Section Two
Content for section two.
```

**Bad (excessive spacing):**
```markdown
# Title


Introduction paragraph.



## Section One
```

**Bad (inconsistent blank lines):**
```markdown
# Title

Introduction paragraph.

## Section One
Content for section one.


### Subsection

More content.
```

**Fix:** Use one blank line between sections and paragraphs consistently.

### Line Length

**Good (readable):**
```markdown
This is a paragraph that follows the recommended line length guidelines.
It breaks naturally at word boundaries and remains easy to read in most
editors and on most displays.
```

**Bad (too long):**
```markdown
This is an extremely long paragraph that doesn't break and makes it very difficult to read in some editors and creates lines that extend far beyond the typical width that most developers prefer to work with in their editors.
```

**Fix:** Keep lines under 80-100 characters for better readability.

## Best Practices

1. **Consistency First** - Use the same formatting style throughout the document
2. **Hierarchy Matters** - Follow proper heading levels without skipping
3. **Whitespace** - Use blank lines to separate logical sections
4. **Lists** - Use consistent markers and indentation
5. **Code** - Always include language identifiers for code blocks
6. **Links** - Use proper markdown syntax, not bare URLs
7. **Tables** - Keep columns aligned and readable
8. **Readability** - Optimize for both human reading and machine parsing

## Example Workflow

**Input (poorly formatted):**
```
#My Document
This is an introduction.
##First Section
Here is a list:
- item 1
* item 2
+ item 3
###Code Example
`def hello():\n    print("hi")`
##Second Section
|Name|Age|
|---|---|
|John|30|
|Jane|25|
```

**Output (improved):**
```
# My Document

This is an introduction.

## First Section

Here is a list:
- Item 1
- Item 2
- Item 3

### Code Example

\`\`\`python
def hello():
    print("hi")
\`\`\`

## Second Section

| Name | Age |
|------|-----|
| John | 30  |
| Jane | 25  |
```

## Common Markdown Mistakes to Avoid

1. **Skipping heading levels** - Jump from H1 to H3
2. **Mixing list markers** - Using `-`, `*`, and `+` in the same list
3. **Improper code block syntax** - Using indentation instead of backticks
4. **Broken tables** - Inconsistent column counts
5. **Bare URLs** - Not wrapping links in markdown syntax
6. **No language identifiers** - Not specifying code block language
7. **Excessive whitespace** - Too many blank lines between sections
8. **Inconsistent emphasis** - Mixing `**bold**` with `__bold__`

## Related Skills and Tools

- Check documentation using `/link-review` for link validation
- Format code using language-specific formatters
- Validate markdown with dedicated validators
- Preview rendered markdown before publishing
