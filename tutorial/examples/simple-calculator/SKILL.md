---
name: simple-calculator
description: A minimal calculator skill demonstrating basic arithmetic operations (add, subtract, multiply, divide) with step-by-step calculations
---

# Simple Calculator Skill

This is a minimal skill that demonstrates the fundamental structure of a Claude skill. It performs basic arithmetic operations and shows intermediate calculation steps.

## Supported Operations

### 1. Addition
Adds two numbers together and displays the calculation.

**Example Operation:**
- Input: `add(15, 27)`
- Process: `15 + 27 = 42`
- Output: `42`

### 2. Subtraction
Subtracts the second number from the first.

**Example Operation:**
- Input: `subtract(50, 18)`
- Process: `50 - 18 = 32`
- Output: `32`

### 3. Multiplication
Multiplies two numbers together.

**Example Operation:**
- Input: `multiply(8, 6)`
- Process: `8 × 6 = 48`
- Output: `48`

### 4. Division
Divides the first number by the second (with zero-check).

**Example Operation:**
- Input: `divide(100, 4)`
- Process: `100 ÷ 4 = 25`
- Output: `25`

## Skill Features

### Basic Arithmetic
- **add(a, b)** - Returns the sum of two numbers
- **subtract(a, b)** - Returns the difference of two numbers
- **multiply(a, b)** - Returns the product of two numbers
- **divide(a, b)** - Returns the quotient of two numbers (handles division by zero)

### Step-by-Step Display
Each operation displays:
1. Input numbers
2. Operation being performed
3. Calculation expression
4. Final result

### Error Handling
- Validates numeric inputs
- Prevents division by zero
- Returns clear error messages

## Example Usage

### Simple Addition
**Request:** "What is 45 plus 37?"

**Process:**
```
Step 1: Identify the numbers (45, 37)
Step 2: Identify the operation (addition)
Step 3: Calculate: 45 + 37
Step 4: Show intermediate: 45 + 37 = 82
Step 5: Return result: 82
```

**Result:** 82

### Multi-Step Calculation
**Request:** "First multiply 12 by 5, then add 30 to the result"

**Process:**
```
Step 1: Multiply 12 × 5
  - Calculation: 12 × 5 = 60
  - Intermediate result: 60

Step 2: Add 30 to the previous result
  - Calculation: 60 + 30 = 90
  - Final result: 90
```

**Result:** 90

## When to Use This Skill

- Performing basic mathematical calculations
- Breaking down complex arithmetic into steps
- Learning skill structure with simple operations
- Building blocks for more advanced calculation skills

## Limitations

- Only supports two-number operations per call
- No support for complex mathematical functions (trigonometry, logarithms)
- No support for percentages or scientific notation
- Basic error handling only

## Implementation Notes

### Core Structure
```
simple-calculator/
├── SKILL.md          # This file - skill definition and instructions
└── README.md         # Documentation of the example
```

### Key Design Principles

1. **Simplicity First** - Single responsibility per function
2. **Clear Steps** - Each calculation shows its working
3. **Error Prevention** - Basic validation for all inputs
4. **Transparent Process** - Users can follow the calculation logic

### Extension Ideas

To extend this basic skill, consider adding:
- Memory storage (previous calculations)
- Parentheses for order of operations
- More complex operations (exponents, square root)
- Calculation history
- Percentage calculations
- Unit conversions

## Quality Checklist

When using or extending this skill:
- [ ] All operations return correct results
- [ ] Error messages are clear and helpful
- [ ] Step-by-step display aids understanding
- [ ] Input validation prevents crashes
- [ ] Code is simple and easy to understand
- [ ] Examples are clear and educational
