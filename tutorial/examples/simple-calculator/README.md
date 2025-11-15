# Simple Calculator Skill Example

This is a minimal skill example designed to teach the fundamental structure and patterns of building a Claude skill.

## What This Example Demonstrates

### 1. Skill Definition (`SKILL.md`)
- **YAML Frontmatter**: The `name` and `description` fields that identify the skill
- **Clear Documentation**: Comprehensive explanation of capabilities without unnecessary complexity
- **Operation Definitions**: Documentation for each supported function (add, subtract, multiply, divide)
- **Usage Examples**: Step-by-step walkthroughs showing how calculations are performed
- **Error Handling Notes**: How the skill manages edge cases like division by zero

### 2. Minimum Viable Skill Structure
This example shows the simplest complete skill with:
- Single, focused purpose (arithmetic operations)
- Four basic operations following a consistent pattern
- Clear input/output specification
- Step-by-step calculation display
- Basic error handling

### 3. Best Practices for Skills
- **One concept per skill**: Single responsibility (mathematics)
- **Transparent processes**: Step-by-step display helps users understand what's happening
- **Clear naming**: Function names match their purpose exactly
- **Error prevention**: Input validation prevents common errors
- **Documentation**: Extensive examples and use cases

## Directory Structure

```
simple-calculator/
├── SKILL.md       # Skill definition with operations and examples
└── README.md      # This file - explains the example
```

## Key Features

### Minimal Implementation
- No external dependencies required for basic math
- Pure calculation logic
- Easy to understand and extend

### Step-by-Step Display
Each operation shows:
1. Input values received
2. Operation being performed
3. Mathematical expression
4. Calculated result

### Example: Addition
```
Input: Add 45 and 37
Step 1: Identify numbers (45, 37)
Step 2: Set operation (addition: +)
Step 3: Calculate: 45 + 37
Step 4: Show work: 45 + 37 = 82
Output: 82
```

### Error Handling Example
```
Input: Divide 100 by 0
Check: Is divisor zero?
Output: Error - Cannot divide by zero
Help: Try dividing by a non-zero number
```

## Learning Outcomes

After studying this example, you'll understand:

1. **Skill Structure**: SKILL.md format with frontmatter and documentation
2. **Operation Definition**: How to document what a skill can do
3. **Step-by-Step Process**: Breaking calculations into understandable steps
4. **Error Management**: Handling edge cases gracefully
5. **Documentation**: Writing clear examples and use cases

## How to Use This Example

### As a Learning Resource
1. Read `SKILL.md` to understand skill structure
2. Study the operation definitions (add, subtract, multiply, divide)
3. Review the step-by-step examples
4. Note the error handling patterns

### As a Starting Point
To create your own skill:
1. Copy this directory: `cp -r simple-calculator/ my-skill/`
2. Update `SKILL.md`:
   - Change `name` to your skill name
   - Update `description` to your skill's purpose
   - Replace operations with your skill's functionality
3. Update `README.md` with your example's specifics

### To Extend This Skill
Consider adding:
- More operations (exponents, square root, modulo)
- Unit conversion
- Calculation history
- Intermediate result caching
- Scientific notation support

## Comparison with More Complex Skills

| Aspect | Simple Calculator | Complex Skill |
|--------|-------------------|---------------|
| Operations | 4 basic arithmetic | 20+ specialized functions |
| Dependencies | None | Multiple libraries |
| Documentation | 1 page | 10+ pages |
| Examples | Simple numbers | Real-world scenarios |
| Error cases | 2-3 main cases | 10+ edge cases |
| Extension point | Very open | Specialized |

## Next Steps

1. **Understand the Structure**: Review SKILL.md format
2. **Explore Examples**: Study the step-by-step walkthroughs
3. **Try Extensions**: Add operations like power or modulo
4. **Build Your Own**: Use this as a template for custom skills

## Resources

- **SKILL.md Guide**: Comprehensive skill definition documentation
- **API Patterns**: Check other examples in `tutorial/examples/` for more complex patterns
- **Style Guide**: See `.claude/skills/cookbook-audit/style_guide.md` for content guidelines

## Summary

The Simple Calculator skill demonstrates that effective skills don't need to be complex. By focusing on:
- Clear documentation
- Transparent processes
- Consistent patterns
- Helpful error messages

...you create skills that are easy to understand, use, and extend.
