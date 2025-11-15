# Skill Activation Flow

This document explains how Claude Code discovers, evaluates, and activates skills.

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER REQUEST                            │
│             "Can you help me analyze this PDF?"                 │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL DISCOVERY PHASE                        │
│                                                                 │
│  1. Scan ~/.claude/skills/ (personal skills)                   │
│  2. Scan .claude/skills/ (project skills)                      │
│  3. Load metadata (name + description) for all skills          │
│                                                                 │
│  Result: List of available skills with descriptions            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SKILL EVALUATION PHASE                        │
│                                                                 │
│  For each skill, Claude asks:                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ 1. Does the user's request match this skill's           │  │
│  │    description keywords?                                 │  │
│  │    ✓ User said "PDF" → pdf-processor mentions "PDF"     │  │
│  │                                                          │  │
│  │ 2. Is this skill relevant to the current context?       │  │
│  │    ✓ User wants to "analyze" → matches "extract text"   │  │
│  │                                                          │  │
│  │ 3. Does this skill provide value for this request?      │  │
│  │    ✓ Skill can extract data → matches user need         │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Result: One or more skills marked for activation              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL ACTIVATION PHASE                       │
│                                                                 │
│  1. Load full SKILL.md content into context                    │
│  2. Parse instructions and workflow                            │
│  3. Note referenced files (style-guide.md, etc.)               │
│                                                                 │
│  Context Usage:                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ [Always Loaded]                                          │  │
│  │ • Conversation history                                   │  │
│  │ • System instructions                                    │  │
│  │ • Tool definitions                                       │  │
│  │                                                          │  │
│  │ [Now Loaded - Skill Activated]                          │  │
│  │ • SKILL.md instructions                                  │  │
│  │ • Workflow steps                                         │  │
│  │ • Initial examples                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EXECUTION PHASE                               │
│                                                                 │
│  Claude follows skill instructions:                            │
│  1. Execute Step 1: "Identify file type"                       │
│  2. Execute Step 2: "Extract text using pdfplumber"            │
│  3. Execute Step 3: "Format extracted data"                    │
│  4. Execute Step 4: "Present results to user"                  │
│                                                                 │
│  If skill references supporting files:                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ [On-Demand Loading]                                      │  │
│  │ Skill says: "For detailed formatting, see format.md"     │  │
│  │ → Claude loads format.md into context                    │  │
│  │ → Uses guidelines from format.md                         │  │
│  │ → Continues execution                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RESPONSE PHASE                             │
│                                                                 │
│  Claude generates response following skill guidelines:         │
│  • Uses formats specified in skill                             │
│  • Follows output templates                                    │
│  • Includes explanations as instructed                         │
│                                                                 │
│  "I've analyzed the PDF and extracted the following data:      │
│   [formatted output following skill guidelines]"               │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Phase Breakdown

### Phase 1: Discovery (Startup)

**When**: Claude Code starts or refreshes skills

**What Happens**:
1. Scan filesystem for skill directories
2. Read YAML frontmatter from each SKILL.md
3. Extract `name` and `description` only
4. Store in skill registry

**Context Usage**: Minimal (~50-100 tokens per skill)

**Example**:
```yaml
# Loaded into context at startup
skills:
  - name: pdf-processor
    description: Extract text and tables from PDF files...
  - name: git-commit-helper
    description: Generate conventional commit messages...
  - name: code-reviewer
    description: Review code against team standards...
```

### Phase 2: Evaluation (Per Request)

**When**: User makes a request

**What Happens**:
Claude evaluates each skill by comparing:
- **User keywords** vs **skill description keywords**
- **User intent** vs **skill capabilities**
- **Context relevance** vs **skill domain**

**Scoring Logic** (simplified):
```python
def should_activate_skill(user_request: str, skill: Skill) -> float:
    score = 0.0

    # Keyword matching
    user_keywords = extract_keywords(user_request)
    skill_keywords = extract_keywords(skill.description)
    keyword_overlap = len(set(user_keywords) & set(skill_keywords))
    score += keyword_overlap * 0.3

    # Intent matching
    user_intent = classify_intent(user_request)  # e.g., "analyze", "generate", "fix"
    skill_intents = extract_intents(skill.description)
    if user_intent in skill_intents:
        score += 0.4

    # Domain relevance
    user_domain = identify_domain(user_request)  # e.g., "pdf", "code", "finance"
    skill_domain = identify_domain(skill.description)
    if user_domain == skill_domain:
        score += 0.3

    return score

# Activate if score > threshold (e.g., 0.5)
```

**Examples**:

| User Request | Skill | Keywords Match | Intent Match | Domain Match | Activate? |
|--------------|-------|----------------|--------------|--------------|-----------|
| "Analyze this PDF" | pdf-processor | ✓ PDF | ✓ analyze/extract | ✓ PDF | **Yes** |
| "Analyze this PDF" | code-reviewer | ✗ | ✗ | ✗ code | No |
| "Generate commit message" | git-commit-helper | ✓ commit | ✓ generate | ✓ git | **Yes** |
| "Generate a report" | git-commit-helper | ✗ | ✓ generate | ✗ | No |

### Phase 3: Activation (When Triggered)

**When**: Skill evaluation score exceeds threshold

**What Happens**:
1. Load full SKILL.md content
2. Parse instructions section
3. Identify workflow steps
4. Note any referenced files (don't load yet)

**Context Usage**: Full SKILL.md (~500-2000 tokens typically)

**Example Context After Activation**:
```markdown
# Already in context:
- Conversation history (2000 tokens)
- System instructions (500 tokens)
- Tool definitions (1000 tokens)
- Skill metadata for all skills (500 tokens)

# Newly loaded:
- pdf-processor SKILL.md full content (1500 tokens)

# Total: 5500 tokens
# Remaining for conversation: ~195,000 tokens (if using Claude Opus 3.5)
```

### Phase 4: Progressive Disclosure (During Execution)

**When**: Skill instructions reference supporting files

**What Happens**:
1. Skill says: "For detailed standards, see style-guide.md"
2. Claude recognizes file reference
3. Loads style-guide.md into context
4. Uses content for current task
5. May unload if context becomes tight

**Example Workflow**:

```markdown
# In SKILL.md:
## Instructions
1. Review code structure
2. Check against standards in `style-guide.md`  ← Reference
3. Generate feedback

# Claude's execution:
1. ✓ Reviews code structure (uses SKILL.md instructions)
2. → Loads style-guide.md (progressive disclosure)
   ✓ Checks naming conventions
   ✓ Checks formatting rules
   ✓ Checks security patterns
3. ✓ Generates feedback (uses both files)
```

**Context Management**:
```
Before loading style-guide.md:  5,500 tokens used
After loading style-guide.md:   8,000 tokens used (+2,500)
After task completion:          6,000 tokens used (may keep or unload)
```

### Phase 5: Execution (Following Instructions)

**When**: Skill is active and Claude processes request

**What Happens**:
Claude follows the skill's instructions like a recipe:

**Example Skill Instructions**:
```markdown
## Workflow
- [ ] Step 1: Identify the type of change
- [ ] Step 2: Determine the scope
- [ ] Step 3: Write descriptive message
- [ ] Step 4: Format as: type(scope): message
```

**Claude's Execution**:
```
User: "I added authentication to the login page"

Claude's internal process:
1. ✓ Type of change: new feature → "feat"
2. ✓ Scope: login page → "auth"
3. ✓ Descriptive message: "add authentication to login page"
4. ✓ Format: "feat(auth): add authentication to login page"

Response: "I recommend this commit message:
feat(auth): add authentication to login page"
```

### Phase 6: Response (Presenting Results)

**When**: Skill execution completes

**What Happens**:
Claude formats response according to skill guidelines

**Example Output Templates**:

```markdown
# From SKILL.md:
## Output Format
Present results as:
1. **Commit Message**: The formatted message
2. **Explanation**: Why this format was chosen
3. **Alternative**: If applicable

# Claude's Response:
**Commit Message:**
feat(auth): add authentication to login page

**Explanation:**
- Type: "feat" because this adds new functionality
- Scope: "auth" because it relates to authentication
- Message: Clear description of what was added

**Alternative:**
feat(login): implement user authentication
(If you prefer to emphasize the login aspect)
```

## Optimization Strategies

### 1. Keyword Optimization

**Good Description** (High activation accuracy):
```yaml
description: Extract text and tables from PDF files, fill PDF forms, and merge PDF documents. Use when user mentions 'PDF', 'extract from PDF', 'PDF form', 'merge PDFs', or needs to process PDF files.
```

**Keywords for activation**: PDF, extract, form, merge, process

**User phrases that trigger**:
- "Can you extract text from this PDF?"
- "I need to fill out a PDF form"
- "Help me merge these PDF files"
- "Process this PDF document"

### 2. Intent Optimization

**Good Description** (Clear intent):
```yaml
description: Generate conventional commit messages following team standards (feat, fix, docs, etc.). Use when the user is about to commit code, asks for commit message help, or mentions 'git commit'.
```

**Intents supported**: generate, help, format

**User intents that trigger**:
- "Generate a commit message" (generate)
- "Help me write a commit" (help)
- "Format my commit message" (format)

### 3. Scope Optimization

**Good Description** (Clear boundaries):
```yaml
description: Review Python code for style, security, and best practices. Use when reviewing Python files (.py). Does NOT review other languages like JavaScript or Go.
```

**In scope**: Python (.py files), style, security, best practices
**Out of scope**: JavaScript, Go, other languages

**Activation decision**:
- "Review this Python code" → ✓ Activate
- "Review this JavaScript" → ✗ Don't activate

## Context Budget Example

Typical context allocation for a conversation with skills:

```
Total Context Window: 200,000 tokens (Claude Opus 3.5)

Allocation:
┌────────────────────────────────────────────┐
│ System Instructions         1,000 tokens   │
├────────────────────────────────────────────┤
│ Tool Definitions           2,000 tokens    │
├────────────────────────────────────────────┤
│ Skill Metadata (all)       1,000 tokens    │  ← Always loaded
├────────────────────────────────────────────┤
│ Conversation History      10,000 tokens    │
├────────────────────────────────────────────┤
│ Active Skill (SKILL.md)    2,000 tokens    │  ← Loaded when activated
├────────────────────────────────────────────┤
│ Supporting File            3,000 tokens    │  ← Loaded on-demand
├────────────────────────────────────────────┤
│ AVAILABLE               181,000 tokens     │  ← For responses and more context
└────────────────────────────────────────────┘

Efficiency: 9.5% of context used for skills and conversation
            90.5% available for ongoing work
```

## Debugging Activation

### Enable Debug Mode

```bash
claude --debug
```

**Output Example**:
```
[DEBUG] Loading skills from ~/.claude/skills/
[DEBUG] Found skill: pdf-processor
[DEBUG] Loaded metadata: name=pdf-processor, description=Extract text...
[DEBUG] Found skill: git-commit-helper
[DEBUG] Loaded metadata: name=git-commit-helper, description=Generate conventional...

User: "Can you help me with this PDF?"

[DEBUG] Evaluating skills for activation
[DEBUG] pdf-processor: score=0.8 (keywords: PDF=0.3, help=0.2, extract=0.3)
[DEBUG] git-commit-helper: score=0.1 (keywords: help=0.1)
[DEBUG] Activating: pdf-processor (score > 0.5)
[DEBUG] Loading SKILL.md for pdf-processor
[DEBUG] Skill active: pdf-processor
```

### Common Activation Issues

**Issue 1: Skill doesn't activate**
```
Symptom: User says "process this PDF" but skill doesn't activate
Cause: Description doesn't include "process" keyword
Fix: Add "process" to description
```

**Issue 2: Skill activates too often**
```
Symptom: pdf-processor activates for "process this data"
Cause: Description too broad ("process documents")
Fix: Make description specific ("process PDF files only")
```

**Issue 3: Wrong skill activates**
```
Symptom: code-reviewer activates for PDF requests
Cause: Both skills mention "analyze" broadly
Fix: Be domain-specific ("analyze Python code" vs "analyze PDF content")
```

## Best Practices Summary

1. **Specific Keywords**: Include exact terms users will say
2. **Clear Intent**: State what the skill does (extract, generate, review)
3. **Defined Scope**: State what the skill does AND doesn't do
4. **Trigger Examples**: Include example phrases in description
5. **Progressive Loading**: Keep SKILL.md under 500 lines, use supporting files
6. **Test Activation**: Verify skill triggers for intended phrases
7. **Debug Mode**: Use `--debug` to see activation decisions

## Related Resources

- [Best Practices Guide](../03-best-practices.md) - Writing effective skills
- [Creating Your First Skill](../02-creating-your-first-skill.md) - Hands-on tutorial
- [Advanced Techniques](../05-advanced-techniques.md) - Multi-file skills and optimization
