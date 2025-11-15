# Claude Cookbooks - Claude Code Guide

## Project Overview

The **Claude Cookbooks** repository is Anthropic's official collection of practical code examples, guides, and tutorials for building with Claude. This repository contains 59+ Jupyter notebooks demonstrating capabilities, tool use, multimodal features, agent patterns, and third-party integrations.

**Target Audience**: Intermediate to advanced Python developers, ML engineers, and software engineers building AI-powered applications with Claude API.

**Repository Type**: Educational resource with production-ready code examples and automated quality assurance.

## Quick Start Commands

### Environment Setup
```bash
# Install uv (recommended package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or with Homebrew: brew install uv

# Clone and setup
git clone https://github.com/anthropics/anthropic-cookbook.git
cd anthropic-cookbook

# Create virtual environment and install dependencies
uv sync --all-extras
# Or with pip: pip install -e ".[dev]"

# Install pre-commit hooks
uv run pre-commit install

# Configure API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running Notebooks
```bash
# Launch Jupyter
uv run jupyter notebook

# Or open in VSCode with Jupyter extension
code .

# Run a specific notebook with execution validation
uv run jupyter nbconvert --to notebook \
  --execute skills/notebooks/01_skills_introduction.ipynb \
  --ExecutePreprocessor.kernel_name=python3 \
  --output test_output.ipynb
```

### Quality Checks
```bash
# Format and lint code
uv run ruff format .
uv run ruff check . --fix

# Validate notebook structure
uv run python scripts/validate_notebooks.py

# Run pre-commit hooks on all files
uv run pre-commit run --all-files

# Run Claude Code slash commands (if using Claude Code)
/notebook-review skills/notebooks/01_skills_introduction.ipynb
/model-check
/link-review README.md
```

## Architecture Overview

### Directory Structure
```
claude-cookbooks/
├── .claude/                          # Claude Code integration
│   ├── commands/                     # Slash commands for CI/CD
│   │   ├── notebook-review.md        # Comprehensive notebook quality check
│   │   ├── model-check.md            # Validate Claude model usage
│   │   └── link-review.md            # Review links for quality/security
│   └── skills/                       # Custom skills
│       └── cookbook-audit/           # Notebook audit skill with style guide
├── .github/workflows/                # CI/CD pipelines (7 workflows)
│   ├── notebook-quality.yml          # Validates notebook structure/linting
│   ├── claude-notebook-review.yml    # AI-powered reviews using Claude
│   ├── claude-model-check.yml        # Validates model references
│   ├── claude-link-review.yml        # Checks link quality
│   ├── links.yml                     # Link validation using lychee
│   ├── lint-format.yml               # Code formatting and linting
│   └── notebook-diff-comment.yml     # Posts notebook diffs as PR comments
├── capabilities/                     # Core Claude capabilities
│   ├── classification/               # Text classification techniques
│   ├── contextual-embeddings/        # Contextual embeddings
│   ├── retrieval_augmented_generation/ # RAG implementations
│   ├── summarization/                # Summarization methods
│   └── text_to_sql/                  # Text-to-SQL generation
├── claude_agent_sdk/                 # Agent SDK tutorials (NEW)
│   ├── chief_of_staff_agent/         # Executive assistant agent
│   ├── observability_agent/          # Monitoring and logging agent
│   ├── research_agent/               # Research and analysis agent
│   └── utils/                        # Shared utilities
├── skills/                           # Skills feature cookbook
│   ├── notebooks/                    # Skills tutorials (Excel, PowerPoint, PDF)
│   ├── custom_skills/                # Custom skill development
│   └── sample_data/                  # Financial datasets
├── tool_use/                         # Tool use examples
│   ├── customer_service_agent.ipynb  # Customer service automation
│   ├── calculator_tool.ipynb         # Basic tool integration
│   ├── tools_with_memory.ipynb       # Stateful tool interactions
│   └── parallel_tool_calls.ipynb     # Concurrent tool execution
├── multimodal/                       # Vision capabilities
│   ├── getting_started_with_vision.ipynb
│   ├── best_practices_for_vision.ipynb
│   ├── reading_charts_graphs_powerpoints.ipynb
│   └── how_to_transcribe_text.ipynb
├── patterns/                         # Advanced patterns
│   └── agents/                       # Agent workflow patterns
│       ├── basic_agentic_loop.ipynb
│       ├── orchestrator_workers_pattern.ipynb
│       └── evaluator_optimizer_pattern.ipynb
├── third_party/                      # External integrations
│   ├── Deepgram/                     # Speech-to-text
│   ├── ElevenLabs/                   # Text-to-speech
│   ├── LlamaIndex/                   # RAG framework
│   ├── MongoDB/                      # Vector database
│   ├── Pinecone/                     # Vector database
│   ├── VoyageAI/                     # Embeddings
│   ├── Wikipedia/                    # Knowledge retrieval
│   └── WolframAlpha/                 # Computational knowledge
├── extended_thinking/                # Extended thinking feature
├── finetuning/                       # Fine-tuning guides
├── observability/                    # Observability tools
├── tool_evaluation/                  # Tool evaluation
├── coding/                           # Coding-specific examples
├── misc/                             # Miscellaneous examples
└── scripts/                          # Validation and utility scripts
```

### Key Technical Details

**Python Requirements:**
- Python 3.11 or 3.12 (3.13 not yet supported)
- Anthropic SDK >= 0.71.0
- Jupyter ecosystem (notebook, ipykernel, nbconvert)

**Package Management:**
- **uv** (recommended) - Modern, fast Python package manager
- **pip** (alternative) - Traditional package manager

**Code Quality Tools:**
- **ruff** - Fast Python linter and formatter (supports Jupyter notebooks)
- **pre-commit** - Git hooks for automated quality checks
- **nbconvert** - Notebook execution testing
- **lychee** - Link validation

**Claude Models:**
- Use current public models (check https://docs.claude.com/en/docs/about-claude/models/overview)
- Latest Haiku: `claude-haiku-4-5-20251001` (Haiku 4.5)
- Prefer model aliases when available for better maintainability

**API Key Management:**
- Store in `.env` file (never commit)
- Access via `os.environ.get("ANTHROPIC_API_KEY")`
- Example template in `.env.example`

## Development Workflow

### Claude Code Integration

This repository includes **slash commands** that work in both Claude Code (local) and GitHub Actions (CI):

**Available Commands:**
- `/notebook-review <path>` - Comprehensive notebook quality check
  - Validates structure, execution, style, best practices
  - Checks for API key exposure, security issues
  - Verifies model usage and error handling

- `/model-check` - Validate Claude model usage
  - Compares models in code against current public models
  - Flags deprecated or non-existent models

- `/link-review <path>` - Review links in markdown/notebooks
  - Checks link quality and security
  - Validates URL accessibility

**Usage Example:**
```bash
# In Claude Code, these commands run the same validation as CI
/notebook-review capabilities/classification/guide.ipynb
/model-check
/link-review README.md
```

**Custom Skills:**
- `cookbook-audit` - Comprehensive notebook auditing with style guide
  - Located in `.claude/skills/cookbook-audit/`
  - Includes detailed style guide in `style_guide.md`
  - Use: Invoke the skill when you need to audit notebooks

### Git Workflow

**Branch Naming:**
```bash
git checkout -b <your-name>/<feature-description>
# Example: git checkout -b alice/add-rag-example
```

**Conventional Commits:**
```bash
# Format: <type>(<scope>): <subject>

# Types:
feat     # New feature
fix      # Bug fix
docs     # Documentation
style    # Formatting
refactor # Code restructuring
test     # Tests
chore    # Maintenance
ci       # CI/CD changes

# Examples:
git commit -m "feat(skills): add text-to-sql notebook"
git commit -m "fix(api): use environment variable for API key"
git commit -m "docs(readme): update installation instructions"
```

**Pull Request Guidelines:**
1. Use conventional commit format for PR title
2. Include clear description with context and testing steps
3. Keep PRs focused (one feature/fix per PR)
4. Respond to review comments promptly
5. Ensure all CI checks pass

### Quality Standards

**Before Committing:**
```bash
# 1. Format and lint
uv run ruff format .
uv run ruff check . --fix

# 2. Validate notebooks
uv run python scripts/validate_notebooks.py

# 3. Run pre-commit hooks
uv run pre-commit run --all-files

# 4. Optional: Test notebook execution (requires API key)
uv run jupyter nbconvert --to notebook --execute \
  path/to/notebook.ipynb \
  --ExecutePreprocessor.kernel_name=python3 \
  --output test_output.ipynb
```

**Pre-commit Hooks:**
Pre-commit hooks automatically run before each commit:
- Format code with ruff
- Validate notebook structure
- Check for common issues

If a hook fails, fix the issues and commit again.

**CI/CD Validation:**
GitHub Actions automatically run:
- Notebook structure validation
- Ruff linting and formatting checks
- Link validation (lychee)
- Claude-powered code review
- Model validation
- Notebook execution (for maintainers)

## Development Gotchas

### 1. Python Version Compatibility
**Problem**: SDK or dependencies fail to install
**Solution**: Ensure Python 3.11 or 3.12 (3.13 not yet supported)
```bash
python --version  # Should show 3.11.x or 3.12.x
```

### 2. uv vs pip Differences
**Problem**: Dependencies installed with pip don't work with uv
**Solution**: Stick to one package manager per environment
```bash
# Recommended: Use uv for everything
uv sync --all-extras
uv run jupyter notebook

# Alternative: Use pip for everything
pip install -e ".[dev]"
jupyter notebook
```

### 3. Jupyter Kernel Selection
**Problem**: Wrong Python interpreter = wrong dependencies
**Solution**: Always select correct kernel
- VSCode: Cmd+Shift+P → "Python: Select Interpreter" → select venv
- Jupyter: Kernel → Change Kernel → select correct environment

### 4. API Key Not Found
**Problem**: `anthropic.APIError: API key not found`
**Solution**: Ensure `.env` file exists and is loaded
```python
# In notebooks, use:
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY not found in environment")
```

### 5. Notebook Outputs in Git
**Important**: This repository KEEPS notebook outputs (unlike typical repos)
- Outputs demonstrate expected results for users
- Don't strip outputs before committing
- CI validates that outputs are present

### 6. Model Deprecation
**Problem**: Using outdated or non-existent models
**Solution**: Use `/model-check` slash command or check docs
```bash
# Verify current models
/model-check

# Or check: https://docs.claude.com/en/docs/about-claude/models/overview
```

### 7. Skills API Beta Namespace
**Problem**: `container` parameter not recognized (in Skills notebooks)
**Solution**: Use `client.beta.*` namespace for Skills
```python
# ❌ Wrong
response = client.messages.create(container={...})

# ✅ Correct
response = client.beta.messages.create(
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
    container={...}
)
```

### 8. Pre-commit Hook Failures
**Problem**: Pre-commit hook fails after making changes
**Solution**: Fix the issues and re-commit
```bash
# View what failed
git status

# Fix issues (often auto-fixed by ruff)
uv run ruff format .
uv run ruff check . --fix

# Re-commit
git add .
git commit -m "fix: your message here"
```

## Notebook Best Practices

### Structure
1. **One concept per notebook** - Keep focused and clear
2. **Clear sections** - Use markdown headers for organization
3. **Setup cells** - Include imports and configuration at top
4. **Explanatory text** - Use markdown cells to explain concepts
5. **Expected outputs** - Include outputs as markdown cells showing what users should see

### API Usage
```python
# ✅ Good: Use environment variables
import os
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

# ❌ Bad: Hardcoded API keys
client = Anthropic(api_key="sk-ant-...")  # NEVER DO THIS

# ✅ Good: Use current models
model = "claude-haiku-4-5-20251001"

# ❌ Bad: Deprecated or non-existent models
model = "claude-2.1"  # Outdated

# ✅ Good: Include error handling
try:
    response = client.messages.create(...)
except anthropic.APIError as e:
    print(f"API error: {e}")

# ✅ Good: Minimize token usage in examples
max_tokens = 100  # Keep low for examples

# ❌ Bad: Excessive tokens
max_tokens = 4096  # Too much for simple examples
```

### Testing
```bash
# Run notebook from top to bottom
# Kernel → Restart & Run All

# Verify in clean environment
cd /tmp
git clone <your-fork>
cd anthropic-cookbook
uv sync --all-extras
uv run jupyter notebook
# Run your notebook
```

## Common Tasks

### Adding a New Notebook
1. Create notebook in appropriate directory
2. Follow structure of existing notebooks
3. Include setup cells with imports
4. Add clear explanations in markdown cells
5. Test notebook execution (Restart & Run All)
6. Run quality checks:
   ```bash
   /notebook-review path/to/your-notebook.ipynb
   uv run ruff format path/to/your-notebook.ipynb
   uv run python scripts/validate_notebooks.py
   ```
7. Update README.md table if adding new category
8. Create PR with conventional commit format

### Updating Dependencies
```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add anthropic@latest

# Or with pip
pip install --upgrade anthropic
```

### Running Claude Code Slash Commands Locally
```bash
# These commands use the exact same logic as CI
/notebook-review capabilities/rag/guide.ipynb
/model-check
/link-review README.md

# Commands are defined in .claude/commands/
```

### Testing Notebook Execution
```bash
# Test single notebook
uv run jupyter nbconvert --to notebook --execute \
  capabilities/classification/guide.ipynb \
  --ExecutePreprocessor.kernel_name=python3 \
  --output test_output.ipynb

# Cleanup
rm test_output.ipynb
```

### Validating Links
```bash
# Using lychee (recommended)
lychee --config lychee.toml .

# Using slash command
/link-review README.md
```

## Testing Checklist

Before submitting a PR:
- [ ] Code formatted with ruff: `uv run ruff format .`
- [ ] Linting passes: `uv run ruff check . --fix`
- [ ] Notebook structure validated: `uv run python scripts/validate_notebooks.py`
- [ ] Pre-commit hooks pass: `uv run pre-commit run --all-files`
- [ ] Notebook executes without errors (Restart & Run All)
- [ ] API keys not exposed in code or outputs
- [ ] Using current Claude models
- [ ] Links are valid and accessible
- [ ] Conventional commit format used
- [ ] PR description is clear and complete

## Resources

### Official Documentation
- **Anthropic API Docs**: https://docs.claude.com/
- **Claude API Fundamentals Course**: https://github.com/anthropics/courses/tree/master/anthropic_api_fundamentals
- **Skills Documentation**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Model Overview**: https://docs.claude.com/en/docs/about-claude/models/overview

### Tools Documentation
- **uv Package Manager**: https://docs.astral.sh/uv/
- **ruff Linter**: https://docs.astral.sh/ruff/
- **nbconvert**: https://nbconvert.readthedocs.io/
- **lychee Link Checker**: https://github.com/lycheeverse/lychee

### Community
- **GitHub Issues**: https://github.com/anthropics/anthropic-cookbook/issues
- **GitHub Discussions**: https://github.com/anthropics/anthropic-cookbook/discussions
- **Discord**: https://www.anthropic.com/discord
- **Support Docs**: https://support.anthropic.com

## Project-Specific Notes

### Repository Statistics
- **Total Notebooks**: 59+
- **Main Categories**: 8 (capabilities, tool_use, multimodal, skills, patterns, third_party, extended_thinking, misc)
- **CI/CD Workflows**: 7
- **Slash Commands**: 3
- **Custom Skills**: 1 (cookbook-audit)

### Special Features

**1. Claude-Powered CI/CD**
- Automated notebook reviews using Claude
- Model validation against current releases
- Link quality and security checks
- Same validation tools work locally (Claude Code) and in CI

**2. Skills Cookbook**
- Progressive tutorial series for Claude Skills
- Focus on financial applications and business automation
- Excel, PowerPoint, PDF generation examples
- Custom skills development guides

**3. Agent SDK Examples**
- Chief of Staff agent (executive assistant)
- Research agent (information gathering)
- Observability agent (monitoring and logging)

**4. Quality Assurance**
- Pre-commit hooks for instant feedback
- Comprehensive notebook validation
- Automated execution testing
- AI-powered code review

### Contribution Philosophy
- **Copy-able code** - Examples should work out-of-the-box
- **Production-ready** - Demonstrate best practices
- **Educational** - Clear explanations and context
- **Community-driven** - Open to contributions from developers

## Environment Variables

Required in `.env`:
```bash
ANTHROPIC_API_KEY=your-api-key-here
```

Optional:
```bash
ANTHROPIC_BASE_URL=https://api.anthropic.com  # For proxy/custom endpoint
```

## Security

- **Never commit API keys or secrets** - Use `.env` file
- **Use environment variables** - Never hardcode credentials
- **Report security issues** - Email security@anthropic.com privately
- **Review before pushing** - Check for exposed credentials

## License

MIT License - See LICENSE file for details

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Quick Links:**
- [README.md](README.md) - Repository overview
- [CONTRIBUTING.md](CONTRIBUTING.md) - Detailed contribution guidelines
- [.env.example](.env.example) - API key configuration template
- [Makefile](Makefile) - Development commands

**For Claude Code users**: This repository is optimized for Claude Code with custom slash commands and skills. Use `/notebook-review`, `/model-check`, and `/link-review` for the same validation that runs in CI.
