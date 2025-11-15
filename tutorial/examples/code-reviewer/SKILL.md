---
name: code-reviewer
description: Perform comprehensive code reviews using style guides and checklists. Use when the user requests code review, quality assessment, security audit, or needs feedback on code architecture, best practices, and maintainability.
---

# Code Reviewer Skill

## Overview

This skill demonstrates a **multi-file skill architecture** using progressive disclosure - providing immediate guidance while referencing detailed standards and checklists as needed. This pattern helps manage context effectively across complex review workflows.

## Progressive Disclosure Pattern

This skill is structured in 4 files, each with a specific purpose:

1. **SKILL.md** (you are here) - Core workflow and immediate instructions
2. **style-guide.md** - Detailed coding standards and best practices (reference)
3. **checklist.md** - Structured review checklist (reference)
4. **README.md** - Architecture documentation and pattern explanation

**Why this matters**: Instead of overwhelming the user with all details upfront, the skill provides:
- Immediate workflow steps (SKILL.md)
- Links to detailed references as needed
- Structured checklist for comprehensive coverage

This reduces cognitive load while ensuring comprehensive reviews.

## Quick Start

1. **Receive code or repository path** - Ask user what they want reviewed
2. **Read the style guide** - Skim `style-guide.md` to understand standards for the language/context
3. **Follow the workflow** - Execute the steps below systematically
4. **Use the checklist** - Reference `checklist.md` to ensure comprehensive coverage
5. **Deliver report** - Provide structured findings and recommendations

## Workflow

### Step 1: Understand Context & Scope

**Ask the user:**
- What is the purpose of this code?
- What specific areas should I focus on? (e.g., performance, security, readability, testing)
- Are there specific concerns or requirements?
- What language(s) are we reviewing? (Python, JavaScript, Go, etc.)
- Is this a new feature, bug fix, or refactoring?

**Why**: Context shapes review priorities. A financial system needs different scrutiny than a prototype.

### Step 2: Read Reference Materials

**Before the review:**
1. Skim the relevant section of `style-guide.md` for the language/domain
2. Note the key standards that apply to this code
3. Identify any specific patterns or anti-patterns to watch for

**Reference formats in style-guide.md**:
- **Good pattern** - Shows exemplary code with explanations
- **Anti-pattern** - Shows common mistakes to avoid
- **Standard** - Required practice for all code in this context
- **Consider** - Trade-offs to discuss with the author

### Step 3: Conduct Systematic Review

Perform review in this order:

#### A. Architecture & Design (10 min)
- [ ] Is the overall structure clear and logical?
- [ ] Does it follow the language/framework conventions?
- [ ] Are responsibilities well-separated?
- [ ] Can you explain the flow in 30 seconds?

**Reference**: See `style-guide.md` - Architecture section

#### B. Code Quality (15 min)
- [ ] Is the code readable? (naming, structure, comments)
- [ ] Are there obvious bugs or logic errors?
- [ ] Is error handling comprehensive?
- [ ] Are there duplicated patterns that could be extracted?

**Reference**: See `style-guide.md` - Code Quality section and `checklist.md` - Code Quality items

#### C. Security & Data Handling (10 min)
- [ ] Are credentials/secrets properly managed?
- [ ] Is input validation present?
- [ ] Are there SQL injection / XSS / injection vulnerabilities?
- [ ] Is sensitive data handled securely?

**Reference**: See `style-guide.md` - Security section

#### D. Testing & Edge Cases (10 min)
- [ ] What happens with edge cases? (empty inputs, null, max values, etc.)
- [ ] Is error handling tested?
- [ ] Are there obvious scenarios missing from tests?

**Reference**: See `style-guide.md` - Testing section

#### E. Performance & Efficiency (10 min)
- [ ] Are there obvious performance issues?
- [ ] Could algorithms be optimized?
- [ ] Are there unnecessary computations or queries?

**Reference**: See `style-guide.md` - Performance section

#### F. Dependencies & Maintenance (5 min)
- [ ] Are external dependencies justified?
- [ ] Are versions pinned appropriately?
- [ ] Is the code easy to maintain/modify?

**Reference**: See `style-guide.md` - Dependencies section

### Step 4: Comprehensive Checklist Review

Work through `checklist.md` systematically:
- Use it as a final verification that nothing was missed
- Check off items as you evaluate them
- Note any items that don't apply and why

### Step 5: Deliver Structured Report

Follow this format for your review:

```markdown
## Code Review Report

### Executive Summary
- **Overall Assessment**: [Approve / Approve with minor comments / Request changes]
- **Key Strengths**: [2-3 positive aspects]
- **Critical Issues**: [Issues that must be addressed]

### Detailed Findings

#### 1. Architecture & Design [✓/⚠/✗]
[Specific findings with examples]

#### 2. Code Quality [✓/⚠/✗]
[Specific findings with examples]

#### 3. Security & Data Handling [✓/⚠/✗]
[Specific findings with examples]

#### 4. Testing [✓/⚠/✗]
[Specific findings with examples]

#### 5. Performance [✓/⚠/✗]
[Specific findings with examples]

#### 6. Dependencies & Maintenance [✓/⚠/✗]
[Specific findings with examples]

### Specific Comments

[Line-by-line or section-by-section comments with references to style guide]

### Recommendations

[Prioritized list of improvements, labeled as:]
- **MUST**: Critical issues that block approval
- **SHOULD**: Important improvements strongly recommended
- **COULD**: Nice-to-have enhancements or considerations

### References

[Link to relevant sections of style-guide.md for each recommendation]
```

## Managing Context Across Files

This skill demonstrates how to structure complex guidance across multiple files:

### When to Reference Each File

| Situation | Reference |
|-----------|-----------|
| "What should I focus on?" | SKILL.md (this file) - Step 1 context |
| "What's the standard?" | style-guide.md - Detailed standards |
| "Did I cover everything?" | checklist.md - Comprehensive checklist |
| "How does this pattern work?" | README.md - Pattern explanation |
| "What's the workflow again?" | SKILL.md - Step 3 systematic review |

### Progressive Disclosure Benefits

1. **Reduces cognitive load** - User doesn't read 100 standards upfront
2. **Enables reuse** - Different reviews reference same standards
3. **Maintains consistency** - Single source of truth for each topic
4. **Scales knowledge** - Easy to add new standards without overwhelming users
5. **Improves findability** - Specific files for specific questions

## Advanced Patterns

### A. Targeted Reviews

For focused reviews, ask the user which section matters most:

```
"Should I focus on:
- Architecture & Design
- Performance optimization
- Security hardening
- Test coverage
- All of the above?"
```

Then skip irrelevant sections and dive deep into requested areas.

### B. Iterative Reviews

For large codebases, break into multiple review cycles:

1. **Cycle 1**: Architecture & design review
2. **Cycle 2**: Code quality & testing review
3. **Cycle 3**: Security & performance review

Ask: "Would you like me to do a comprehensive review, or focus on specific areas first?"

### C. Comparative Reviews

Compare code against style guide patterns:

```markdown
### Pattern Comparison

**Current (lines 42-47):**
[Show current code]

**Style guide standard (see style-guide.md - Pattern X):**
[Show recommended pattern]

**Benefits of change:**
- Reason 1
- Reason 2
```

## Tips for Effective Reviews

1. **Lead with strengths** - Start with what's working well
2. **Be specific** - Reference line numbers, file names, concrete examples
3. **Explain why** - Don't just flag issues; explain the reasoning
4. **Offer solutions** - For every problem, suggest how to improve
5. **Distinguish severity** - MUST vs SHOULD vs COULD
6. **Ask questions** - "Why was this approach chosen?" can reveal design decisions
7. **Consider context** - A prototype needs different standards than production code

## Common Review Scenarios

### Scenario 1: New Feature Review
Focus on: Architecture (does it fit?), Testing (is it covered?), Documentation (is intent clear?)

### Scenario 2: Bug Fix Review
Focus on: Does the fix actually solve the problem? Are edge cases covered? Could it break other code?

### Scenario 3: Refactoring Review
Focus on: Correctness (behavior unchanged?), Clarity (is it more readable?), Completeness (all code updated?)

### Scenario 4: Security Audit
Focus on: Input validation, output encoding, authentication, authorization, secrets management, data handling.

## Reference: Multi-File Skill Architecture

This skill exemplifies effective multi-file architecture:

```
code-reviewer/
├── SKILL.md           ← Workflow and instructions (you are here)
├── style-guide.md     ← Detailed standards (reference)
├── checklist.md       ← Review checklist (reference)
├── README.md          ← Pattern documentation
└── examples/          ← (optional) Example reviews
    ├── python-example.md
    ├── javascript-example.md
    └── go-example.md
```

**Key principle**: Each file serves a specific purpose. Together they enable comprehensive, context-aware guidance without overwhelming the user.

## Next Steps

Ready to review code?

1. Ask the user for the code/repository path
2. Ask about context (Step 1 above)
3. Skim the relevant section of `style-guide.md`
4. Follow the systematic review workflow (Step 3)
5. Use `checklist.md` to verify completeness
6. Deliver the structured report (Step 5)

---

**Learn more**: See `README.md` for detailed explanation of the multi-file skill architecture and progressive disclosure pattern.
