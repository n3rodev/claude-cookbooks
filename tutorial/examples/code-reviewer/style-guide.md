# Code Review Style Guide

This document provides detailed coding standards and patterns for comprehensive code reviews. It's a **reference document** that the main workflow (SKILL.md) refers to.

## How to Use This Guide

- **By line number in review**: "See style-guide.md - Architecture section"
- **By pattern name**: "This violates the 'Single Responsibility' principle (style-guide.md - Architecture)"
- **For quick lookup**: Use section headers to find relevant standards

---

## 1. Architecture & Design

### 1.1 Single Responsibility Principle (SRP)

**Standard**: Each module, class, or function should have exactly one reason to change.

**Good pattern**:
```python
# Good: Separate concerns
class UserRepository:
    """Handles user data persistence only"""
    def get_user(self, id):
        return self.db.query(User).filter_by(id=id).first()

class UserValidator:
    """Handles user data validation only"""
    def validate_email(self, email):
        return "@" in email

class UserService:
    """Orchestrates user operations"""
    def __init__(self, repo, validator):
        self.repo = repo
        self.validator = validator

    def create_user(self, email):
        if not self.validator.validate_email(email):
            raise ValueError("Invalid email")
        return self.repo.save(User(email=email))
```

**Anti-pattern**:
```python
# Bad: Mixing concerns (validation, persistence, orchestration)
class User:
    def __init__(self, email):
        self.email = email

    def validate(self):
        return "@" in self.email

    def save(self):
        db.query(...).filter_by(...).insert(self)

    def send_welcome_email(self):
        # This shouldn't be in User class
        smtp.send(...)
```

**What to watch for**:
- Classes doing multiple unrelated things
- Functions that need to change for multiple reasons
- Mixing UI, business logic, and data access

---

### 1.2 Dependency Injection

**Standard**: Pass dependencies as arguments, don't create them inside functions.

**Good pattern**:
```python
# Good: Dependencies injected
class UserService:
    def __init__(self, db, logger, email_client):
        self.db = db
        self.logger = logger
        self.email_client = email_client

    def create_user(self, email):
        self.logger.info(f"Creating user: {email}")
        user = self.db.save(User(email=email))
        self.email_client.send_welcome(email)
        return user

# Usage
service = UserService(db, logger, email_client)
```

**Anti-pattern**:
```python
# Bad: Creating dependencies inside
class UserService:
    def create_user(self, email):
        db = Database()  # Should be injected!
        logger = Logger()  # Should be injected!
        email = EmailClient()  # Should be injected!
        # Now hard to test, hard to swap implementations
```

**Why it matters**:
- Enables testing with mocks
- Allows swapping implementations
- Makes dependencies explicit

---

### 1.3 Error Handling Architecture

**Standard**: Errors should be handled at the appropriate level; propagate up when needed.

**Good pattern**:
```python
# Good: Clear error handling strategy
def fetch_user_data(user_id):
    """Raises UserNotFound if user doesn't exist"""
    try:
        response = api.get(f"/users/{user_id}")
        return response.json()
    except requests.exceptions.Timeout:
        # Retryable error - handle here
        return fetch_user_data_with_retry(user_id)
    except requests.exceptions.ConnectionError as e:
        # Log and raise - let caller decide
        logger.error(f"Connection failed for user {user_id}")
        raise

class UserService:
    def get_user(self, user_id):
        try:
            data = fetch_user_data(user_id)
            return User(data)
        except Exception as e:
            # Transform to domain error
            raise UserNotFound(user_id) from e
```

**Anti-pattern**:
```python
# Bad: Silent failures and bare except
def fetch_user_data(user_id):
    try:
        return api.get(f"/users/{user_id}").json()
    except:
        return None  # Lost the actual error!

# Bad: Catching everything
def get_user(user_id):
    try:
        data = fetch_user_data(user_id)
        return User(data)
    except:
        # What was the error? We don't know!
        pass
```

**What to watch for**:
- Silent failures (`except: pass`)
- Bare `except` clauses
- Swallowing exceptions without logging
- Not re-raising when appropriate

---

## 2. Code Quality

### 2.1 Naming Conventions

**Standard**: Names should be clear, specific, and pronounceable.

**Good naming**:
```python
# Good: Clear intent
users_over_thirty = [u for u in users if u.age > 30]
elapsed_seconds = end_time - start_time
is_valid_email = "@" in email

# Good: Specific names
def calculate_shipping_cost(weight_kg, destination_country):
    """Clear what it calculates"""
    pass

def validate_credit_card_number(number):
    """Clear what it validates"""
    pass
```

**Anti-patterns**:
```python
# Bad: Cryptic names
uos = [u for u in users if u.age > 30]  # What is "uos"?
t = end_time - start_time  # What is "t"?
v = "@" in email  # What does "v" mean?

# Bad: Unclear intent
def process(data):  # Process what?
    pass

def handle(item):  # Handle how?
    pass
```

**Conventions by language**:
- **Python**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants
- **JavaScript**: `camelCase` for functions/variables, `PascalCase` for classes/components
- **Go**: `mixedCase` for exported, `camelCase` for unexported

---

### 2.2 Function Length & Complexity

**Standard**: Functions should be short enough to understand at a glance (typically 15-25 lines).

**Good pattern** (one task, easy to understand):
```python
def process_order(order):
    """Process a single order through the system"""
    validate_order(order)  # One task per line
    charge_payment(order)
    send_confirmation(order)
    return OrderResult(status="processed")
```

**Anti-pattern** (doing too much):
```python
def process_order(order):
    """Does everything"""
    # Validate
    if not order.items or not all(item.price > 0 for item in order.items):
        raise ValueError("Invalid items")
    if not order.customer or not order.customer.email:
        raise ValueError("Invalid customer")

    # Charge payment (mixing concerns)
    try:
        response = requests.post(
            "https://payment-api.com/charge",
            json={"amount": sum(item.price for item in order.items), "customer": order.customer.id},
            timeout=30
        )
        if response.status_code != 200:
            raise PaymentError(response.text)
    except requests.exceptions.Timeout:
        retry_count = 0
        while retry_count < 3:
            # ... retry logic mixed in
            pass

    # Send email (more concerns)
    # ... 50 more lines ...

    return OrderResult(status="processed")
```

**What to watch for**:
- Functions doing multiple things
- High nesting levels (> 3 levels)
- Multiple reasons to modify a function
- Difficulty naming the function

---

### 2.3 Comments & Documentation

**Standard**: Code should be self-documenting; comments explain *why*, not *what*.

**Good pattern**:
```python
# Good: Code is clear
def calculate_total_price(items, tax_rate):
    """Calculate total price including tax."""
    subtotal = sum(item.price * item.quantity for item in items)
    # Apply tax only to taxable items (luxury goods are pre-tax)
    taxable_subtotal = sum(
        item.price * item.quantity for item in items if not item.is_luxury
    )
    tax = taxable_subtotal * tax_rate
    return subtotal + tax
```

**Anti-patterns**:
```python
# Bad: Comments explain obvious code
x = 5  # Set x to 5
if user.age > 18:  # Check if age is greater than 18
    can_vote = True  # Set can_vote to True

# Bad: No explanation of why
def complex_calculation(a, b, c):
    return (a * b) + (c ** 2) - (b / a)  # Why this formula? When should we use it?

# Bad: Outdated comments
def get_users():
    # TODO: This used to fetch from database but now it's in memory
    # and returns cached results. Still works though.
    return memory_cache.users
```

**Best practices**:
- Explain *why* decisions were made
- Document edge cases and assumptions
- Use docstrings for public APIs
- Keep comments updated with code

---

## 3. Security & Data Handling

### 3.1 Secrets Management

**Standard**: Never hardcode secrets; use environment variables or secret management systems.

**Good pattern**:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file (NEVER commit)

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment")

client = APIClient(api_key=API_KEY)
```

**Anti-patterns**:
```python
# NEVER DO THIS
API_KEY = "sk-1234567890abcdefghij"  # Hardcoded!
DATABASE_PASSWORD = "admin123"  # Hardcoded!

# Bad: Logging secrets
logger.info(f"Connecting with API_KEY: {api_key}")

# Bad: Storing in default values
def create_client(api_key="sk-1234567890abcdefghij"):  # Default secret!
    pass
```

**What to watch for**:
- Hardcoded API keys, passwords, tokens
- Secrets in logs or error messages
- Secrets in version control
- Default values containing secrets

---

### 3.2 Input Validation

**Standard**: Never trust user input; validate all inputs at system boundaries.

**Good pattern**:
```python
def create_user(email, age):
    """Create user with validated inputs"""
    # Validate email format
    if not isinstance(email, str) or "@" not in email or "." not in email.split("@")[1]:
        raise ValueError(f"Invalid email format: {email}")

    # Validate age
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValueError(f"Invalid age: {age}")

    return User(email=email, age=age)
```

**Anti-patterns**:
```python
# Bad: No input validation
def create_user(email, age):
    return User(email=email, age=age)  # What if email is None? age is -5?

# Bad: Incomplete validation
def create_user(email, age):
    if email:
        return User(email=email, age=age)  # Still no format check, no age validation

# Bad: Trusting the client
def create_user(request):
    # Assumes client validated - WRONG!
    return User(email=request.email, age=request.age)
```

**What to watch for**:
- Missing validation at system boundaries
- Type mismatches (int vs string)
- Range violations (age = -5, max_items = 999999)
- Format violations (email without @)

---

### 3.3 Data Access Control

**Standard**: Only expose data that users are authorized to access.

**Good pattern**:
```python
def get_user_data(current_user_id, requested_user_id):
    """Get user data with authorization check"""
    if current_user_id != requested_user_id:
        # Users can only access their own data
        raise AuthorizationError("Cannot access other users' data")

    return db.get_user(requested_user_id)

def get_all_users(current_user):
    """Get all users - admin only"""
    if not current_user.is_admin:
        raise AuthorizationError("Admin access required")

    return db.get_all_users()
```

**Anti-patterns**:
```python
# Bad: No authorization check
def get_user_data(current_user_id, requested_user_id):
    return db.get_user(requested_user_id)  # No check if user is allowed!

# Bad: Assuming authorization happens elsewhere
def delete_user(user_id):
    # Authorization should happen here, not in the caller
    db.delete_user(user_id)

# Bad: Checking authorization after loading data
def get_report(user_id):
    report = load_huge_report(user_id)  # Expensive!
    if not user.can_access(report):  # Check AFTER loading
        raise AuthorizationError()
```

**What to watch for**:
- Missing authorization checks
- Authorization checks after data access
- Assuming authorization elsewhere
- Checking user ID after returning data

---

## 4. Testing

### 4.1 Unit Test Patterns

**Standard**: Unit tests should be isolated, focused, and have clear intent.

**Good pattern**:
```python
import pytest

class TestUserValidation:
    """Tests for user validation logic"""

    def test_valid_email_passes(self):
        """Valid email should not raise"""
        assert validate_email("user@example.com") is True

    def test_missing_at_sign_fails(self):
        """Email without @ should fail"""
        with pytest.raises(ValueError, match="@ required"):
            validate_email("userexample.com")

    def test_age_must_be_positive(self):
        """Negative age should fail"""
        with pytest.raises(ValueError):
            validate_age(-5)

    def test_age_above_150_is_invalid(self):
        """Age > 150 should fail"""
        with pytest.raises(ValueError):
            validate_age(200)
```

**Anti-patterns**:
```python
# Bad: Tests are too broad
def test_user_validation():
    # What is this testing?
    assert validate_user({"email": "test@example.com", "age": 30})

# Bad: Multiple assertions per test
def test_validation():
    assert validate_email("test@example.com")
    assert validate_age(30)
    assert validate_name("John")
    # If one fails, the others don't run

# Bad: Not testing edge cases
def test_email_validation():
    assert validate_email("test@example.com")
    # What about: missing @, no domain, null, empty string?

# Bad: Unclear test names
def test_1():
    # What is this testing?
    pass
```

**What to watch for**:
- Tests that don't test what they claim
- Missing edge case tests
- Tests that are too broad
- Non-deterministic tests (flaky tests)

---

### 4.2 Test Coverage

**Standard**: Critical paths should be tested; aim for 80%+ coverage of business logic.

**Good pattern**:
```python
# Test the happy path
def test_create_user_success(mock_db):
    """Successfully create user with valid data"""
    result = create_user("user@example.com", mock_db)
    assert result.email == "user@example.com"
    mock_db.save.assert_called_once()

# Test error cases
def test_create_user_invalid_email(mock_db):
    """Reject invalid email"""
    with pytest.raises(ValueError):
        create_user("invalid", mock_db)
    mock_db.save.assert_not_called()

# Test boundary cases
def test_create_user_email_too_long(mock_db):
    """Reject emails exceeding max length"""
    long_email = "a" * 255 + "@example.com"
    with pytest.raises(ValueError):
        create_user(long_email, mock_db)
```

**What to watch for**:
- No tests for error cases
- Only happy path tested
- Missing boundary/edge case tests
- Mock objects not verified

---

## 5. Performance

### 5.1 Algorithmic Complexity

**Standard**: Be aware of algorithm complexity; prefer O(n) to O(n²) when possible.

**Good pattern**:
```python
# Good: O(n) - single pass
def find_duplicates(items):
    """Find duplicate items in O(n) time"""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return duplicates

# Good: O(n log n) - acceptable for sorting
def get_top_users_by_score(users):
    """Get top 10 users by score"""
    return sorted(users, key=lambda u: u.score, reverse=True)[:10]
```

**Anti-patterns**:
```python
# Bad: O(n²) - nested loops
def find_duplicates(items):
    """Find duplicates inefficiently"""
    duplicates = []
    for i, item in enumerate(items):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:  # Nested loop!
                duplicates.append(item)
    return duplicates

# Bad: Repeated computations
def get_expensive_value():
    """Recalculates every time"""
    result = expensive_operation()  # Called multiple times?
    return result

# Bad: Database queries in loops
def process_users(user_ids):
    """N+1 query problem"""
    results = []
    for user_id in user_ids:
        user = db.query(User).filter_by(id=user_id).first()  # Query per iteration!
        results.append(user)
    return results
```

**What to watch for**:
- Nested loops that could be single pass
- Database queries in loops (N+1 problem)
- Repeated expensive operations
- Sorting large datasets unnecessarily

---

### 5.2 Resource Management

**Standard**: Allocate and release resources explicitly; use context managers when available.

**Good pattern**:
```python
# Good: Context manager handles cleanup
with open("data.csv") as f:
    data = f.read()
    # File automatically closed

# Good: Explicit resource management
db = Database()
try:
    results = db.query(Users)
    process(results)
finally:
    db.close()  # Guaranteed to run
```

**Anti-patterns**:
```python
# Bad: File not closed
f = open("data.csv")
data = f.read()
# File handle leaked!

# Bad: Exception skips cleanup
db = Database()
results = db.query(Users)
process(results)
db.close()  # Skipped if exception above
```

---

## 6. Dependencies & Maintenance

### 6.1 Dependency Management

**Standard**: Pin versions for reproducibility; document why external dependencies exist.

**Good pattern**:
```toml
# pyproject.toml - Good: versions pinned
[dependencies]
anthropic = "0.71.0"  # Main API client
pydantic = "2.5.0"    # Data validation
requests = "2.31.0"   # HTTP requests

[optional-dependencies]
dev = [
    "pytest==7.4.0",       # Testing framework
    "ruff==0.1.0",         # Code formatting
]
```

**Anti-patterns**:
```toml
# Bad: No version constraints
anthropic = "*"  # Any version? Could break!

# Bad: Overly loose constraints
requests = ">=2.0"  # Could be any version >= 2.0

# Bad: Outdated dependencies
anthropic = "0.50.0"  # Uses deprecated APIs
```

**Documentation pattern**:
```python
"""
Dependencies:
- anthropic: For Claude API interactions (required)
- pydantic: Data validation (required)
- numpy: Scientific computing (optional, required only for analytics)
"""
```

---

### 6.2 Code Maintainability

**Standard**: Code should be easy to understand and modify without breaking things.

**Good pattern**:
```python
# Good: Clear structure, easy to modify
CONFIG = {
    "max_retries": 3,
    "timeout_seconds": 30,
    "batch_size": 100,
}

class DataProcessor:
    def __init__(self, config):
        self.max_retries = config["max_retries"]
        self.timeout = config["timeout_seconds"]
        self.batch_size = config["batch_size"]
```

**Anti-patterns**:
```python
# Bad: Magic numbers scattered around
def process_data(items):
    for batch in chunks(items, 100):  # Where did 100 come from?
        for attempt in range(3):  # Why 3 retries?
            try:
                with timeout(30):  # Why 30 seconds?
                    send_batch(batch)

# Bad: Tight coupling makes changes hard
def process_order(order):
    # Tightly coupled to database implementation
    db.orders.insert(order)
    # Tightly coupled to email service
    smtp.send_mail(...)
    # Hard to change without breaking everything
```

---

## Quick Reference Table

| Category | Good | Bad |
|----------|------|-----|
| **SRP** | One reason to change | Multiple responsibilities |
| **DI** | Inject dependencies | Create inside functions |
| **Naming** | `user_age`, `is_valid` | `ua`, `v` |
| **Validation** | Check at boundary | Trust user input |
| **Secrets** | Environment variables | Hardcoded |
| **Tests** | Edge cases covered | Happy path only |
| **Complexity** | O(n), O(n log n) | O(n²) loops |
| **Resources** | Context managers | Manual cleanup |
| **Versions** | Pinned exactly | Loose constraints |

---

## Using This Guide in Reviews

When reviewing code:

1. **Check against patterns** - Does the code match good patterns or anti-patterns?
2. **Reference by section** - "See style-guide.md - Section 3.1: Secrets Management"
3. **Provide examples** - Show the anti-pattern in their code and the good pattern
4. **Explain the why** - "This pattern makes testing easier because..."
5. **Suggest fixes** - "Consider using a context manager (see example in style-guide.md)"

---

**Back to SKILL.md**: Return to main workflow for comprehensive review steps.
