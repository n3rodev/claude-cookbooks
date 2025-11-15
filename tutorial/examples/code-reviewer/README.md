# Code Reviewer Skill - Multi-File Architecture Example

This directory demonstrates a **multi-file skill architecture** using the **progressive disclosure pattern**. This example is designed to show how to structure complex guidance across multiple files for better context management.

## Quick Navigation

| File | Purpose | When to Use |
|------|---------|------------|
| **[SKILL.md](SKILL.md)** | Core workflow and instructions | Start here - follow the workflow |
| **[style-guide.md](style-guide.md)** | Detailed coding standards (reference) | Look up specific standards and patterns |
| **[checklist.md](checklist.md)** | Structured review checklist | Final verification step to ensure comprehensive coverage |
| **[README.md](README.md)** | This file - architecture explanation | Understand how the skill is organized |

## What is Progressive Disclosure?

**Progressive disclosure** is a UX principle that presents information on-demand rather than all at once:

```
User needs help with code review
         ↓
SKILL.md: "Here's the workflow. See style-guide.md for details."
         ↓
User wants to know about naming conventions
         ↓
style-guide.md: "Good naming looks like X. Anti-pattern is Y."
         ↓
User wants to ensure comprehensive review
         ↓
checklist.md: "Did you check all these items?"
```

**Benefits**:
1. **Reduces cognitive load** - User doesn't read 100 standards upfront
2. **Faster onboarding** - Quick start without drowning in details
3. **Better focus** - Provides information exactly when needed
4. **Enables reuse** - Different reviews reference same standards
5. **Scales knowledge** - Easy to add new standards without overwhelming users

## Directory Structure

```
code-reviewer/
├── SKILL.md           ← Main skill file (core workflow)
├── style-guide.md     ← Reference material (detailed standards)
├── checklist.md       ← Reference material (review checklist)
├── README.md          ← This file (architecture explanation)
└── examples/          ← (Optional) Example reviews in different languages
    ├── python-review-example.md
    ├── javascript-review-example.md
    └── go-review-example.md
```

## How This Skill Uses Progressive Disclosure

### Level 1: Immediate Guidance (SKILL.md)

The main file provides:
- Quick start instructions
- High-level workflow (5 steps)
- When to reference other files
- Common scenarios
- Tips for effective reviews

**User gets up and running** without reading 100 pages.

### Level 2: Deep Dives (style-guide.md)

Referenced by SKILL.md, this file provides:
- Detailed standards for each dimension
- Good vs. bad code patterns
- Explanations of why patterns matter
- Language-specific conventions
- Quick reference table

**User can look up exactly what they need** without wading through irrelevant sections.

### Level 3: Systematic Coverage (checklist.md)

Referenced in Step 4 of SKILL.md, this file provides:
- Exhaustive checklist of review items
- Organization by category
- Conditional sections (bug fix, new feature, refactoring)
- Scoring guidance
- Reviewers can ensure nothing is missed

**User can verify comprehensive coverage** without manually tracking what was reviewed.

## The Four-File Pattern

This skill demonstrates an effective pattern for multi-file complex guidance:

### File 1: SKILL.md (Core Instructions)
```
Purpose: How to use the skill
Content: Workflow, steps, examples, quick reference
Length: 2-3 pages
Reader: Anyone using the skill
```

### File 2: Reference Guides (style-guide.md)
```
Purpose: Detailed standards and patterns
Content: Standards, good/bad examples, explanations
Length: 5-10 pages (one file per domain)
Reader: Users looking up specific standards
Note: Could be multiple files (python-style-guide.md, security-guide.md, etc.)
```

### File 3: Checklists (checklist.md)
```
Purpose: Ensure systematic coverage
Content: Exhaustive checklist, conditional items, scoring
Length: 2-3 pages
Reader: Reviewers doing final verification
```

### File 4: README.md (Meta Documentation)
```
Purpose: Explain how the skill is organized
Content: Navigation, patterns, when to use each file
Length: 1-2 pages
Reader: People new to this skill or the pattern
```

## Building Your Own Multi-File Skills

If you're building a skill with complex guidance, follow this pattern:

### 1. Identify the User Journey

```
User learns about skill
    ↓
User wants to use it
    ↓
User needs specific guidance
    ↓
User needs to verify completeness
```

### 2. Create Core Instruction File

**File**: `SKILL.md`
- What is this skill?
- Quick start workflow (5-10 steps max)
- When to reference other files
- Common scenarios

### 3. Create Reference Files

**Files**: `[domain]-guide.md` (e.g., `security-guide.md`, `performance-guide.md`)
- Detailed standards
- Good and bad patterns
- Explanations and reasoning
- When each applies

### 4. Create Verification Tools

**File**: `checklist.md`
- Systematic checklist
- Conditional sections
- Scoring guidance

### 5. Document the Architecture

**File**: `README.md`
- Navigation guide
- When to use each file
- Pattern explanation
- Usage examples

## Cross-Reference Strategy

Effective multi-file skills use **strategic cross-referencing**:

### From SKILL.md
```markdown
## Step 3: Code Quality Review

Evaluate readability, naming, and structure.

**For standards**: See `style-guide.md` - Code Quality section
**For detailed checklist**: See `checklist.md` - Code Quality items
```

### From style-guide.md
```markdown
## 2.1 Naming Conventions

**Good naming**:
[examples]

**What to watch for**:
- [watchouts]

**See also**: SKILL.md - Step 3A (Architecture Review) for how this fits in workflow
**Checklist**: checklist.md - Code Quality / Readability section
```

### From checklist.md
```markdown
### Naming Conventions
- [ ] Variable names are clear and specific
- [ ] Function/method names clearly describe purpose

**Details**: See style-guide.md - Section 2.1 for patterns and examples
**Workflow**: This is part of Code Quality review in SKILL.md - Step 3B
```

## Benefits of This Architecture

### For Users
- **Fast start**: SKILL.md gets them reviewing in 5 minutes
- **Deep dives**: Can reference standards without context switching
- **Comprehensive**: Checklist ensures nothing is missed
- **Clear navigation**: README explains where to find things

### For Maintainers
- **Modular**: Update one standard without affecting others
- **Reusable**: Same standards referenced across multiple skills
- **Scalable**: Add new files without overwhelming existing ones
- **Testable**: Each file has clear purpose and success criteria

### For Knowledge Management
- **Single source of truth**: One standard per file
- **Easy to find**: Clear naming and structure
- **Easy to update**: Changes in one place propagate everywhere
- **Easy to version**: Files can have independent versioning

## Real-World Examples

### Security Audit Workflow
```
User says: "Can you audit this for security issues?"

SKILL.md Step 1: Ask about scope
            ↓
SKILL.md Step 2: Skim style-guide.md - Security section
            ↓
SKILL.md Step 3C: Conduct Security Review
            ↓
checklist.md - Security section: Verify all checks done
            ↓
SKILL.md Step 5: Deliver report (detailed findings)
```

### Performance Review Workflow
```
User says: "Is this code performant?"

SKILL.md Step 1: Ask about constraints (latency budget, etc.)
            ↓
SKILL.md Step 2: Skim style-guide.md - Performance section
            ↓
SKILL.md Step 3E: Conduct Performance Review
            ↓
checklist.md - Performance section: Verify all checks done
            ↓
SKILL.md Step 5: Deliver report with profiling results
```

### Quick Code Quality Check Workflow
```
User says: "Quick review of this PR?"

SKILL.md Step 1: Confirm scope (full review or quick check)
            ↓
SKILL.md Step 3A+B+C: Focus on Architecture, Quality, Testing
            ↓
checklist.md - Quick Reference: Use relevant sections
            ↓
SKILL.md Step 5: Deliver focused report
```

## Context Management Strategy

One of the biggest challenges with complex skills is **context management** - what does the user need to know right now?

This architecture solves it:

| Question | Answer | File |
|----------|--------|------|
| "How do I use this?" | Follow the workflow | SKILL.md |
| "What's the standard for X?" | See the detailed pattern | style-guide.md |
| "Did I cover everything?" | Check the list | checklist.md |
| "How is this organized?" | See the pattern explanation | README.md |

Without this, users might:
- Get overwhelmed by 100 standards at once
- Miss important checks
- Not understand why standards exist
- Have trouble finding specific guidance

With this pattern:
- They start with a simple workflow
- They reference details on-demand
- They verify systematically
- They understand the architecture

## Extending This Example

To adapt this pattern for other complex skills:

### Multi-Domain Skills

Instead of one `style-guide.md`, use multiple:
```
code-reviewer/
├── SKILL.md
├── python-style-guide.md
├── javascript-style-guide.md
├── go-style-guide.md
├── security-guide.md
├── performance-guide.md
├── checklist.md
└── README.md
```

### Progressive Expertise Levels

Add files for different expertise levels:
```
code-reviewer/
├── SKILL.md (beginner)
├── style-guide.md (beginner)
├── advanced-patterns.md (expert)
├── performance-optimization.md (expert)
├── checklist.md
└── README.md
```

### Language-Specific Examples

Add example reviews:
```
code-reviewer/
├── SKILL.md
├── style-guide.md
├── checklist.md
├── examples/
│   ├── python-review.md
│   ├── javascript-review.md
│   └── go-review.md
└── README.md
```

## Key Principles

When building multi-file skills, follow these principles:

### 1. **Progressive Disclosure**
Provide information on-demand, not all at once.

### 2. **Single Responsibility**
Each file has one primary purpose.

### 3. **Clear Navigation**
Always indicate when to reference other files.

### 4. **Consistent Structure**
Similar sections use similar formatting.

### 5. **Modular Knowledge**
Changes in one file shouldn't require changes in others.

### 6. **Reusability**
Standards can be referenced from multiple contexts.

### 7. **Scalability**
Easy to add new files without complexity explosion.

## Summary

This example demonstrates:

✓ How to break complex guidance into manageable pieces
✓ How to use progressive disclosure for better UX
✓ How to organize files for easy navigation
✓ How to maintain consistency across files
✓ How to structure knowledge for reusability
✓ How to enable both quick starts and deep dives

Use this pattern when:
- Your skill covers multiple domains
- You have both quick workflows and detailed standards
- Users need different information at different times
- You want guidance to be reusable and maintainable

---

## File Reading Order

**First time using this skill?**
1. Read this README.md
2. Skim SKILL.md - Workflow section
3. Follow the Quick Start steps in SKILL.md

**Looking for a specific standard?**
1. Use SKILL.md to understand context
2. Jump to relevant section in style-guide.md

**Doing a comprehensive review?**
1. Follow SKILL.md workflow
2. Reference style-guide.md as needed
3. Use checklist.md for final verification

**Want to understand the architecture?**
1. Read this README.md - How This Skill Uses Progressive Disclosure
2. Explore the files to see the pattern in action

---

**Questions?** See SKILL.md for the workflow, style-guide.md for standards, or checklist.md for systematic coverage.
